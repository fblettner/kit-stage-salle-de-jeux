"""Tests automatiques du jeu Coach.

Lancer avec :  pytest
"""
import random

from fastapi.testclient import TestClient

from app.coach.ia import choisir_tactique, predire_tactique
from app.coach.joueurs import BUDGET, EQUIPES_IA, JOUEURS, JOUEURS_PAR_ID, cout_equipe
from app.coach.simulateur import TACTIQUES, simuler
from app.main import app

client = TestClient(app)

# Une équipe valide (1 gardien, 4 joueurs de champ, 43 M€) avec une star en attaque
EQUIPE_STAR = [4, 10, 9, 15, 16]
# Une équipe valide (45 M€) très défensive
EQUIPE_DEFENSE = [3, 6, 13, 9, 20]


def equipe(ids):
    return [JOUEURS_PAR_ID[i] for i in ids]


def resultat_moyen(ids_a, tactique_a, equipe_b, tactique_b, n=300, graine=1):
    """Renvoie (victoires de A, nuls, défaites de A, buts par match) sur n matchs simulés."""
    rng = random.Random(graine)
    v = nul = d = buts = 0
    for _ in range(n):
        a, b = simuler(equipe(ids_a), tactique_a, equipe_b, tactique_b, rng=rng, commentaires=False)["score"]
        v += a > b
        nul += a == b
        d += a < b
        buts += a + b
    return v / n, nul / n, d / n, buts / n


# --- Les données -----------------------------------------------------------------

def test_les_prix_et_notes_sont_raisonnables():
    for j in JOUEURS:
        assert 3 <= j["prix"] <= 30
        assert 50 <= j["note"] <= 99


def test_les_equipes_de_test_respectent_le_budget():
    assert cout_equipe(equipe(EQUIPE_STAR)) <= BUDGET
    assert cout_equipe(equipe(EQUIPE_DEFENSE)) <= BUDGET


# --- Le moteur de match ----------------------------------------------------------

def test_un_match_est_reproductible_avec_la_meme_graine():
    adverse = EQUIPES_IA[2]["joueurs"]
    r1 = simuler(equipe(EQUIPE_STAR), "offensive", adverse, "contre", rng=random.Random(42))
    r2 = simuler(equipe(EQUIPE_STAR), "offensive", adverse, "contre", rng=random.Random(42))
    assert r1 == r2


def test_le_score_correspond_aux_buts_commentes():
    r = simuler(equipe(EQUIPE_STAR), "offensive", EQUIPES_IA[2]["joueurs"], "offensive", rng=random.Random(7))
    buts = [e for e in r["evenements"] if e["type"] == "but"]
    assert len(buts) == sum(r["score"])
    assert len(r["possession"]) == 90


def test_une_seconde_mi_temps_part_du_score_de_la_premiere():
    r = simuler(equipe(EQUIPE_STAR), "equilibree", EQUIPES_IA[2]["joueurs"], "equilibree",
                minute_debut=46, score=(2, 1), rng=random.Random(3))
    assert r["score"][0] >= 2 and r["score"][1] >= 1
    assert len(r["possession"]) == 45


def test_la_meilleure_equipe_gagne_plus_souvent():
    victoires, _, defaites, _ = resultat_moyen(EQUIPE_STAR, "equilibree", EQUIPES_IA[1]["joueurs"], "equilibree")
    assert victoires > 0.5 > defaites


def test_jouer_offensif_donne_des_matchs_avec_plus_de_buts():
    *_, buts_offensif = resultat_moyen(EQUIPE_STAR, "offensive", EQUIPES_IA[2]["joueurs"], "offensive")
    *_, buts_defensif = resultat_moyen(EQUIPE_STAR, "defensive", EQUIPES_IA[2]["joueurs"], "defensive")
    assert buts_offensif > buts_defensif + 1


