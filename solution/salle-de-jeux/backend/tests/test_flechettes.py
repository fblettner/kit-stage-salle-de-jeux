"""Tests automatiques des fléchettes.

Lancer avec :  pytest
"""
import random

from fastapi.testclient import TestClient

from app.flechettes.cible import appliquer, score
from app.flechettes.ia import NIVEAUX, T20, choisir_visee, estimer_ecart, jouer_volee, tirages, valeur_moyenne
from app.main import app

client = TestClient(app)


# --- La cible --------------------------------------------------------------------

def test_les_zones_de_la_cible():
    assert score(0, 0)["points"] == 50          # le centre
    assert score(0, 10)["points"] == 25         # l'anneau autour du centre
    assert score(0, 103)["libelle"] == "T20"    # triple 20, en haut
    assert score(0, 166)["libelle"] == "D20"    # double 20, tout en haut
    assert score(0, 140)["points"] == 20        # simple 20
    assert score(103, 0)["libelle"] == "T6"     # le 6 est à droite
    assert score(-103, 0)["libelle"] == "T11"   # le 11 est à gauche
    assert score(0, -103)["libelle"] == "T3"    # le 3 est en bas
    assert score(0, 200)["points"] == 0         # hors de la cible


def test_les_regles_du_301():
    t20, d20, s5 = score(0, 103), score(0, 166), score(-40, 120)
    assert appliquer(301, t20, False) == ("ok", 241)
    assert appliquer(40, t20, False) == ("bust", 40)         # on ne descend pas sous 0
    assert appliquer(40, d20, True) == ("gagne", 0)          # finir sur un double
    assert appliquer(60, t20, True) == ("bust", 60)          # avec « double pour finir », un triple ne suffit pas
    assert appliquer(60, t20, False) == ("gagne", 0)         # sans l'option, c'est gagné
    assert appliquer(6, s5, True) == ("bust", 6)             # rester à 1 est impossible avec un double à la fin


# --- L'IA ------------------------------------------------------------------------

def test_un_champion_vise_le_triple_20():
    choix = choisir_visee(301, False, 5, random.Random(1))
    assert choix["libelle"] == "T20"


def test_un_joueur_imprecis_a_interet_a_ne_pas_viser_le_triple_20():
    rng = random.Random(2)
    choix = choisir_visee(301, False, 40, rng)
    assert choix["libelle"] != "T20"
    # … et c'est vrai : sur 2000 lancers, son choix rapporte plus que le triple 20
    ecarts = tirages(40, 2000, random.Random(3))
    visee = (choix["visee"]["x"], choix["visee"]["y"])
    assert valeur_moyenne(visee, 301, False, ecarts) < valeur_moyenne(T20, 301, False, ecarts)


def test_l_ia_sait_finir():
    rng = random.Random(4)
    assert choisir_visee(40, True, 8, rng)["libelle"] == "D20"
    assert choisir_visee(50, True, 5, rng)["libelle"] == "Bull 50"


def test_une_volee_respecte_les_regles():
    for graine in range(30):
        volee = jouer_volee(60, True, 2, random.Random(graine))
        assert 1 <= len(volee["flechettes"]) <= 3
        assert volee["restant"] in range(0, 61) and volee["restant"] != 1


def test_le_niveau_difficile_finit_plus_vite():
    def volees_pour_finir(niveau, graine):
        rng, restant, n = random.Random(graine), 301, 0
        while restant > 0 and n < 60:
            restant = jouer_volee(restant, False, niveau, rng)["restant"]
            n += 1
        return n
    facile = sum(volees_pour_finir(1, g) for g in range(6))
    difficile = sum(volees_pour_finir(3, g) for g in range(6))
    assert difficile < facile


def test_le_conseiller_mesure_la_precision():
    assert estimer_ecart([]) == 25.0
    precis = estimer_ecart([((0, 0), (3, 0))] * 20)
    imprecis = estimer_ecart([((0, 0), (60, 0))] * 20)
    assert precis < 10 < 30 < imprecis


# --- L'API -----------------------------------------------------------------------

def test_api_lancer():
    reponse = client.post("/api/flechettes/lancer", json={"impact": {"x": 0, "y": 103}, "restant": 301})
    assert reponse.json() == {"points": 60, "double": False, "libelle": "T20", "resultat": "ok", "restant": 241}


def test_api_volee_ia():
    reponse = client.post("/api/flechettes/ia/volee", json={"restant": 301, "niveau": NIVEAUX[3] and 3})
    assert reponse.status_code == 200
    assert len(reponse.json()["carte"]) > 100


def test_api_conseil():
    lancers = [{"visee": {"x": 0, "y": 103}, "impact": {"x": 8, "y": 95}}] * 5
    reponse = client.post("/api/flechettes/conseil", json={"restant": 40, "double_sortie": True, "lancers": lancers})
    assert reponse.status_code == 200
    assert "lancers" in reponse.json()["explication"]
