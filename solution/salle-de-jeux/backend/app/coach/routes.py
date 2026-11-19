"""Les routes de l'API du jeu Coach. Toutes commencent par /api/coach."""
import random
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.coach.ia import NIVEAUX, choisir_tactique
from app.coach.joueurs import BUDGET, EQUIPES_IA, JOUEURS, JOUEURS_PAR_ID, POSTES, TAILLE_EQUIPE, cout_equipe
from app.coach.simulateur import TACTIQUES, simuler

routeur = APIRouter(prefix="/api/coach", tags=["Coach"])

Tactique = Literal["defensive", "equilibree", "offensive", "pressing", "contre"]


def valider_equipe(ids: list[int]) -> list[dict]:
    """Vérifie que l'équipe respecte les règles. Le serveur ne fait jamais confiance au navigateur !"""
    if len(set(ids)) != len(ids):
        raise HTTPException(400, "Un joueur ne peut pas être recruté deux fois.")
    if any(i not in JOUEURS_PAR_ID for i in ids):
        raise HTTPException(400, "Joueur inconnu.")
    joueurs = [JOUEURS_PAR_ID[i] for i in ids]
    if len(joueurs) != TAILLE_EQUIPE:
        raise HTTPException(400, f"Il faut exactement {TAILLE_EQUIPE} joueurs.")
    if sum(j["poste"] == "G" for j in joueurs) != 1:
        raise HTTPException(400, "Il faut exactement 1 gardien.")
    if cout_equipe(joueurs) > BUDGET:
        raise HTTPException(400, f"Budget dépassé : {cout_equipe(joueurs)} M€ sur {BUDGET} M€.")
    return joueurs


class DemandeEntraineur(BaseModel):
    """Ce que le navigateur envoie à l'entraîneur adverse.

    Il n'y a PAS la tactique du joueur pour ce match : l'entraîneur ne la connaît pas.
    (extra="forbid" : si on essaie de la lui envoyer quand même, le serveur refuse.)
    """

    model_config = ConfigDict(extra="forbid")
    equipe: list[int]
    historique_tactiques: list[Tactique] = Field(default_factory=list, max_length=100)
    niveau: int = Field(default=2, ge=1, le=3)
    minute_debut: int = Field(default=1, ge=1, le=90)
    score: tuple[int, int] = (0, 0)


class DemandeMatch(BaseModel):
    """Ce que le navigateur envoie pour jouer (une partie d') un match."""

    equipe: list[int]
    tactique: Tactique
    niveau: int = Field(default=2, ge=1, le=3)
    tactique_ia: Tactique
    minute_debut: int = Field(default=1, ge=1, le=90)
    minute_fin: int = Field(default=90, ge=1, le=90)
    score: tuple[int, int] = (0, 0)


@routeur.get("/statut")
def statut():
    return {"jeu": "coach", "message": "Le jeu Coach est prêt ⚽"}


@routeur.get("/joueurs")
def joueurs():
    """Le catalogue des joueurs à recruter et les règles du mercato."""
    return {"budget": BUDGET, "taille_equipe": TAILLE_EQUIPE, "postes": POSTES, "joueurs": JOUEURS}


@routeur.get("/tactiques")
def tactiques():
    return [{"id": t, "nom": v["nom"], "emoji": v["emoji"], "description": v["description"]}
            for t, v in TACTIQUES.items()]


@routeur.get("/adversaires")
def adversaires():
    """L'équipe de l'ordinateur pour chaque niveau."""
    return {n: {"niveau": n, "niveau_nom": NIVEAUX[n]["nom"], **equipe} for n, equipe in EQUIPES_IA.items()}


@routeur.post("/entraineur")
def entraineur(demande: DemandeEntraineur):
    """L'entraîneur adverse choisit sa tactique en simulant des matchs."""
    equipe_joueur = valider_equipe(demande.equipe)
    return choisir_tactique(equipe_joueur, EQUIPES_IA[demande.niveau]["joueurs"], demande.historique_tactiques,
                            demande.niveau, demande.minute_debut, demande.score)


@routeur.post("/match")
def match(demande: DemandeMatch):
    """Simule le match (ou une mi-temps) entre l'équipe du joueur et celle de l'ordinateur."""
    if demande.minute_fin < demande.minute_debut:
        raise HTTPException(400, "La minute de fin doit être après la minute de début.")
    equipe_joueur = valider_equipe(demande.equipe)
    resultat = simuler(equipe_joueur, demande.tactique, EQUIPES_IA[demande.niveau]["joueurs"], demande.tactique_ia,
                       minute_debut=demande.minute_debut, minute_fin=demande.minute_fin,
                       score=demande.score, rng=random.Random())
    # Dans la réponse, on parle de "joueur" et "ia" plutôt que de "a" et "b"
    noms = {"a": "joueur", "b": "ia", None: None}
    for evenement in resultat["evenements"]:
        evenement["equipe"] = noms[evenement["equipe"]]
    resultat["possession"] = [noms[c] for c in resultat["possession"]]
    return resultat