def test_la_contre_attaque_punit_le_jeu_offensif():
    # Contre une équipe offensive, l'ordinateur gagne plus souvent en contre-attaque qu'en jouant offensif lui aussi
    adverse = EQUIPES_IA[2]["joueurs"]
    _, _, ia_gagne_en_contre, _ = resultat_moyen(EQUIPE_STAR, "offensive", adverse, "contre", n=600)
    _, _, ia_gagne_en_offensif, _ = resultat_moyen(EQUIPE_STAR, "offensive", adverse, "offensive", n=600)
    assert ia_gagne_en_contre > ia_gagne_en_offensif


# --- L'entraîneur IA -------------------------------------------------------------

def test_l_entraineur_apprend_les_habitudes():
    prediction = predire_tactique(["offensive", "offensive", "offensive", "pressing"])
    assert max(prediction, key=prediction.get) == "offensive"
    assert abs(sum(prediction.values()) - 1) < 1e-9


def test_le_rapport_est_coherent():
    decision = choisir_tactique(equipe(EQUIPE_STAR), EQUIPES_IA[2]["joueurs"], ["offensive"], niveau=2, graine=1)
    assert decision["matchs_simules"] == 100 * len(TACTIQUES)
    for ligne in decision["rapport"]:
        assert 98 <= ligne["victoire"] + ligne["nul"] + ligne["defaite"] <= 102  # arrondis
    # La tactique choisie est celle qui rapporte le plus de points
    assert decision["tactique"] == max(decision["rapport"], key=lambda l: l["points"])["tactique"]


def test_l_entraineur_difficile_fait_mieux_que_le_hasard():
    # Le joueur joue toujours offensif. L'entraîneur difficile l'a remarqué…
    historique = ["offensive"] * 5
    adverse = EQUIPES_IA[3]["joueurs"]
    choix = choisir_tactique(equipe(EQUIPE_STAR), adverse, historique, niveau=3, graine=2)["tactique"]
    _, _, ia_gagne_choix, _ = resultat_moyen(EQUIPE_STAR, "offensive", adverse, choix, n=600, graine=9)
    moyenne_hasard = sum(
        resultat_moyen(EQUIPE_STAR, "offensive", adverse, t, n=200, graine=9)[2] for t in TACTIQUES
    ) / len(TACTIQUES)
    assert ia_gagne_choix > moyenne_hasard


# --- L'API -----------------------------------------------------------------------

def test_api_catalogue():
    reponse = client.get("/api/coach/joueurs").json()
    assert reponse["budget"] == BUDGET and len(reponse["joueurs"]) == len(JOUEURS)


def test_api_refuse_une_equipe_trop_chere():
    trop_chere = [1, 5, 11, 16, 17]  # les meilleurs joueurs : bien plus que 50 M€
    reponse = client.post("/api/coach/match", json={"equipe": trop_chere, "tactique": "offensive", "tactique_ia": "contre"})
    assert reponse.status_code == 400
    assert "Budget" in reponse.json()["detail"]


def test_api_refuse_deux_gardiens():
    reponse = client.post("/api/coach/match", json={"equipe": [3, 4, 9, 10, 15], "tactique": "offensive", "tactique_ia": "contre"})
    assert reponse.status_code == 400


def test_api_l_entraineur_ne_peut_pas_recevoir_la_tactique_du_joueur():
    reponse = client.post("/api/coach/entraineur", json={"equipe": EQUIPE_STAR, "niveau": 2, "tactique": "offensive"})
    assert reponse.status_code == 422


def test_api_match_complet():
    decision = client.post("/api/coach/entraineur", json={"equipe": EQUIPE_STAR, "niveau": 2}).json()
    reponse = client.post("/api/coach/match", json={
        "equipe": EQUIPE_STAR, "tactique": "pressing", "niveau": 2, "tactique_ia": decision["tactique"]})
    assert reponse.status_code == 200
    assert {e["equipe"] for e in reponse.json()["evenements"]} <= {"joueur", "ia", None}
