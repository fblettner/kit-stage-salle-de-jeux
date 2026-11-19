"""Lire les fichiers .md du kit, en découper des morceaux et les transformer en « blocs ».

Un bloc, c'est un morceau de page que le site sait afficher :
- {"type": "md", "texte": "..."}                       du texte normal (Markdown)
- {"type": "prompt", "texte": "..."}                   un prompt à copier dans Claude (bouton « Copier »)
- {"type": "code", "langage": "bash", "texte": "..."}  une commande ou du code
- {"type": "verif", "titre": "...", "items": [{"cle", "texte"}]}  une liste « Ce qu'on vérifie » à cocher
- {"type": "prompt", "secret": True, ...}              un prompt caché : on le copie sans le lire (le rôle du client)
- {"type": "fichier", "nom": "...", "texte": "..."}    un fichier à télécharger (le CLAUDE.md déjà rempli)
- {"type": "repli", "titre": "...", "blocs": [...]}    des blocs repliés derrière un titre cliquable
"""
import hashlib
import re
from functools import lru_cache

from app.config import CONTENU_DIR
from app.programme import JEUX


# Les fichiers écrits POUR les élèves (dossier autonomie/)
GUIDE = "autonomie/parcours-eleves.md"
DEPANNAGE = "autonomie/depannage.md"
MARQUEURS = ("[[PROMPTS]]", "[[CLAUDE_MD]]")


@lru_cache(maxsize=64)
def lire(fichier: str) -> str:
    chemin = (CONTENU_DIR / fichier).resolve()
    if CONTENU_DIR.resolve() not in chemin.parents or chemin.suffix != ".md":
        raise FileNotFoundError(fichier)
    return chemin.read_text(encoding="utf-8")


def decouper(texte: str, depuis: str | None = None, jusqua: str | None = None) -> str:
    """Garde les lignes entre le titre « ## » qui contient `depuis` et le titre « ## » suivant qui contient `jusqua`.
    Le grand titre « # » du fichier est retiré : le site affiche déjà le titre de l'activité."""
    lignes = texte.splitlines()
    debut, fin = 0, len(lignes)
    if depuis:
        debut = next((i for i, l in enumerate(lignes) if l.startswith("## ") and depuis in l), None)
        if debut is None:
            return ""
    if jusqua:
        fin = next((i for i in range(debut + 1, len(lignes)) if lignes[i].startswith("## ") and jusqua in lignes[i]), fin)
    morceau = [l for l in lignes[debut:fin] if not l.startswith("# ")]
    # Les séparateurs « --- » en fin de morceau ne servent à rien
    while morceau and morceau[-1].strip() in ("", "---"):
        morceau.pop()
    while morceau and morceau[0].strip() in ("", "---"):
        morceau.pop(0)
    return "\n".join(morceau)


def section(texte: str, debut: str) -> str:
    """Une partie « ## … » dont le titre commence par `debut`, SANS son titre, jusqu'au « ## » suivant."""
    lignes = texte.splitlines()
    i = next((n for n, l in enumerate(lignes) if l.startswith("## ") and l[3:].strip().startswith(debut)), None)
    if i is None:
        return ""
    fin = next((n for n in range(i + 1, len(lignes)) if lignes[n].startswith("## ")), len(lignes))
    morceau = lignes[i + 1:fin]
    while morceau and morceau[-1].strip() in ("", "---"):
        morceau.pop()
    while morceau and morceau[0].strip() in ("", "---"):
        morceau.pop(0)
    return "\n".join(morceau)


def pour_stagiaire(texte: str, surprise: bool = False) -> str:
    """Adapte un morceau pour l'écran d'un stagiaire :
    - la phrase de départ (« Toujours commencer la séance… ») est déjà affichée en haut de l'activité ;
    - dans la surprise, on ne garde que les paroles du client (les citations « > ») et les prompts :
      les conseils à l'animateur (« Laisse l'élève réagir… ») ne sont pas pour l'élève."""
    lignes = [l for l in texte.splitlines() if not (l.startswith(">") and "Toujours commencer la séance" in l)]
    if surprise:
        premier_sous_titre = next((i for i, l in enumerate(lignes) if l.startswith("### ")), len(lignes))
        avant = [l for l in lignes[:premier_sous_titre] if l.startswith("## ") or l.startswith(">") or not l.strip()]
        lignes = avant + lignes[premier_sous_titre:]
    return "\n".join(lignes)


def remplacer_dossier(prompt: str, jeu: str, dossier: str) -> str:
    """Formule « deux agences concurrentes » : chaque version a son dossier (ex. flechettes_lea).
    On remplace le nom du dossier, le préfixe de l'API et le préfixe CSS dans les prompts."""
    if not dossier or dossier == jeu:
        return prompt
    return re.sub(rf"(?<![\w-]){jeu}(?=[/.\-])|(?<=test_){jeu}\b|(?<=/api/){jeu}\b", dossier, prompt)


def cle_verif(fichier: str, texte: str) -> str:
    return fichier.rsplit("/", 1)[-1].removesuffix(".md") + ":" + hashlib.sha1(texte.encode()).hexdigest()[:8]


