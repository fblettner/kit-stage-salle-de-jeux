import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["ANIMATEUR_MOT_DE_PASSE"] = "secret-test"
os.environ["SALLE"] = "0"   # pas besoin de lancer les jeux d'exemple pour tester le compagnon

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import base, contenu, services  # noqa: E402
from app.base import connexion  # noqa: E402
from app.main import app  # noqa: E402
from app.programme import ACTIVITES, JEUX  # noqa: E402

base.initialiser()


@pytest.fixture()
def client():
    with TestClient(app) as c:
        a = c.post("/api/connexion/animateur", json={"mot_de_passe": "secret-test"}).json()["jeton"]
        c.post("/api/animateur/effacer-tout", json={"confirmation": "EFFACER"}, headers=h(a))
        c.put("/api/animateur/reglages", json={"jour_force": "", "date_debut": "", "choix_verrouille": False,
                                               "message": "", "url_depot": ""}, headers=h(a))
        c.anim = a
        yield c


def h(jeton):
    return {"Authorization": f"Bearer {jeton}"}


def creer(c, prenom, jeu=None):
    r = c.post("/api/animateur/stagiaires", json={"prenom": prenom}, headers=h(c.anim)).json()
    jeton = c.post("/api/connexion/stagiaire", json={"code": r["code"].lower()}).json()["jeton"]
    if jeu:
        assert c.put("/api/moi/jeu", json={"jeu": jeu}, headers=h(jeton)).status_code == 200
    return r["id"], jeton


# ---------------------------------------------------------------- le contenu des fichiers .md

def test_chaque_activite_a_du_contenu_pour_chaque_jeu():
    """Si quelqu'un renomme un titre dans un fichier .md, ce test le signale."""
    with connexion() as db:
        for a in ACTIVITES:
            if not a["source"]:
                continue
            for jeu in JEUX:
                r = services.contenu_activite(db, a, "animateur", jeu, jeu, True)
                assert r["blocs"], f"{a['id']} est vide pour {jeu}"


def test_les_etapes_perso_ont_des_prompts_et_des_cases_a_cocher():
    with connexion() as db:
        for a in ACTIVITES:
            if a["mode"] != "perso" or a["id"] == "j4":
                continue
            for jeu in JEUX:
                types = {b["type"] for b in services.contenu_activite(db, a, "stagiaire", jeu, jeu, True)["blocs"]}
                assert "prompt" in types, (a["id"], jeu)
                if a["id"] in ("m5", "w1", "w3"):
                    assert "verif" in types, (a["id"], jeu)


def test_le_matin_et_l_apres_midi_sont_bien_separes():
    texte = contenu.lire(JEUX["flechettes"]["fichiers"][34])
    matin = contenu.decouper(texte, "Matin", "Après-midi")
    aprem = contenu.decouper(texte, "Après-midi")
    assert "D3a" in matin and "D4a" not in matin
    assert "D4a" in aprem and "D3a" not in aprem


def test_si_ca_coince_renvoie_au_dernier_commit():
    # Plus de « point de sauvegarde » : quand on est bloqué, on revient à SON dernier commit
    with connexion() as db:
        a = next(a for a in ACTIVITES if a["id"] == "w3")
        for jeu in JEUX:
            tout = tout_le_texte(services.contenu_activite(db, a, "stagiaire", jeu, jeu, True)["blocs"])
            assert "git checkout" not in tout and "dernier commit" in tout


def test_la_surprise_cache_les_conseils_a_l_animateur():
    with connexion() as db:
        a = next(a for a in ACTIVITES if a["id"] == "j3")
        verrouille = services.contenu_activite(db, a, "stagiaire", "echecs", "echecs", False)
        assert verrouille["verrouille"] and not verrouille["blocs"]
        blocs = services.contenu_activite(db, a, "stagiaire", "echecs", "echecs", True)["blocs"]
        tout = "\n".join(b.get("texte", "") for b in blocs)
        assert "mode débutant" in tout          # le prompt
        assert "petits ne savent pas" in tout   # la parole du client
        assert "Laisse l'élève" not in tout     # le conseil à l'animateur


def test_deux_agences_concurrentes_renomment_le_dossier():
    p = "Crée backend/app/flechettes/ia.py, la route /api/flechettes/lancer, tests/test_flechettes.py, " \
        "des classes qui commencent par flechettes- dans flechettes.css. Je travaille sur les fléchettes."
    r = contenu.remplacer_dossier(p, "flechettes", "flechettes_lea")
    assert "app/flechettes_lea/ia.py" in r and "/api/flechettes_lea/lancer" in r
    assert "test_flechettes_lea.py" in r and "flechettes_lea-" in r and "flechettes_lea.css" in r
    assert "sur les fléchettes" in r


