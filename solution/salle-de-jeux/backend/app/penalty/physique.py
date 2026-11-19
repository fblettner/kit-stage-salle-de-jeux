"""La « physique » et l'arbitre de Penalty Pro.

Le but est vu de face. Une position dans le but est un point (x, y) :
    x va de 0 (poteau gauche) à 1 (poteau droit)
    y va de 0 (la barre transversale) à 1 (le sol)

Les règles, à expliquer aux élèves :
- Plus on frappe FORT, moins on est PRÉCIS, et une frappe très forte a tendance à monter.
- Plus on frappe FORT, moins le gardien a le temps d'aller loin : sa « portée » diminue.
Il faut donc choisir entre puissance et précision… comme un vrai tireur !
"""
import math
import random

# Un vrai but mesure 7,32 m de large pour 2,44 m de haut : 3 fois plus large que haut.
LARGEUR, HAUTEUR = 3.0, 1.0
MARGE_CADRE = 0.03  # un ballon qui sort de très peu touche le poteau ou la barre


def trajectoire(cible: tuple[float, float], puissance: float, rng: random.Random) -> tuple[float, float]:
    """Où arrive vraiment le ballon : la cible, plus une erreur qui grandit avec la puissance."""
    ecart = 0.015 + 0.06 * puissance ** 2
    x = cible[0] + rng.gauss(0, ecart)
    y = cible[1] + rng.gauss(0, ecart * 1.5)
    if puissance > 0.8:
        y -= (puissance - 0.8) * 0.7  # une frappe trop puissante monte
    return round(x, 3), round(min(y, 0.97), 3)  # le ballon ne passe pas sous le sol !


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Distance entre deux points du but (en tenant compte du fait que le but est 3 fois plus large que haut)."""
    return math.hypot((a[0] - b[0]) * LARGEUR, (a[1] - b[1]) * HAUTEUR)


def portee_gardien(puissance: float) -> float:
    """Jusqu'où le gardien peut aller chercher le ballon depuis l'endroit où il plonge."""
    return 0.22 + 0.33 * (1 - puissance)


def arbitrer(impact: tuple[float, float], plongeon: tuple[float, float], puissance: float) -> str:
    """Renvoie 'dehors', 'poteau', 'arret' ou 'but'."""
    x, y = impact
    if x < -MARGE_CADRE or x > 1 + MARGE_CADRE or y < -MARGE_CADRE:
        return "dehors"
    if x < 0 or x > 1 or y < 0:
        return "poteau"
    if distance(impact, plongeon) <= portee_gardien(puissance):
        return "arret"
    return "but"