def en_blocs(texte: str, fichier: str, jeu: str | None = None, dossier: str | None = None) -> list[dict]:
    blocs: list[dict] = []
    tampon: list[str] = []
    verif = None  # la liste « Ce qu'on vérifie » en cours

    def vider():
        nonlocal tampon
        contenu = "\n".join(tampon).strip()
        if contenu and contenu != "---":
            blocs.append({"type": "md", "texte": contenu})
        tampon = []

    lignes = texte.splitlines()
    i = 0
    while i < len(lignes):
        l = lignes[i]
        if l.startswith("```"):
            vider()
            verif = None
            langage = l[3:].strip()
            code = []
            i += 1
            while i < len(lignes) and not lignes[i].startswith("```"):
                code.append(lignes[i])
                i += 1
            contenu = "\n".join(code)
            if langage == "secret":
                blocs.append({"type": "prompt", "secret": True, "texte": contenu})
            elif langage:
                blocs.append({"type": "code", "langage": langage, "texte": contenu})
            else:
                if jeu:
                    contenu = remplacer_dossier(contenu, jeu, dossier)
                blocs.append({"type": "prompt", "texte": contenu})
        elif l.startswith("#") and "Ce qu'on vérifie" in l:
            vider()
            verif = {"type": "verif", "titre": l.lstrip("# ").strip(), "items": []}
            blocs.append(verif)
        elif verif is not None and re.match(r"^\s*[-*] ", l):
            item = re.sub(r"^\s*[-*] ", "", l).strip()
            verif["items"].append({"cle": cle_verif(fichier, item), "texte": item})
        elif verif is not None and l.startswith("  ") and verif["items"]:
            # suite d'un élément de liste sur la ligne suivante
            verif["items"][-1]["texte"] += " " + l.strip()
        else:
            if verif is not None and l.strip() == "":
                pass  # une ligne vide ne termine pas la liste
            else:
                verif = None
                tampon.append(l)
        i += 1
    vider()
    # Une liste « Ce qu'on vérifie » vide (cas rare) n'a pas d'intérêt
    return [b for b in blocs if b["type"] != "verif" or b["items"]]


# --- Les remplacements dans les prompts communs (les jeux choisis par les stagiaires) ---

def nom_jeu_pour_prompt(jeu: str) -> str:
    return {"echecs": "les échecs", "coach": "Coach, un jeu d'entraîneur de foot",
            "penalty": "Penalty Pro, des tirs au but", "flechettes": "des fléchettes"}.get(jeu, jeu)


def remplir_placeholders(texte: str, stagiaires: list[dict]) -> str:
    """Remplace les [EX. : …], [JEU A, dossier xxx]… des prompts communs par les choix des stagiaires."""
    choisis = [s for s in stagiaires if s.get("jeu")]
    if not choisis:
        return texte
    # J1 : « Voici les jeux qu'on a choisis : [EX. : …] »
    liste = " et ".join(f"{nom_jeu_pour_prompt(s['jeu'])} ({s['prenom']})" for s in choisis)
    texte = re.sub(r"\[EX\. : [^\]]*\]", liste, texte)
    # J5 : [NOS JEUX]
    noms = " et ".join(dict.fromkeys(JEUX[s["jeu"]]["nom"] for s in choisis))
    texte = texte.replace("[NOS JEUX]", noms)
    # J2 : le socle avec un dossier par version
    dossiers = list(dict.fromkeys((s.get("dossier") or s["jeu"], s["jeu"]) for s in choisis))
    if len(dossiers) >= 2:
        (da, ja), (db, jb) = dossiers[0], dossiers[1]
        texte = texte.replace("[JEU A, dossier xxx]", f"{JEUX[ja]['nom']}, dossier {da}")
        texte = texte.replace("[JEU B, dossier yyy]", f"{JEUX[jb]['nom']}, dossier {db}")
        texte = texte.replace("[xxx]", da).replace("[yyy]", db)
    return texte


def claude_md_rempli(stagiaires: list[dict]) -> str:
    texte = lire("CLAUDE.md")
    choisis = [s for s in stagiaires if s.get("jeu")]
    if choisis:
        parts = []
        for s in choisis:
            d = s.get("dossier") or s["jeu"]
            parts.append(f"{JEUX[s['jeu']]['nom']} ({s['prenom']}, dossier `{d}`)")
        texte = re.sub(r"\[à compléter[^\]]*\]", " et ".join(parts), texte)
    return texte


# --- Le guide des élèves (autonomie/parcours-eleves.md) ---

def guide_brut(aid: str) -> list[dict]:
    """La partie du guide des élèves pour une activité, en blocs. Les marqueurs [[PROMPTS]] et [[CLAUDE_MD]]
    deviennent des blocs « marqueur », et les {{…}} ne sont pas encore remplacés : les clés des cases à cocher
    ne dépendent donc pas du prénom ou du jeu de celui qui regarde."""
    texte = section(lire(GUIDE), f"{aid} ·")
    if not texte:
        return []
    blocs: list[dict] = []
    tampon: list[str] = []
    for l in texte.splitlines() + [MARQUEURS[0] + "fin"]:
        if l.strip() in MARQUEURS or l == MARQUEURS[0] + "fin":
            blocs.extend(en_blocs("\n".join(tampon), f"guide-{aid}.md"))
            tampon = []
            if l.strip() in MARQUEURS:
                blocs.append({"type": "marqueur", "nom": l.strip().strip("[]")})
        else:
            tampon.append(l)
    return blocs