def test_les_placeholders_du_socle_sont_remplis():
    st = [{"prenom": "Léa", "jeu": "penalty", "dossier": "penalty"}, {"prenom": "Tom", "jeu": "flechettes", "dossier": "flechettes"}]
    j2 = contenu.remplir_placeholders(contenu.lire("prompts/J2-architecture-et-socle.md"), st)
    assert "[xxx]" not in j2 and "Penalty Pro, dossier penalty" in j2 and "/api/flechettes" in j2
    j1 = contenu.remplir_placeholders(contenu.lire("prompts/J1-le-besoin.md"), st)
    assert "Penalty Pro, des tirs au but (Léa)" in j1 and "[EX." not in j1
    assert "Penalty Pro (Léa, dossier `penalty`)" in contenu.claude_md_rempli(st)


def test_catalogue_lexique_et_carnet():
    assert [f["jeu"] for f in contenu.catalogue()] == list(JEUX)
    assert all(f["texte"] for f in contenu.catalogue())
    mots = contenu.lexique()
    assert any(m["mot"] == "API" for m in mots) and len(mots) > 20
    jours = contenu.questions_carnet()
    assert [j["titre"].split(" ")[0] for j in jours] == ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Bilan"]
    tableau = next(q for q in jours[2]["questions"] if q["type"] == "tableau")
    assert tableau["lignes"] == ["Facile", "Moyen", "Difficile"]


# ---------------------------------------------------------------- l'API

def test_connexions(client):
    assert client.post("/api/connexion/animateur", json={"mot_de_passe": "faux"}).status_code == 401
    assert client.post("/api/connexion/stagiaire", json={"code": "ZZZZZZ"}).status_code == 401
    assert client.get("/api/programme").status_code == 401
    _, jeton = creer(client, "Léa")
    assert client.get("/api/animateur/tableau", headers=h(jeton)).status_code == 403
    assert client.get("/api/moi", headers=h(client.anim)).status_code == 403


def test_parcours_d_un_stagiaire(client):
    sid, jeton = creer(client, "Léa", "penalty")
    moi = client.get("/api/moi", headers=h(jeton)).json()
    assert moi["jeu"] == "penalty" and moi["dossier"] == "penalty"
    m5 = client.get("/api/activite/m5", headers=h(jeton)).json()
    assert m5["phrase_depart"] == "« Je travaille sur Penalty Pro. »"
    cle = next(b for b in m5["blocs"] if b["type"] == "verif")["items"][0]["cle"]
    client.put("/api/moi/coche", json={"cle": cle, "fait": True}, headers=h(jeton))
    client.put("/api/moi/coche", json={"cle": "fini:m5", "fait": True}, headers=h(jeton))
    client.put("/api/moi/reponse", json={"cle": "1-1", "texte": "Il crée des logiciels."}, headers=h(jeton))
    moi = client.get("/api/moi", headers=h(jeton)).json()
    assert moi["reponses"]["1-1"] == "Il crée des logiciels."
    assert moi["avancement"]["m5"]["fini"] and moi["avancement"]["m5"]["coches"] == 1
    detail = client.get(f"/api/animateur/stagiaires/{sid}", headers=h(client.anim)).json()
    assert detail["reponses"]["1-1"] == "Il crée des logiciels."


def test_meme_jeu_deux_dossiers(client):
    _, lea = creer(client, "Léa", "flechettes")
    _, tom = creer(client, "Tom", "flechettes")
    assert client.get("/api/moi", headers=h(lea)).json()["dossier"] == "flechettes_lea"
    w3 = client.get("/api/activite/w3", headers=h(tom)).json()
    prompts = "\n".join(b["texte"] for b in w3["blocs"] if b["type"] == "prompt")
    assert "backend/app/flechettes_tom/ia.py" in prompts and "/api/flechettes_tom/ia/volee" in prompts


def test_surprise_declenchee_par_l_animateur(client):
    sid, lea = creer(client, "Léa", "coach")
    assert client.get("/api/activite/j3", headers=h(lea)).json()["verrouille"]
    client.post("/api/animateur/surprises", json={"activite": "j3"}, headers=h(client.anim))
    j3 = client.get("/api/activite/j3", headers=h(lea)).json()
    assert not j3["verrouille"] and any("mi-temps" in b.get("texte", "") for b in j3["blocs"])
    assert client.post("/api/animateur/surprises", json={"activite": "m5"}, headers=h(client.anim)).status_code == 400


