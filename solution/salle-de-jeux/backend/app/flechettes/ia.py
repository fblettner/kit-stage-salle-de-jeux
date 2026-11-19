"""Le « cerveau » du joueur de fléchettes : où viser quand on n'est pas parfaitement précis ?

L'idée, à expliquer aux élèves :
- Une fléchette n'arrive jamais exactement où on vise : elle s'écarte un peu, au hasard.
  Chaque joueur a son « écart » (en mm) : petit pour un champion, grand pour un débutant.
- Viser le triple 20 rapporte 60… si on le touche ! Mais juste à côté, il y a le 1 et le 5.
  Un joueur imprécis a parfois intérêt à viser ailleurs.
- Alors l'IA SIMULE : pour des centaines d'endroits de la cible, elle imagine des dizaines de lancers avec
  son propre écart, et calcule combien il lui resterait en moyenne.
  Plus elle est imprécise, plus elle simule de lancers (sinon la moyenne serait trompeuse). Elle vise l'endroit le meilleur.
  (C'est encore la méthode de Monte-Carlo, comme dans Coach !)
- Le conseiller utilise le même calcul, mais avec TA précision, qu'il MESURE en regardant
  l'écart entre l'endroit où tu visais et celui où ta fléchette s'est plantée.
"""
import math
import random

from app.flechettes.cible import RAYON_CIBLE, appliquer, score

NIVEAUX = {
    1: {"nom": "Facile", "ecart": 38.0},
    2: {"nom": "Moyen", "ecart": 22.0},
    3: {"nom": "Difficile", "ecart": 11.0},
}
BONUS_VICTOIRE = 40  # finir la partie vaut plus que de simplement marquer des points

# Les endroits que l'IA envisage de viser : des cercles autour du centre, tous les 9° (centres et bords des secteurs)
RAYONS = [0, 11, 40, 70, 103, 135, 166]
CANDIDATS = [(0.0, 0.0)] + [
    (round(r * math.sin(math.radians(a)), 2), round(r * math.cos(math.radians(a)), 2))
    for r in RAYONS[1:] for a in range(0, 360, 9)
]
T20 = (0.0, 103.0)


def valeur_moyenne(visee, restant, double_sortie, ecarts) -> float:
    """Le score qu'il resterait EN MOYENNE après un lancer vers « visee » (plus c'est bas, mieux c'est)."""
    total = 0.0
    for dx, dy in ecarts:
        resultat, nouveau = appliquer(restant, score(visee[0] + dx, visee[1] + dy), double_sortie)
        total += nouveau - (BONUS_VICTOIRE if resultat == "gagne" else 0)
    return total / len(ecarts)


def tirages(ecart: float, n: int, rng: random.Random) -> list[tuple[float, float]]:
    """n écarts au hasard pour un joueur qui a cette précision."""
    return [(rng.gauss(0, ecart), rng.gauss(0, ecart)) for _ in range(n)]


def choisir_visee(restant: int, double_sortie: bool, ecart: float, rng: random.Random) -> dict:
    """Essaie tous les endroits candidats et garde celui où il restera le moins de points en moyenne."""
    # Plus le joueur est imprécis, plus il faut simuler de lancers pour que la moyenne soit fiable
    n = int(40 + 3 * ecart)
    ecarts = tirages(ecart, n, rng)  # les MÊMES lancers pour tous les candidats : la comparaison est juste
    resultats = [(valeur_moyenne(c, restant, double_sortie, ecarts), c) for c in CANDIDATS]
    meilleure_valeur, visee = min(resultats)
    return {
        "visee": {"x": visee[0], "y": visee[1]},
        "libelle": score(*visee)["libelle"],
        "gain_moyen": round(restant - meilleure_valeur, 1),
        "gain_t20": round(restant - valeur_moyenne(T20, restant, double_sortie, ecarts), 1),
        "candidats_testes": len(CANDIDATS),
        "lancers_simules": len(CANDIDATS) * n,
    }


def expliquer(choix: dict, restant: int, ecart: float) -> str:
    lancers = f"{choix['lancers_simules']:,}".replace(",", " ")  # 25546 → « 25 546 »
    texte = (f"Il me reste {restant}. J'ai simulé {lancers} lancers avec ma précision "
             f"(environ {round(ecart)} mm d'écart). Je vise {choix['libelle']} : je gagne en moyenne "
             f"{choix['gain_moyen']} points.")
    if choix["libelle"] != "T20" and choix["gain_t20"] < choix["gain_moyen"]:
        texte += f" Viser le triple 20 ne me rapporterait que {choix['gain_t20']} en moyenne."
    return texte


def jouer_volee(restant: int, double_sortie: bool, niveau: int, rng: random.Random) -> dict:
    """L'IA lance ses 3 fléchettes."""
    ecart = NIVEAUX[niveau]["ecart"]
    depart = restant
    flechettes, explication = [], ""
    for numero in range(3):
        choix = choisir_visee(restant, double_sortie, ecart, rng)
        if numero == 0:
            explication = expliquer(choix, restant, ecart)
        visee = (choix["visee"]["x"], choix["visee"]["y"])
        impact = (round(visee[0] + rng.gauss(0, ecart), 1), round(visee[1] + rng.gauss(0, ecart), 1))
        coup = score(*impact)
        resultat, restant = appliquer(restant, coup, double_sortie)
        flechettes.append({"visee": choix["visee"], "libelle_visee": choix["libelle"],
                           "impact": {"x": impact[0], "y": impact[1]}, **coup, "resultat": resultat})
        if resultat == "bust":
            restant = depart  # la volée ne compte pas
            break
        if resultat == "gagne":
            break
    return {"flechettes": flechettes, "restant": restant, "explication": explication}


def carte_de_chaleur(restant: int, double_sortie: bool, ecart: float, rng: random.Random,
                     pas: float = 17.0, n: int = 80) -> list[dict]:
    """Pour une grille de points de la cible : combien on gagne en moyenne en visant là ?"""
    ecarts = tirages(ecart, n, rng)
    carte = []
    k = int(RAYON_CIBLE // pas)
    for i in range(-k, k + 1):
        for j in range(-k, k + 1):
            x, y = i * pas, j * pas
            if math.hypot(x, y) <= RAYON_CIBLE:
                carte.append({"x": x, "y": y, "gain": round(restant - valeur_moyenne((x, y), restant, double_sortie, ecarts), 1)})
    return carte


def estimer_ecart(lancers: list[tuple[tuple[float, float], tuple[float, float]]]) -> float:
    """Mesure la précision d'un joueur : l'écart moyen entre où il visait et où la fléchette s'est plantée.

    Tant qu'on a peu de lancers, on part d'une précision « moyenne » de 25 mm.
    """
    a_priori, poids = 25.0, 3  # comme si on avait déjà vu 3 lancers à 25 mm
    carres = sum(((i[0] - v[0]) ** 2 + (i[1] - v[1]) ** 2) / 2 for v, i in lancers)
    return round(math.sqrt((carres + poids * a_priori ** 2) / (len(lancers) + poids)), 1)
