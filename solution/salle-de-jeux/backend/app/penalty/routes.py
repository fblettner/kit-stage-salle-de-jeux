"""Les routes de l'API de Penalty Pro. Toutes commencent par /api/penalty.

Le SERVEUR est l'arbitre : c'est lui qui calcule où va le ballon et s'il y a but.
Le navigateur envoie seulement ce que le joueur a choisi.
"""
import random

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.penalty.ia import NIVEAUX, choisir_plongeon, choisir_tir, zone_de
from app.penalty.physique import arbitrer, trajectoire

routeur = APIRouter(prefix="/api/penalty", tags=["Penalty Pro"])


class Point(BaseModel):
    """Un point du but : x de 0 (poteau gauche) à 1 (poteau droit), y de 0 (barre) à 1 (sol)."""

    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)


class DemandeTir(BaseModel):
    """Le joueur tire : où il vise, avec quelle puissance, et ses tirs précédents."""

    cible: Point
    puissance: float = Field(ge=0, le=1)
    historique: list[Point] = Field(default_factory=list, max_length=200)
    niveau: int = Field(default=2, ge=1, le=3)


class DemandeArret(BaseModel):
    """Le joueur est gardien : où il plonge, et ses plongeons précédents."""

    plongeon: Point
    historique: list[Point] = Field(default_factory=list, max_length=200)
    niveau: int = Field(default=2, ge=1, le=3)


@routeur.get("/statut")
def statut():
    return {"jeu": "penalty", "message": "Penalty Pro est prêt ⚽"}


@routeur.get("/niveaux")
def niveaux():
    return [{"niveau": n, "nom": r["nom"]} for n, r in NIVEAUX.items()]


@routeur.post("/tir")
def tir(demande: DemandeTir):
    """Le joueur tire, le gardien IA plonge."""
    rng = random.Random()
    # 1. Le gardien décide AVANT de regarder le tir : on ne lui donne que l'historique.
    gardien = choisir_plongeon([(p.x, p.y) for p in demande.historique], demande.niveau, rng)
    plongeon = (gardien["plongeon"]["x"], gardien["plongeon"]["y"])
    # 2. Le ballon part (avec l'imprécision due à la puissance)
    impact = trajectoire((demande.cible.x, demande.cible.y), demande.puissance, rng)
    # 3. L'arbitre décide
    resultat = arbitrer(impact, plongeon, demande.puissance)
    return {
        "impact": {"x": impact[0], "y": impact[1]},
        "plongeon": gardien["plongeon"],
        "resultat": resultat,
        "zone_visee": zone_de((demande.cible.x, demande.cible.y)),
        "prediction": gardien["prediction"],
        "explication": gardien["explication"],
    }


@routeur.post("/arret")
def arret(demande: DemandeArret):
    """L'IA tire, le joueur plonge."""
    rng = random.Random()
    # 1. Le tireur décide AVANT de regarder le plongeon : on ne lui donne que l'historique.
    tireur = choisir_tir([(p.x, p.y) for p in demande.historique], demande.niveau, rng)
    cible = (tireur["cible"]["x"], tireur["cible"]["y"])
    impact = trajectoire(cible, tireur["puissance"], rng)
    resultat = arbitrer(impact, (demande.plongeon.x, demande.plongeon.y), tireur["puissance"])
    return {
        "cible": tireur["cible"],
        "puissance": tireur["puissance"],
        "impact": {"x": impact[0], "y": impact[1]},
        "resultat": resultat,
        "prediction": tireur["prediction"],
        "explication": tireur["explication"],
    }