def remplir_accolades(texte: str, valeurs: dict) -> str:
    """Remplace {{url_depot}}, {{dossier}}… par leur valeur."""
    for cle, valeur in valeurs.items():
        texte = texte.replace("{{" + cle + "}}", valeur)
    return texte


def remplir_blocs(blocs: list[dict], valeurs: dict) -> list[dict]:
    resultat = []
    for b in blocs:
        b = dict(b)
        if "texte" in b:
            b["texte"] = remplir_accolades(b["texte"], valeurs)
        if "items" in b:
            b["items"] = [{"cle": i["cle"], "texte": remplir_accolades(i["texte"], valeurs)} for i in b["items"]]
        if "blocs" in b:
            b["blocs"] = remplir_blocs(b["blocs"], valeurs)
        resultat.append(b)
    return resultat


def routine_du_matin() -> list[dict]:
    return en_blocs(section(lire(GUIDE), "Routine du matin"), "guide-routine.md")


def depannage() -> list[dict]:
    """La page « Je suis bloqué » : le fichier entier, sans son grand titre ni la note du début."""
    lignes = [l for l in lire(DEPANNAGE).splitlines() if not l.startswith("# ") and not l.startswith("> ")]
    return en_blocs("\n".join(lignes).strip(), "depannage.md")


# --- Les pages « de référence » ---

def phrase_de_depart(jeu: str) -> str:
    """« Toujours commencer la séance Claude par : … », trouvée dans le fichier de l'étape 2 du jeu."""
    m = re.search(r"Toujours commencer la séance Claude par : \*\*(.+?)\*\*", lire(JEUX[jeu]["fichiers"][2]))
    return m.group(1) if m else ""


def catalogue() -> list[dict]:
    texte = lire("01-CATALOGUE-DES-PROJETS.md")
    fiches = []
    for jeu, infos in JEUX.items():
        morceau = decouper(texte, infos["catalogue"])
        lignes = morceau.splitlines()
        titre = lignes[0].lstrip("# ").strip() if lignes else infos["nom"]
        fiches.append({"jeu": jeu, "nom": infos["nom"], "icone": infos["icone"], "titre": titre,
                       "texte": "\n".join(lignes[1:]).strip()})
    return fiches


def formules_meme_jeu() -> str:
    return decouper(lire("01-CATALOGUE-DES-PROJETS.md"), "Et si les deux", "Résumé")


def lexique() -> list[dict]:
    mots = []
    for l in lire("fiches/lexique.md").splitlines():
        cases = [c.strip() for c in l.strip().strip("|").split("|")]
        if l.startswith("|") and len(cases) >= 2 and cases[0] not in ("Mot", "") and not set(cases[0]) <= set("-: "):
            mots.append({"mot": cases[0].replace("**", ""), "definition": cases[1],
                         "souvenir": cases[2] if len(cases) > 2 and cases[2] != "—" else ""})
    return mots


def questions_carnet() -> list[dict]:
    """Les questions du carnet de bord, jour par jour : chaque ligne « **…:** » devient une question.
    Un tableau devient une question « tableau » avec ses colonnes et ses lignes."""
    jours = []
    jour = None
    lignes = lire("fiches/carnet-de-bord.md").splitlines()
    derniere_question = None
    for i, l in enumerate(lignes):
        if l.startswith("## "):
            jour = {"titre": l[3:].strip(), "questions": []}
            jours.append(jour)
            derniere_question = None
            continue
        if jour is None:
            continue
        m = re.match(r"^\*\*(.+?)\s*:\*\*\s*(.*)$", l.strip())
        if m:
            titre = m.group(1).strip()
            q = {"cle": f"{len(jours)}-{len(jour['questions']) + 1}", "titre": titre, "type": "texte"}
            if "schéma" in titre.lower() or "dessine" in titre.lower():
                q["type"] = "schema"   # à dessiner sur papier, on peut quand même écrire une légende
            if "https://" in m.group(2):
                q["type"] = "ligne"
                q["prefixe"] = "https://"
            jour["questions"].append(q)
            derniere_question = q
            continue
        if l.startswith("|") and derniere_question is not None and derniere_question["type"] != "tableau":
            cases = [c.strip() for c in l.strip().strip("|").split("|")]
            derniere_question["type"] = "tableau"
            derniere_question["colonnes"] = cases
            derniere_question["lignes"] = []
            # les lignes suivantes du tableau : la 1re case est l'intitulé de la ligne (Facile, Moyen…) ou vide
            for suite in lignes[i + 2:]:
                if not suite.startswith("|"):
                    break
                premiere = suite.strip().strip("|").split("|")[0].strip()
                derniere_question["lignes"].append(premiere)
    return jours
