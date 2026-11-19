"""Les calculs partagés entre l'écran animateur et l'écran stagiaire."""
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app import contenu, salle
from app.base import lire_reglage
from app.config import FUSEAU
from app.programme import ACTIVITES, ACTIVITES_PAR_ID, JEUX, JOURS, THEMES


def stagiaires(db) -> list[dict]:
    """Tous les stagiaires, avec le dossier de leur version calculé :
    - si l'animateur a fixé un dossier, on le garde ;
    - si deux stagiaires ont choisi le même jeu : « deux agences concurrentes », chacun son dossier (flechettes_lea) ;
    - sinon, le dossier porte le nom du jeu."""
    lignes = [dict(l) for l in db.execute("SELECT * FROM stagiaires ORDER BY id")]
    for s in lignes:
        s["dossier_auto"] = not s["dossier"]
        if s["jeu"] and not s["dossier"]:
            meme_jeu = sum(1 for autre in lignes if autre["jeu"] == s["jeu"])
            s["dossier"] = f"{s['jeu']}_{slug(s['prenom'])}" if meme_jeu > 1 else s["jeu"]
    return lignes


def slug(prenom: str) -> str:
    remplacements = str.maketrans("àâäéèêëîïôöùûüçñ", "aaaeeeeiioouuucn")
    s = prenom.lower().translate(remplacements)
    return "".join(c for c in s if c.isalnum()) or "eleve"


def un_stagiaire(db, sid: int) -> dict | None:
    return next((s for s in stagiaires(db) if s["id"] == sid), None)


def aujourdhui() -> date:
    return datetime.now(ZoneInfo(FUSEAU)).date()


def heure() -> str:
    return datetime.now(ZoneInfo(FUSEAU)).strftime("%H:%M")


def jour_actuel(db) -> int | None:
    """Le jour du stage (0 = lundi … 4 = vendredi) : forcé par l'animateur, ou calculé à partir de la date de début."""
    force = lire_reglage(db, "jour_force")
    if force != "":
        return int(force)
    debut = lire_reglage(db, "date_debut")
    if not debut:
        return None
    try:
        ecart = (aujourdhui() - date.fromisoformat(debut)).days
    except ValueError:
        return None
    return ecart if 0 <= ecart <= 4 else None


def activite_actuelle(jour: int | None) -> str | None:
    if jour is None:
        return None
    h = heure()
    du_jour = [a for a in ACTIVITES if a["jour"] == jour]
    for a in du_jour:
        if a["debut"] <= h < a["fin"]:
            return a["id"]
    # Avant le début : la première ; pendant la pause de midi : la première de l'après-midi ; après : la dernière
    suivantes = [a for a in du_jour if a["debut"] > h]
    return suivantes[0]["id"] if suivantes else du_jour[-1]["id"]


def resume_activite(a: dict) -> dict:
    return {k: a[k] for k in ("id", "jour", "debut", "fin", "titre", "description", "mode", "surprise", "lien", "idees",
                              "bilan")} | {"a_contenu": a["source"] is not None}


# ---------------------------------------------------------------- Le guide des élèves (dossier autonomie/)

def valeurs_guide(db, s: dict | None) -> dict:
    """Ce qui remplace les {{…}} dans les fichiers du dossier autonomie/."""
    autre = next((x for x in stagiaires(db) if s and x["id"] != s["id"]), None)
    return {
        "url_depot": lire_reglage(db, "url_depot") or "<adresse-du-depot>",
        "dossier": (s and s.get("dossier")) or "ton-jeu",
        "dossier_autre": (autre and autre.get("dossier")) or "son-jeu",
        "prenom_autre": autre["prenom"] if autre else "l'autre stagiaire",
    }


def prompts_de_la_fiche(db, a: dict) -> list[dict]:
    """Les prompts de la fiche de l'animateur (pour ne pas les recopier dans le guide des élèves)."""
    src = a["source"]
    if not src or "fichier" not in src:
        return []
    texte = contenu.decouper(contenu.lire(src["fichier"]), src.get("depuis"), src.get("jusqua"))
    texte = contenu.remplir_placeholders(texte, stagiaires(db))
    return [b for b in contenu.en_blocs(texte, src["fichier"]) if b["type"] == "prompt"]


def guide_eleves(db, a: dict, s: dict | None) -> list[dict]:
    """Le pas-à-pas que les stagiaires lisent pour une activité « ensemble » (la fiche de l'animateur, elle, reste pour lui)."""
    blocs = []
    for b in contenu.guide_brut(a["id"]):
        if b["type"] != "marqueur":
            blocs.append(b)
        elif b["nom"] == "PROMPTS":
            blocs.extend(prompts_de_la_fiche(db, a))
        elif b["nom"] == "CLAUDE_MD":
            blocs.append({"type": "fichier", "nom": "CLAUDE.md", "texte": contenu.claude_md_rempli(stagiaires(db))})
    return contenu.remplir_blocs(blocs, valeurs_guide(db, s))


