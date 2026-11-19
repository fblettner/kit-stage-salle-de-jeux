"""Les routes de l'API du jeu d'échecs. Toutes commencent par /api/echecs."""
import chess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.echecs.moteur import NIVEAUX, choisir_coup

routeur = APIRouter(prefix="/api/echecs", tags=["Échecs"])


class DemandeCoup(BaseModel):
    """Ce que le navigateur nous envoie : la position et le niveau choisi."""

    fen: str
    niveau: int = Field(default=2, ge=1, le=3)


@routeur.get("/statut")
def statut():
    return {"jeu": "echecs", "message": "Le jeu d'échecs est prêt ♞"}


@routeur.get("/niveaux")
def niveaux():
    """La liste des niveaux de difficulté disponibles."""
    return [{"niveau": n, "nom": r["nom"]} for n, r in NIVEAUX.items()]


@routeur.post("/coup-ia")
def coup_ia(demande: DemandeCoup):
    """Choisit le coup de l'ordinateur avec l'algorithme minimax."""
    try:
        plateau = chess.Board(demande.fen)
    except ValueError:
        raise HTTPException(status_code=400, detail="Position invalide")

    if plateau.is_game_over():
        raise HTTPException(status_code=400, detail="La partie est déjà terminée")

    coup, positions_examinees = choisir_coup(plateau, demande.niveau)

    return {
        "coup": coup.uci(),
        "positions_examinees": positions_examinees,
    }