def test_aides_et_bugs(client):
    lea_id, lea = creer(client, "Léa", "echecs")
    tom_id, tom = creer(client, "Tom", "coach")
    client.post("/api/moi/aides", json={"activite": "m5", "message": "Mon échiquier ne s'affiche pas"}, headers=h(lea))
    aides = client.get("/api/animateur/aides", headers=h(client.anim)).json()
    assert aides[0]["prenom"] == "Léa" and aides[0]["statut"] == "ouverte"
    client.patch(f"/api/animateur/aides/{aides[0]['id']}", json={"reponse": "Relance npm run dev"}, headers=h(client.anim))
    assert client.get("/api/moi", headers=h(lea)).json()["aides"][0]["reponse"] == "Relance npm run dev"
    # Tom teste le jeu de Léa
    assert client.post("/api/moi/bugs", json={"cible_id": tom_id, "action": "aa", "resultat": "bb", "attendu": "cc"},
                       headers=h(tom)).status_code == 400
    client.post("/api/moi/bugs", json={"cible_id": lea_id, "action": "Je roque", "resultat": "Le roi disparaît",
                                       "attendu": "Le roi et la tour bougent"}, headers=h(tom))
    recus = client.get("/api/moi", headers=h(lea)).json()["bugs"]["recus"]
    assert recus[0]["auteur"] == "Tom"
    assert client.put(f"/api/moi/bugs/{recus[0]['id']}", json={"corrige": True}, headers=h(tom)).status_code == 404
    assert client.put(f"/api/moi/bugs/{recus[0]['id']}", json={"corrige": True}, headers=h(lea)).status_code == 200


def test_verrouillage_des_choix_et_nouveau_code(client):
    sid, lea = creer(client, "Léa", "echecs")
    client.put("/api/animateur/reglages", json={"choix_verrouille": True}, headers=h(client.anim))
    assert client.put("/api/moi/jeu", json={"jeu": "coach"}, headers=h(lea)).status_code == 409
    client.post(f"/api/animateur/stagiaires/{sid}/nouveau-code", headers=h(client.anim))
    assert client.get("/api/moi", headers=h(lea)).status_code == 401


def test_jour_actuel(client):
    client.put("/api/animateur/reglages", json={"jour_force": "2"}, headers=h(client.anim))
    p = client.get("/api/programme", headers=h(client.anim)).json()
    assert p["jour_actuel"] == 2 and p["activite_actuelle"].startswith("w")
    assert len(p["jours"]) == 5


def test_documents_et_effacer_tout(client):
    docs = client.get("/api/animateur/documents", headers=h(client.anim)).json()
    assert any(d["fichier"] == "guides/deploiement-oci.md" for d in docs)
    assert client.get("/api/animateur/document", params={"fichier": "../../etc/passwd"}, headers=h(client.anim)).status_code == 404
    assert client.get("/api/animateur/document", params={"fichier": "00-LISEZ-MOI.md"}, headers=h(client.anim)).json()["blocs"]
    creer(client, "Léa")
    assert client.post("/api/animateur/effacer-tout", json={"confirmation": "oui"}, headers=h(client.anim)).status_code == 400
    client.post("/api/animateur/effacer-tout", json={"confirmation": "EFFACER"}, headers=h(client.anim))
    assert client.get("/api/animateur/tableau", headers=h(client.anim)).json()["stagiaires"] == []


# ---------------------------------------------------------------- le guide des élèves (dossier autonomie/)

def reglages(c, **corps):
    assert c.put("/api/animateur/reglages", json=corps, headers=h(c.anim)).status_code == 200


def tout_le_texte(blocs):
    morceaux = []
    for b in blocs:
        morceaux.append(b.get("texte", ""))
        morceaux.extend(i["texte"] for i in b.get("items", []))
        morceaux.append(tout_le_texte(b.get("blocs", [])))
    return "\n".join(morceaux)


def test_chaque_activite_ensemble_a_son_guide_pour_les_eleves():
    """Si quelqu'un renomme un « ## l3 · … » dans autonomie/parcours-eleves.md, ce test le signale."""
    for a in ACTIVITES:
        if a["mode"] != "ensemble":
            continue
        blocs = contenu.guide_brut(a["id"])
        assert blocs, f"pas de guide élèves pour {a['id']}"
        assert any(b["type"] == "verif" for b in blocs), f"pas de cases à cocher dans le guide de {a['id']}"
    assert contenu.routine_du_matin() and len(contenu.depannage()) > 5
    # Rien dans ces textes ne suppose que le maître de stage est absent
    for fichier in (contenu.GUIDE, contenu.DEPANNAGE):
        assert "n'est pas là" not in contenu.lire(fichier) and "{{referent}}" not in contenu.lire(fichier)


