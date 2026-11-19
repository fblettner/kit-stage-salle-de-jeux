"""Toutes les routes de l'API : connexion, programme, contenu, espace stagiaire, espace animateur."""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict, Field

from app import auth, contenu, services
from app.base import connexion, ecrire_reglage, lire_reglage, maintenant
from app.config import CONTENU_DIR, MOT_DE_PASSE_ANIMATEUR
from app.programme import ACTIVITES_PAR_ID, JEUX

api = APIRouter(prefix="/api")


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


# ---------------------------------------------------------------- Connexion

class ConnexionAnimateur(Strict):
    mot_de_passe: str = Field(max_length=200)


class ConnexionStagiaire(Strict):
    code: str = Field(max_length=20)


@api.post("/connexion/animateur")
def connexion_animateur(corps: ConnexionAnimateur):
    auth.freiner("animateur")
    if not MOT_DE_PASSE_ANIMATEUR:
        raise HTTPException(503, "Le mot de passe animateur n'est pas configuré (variable ANIMATEUR_MOT_DE_PASSE).")
    if not auth.comparer(corps.mot_de_passe, MOT_DE_PASSE_ANIMATEUR):
        auth.noter_echec("animateur")
        raise HTTPException(401, "Mot de passe incorrect.")
    return {"jeton": auth.nouveau_jeton("animateur"), "role": "animateur"}


@api.post("/connexion/stagiaire")
def connexion_stagiaire(corps: ConnexionStagiaire):
    auth.freiner("stagiaire")
    code = corps.code.upper().replace(" ", "").replace("-", "")
    with connexion() as db:
        s = db.execute("SELECT id, prenom FROM stagiaires WHERE code = ?", (code,)).fetchone()
    if not s:
        auth.noter_echec("stagiaire")
        raise HTTPException(401, "Code inconnu. Vérifie avec ton maître de stage.")
    return {"jeton": auth.nouveau_jeton("stagiaire", s["id"]), "role": "stagiaire", "prenom": s["prenom"]}


@api.post("/deconnexion")
def deconnexion(s: dict = Depends(auth.session)):
    with connexion() as db:
        db.execute("DELETE FROM sessions WHERE jeton = ?", (s["jeton"],))
    return {"ok": True}


@api.get("/session")
def qui_suis_je(s: dict = Depends(auth.session)):
    if s["role"] == "animateur":
        return {"role": "animateur"}
    with connexion() as db:
        st = services.un_stagiaire(db, s["stagiaire_id"])
    return {"role": "stagiaire", "prenom": st["prenom"]}


# ---------------------------------------------------------------- Programme et contenus (tout le monde)

@api.get("/programme")
def programme(s: dict = Depends(auth.session)):
    with connexion() as db:
        return services.programme(db)


@api.get("/activite/{aid}")
def activite(aid: str, jeu: str | None = Query(default=None), s: dict = Depends(auth.session)):
    a = ACTIVITES_PAR_ID.get(aid)
    if not a:
        raise HTTPException(404, "Activité inconnue.")
    with connexion() as db:
        if s["role"] == "stagiaire":
            st = services.un_stagiaire(db, s["stagiaire_id"])
            declenchee = db.execute("SELECT 1 FROM surprises WHERE stagiaire_id = ? AND activite = ?",
                                    (st["id"], aid)).fetchone() is not None
            return services.contenu_activite(db, a, "stagiaire", st["jeu"], st["dossier"], declenchee, stagiaire=st)
        if jeu is not None and jeu not in JEUX:
            raise HTTPException(400, "Jeu inconnu.")
        return services.contenu_activite(db, a, "animateur", jeu, jeu, True)


@api.get("/catalogue")
def catalogue(s: dict = Depends(auth.session)):
    return {"jeux": contenu.catalogue(), "meme_jeu": contenu.formules_meme_jeu()}


@api.get("/lexique")
def lexique(s: dict = Depends(auth.session)):
    return contenu.lexique()


@api.get("/depannage")
def depannage(s: dict = Depends(auth.session)):
    """La page « Je suis bloqué » (fichier autonomie/depannage.md)."""
    with connexion() as db:
        st = services.un_stagiaire(db, s["stagiaire_id"]) if s["role"] == "stagiaire" else None
        return contenu.remplir_blocs(contenu.depannage(), services.valeurs_guide(db, st))


@api.get("/carnet/questions")
def carnet_questions(s: dict = Depends(auth.session)):
    return contenu.questions_carnet()


