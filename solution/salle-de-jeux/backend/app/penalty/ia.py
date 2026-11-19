"""Le « cerveau » de Penalty Pro : un gardien (et un tireur) qui APPREND tes habitudes.

Comment ça marche, à expliquer aux élèves :
- On découpe le but en 6 zones (3 colonnes × 2 lignes).
- L'IA retient où tu as visé (ou plongé) lors des tirs PRÉCÉDENTS.
- Elle en déduit la PROBABILITÉ de chaque zone pour le prochain tir, puis :
    * comme gardien, elle plonge dans la zone la plus probable, à l'endroit précis où tu vises d'habitude ;
    * comme tireur, elle vise là où tu plonges le moins, sans prendre trop de risques.

Les niveaux :
- Facile    : l'IA ne retient rien, elle choisit au hasard.
- Moyen     : l'IA compte dans quelles zones tu vas le plus souvent (les fréquences).
- Difficile : l'IA repère aussi tes enchaînements (« après un tir à gauche, il tire à droite »).
"""
import random
from collections import Counter

from app.penalty.physique import arbitrer, trajectoire

ZONES = ["haut-gauche", "haut-centre", "haut-droite", "bas-gauche", "bas-centre", "bas-droite"]
NOMS = {
    "haut-gauche": "en haut à gauche", "haut-centre": "en haut au centre", "haut-droite": "en haut à droite",
    "bas-gauche": "en bas à gauche", "bas-centre": "en bas au centre", "bas-droite": "en bas à droite",
}
NIVEAUX = {1: {"nom": "Facile"}, 2: {"nom": "Moyen"}, 3: {"nom": "Difficile"}}


def zone_de(point: tuple[float, float]) -> str:
    """Dans quelle zone se trouve ce point du but ?"""
    colonne = ["gauche", "centre", "droite"][min(2, max(0, int(point[0] * 3)))]
    ligne = "haut" if point[1] < 0.5 else "bas"
    return f"{ligne}-{colonne}"


def centre_de(zone: str) -> tuple[float, float]:
    colonne = ["gauche", "centre", "droite"].index(zone.split("-")[1])
    return ((2 * colonne + 1) / 6, 0.25 if zone.startswith("haut") else 0.75)


def predire(historique: list[tuple[float, float]], niveau: int) -> tuple[dict[str, float], str]:
    """Probabilité de chaque zone pour le prochain choix du joueur, et une phrase d'explication."""
    if niveau == 1:
        return {z: 1 / 6 for z in ZONES}, "Niveau facile : je ne retiens rien, je choisis au hasard."
    if not historique:
        return {z: 1 / 6 for z in ZONES}, "Je ne te connais pas encore : toutes les zones se valent."

    zones = [zone_de(p) for p in historique]
    # 1. On compte. On part de 1 (et pas de 0) : aucune zone n'est jamais impossible.
    compte = Counter(zones)
    poids = {z: 1 + compte[z] for z in ZONES}
    preferee, nombre = compte.most_common(1)[0]
    explication = f"Tu as choisi {NOMS[preferee]} {nombre} fois sur {len(zones)}."

    # 2. Niveau difficile : que fait-il d'habitude APRÈS ce qu'il vient de faire ?
    if niveau >= 3 and len(zones) >= 2:
        dernier = zones[-1]
        suites = Counter(zones[i + 1] for i in range(len(zones) - 1) if zones[i] == dernier)
        if suites:
            for z in ZONES:
                poids[z] += 3 * suites[z]  # les enchaînements comptent 3 fois plus
            suivante, fois = suites.most_common(1)[0]
            explication = f"Après {NOMS[dernier]}, tu as choisi {NOMS[suivante]} {fois} fois sur {sum(suites.values())}."

    total = sum(poids.values())
    return {z: poids[z] / total for z in ZONES}, explication


def meilleure_zone(scores: dict[str, float], rng: random.Random, marge: float) -> str:
    """Une zone parmi celles qui ont presque le meilleur score (un peu de hasard rend l'IA moins prévisible)."""
    meilleur = max(scores.values())
    return rng.choice([z for z, s in scores.items() if s >= meilleur * marge])


def choisir_plongeon(historique_tirs: list[tuple[float, float]], niveau: int, rng: random.Random) -> dict:
    """Le gardien choisit où plonger. Il ne connaît QUE les tirs précédents : il ne peut pas tricher."""
    prediction, explication = predire(historique_tirs, niveau)
    if niveau == 1:
        zone = rng.choice(ZONES)
        point = centre_de(zone)
    else:
        zone = meilleure_zone(prediction, rng, marge=0.95)
        # Il plonge vers l'endroit PRÉCIS où tu vises d'habitude dans cette zone
        dans_la_zone = [p for p in historique_tirs if zone_de(p) == zone]
        if dans_la_zone:
            point = (sum(p[0] for p in dans_la_zone) / len(dans_la_zone), sum(p[1] for p in dans_la_zone) / len(dans_la_zone))
        else:
            point = centre_de(zone)
    return {"plongeon": {"x": round(point[0], 3), "y": round(point[1], 3)}, "zone": zone,
            "prediction": prediction, "explication": explication}


# Pour chaque zone, l'endroit où l'IA vise : près des poteaux, sans être trop près de la barre
CIBLES_IA = {
    "haut-gauche": (0.1, 0.18), "haut-centre": (0.5, 0.15), "haut-droite": (0.9, 0.18),
    "bas-gauche": (0.1, 0.8), "bas-centre": (0.5, 0.8), "bas-droite": (0.9, 0.8),
}
PUISSANCE_IA = {1: 0.55, 2: 0.75, 3: 0.8}


def choisir_tir(historique_plongeons: list[tuple[float, float]], niveau: int, rng: random.Random) -> dict:
    """Le tireur choisit où viser. Il ne connaît QUE les plongeons précédents du joueur."""
    prediction, explication = predire(historique_plongeons, niveau)
    explication = explication.replace("Tu as choisi", "Tu as plongé").replace("tu as choisi", "tu as plongé")
    puissance = PUISSANCE_IA[niveau]
    if niveau == 1:
        zone = rng.choice(ZONES)
    else:
        # Pour chaque zone, on SIMULE 200 tirs : combien finiraient dans le cadre ? (les lucarnes sont risquées)
        cadres = {}
        for z in ZONES:
            essais = [trajectoire(CIBLES_IA[z], puissance, rng) for _ in range(200)]
            cadres[z] = sum(arbitrer(e, (-9, -9), puissance) == "but" for e in essais) / 200
        # Chance de marquer ≈ (le gardien ne plonge pas là) × (le tir est cadré)
        chances = {z: (1 - prediction[z]) * cadres[z] for z in ZONES}
        zone = meilleure_zone(chances, rng, marge=0.9)
    cible = CIBLES_IA[zone]
    return {"cible": {"x": cible[0], "y": cible[1]}, "puissance": puissance, "zone": zone,
            "prediction": prediction, "explication": explication}
