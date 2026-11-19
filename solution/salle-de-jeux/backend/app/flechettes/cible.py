"""La cible de fléchettes et les règles du jeu « 301 ».

Une position sur la cible est un point (x, y) en millimètres, depuis le centre :
    x vers la droite, y vers le HAUT (comme en maths).

Les dimensions sont celles d'une vraie cible de compétition.
"""
import math

RAYON_BULL = 6.35  # le centre (« bull ») : 50 points
RAYON_BULL_25 = 15.9  # l'anneau autour du centre : 25 points
TRIPLE = (99.0, 107.0)  # l'anneau des triples (entre ces deux rayons)
DOUBLE = (162.0, 170.0)  # l'anneau des doubles, au bord de la zone qui rapporte des points
RAYON_CIBLE = DOUBLE[1]

# Les 20 secteurs, dans le sens des aiguilles d'une montre, en partant du haut
SECTEURS = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]


def score(x: float, y: float) -> dict:
    """Combien rapporte une fléchette plantée en (x, y) ?"""
    r = math.hypot(x, y)
    if r <= RAYON_BULL:
        return {"points": 50, "double": True, "libelle": "Bull 50"}
    if r <= RAYON_BULL_25:
        return {"points": 25, "double": False, "libelle": "Bull 25"}
    if r > RAYON_CIBLE:
        return {"points": 0, "double": False, "libelle": "Raté"}

    # Dans quel secteur ? On mesure l'angle depuis le haut, dans le sens des aiguilles d'une montre.
    angle = math.degrees(math.atan2(x, y)) % 360
    secteur = SECTEURS[int(((angle + 9) % 360) // 18)]  # chaque secteur fait 18°, le 20 est centré en haut

    if TRIPLE[0] < r <= TRIPLE[1]:
        return {"points": 3 * secteur, "double": False, "libelle": f"T{secteur}"}
    if DOUBLE[0] < r <= DOUBLE[1]:
        return {"points": 2 * secteur, "double": True, "libelle": f"D{secteur}"}
    return {"points": secteur, "double": False, "libelle": str(secteur)}


def appliquer(restant: int, coup: dict, double_sortie: bool) -> tuple[str, int]:
    """Applique une fléchette au score restant. Renvoie (résultat, nouveau score restant).

    Règles du 301 : on part de 301 et il faut arriver EXACTEMENT à 0.
    - Si on descend sous 0, c'est « bust » : la volée ne compte pas.
    - Option « double pour finir » (comme les pros) : la dernière fléchette doit être un double,
      donc il ne faut jamais rester à 1.
    """
    nouveau = restant - coup["points"]
    if nouveau < 0:
        return "bust", restant
    if nouveau == 0:
        if double_sortie and not coup["double"]:
            return "bust", restant
        return "gagne", 0
    if double_sortie and nouveau == 1:
        return "bust", restant
    return "ok", nouveau
