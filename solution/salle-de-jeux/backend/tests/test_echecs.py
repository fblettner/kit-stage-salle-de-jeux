"""Tests automatiques : on vérifie que l'ordinateur fait des choses sensées.

Lancer avec :  pytest
"""
import time

import chess
from fastapi.testclient import TestClient

from app.main import app
from app.echecs.moteur import choisir_coup, evaluer

client = TestClient(app)


def test_le_coup_choisi_est_toujours_autorise():
    plateau = chess.Board()
    for niveau in (1, 2, 3):
        coup, _ = choisir_coup(plateau, niveau)
        assert coup in plateau.legal_moves


def test_position_de_depart_equilibree():
    assert evaluer(chess.Board()) == 0


def test_l_ordinateur_mange_une_dame_offerte():
    # La dame noire en d5 peut être prise gratuitement par le pion blanc e4
    plateau = chess.Board("rnb1kbnr/pppp1ppp/8/3q4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 3")
    coup, _ = choisir_coup(plateau, niveau=2)
    assert coup.uci() == "e4d5"


def test_l_ordinateur_trouve_un_mat_en_un_coup():
    # Mat du couloir : la tour blanche va en a8
    plateau = chess.Board("6k1/5ppp/8/8/8/8/8/R5K1 w - - 0 1")
    coup, _ = choisir_coup(plateau, niveau=2)
    assert coup.uci() == "a1a8"


def test_le_niveau_difficile_repond_assez_vite():
    plateau = chess.Board("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
    debut = time.time()
    choisir_coup(plateau, niveau=3)
    assert time.time() - debut < 5  # secondes


def test_api_repond_un_coup():
    reponse = client.post("/api/echecs/coup-ia", json={"fen": chess.STARTING_FEN, "niveau": 2})
    assert reponse.status_code == 200
    assert chess.Move.from_uci(reponse.json()["coup"]) in chess.Board().legal_moves


def test_api_refuse_une_position_invalide():
    reponse = client.post("/api/echecs/coup-ia", json={"fen": "n'importe quoi"})
    assert reponse.status_code == 400