# ---------------------------------------------------------------- Espace stagiaire

def autres(db, sid: int) -> list[dict]:
    return [{"id": a["id"], "prenom": a["prenom"], "jeu": a["jeu"], "dossier": a["dossier"]}
            for a in services.stagiaires(db) if a["id"] != sid]


def bugs_de(db, sid: int) -> dict:
    noms = {s["id"]: s["prenom"] for s in services.stagiaires(db)}

    def enrichir(l):
        b = dict(l)
        b["auteur"] = noms.get(b["auteur_id"], "?")
        b["cible"] = noms.get(b["cible_id"], "?")
        b["corrige"] = bool(b["corrige"])
        return b

    trouves = [enrichir(l) for l in db.execute("SELECT * FROM bugs WHERE auteur_id = ? ORDER BY id", (sid,))]
    recus = [enrichir(l) for l in db.execute("SELECT * FROM bugs WHERE cible_id = ? ORDER BY id", (sid,))]
    return {"trouves": trouves, "recus": recus}


@api.get("/moi")
def moi(sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        # On note que son écran est ouvert : à distance, l'animateur voit ainsi qui est « en ligne »
        db.execute("UPDATE stagiaires SET vu_le = ? WHERE id = ?", (maintenant(), sid))
        s = services.un_stagiaire(db, sid)
        return {
            "id": sid, "prenom": s["prenom"], "jeu": s["jeu"], "dossier": s["dossier"],
            "choix_verrouille": lire_reglage(db, "choix_verrouille") == "1",
            "coches": {l["cle"]: bool(l["fait"]) for l in db.execute("SELECT cle, fait FROM coches WHERE stagiaire_id = ?", (sid,))},
            "reponses": {l["cle"]: l["texte"] for l in db.execute("SELECT cle, texte FROM reponses WHERE stagiaire_id = ?", (sid,))},
            "aides": [dict(l) for l in db.execute("SELECT * FROM aides WHERE stagiaire_id = ? ORDER BY id DESC", (sid,))],
            "surprises": [l["activite"] for l in db.execute("SELECT activite FROM surprises WHERE stagiaire_id = ?", (sid,))],
            "bugs": bugs_de(db, sid),
            "autres": autres(db, sid),
            "avancement": services.avancement(db, s),
        }


class ChoixJeu(Strict):
    jeu: Literal["echecs", "coach", "penalty", "flechettes"]


@api.put("/moi/jeu")
def choisir_jeu(corps: ChoixJeu, sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        if lire_reglage(db, "choix_verrouille") == "1":
            raise HTTPException(409, "Les choix sont validés : demande à ton maître de stage pour changer.")
        db.execute("UPDATE stagiaires SET jeu = ? WHERE id = ?", (corps.jeu, sid))
    return {"ok": True}


CLE = r"^[\w:.\-]{1,80}$"


class Coche(Strict):
    cle: str = Field(pattern=CLE)
    fait: bool


@api.put("/moi/coche")
def cocher(corps: Coche, sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        db.execute("""INSERT INTO coches (stagiaire_id, cle, fait, maj) VALUES (?, ?, ?, ?)
                      ON CONFLICT(stagiaire_id, cle) DO UPDATE SET fait = excluded.fait, maj = excluded.maj""",
                   (sid, corps.cle, int(corps.fait), maintenant()))
    return {"ok": True}


class Reponse(Strict):
    cle: str = Field(pattern=CLE)
    texte: str = Field(max_length=5000)


@api.put("/moi/reponse")
def repondre(corps: Reponse, sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        db.execute("""INSERT INTO reponses (stagiaire_id, cle, texte, maj) VALUES (?, ?, ?, ?)
                      ON CONFLICT(stagiaire_id, cle) DO UPDATE SET texte = excluded.texte, maj = excluded.maj""",
                   (sid, corps.cle, corps.texte, maintenant()))
    return {"ok": True}


class DemandeAide(Strict):
    activite: str = Field(max_length=10)
    message: str = Field(min_length=3, max_length=1000)


@api.post("/moi/aides")
def demander_aide(corps: DemandeAide, sid: int = Depends(auth.stagiaire)):
    if not services.activite_existe(corps.activite) and corps.activite != "autre":
        raise HTTPException(400, "Activité inconnue.")
    with connexion() as db:
        ouvertes = db.execute("SELECT COUNT(*) FROM aides WHERE stagiaire_id = ? AND statut != 'resolue'", (sid,)).fetchone()[0]
        if ouvertes >= 5:
            raise HTTPException(429, "Tu as déjà 5 demandes en attente : ton maître de stage arrive !")
        db.execute("INSERT INTO aides (stagiaire_id, activite, message, cree_le, maj) VALUES (?, ?, ?, ?, ?)",
                   (sid, corps.activite, corps.message, maintenant(), maintenant()))
    return {"ok": True}


@api.post("/moi/aides/{aid}/resolue")
def aide_resolue(aid: int, sid: int = Depends(auth.stagiaire)):
    """Le stagiaire a trouvé tout seul (ou avec Claude) : bravo, on ferme la demande."""
    with connexion() as db:
        db.execute("UPDATE aides SET statut = 'resolue', maj = ? WHERE id = ? AND stagiaire_id = ?", (maintenant(), aid, sid))
    return {"ok": True}


class Bug(Strict):
    cible_id: int
    action: str = Field(min_length=2, max_length=1000)
    resultat: str = Field(min_length=2, max_length=1000)
    attendu: str = Field(min_length=2, max_length=1000)


@api.post("/moi/bugs")
def signaler_bug(corps: Bug, sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        if corps.cible_id == sid or not services.un_stagiaire(db, corps.cible_id):
            raise HTTPException(400, "On teste le jeu de l'autre stagiaire.")
        db.execute("INSERT INTO bugs (auteur_id, cible_id, action, resultat, attendu, cree_le) VALUES (?, ?, ?, ?, ?, ?)",
                   (sid, corps.cible_id, corps.action, corps.resultat, corps.attendu, maintenant()))
    return {"ok": True}


class BugCorrige(Strict):
    corrige: bool


@api.put("/moi/bugs/{bid}")
def bug_corrige(bid: int, corps: BugCorrige, sid: int = Depends(auth.stagiaire)):
    """Seul le développeur du jeu (celui qui a REÇU le bug) peut dire qu'il est corrigé."""
    with connexion() as db:
        n = db.execute("UPDATE bugs SET corrige = ? WHERE id = ? AND cible_id = ?", (int(corps.corrige), bid, sid)).rowcount
    if not n:
        raise HTTPException(404, "Bug introuvable.")
    return {"ok": True}


@api.delete("/moi/bugs/{bid}")
def supprimer_bug(bid: int, sid: int = Depends(auth.stagiaire)):
    with connexion() as db:
        db.execute("DELETE FROM bugs WHERE id = ? AND auteur_id = ?", (bid, sid))
    return {"ok": True}


# ---------------------------------------------------------------- Espace animateur

anim = APIRouter(prefix="/api/animateur", dependencies=[Depends(auth.animateur)])


@anim.get("/tableau")
def tableau():
    with connexion() as db:
        liste = services.stagiaires(db)
        aides = db.execute("SELECT stagiaire_id, COUNT(*) n FROM aides WHERE statut = 'ouverte' GROUP BY stagiaire_id").fetchall()
        par_stagiaire = {l["stagiaire_id"]: l["n"] for l in aides}
        for s in liste:
            s["avancement"] = services.avancement(db, s)
            s["aides_ouvertes"] = par_stagiaire.get(s["id"], 0)
            s["surprises"] = [l["activite"] for l in db.execute("SELECT activite FROM surprises WHERE stagiaire_id = ?", (s["id"],))]
            # Le bilan écrit chaque soir (clés « bilan-0 » pour lundi … « bilan-4 » pour vendredi)
            s["bilans"] = {l["cle"]: l["texte"] for l in db.execute(
                "SELECT cle, texte FROM reponses WHERE stagiaire_id = ? AND cle LIKE 'bilan-%' AND texte != ''", (s["id"],))}
        return {
            "stagiaires": liste,
            "aides_ouvertes": sum(par_stagiaire.values()),
            "reglages": {"date_debut": lire_reglage(db, "date_debut"), "jour_force": lire_reglage(db, "jour_force"),
                         "choix_verrouille": lire_reglage(db, "choix_verrouille") == "1",
                         "message": lire_reglage(db, "message"),
                         "url_depot": lire_reglage(db, "url_depot")},
        }


class NouveauStagiaire(Strict):
    prenom: str = Field(min_length=1, max_length=40)


@anim.post("/stagiaires")
def creer_stagiaire(corps: NouveauStagiaire):
    with connexion() as db:
        if db.execute("SELECT COUNT(*) FROM stagiaires").fetchone()[0] >= 6:
            raise HTTPException(400, "6 stagiaires au maximum.")
        while True:
            code = auth.nouveau_code()
            if not db.execute("SELECT 1 FROM stagiaires WHERE code = ?", (code,)).fetchone():
                break
        cur = db.execute("INSERT INTO stagiaires (prenom, code, cree_le) VALUES (?, ?, ?)", (corps.prenom, code, maintenant()))
        return {"id": cur.lastrowid, "code": code}


class ModifStagiaire(Strict):
    prenom: str | None = Field(default=None, min_length=1, max_length=40)
    jeu: Literal["echecs", "coach", "penalty", "flechettes", ""] | None = None
    dossier: str | None = Field(default=None, pattern=r"^[a-z0-9_]{0,40}$")


@anim.patch("/stagiaires/{sid}")
def modifier_stagiaire(sid: int, corps: ModifStagiaire):
    with connexion() as db:
        if not services.un_stagiaire(db, sid):
            raise HTTPException(404, "Stagiaire introuvable.")
        for champ in ("prenom", "jeu", "dossier"):
            valeur = getattr(corps, champ)
            if valeur is not None:
                db.execute(f"UPDATE stagiaires SET {champ} = ? WHERE id = ?", (valeur or None, sid))
    return {"ok": True}


@anim.post("/stagiaires/{sid}/nouveau-code")
def nouveau_code(sid: int):
    """Si un code a circulé : on en crée un autre, et l'ancien ne marche plus (les sessions ouvertes sont fermées)."""
    with connexion() as db:
        code = auth.nouveau_code()
        if not db.execute("UPDATE stagiaires SET code = ? WHERE id = ?", (code, sid)).rowcount:
            raise HTTPException(404, "Stagiaire introuvable.")
        db.execute("DELETE FROM sessions WHERE stagiaire_id = ?", (sid,))
    return {"code": code}


@anim.delete("/stagiaires/{sid}")
def supprimer_stagiaire(sid: int):
    with connexion() as db:
        db.execute("DELETE FROM stagiaires WHERE id = ?", (sid,))
    return {"ok": True}


@anim.get("/stagiaires/{sid}")
def detail_stagiaire(sid: int):
    with connexion() as db:
        s = services.un_stagiaire(db, sid)
        if not s:
            raise HTTPException(404, "Stagiaire introuvable.")
        s["reponses"] = {l["cle"]: l["texte"] for l in db.execute("SELECT cle, texte FROM reponses WHERE stagiaire_id = ?", (sid,))}
        s["coches"] = {l["cle"]: bool(l["fait"]) for l in db.execute("SELECT cle, fait FROM coches WHERE stagiaire_id = ?", (sid,))}
        s["aides"] = [dict(l) for l in db.execute("SELECT * FROM aides WHERE stagiaire_id = ? ORDER BY id DESC", (sid,))]
        s["bugs"] = bugs_de(db, sid)
        s["avancement"] = services.avancement(db, s)
        return s


@anim.get("/aides")
def toutes_les_aides():
    with connexion() as db:
        return [dict(l) for l in db.execute(
            """SELECT a.*, s.prenom FROM aides a JOIN stagiaires s ON s.id = a.stagiaire_id
               ORDER BY CASE a.statut WHEN 'ouverte' THEN 0 WHEN 'repondue' THEN 1 ELSE 2 END, a.id DESC""")]


class ReponseAide(Strict):
    reponse: str | None = Field(default=None, max_length=2000)
    statut: Literal["ouverte", "repondue", "resolue"] | None = None


@anim.patch("/aides/{aid}")
def repondre_aide(aid: int, corps: ReponseAide):
    with connexion() as db:
        if corps.reponse is not None:
            db.execute("UPDATE aides SET reponse = ?, statut = 'repondue', maj = ? WHERE id = ?", (corps.reponse, maintenant(), aid))
        if corps.statut is not None:
            db.execute("UPDATE aides SET statut = ?, maj = ? WHERE id = ?", (corps.statut, maintenant(), aid))
    return {"ok": True}


class Surprise(Strict):
    activite: str
    stagiaire_id: int | None = None   # None = tous les stagiaires
    active: bool = True


@anim.post("/surprises")
def declencher_surprise(corps: Surprise):
    a = ACTIVITES_PAR_ID.get(corps.activite)
    if not a or not a["surprise"]:
        raise HTTPException(400, "Cette activité n'est pas une surprise.")
    with connexion() as db:
        ids = [corps.stagiaire_id] if corps.stagiaire_id else [s["id"] for s in services.stagiaires(db)]
        for sid in ids:
            if corps.active:
                db.execute("INSERT OR IGNORE INTO surprises (stagiaire_id, activite) VALUES (?, ?)", (sid, corps.activite))
            else:
                db.execute("DELETE FROM surprises WHERE stagiaire_id = ? AND activite = ?", (sid, corps.activite))
    return {"ok": True}


class Reglages(Strict):
    date_debut: str | None = Field(default=None, pattern=r"^(\d{4}-\d{2}-\d{2})?$")
    jour_force: str | None = Field(default=None, pattern=r"^[0-4]?$")
    choix_verrouille: bool | None = None
    # Ce que voient les stagiaires
    message: str | None = Field(default=None, max_length=1000)
    # Cette adresse est recopiée dans des commandes : on n'accepte que les caractères d'une adresse Git
    url_depot: str | None = Field(default=None, max_length=300, pattern=r"^[A-Za-z0-9@:/._~\-]*$")


@anim.put("/reglages")
def changer_reglages(corps: Reglages):
    with connexion() as db:
        for cle in ("message", "url_depot"):
            if getattr(corps, cle) is not None:
                ecrire_reglage(db, cle, getattr(corps, cle))
        if corps.date_debut is not None:
            ecrire_reglage(db, "date_debut", corps.date_debut)
        if corps.jour_force is not None:
            ecrire_reglage(db, "jour_force", corps.jour_force)
        if corps.choix_verrouille is not None:
            ecrire_reglage(db, "choix_verrouille", "1" if corps.choix_verrouille else "0")
    return {"ok": True}


@anim.get("/claude-md", response_class=PlainTextResponse)
def claude_md():
    """Le fichier CLAUDE.md du projet, avec la ligne « Les jeux de NOTRE projet » déjà remplie."""
    with connexion() as db:
        return contenu.claude_md_rempli(services.stagiaires(db))


def documents_disponibles() -> list[dict]:
    racine = CONTENU_DIR.resolve()
    docs = []
    for dossier, groupe in (("", "Le kit"), ("guides", "Guides"), ("autonomie", "Le guide des élèves"),
                            ("fiches", "Fiches"), ("prompts", "Prompts communs")):
        for f in sorted((racine / dossier).glob("*.md")):
            premiere = f.read_text(encoding="utf-8").splitlines()[:1]
            titre = premiere[0].lstrip("# ").strip() if premiere else f.stem
            docs.append({"fichier": str(f.relative_to(racine)), "titre": titre, "groupe": groupe})
    for jeu, infos in JEUX.items():
        for etape, f in infos["fichiers"].items():
            if (racine / f).exists():
                titre = (racine / f).read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
                docs.append({"fichier": f, "titre": titre, "groupe": f"{infos['icone']} {infos['nom']}"})
    return docs


@anim.get("/documents")
def documents():
    return documents_disponibles()


@anim.get("/document")
def document(fichier: str):
    if fichier not in {d["fichier"] for d in documents_disponibles()}:
        raise HTTPException(404, "Document introuvable.")
    texte = contenu.lire(fichier)
    with connexion() as db:
        texte = contenu.remplir_placeholders(texte, services.stagiaires(db))
    titre = texte.splitlines()[0].lstrip("# ").strip() if texte else fichier
    return {"fichier": fichier, "titre": titre,
            "blocs": contenu.en_blocs(contenu.decouper(texte), fichier)}


class Effacer(Strict):
    confirmation: str


@anim.post("/effacer-tout")
def effacer_tout(corps: Effacer):
    """À la fin du stage : on efface les stagiaires et tout ce qu'ils ont écrit (les données de mineurs ne traînent pas)."""
    if corps.confirmation != "EFFACER":
        raise HTTPException(400, "Écris EFFACER pour confirmer.")
    with connexion() as db:
        for table in ("coches", "reponses", "aides", "bugs", "surprises", "stagiaires"):
            db.execute(f"DELETE FROM {table}")
        db.execute("DELETE FROM sessions WHERE role = 'stagiaire'")
        db.execute("DELETE FROM reglages WHERE cle != 'date_debut'")
    return {"ok": True}