def test_les_activites_ensemble_sont_guidees_pour_les_eleves(client):
    _, lea = creer(client, "Léa", "echecs")
    creer(client, "Tom", "coach")
    reglages(client, url_depot="git@exemple.fr:stage/salle.git")
    # L'interview : Claude peut jouer le client, avec un prompt « secret »
    l3 = client.get("/api/activite/l3", headers=h(lea)).json()
    assert any(b["type"] == "prompt" and b.get("secret") for b in l3["blocs"])
    assert any(b["type"] == "verif" for b in l3["blocs"])
    # Les {{…}} sont remplacés par les réglages et par les choix des stagiaires
    m4 = tout_le_texte(client.get("/api/activite/m4", headers=h(lea)).json()["blocs"])
    assert "git clone git@exemple.fr:stage/salle.git" in m4 and "git switch -c echecs" in m4 and "{{" not in m4
    j5 = tout_le_texte(client.get("/api/activite/j5", headers=h(lea)).json()["blocs"])
    assert "git merge origin/echecs" in j5 and "git merge origin/coach" in j5
    # [[PROMPTS]] reprend le prompt de la fiche de l'animateur, déjà rempli avec les jeux choisis
    l5 = client.get("/api/activite/l5", headers=h(lea)).json()["blocs"]
    assert any(b["type"] == "prompt" and "les échecs (Léa) et Coach" in b["texte"] for b in l5)
    assert "[[" not in tout_le_texte(l5)
    # [[CLAUDE_MD]] donne le fichier déjà rempli
    m2 = client.get("/api/activite/m2", headers=h(lea)).json()["blocs"]
    fichier = next(b for b in m2 if b["type"] == "fichier")
    assert fichier["nom"] == "CLAUDE.md" and "Échecs (Léa, dossier `echecs`)" in fichier["texte"]
    # Les cases cochées dans le guide comptent dans l'avancement
    cle = next(b for b in l3["blocs"] if b["type"] == "verif")["items"][0]["cle"]
    client.put("/api/moi/coche", json={"cle": cle, "fait": True}, headers=h(lea))
    av = client.get("/api/moi", headers=h(lea)).json()["avancement"]["l3"]
    assert av["coches"] == 1 and av["total"] >= 3
    # L'animateur, lui, garde sa fiche (les réponses du client), et peut relire le guide des élèves
    fiche = client.get("/api/activite/l3", headers=h(client.anim)).json()
    assert "Tu joues" in tout_le_texte(fiche["blocs"]) and fiche["guide"]
    assert "Tu joues" not in tout_le_texte([b for b in l3["blocs"] if not b.get("secret")])


def test_deux_cases_identiques_dans_deux_activites_ont_des_cles_differentes():
    cles = [i["cle"] for a in ACTIVITES if a["mode"] == "ensemble"
            for b in contenu.guide_brut(a["id"]) if b["type"] == "verif" for i in b["items"]]
    assert len(cles) == len(set(cles))


def test_la_routine_du_matin(client):
    _, lea = creer(client, "Léa", "penalty")
    w1 = client.get("/api/activite/w1", headers=h(lea)).json()["blocs"]
    assert w1[0]["type"] == "repli" and "fastapi dev" in tout_le_texte(w1[0]["blocs"])


def test_depannage_presence_et_bilan(client):
    sid, lea = creer(client, "Léa", "echecs")
    reglages(client, message="Bon courage pour l'étape 3 !")
    assert "échelle" in tout_le_texte(client.get("/api/depannage", headers=h(lea)).json())
    assert client.get("/api/programme", headers=h(lea)).json()["message"] == "Bon courage pour l'étape 3 !"
    # « La salle de jeux » : désactivée pendant les tests, donc pas dans le menu et pas servie
    assert client.get("/api/programme", headers=h(lea)).json()["salle"] is False
    assert client.get("/jeux/").status_code == 404 and client.get("/api/echecs/statut").status_code == 404
    client.put("/api/moi/reponse", json={"cle": "bilan-1", "texte": "Mon échiquier s'affiche."}, headers=h(lea))
    client.get("/api/moi", headers=h(lea))   # son écran est ouvert : l'animateur le voit « en ligne »
    s = client.get("/api/animateur/tableau", headers=h(client.anim)).json()["stagiaires"][0]
    assert s["vu_le"] and s["bilans"] == {"bilan-1": "Mon échiquier s'affiche."}
    # Les réglages refusent une adresse de dépôt qui contiendrait une commande
    assert client.put("/api/animateur/reglages", json={"url_depot": "x; rm -rf ~"}, headers=h(client.anim)).status_code == 422
