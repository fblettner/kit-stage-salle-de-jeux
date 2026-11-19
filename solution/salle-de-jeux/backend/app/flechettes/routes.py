"""Les routes de l'API des fléchettes. Toutes commencent par /api/flechettes.

Le SERVEUR est l'arbitre : c'est lui qui compte les points et applique les règles du 301.
"""
import random

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.flechettes.cible import DOUBLE, RAYON_BULL, RAYON_BULL_25, SECTEURS, TRIPLE, appliquer, score
from app.flechettes.ia import NIVEAUX, carte_de_chaleur, choisir_visee, estimer_ecart, jouer_volee

routeur = APIRouter(prefix="/api/flechettes", tags=["Fléchettes"])


class Point(BaseModel):
    """Un point de la cible, en mm depuis le centre (y vers le haut)."""

    x: float = Field(ge=-250, le=250)
    y: float = Field(ge=-250, le=250)


class DemandeLancer(BaseModel):
    impact: Point
    restant: int = Field(ge=2, le=1001)
    double_sortie: bool = False


class DemandeVolee(BaseModel):
    restant: int = Field(ge=2, le=1001)
    double_sortie: bool = False
    niveau: int = Field(default=2, ge=1, le=3)


@routeur.get("/statut")
def statut():
    return {"jeu": "flechettes", "message": "Les fléchettes sont prêtes 🎯"}


@routeur.get("/niveaux")
def niveaux():
    return [{"niveau": n, "nom": r["nom"], "ecart": r["ecart"]} for n, r in NIVEAUX.items()]


@routeur.get("/cible")
def cible():
    """Les dimensions officielles de la cible, pour la dessiner."""
    return {"bull": RAYON_BULL, "bull_25": RAYON_BULL_25, "triple": TRIPLE, "double": DOUBLE, "secteurs": SECTEURS}


@routeur.post("/lancer")
def lancer(demande: DemandeLancer):
    """Une fléchette du joueur : combien elle rapporte, et ce que ça donne avec les règles du 301."""
    coup = score(demande.impact.x, demande.impact.y)
    resultat, restant = appliquer(demande.restant, coup, demande.double_sortie)
    return {**coup, "resultat": resultat, "restant": restant}


@routeur.post("/ia/volee")
def volee_ia(demande: DemandeVolee):
    """L'IA joue ses 3 fléchettes. On renvoie aussi sa « carte de chaleur » : où il vaut mieux viser pour elle."""
    rng = random.Random()
    volee = jouer_volee(demande.restant, demande.double_sortie, demande.niveau, rng)
    volee["carte"] = carte_de_chaleur(demande.restant, demande.double_sortie, NIVEAUX[demande.niveau]["ecart"], rng)
    return volee


class Lancer(BaseModel):
    """Un lancer du joueur : où il visait, et où la fléchette s'est plantée."""

    visee: Point
    impact: Point


class DemandeConseil(BaseModel):
    restant: int = Field(ge=2, le=1001)
    double_sortie: bool = False
    lancers: list[Lancer] = Field(default_factory=list, max_length=300)


@routeur.post("/conseil")
def conseil(demande: DemandeConseil):
    """Le conseiller : il mesure TA précision, puis cherche où TU as intérêt à viser."""
    rng = random.Random()
    ecart = estimer_ecart([((l.visee.x, l.visee.y), (l.impact.x, l.impact.y)) for l in demande.lancers])
    choix = choisir_visee(demande.restant, demande.double_sortie, ecart, rng)
    if len(demande.lancers) < 3:
        precision = "Je ne connais pas encore bien ta précision : je suppose environ 25 mm d'écart."
    else:
        precision = f"D'après tes {len(demande.lancers)} lancers, ta fléchette s'écarte d'environ {round(ecart)} mm de là où tu vises."
    explication = f"{precision} Avec {demande.restant} à faire, vise {choix['libelle']} : tu gagneras en moyenne {choix['gain_moyen']} points."
    return {**choix, "ecart_estime": ecart, "explication": explication,
            "carte": carte_de_chaleur(demande.restant, demande.double_sortie, ecart, rng)}