def programme(db) -> dict:
    jour = jour_actuel(db)
    return {
        "jours": [{"index": i, "nom": nom, "theme": THEMES[i],
                   "activites": [resume_activite(a) for a in ACTIVITES if a["jour"] == i]} for i, nom in enumerate(JOURS)],
        "jour_actuel": jour,
        "activite_actuelle": activite_actuelle(jour),
        "date_debut": lire_reglage(db, "date_debut"),
        "message": lire_reglage(db, "message"),
        # « La salle de jeux » du menu : les 4 jeux d'exemple, affichés dans le compagnon
        "salle": salle.disponible(),
        "jeux": {cle: {"nom": j["nom"], "icone": j["icone"]} for cle, j in JEUX.items()},
    }


def fichier_source(a: dict, jeu: str | None) -> str | None:
    src = a["source"]
    if not src:
        return None
    if "etape" in src:
        return JEUX[jeu]["fichiers"][src["etape"]] if jeu in JEUX else None
    return src["fichier"]


def contenu_activite(db, a: dict, pour: str, jeu: str | None, dossier: str | None, surprise_declenchee: bool,
                     stagiaire: dict | None = None) -> dict:
    """Le contenu d'une activité, en blocs, adapté à celui qui regarde (animateur ou stagiaire)."""
    reponse = {"activite": resume_activite(a), "blocs": [], "verrouille": False, "manque_jeu": False, "guide": [],
               "phrase_depart": contenu.phrase_de_depart(jeu) if (a["mode"] == "perso" and jeu in JEUX) else ""}
    if a["mode"] == "ensemble":
        guide = guide_eleves(db, a, stagiaire)
        if pour == "animateur":
            reponse["guide"] = guide        # l'animateur peut relire ce que voient les stagiaires
        elif guide:
            reponse["blocs"] = avec_routine(a, guide)
            return reponse
    if not a["source"]:
        return reponse
    fichier = fichier_source(a, jeu)
    if fichier is None:
        reponse["manque_jeu"] = True
        return reponse
    src = a["source"]
    texte = contenu.decouper(contenu.lire(fichier), src.get("depuis"), src.get("jusqua"))
    texte = contenu.remplir_placeholders(texte, stagiaires(db))
    if pour == "stagiaire":
        if a["surprise"] and not surprise_declenchee:
            reponse["verrouille"] = True
            return reponse
        texte = contenu.pour_stagiaire(texte, surprise=a["surprise"])
    blocs = contenu.en_blocs(texte, fichier, jeu if a["mode"] == "perso" else None, dossier)
    if pour == "stagiaire" and a["mode"] == "ensemble":
        # Pour les activités en groupe, le stagiaire n'a pas besoin des notes de l'animateur :
        # il garde seulement les prompts à copier (et les cases à cocher).
        blocs = [b for b in blocs if b["type"] in ("prompt", "verif")] if a["prompts_eleve"] else []
    if a["modele_prompt"]:
        modele = a["modele_prompt"].replace("[PHRASE DE DÉPART]", reponse["phrase_depart"].strip("« »") or "Je travaille sur mon jeu.")
        blocs.append({"type": "md", "texte": "### Mon prompt d'amélioration (modèle à compléter)\n\n"
                      "Pour chaque idée de ta liste : copie ce modèle, remplace ce qui est entre crochets, puis teste et committe."})
        blocs.append({"type": "prompt", "texte": modele})
    reponse["blocs"] = avec_routine(a, blocs) if pour == "stagiaire" else blocs
    return reponse


def avec_routine(a: dict, blocs: list[dict]) -> list[dict]:
    """La première activité sur ordinateur du jour commence par le rappel « comment relancer mon poste »."""
    if not a["routine"]:
        return blocs
    return [{"type": "repli", "titre": "☀️ La routine du matin : relancer mon poste", "blocs": contenu.routine_du_matin()}] + blocs


def cles_verif(db, a: dict, jeu: str | None) -> list[str]:
    """Les cases « Ce qu'on vérifie » d'une activité, pour mesurer l'avancement."""
    if a["mode"] == "ensemble":
        blocs = contenu.guide_brut(a["id"])
        return [i["cle"] for b in blocs if b["type"] == "verif" for i in b["items"]]
    fichier = fichier_source(a, jeu)
    if not fichier or a["mode"] != "perso":
        return []
    src = a["source"]
    texte = contenu.decouper(contenu.lire(fichier), src.get("depuis"), src.get("jusqua"))
    return [i["cle"] for b in contenu.en_blocs(texte, fichier) if b["type"] == "verif" for i in b["items"]]


def avancement(db, s: dict) -> dict:
    """Pour chaque activité : terminée ? combien de cases cochées sur combien ?"""
    coches = {l["cle"] for l in db.execute("SELECT cle FROM coches WHERE stagiaire_id = ? AND fait = 1", (s["id"],))}
    resultat = {}
    for a in ACTIVITES:
        cles = cles_verif(db, a, s["jeu"])
        resultat[a["id"]] = {"fini": f"fini:{a['id']}" in coches, "coches": sum(1 for c in cles if c in coches),
                             "total": len(cles)}
    return resultat


def activite_existe(aid: str) -> bool:
    return aid in ACTIVITES_PAR_ID
