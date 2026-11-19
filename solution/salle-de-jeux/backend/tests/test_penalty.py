"""Tests automatiques de Penalty Pro.

Lancer avec :  pytest
"""
import inspect
import random

from fastapi.testclient import TestClient

from app.main import app
from app.penalty.ia import ZONES, choisir_plongeon, choisir_tir, predire, zone_de
from app.penalty.physique import arbitrer, distance, portee_gardien, trajectoire

client = TestClient(app)


def taux_de_but(cible, puissance, plongeon, n=2000, graine=1):
    rng = random.Random(graine)
    return sum(arbitrer(trajectoire(cible, puissance, rng), plongeon, puissance) == "but" for _ in range(n)) / n


# --- La physique et l'arbitre ----------------------------------------------------

def test_un_tir_doux_est_precis_un_tir_fort_beaucoup_moins():
    rng = random.Random(3)
    ecart_doux = sum(distance(trajectoire((0.5, 0.5), 0.2, rng), (0.5, 0.5)) for _ in range(500))
    ecart_fort = sum(distance(trajectoire((0.5, 0.5), 1.0, rng), (0.5, 0.5)) for _ in range(500))
    assert ecart_fort > 3 * ecart_doux


def test_un_tir_trop_fort_en_lucarne_passe_souvent_au_dessus():
    rng = random.Random(4)
    dehors = sum(arbitrer(trajectoire((0.08, 0.12), 1.0, rng), (-9, -9), 1.0) in ("dehors", "poteau") for _ in range(1000))
    assert dehors > 400


def test_le_gardien_arrete_mieux_les_tirs_lents():
    assert portee_gardien(0.2) > portee_gardien(0.9)
    # Gardien bien placé : un tir lent est presque toujours arrêté, un tir fort passe plus souvent
    assert taux_de_but((0.1, 0.8), 0.3, (1 / 6, 0.75)) < 0.05
    assert taux_de_but((0.1, 0.8), 0.9, (1 / 6, 0.75)) > 0.3


def test_arbitre():
    assert arbitrer((0.5, 0.5), (0.5, 0.5), 0.5) == "arret"
    assert arbitrer((0.05, 0.1), (0.9, 0.8), 0.5) == "but"
    assert arbitrer((0.5, -0.2), (0.5, 0.5), 0.5) == "dehors"
    assert arbitrer((1.01, 0.5), (0.5, 0.5), 0.5) == "poteau"


# --- L'IA ------------------------------------------------------------------------

def test_les_zones():
    assert zone_de((0.1, 0.2)) == "haut-gauche"
    assert zone_de((0.99, 0.9)) == "bas-droite"
    assert zone_de((0.5, 0.5)) == "bas-centre"


def test_le_gardien_moyen_plonge_la_ou_on_tire_le_plus():
    historique = [(0.1, 0.2), (0.12, 0.15), (0.08, 0.22), (0.9, 0.8)]
    for graine in range(20):
        decision = choisir_plongeon(historique, 2, random.Random(graine))
        assert decision["zone"] == "haut-gauche"
        # … et à l'endroit précis où on vise d'habitude
        assert abs(decision["plongeon"]["x"] - 0.1) < 0.01


def test_le_gardien_difficile_repere_les_enchainements():
    # On alterne bas-gauche / haut-droite, et on vient de tirer en bas à gauche
    historique = [(0.1, 0.8), (0.9, 0.2), (0.1, 0.8), (0.9, 0.2), (0.1, 0.8)]
    assert choisir_plongeon(historique, 2, random.Random(1))["zone"] == "bas-gauche"
    for graine in range(20):
        assert choisir_plongeon(historique, 3, random.Random(graine))["zone"] == "haut-droite"


def test_les_probabilites_font_100_pourcent():
    for niveau in (1, 2, 3):
        prediction, _ = predire([(0.1, 0.8), (0.9, 0.2)], niveau)
        assert abs(sum(prediction.values()) - 1) < 1e-9 and set(prediction) == set(ZONES)


def test_le_tireur_evite_la_zone_ou_le_joueur_plonge_toujours():
    historique = [(0.15, 0.8)] * 6
    for graine in range(20):
        assert choisir_tir(historique, 3, random.Random(graine))["zone"] != "bas-gauche"


def test_l_ia_ne_peut_pas_tricher():
    # Les fonctions de l'IA ne reçoivent même pas le choix en cours du joueur
    assert list(inspect.signature(choisir_plongeon).parameters) == ["historique_tirs", "niveau", "rng"]
    assert list(inspect.signature(choisir_tir).parameters) == ["historique_plongeons", "niveau", "rng"]


# --- L'API -----------------------------------------------------------------------

def test_api_tir():
    reponse = client.post("/api/penalty/tir", json={"cible": {"x": 0.1, "y": 0.2}, "puissance": 0.7, "niveau": 2})
    assert reponse.status_code == 200
    assert reponse.json()["resultat"] in ("but", "arret", "poteau", "dehors")
    assert reponse.json()["zone_visee"] == "haut-gauche"


def test_api_arret():
    reponse = client.post("/api/penalty/arret", json={"plongeon": {"x": 0.5, "y": 0.5}, "historique": [{"x": 0.2, "y": 0.7}]})
    assert reponse.status_code == 200
    assert 0 <= reponse.json()["puissance"] <= 1


def test_api_refuse_une_cible_hors_du_but():
    reponse = client.post("/api/penalty/tir", json={"cible": {"x": 1.5, "y": 0.2}, "puissance": 0.7})
    assert reponse.status_code == 422
