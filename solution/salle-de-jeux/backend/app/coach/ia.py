"""Le « cerveau » de l'entraîneur adverse : il SIMULE des centaines de matchs avant de décider.

Troisième façon de faire une IA, à expliquer aux élèves :
- Aux échecs, l'IA CALCULE tous les coups possibles (minimax).
- Ici, impossible : un match dépend du hasard ! Alors l'IA fait comme un météorologue :
  elle SIMULE le match des centaines de fois avec chaque tactique,
  compte combien de fois elle gagne, et choisit la tactique qui rapporte le plus de points.
  On appelle ça la méthode de Monte-Carlo (du nom du casino… car on tire beaucoup au sort !).

Problème : l'entraîneur ne connaît pas la tactique que le joueur va choisir.
Alors il APPREND de ses matchs précédents : « d'habitude, il joue offensif ».

Les niveaux :
- Facile    : équipe faible, tactique choisie au hasard, aucune simulation.
- Moyen     : équipe moyenne ; suppose que tu vas jouer ta tactique habituelle ; 100 matchs simulés par tactique.
- Difficile : bonne équipe ; tient compte de TOUTES tes habitudes ; 300 matchs simulés par tactique.
"""
import random
from collections import Counter

from app.coach.simulateur import TACTIQUES, simuler

NIVEAUX = {
    1: {"nom": "Facile", "simulations": 0},
    2: {"nom": "Moyen", "simulations": 100},
    3: {"nom": "Difficile", "simulations": 300},
}


def predire_tactique(historique: list[str]) -> dict[str, float]:
    """Probabilité que le joueur choisisse chaque tactique, d'après ses matchs précédents.

    On part de 1 pour chaque tactique : aucune n'est jamais impossible.
    """
    compte = Counter(historique)
    poids = {t: 1 + compte[t] for t in TACTIQUES}
    total = sum(poids.values())
    return {t: poids[t] / total for t in TACTIQUES}


def choisir_tactique(equipe_joueur: list[dict], equipe_ia: list[dict], historique: list[str],
                     niveau: int, minute_debut: int = 1, score=(0, 0), graine: int | None = None) -> dict:
    """Choisit la tactique de l'ordinateur pour la suite du match.

    Important : on ne reçoit PAS la tactique choisie par le joueur pour ce match,
    seulement celles de ses matchs précédents. L'entraîneur ne triche pas !
    """
    rng = random.Random(graine)
    nombre = NIVEAUX[niveau]["simulations"]

    if nombre == 0:
        tactique = rng.choice(list(TACTIQUES))
        return {
            "tactique": tactique,
            "rapport": [],
            "matchs_simules": 0,
            "explication": "Niveau facile : je choisis ma tactique au hasard, sans réfléchir.",
        }

    # 1. Que va probablement jouer le joueur ?
    prediction = predire_tactique(historique)
    if niveau == 2:
        # Niveau moyen : on suppose qu'il va jouer sa tactique la plus fréquente (équilibrée s'il n'a jamais joué)
        habituelle = max(prediction, key=prediction.get) if historique else "equilibree"
        prediction = {t: (1.0 if t == habituelle else 0.0) for t in TACTIQUES}

    # 2. Pour chacune de NOS tactiques, on simule la fin du match de nombreuses fois
    rapport = []
    for tactique_ia in TACTIQUES:
        victoires = nuls = defaites = 0
        for _ in range(nombre):
            # On tire au sort la tactique du joueur selon notre prédiction
            tactique_joueur = rng.choices(list(prediction), weights=list(prediction.values()))[0]
            resultat = simuler(equipe_joueur, tactique_joueur, equipe_ia, tactique_ia,
                               minute_debut=minute_debut, score=score, rng=rng, commentaires=False)
            buts_joueur, buts_ia = resultat["score"]
            if buts_ia > buts_joueur:
                victoires += 1
            elif buts_ia == buts_joueur:
                nuls += 1
            else:
                defaites += 1
        rapport.append({
            "tactique": tactique_ia,
            "nom": TACTIQUES[tactique_ia]["nom"],
            "victoire": round(100 * victoires / nombre),
            "nul": round(100 * nuls / nombre),
            "defaite": round(100 * defaites / nombre),
            # Les points qu'on gagne en moyenne : 3 pour une victoire, 1 pour un nul
            "points": round((3 * victoires + nuls) / nombre, 2),
        })

    # 3. On garde la tactique qui rapporte le plus de points en moyenne
    rapport.sort(key=lambda ligne: ligne["points"], reverse=True)
    meilleure = rapport[0]

    # 4. On explique notre raisonnement
    habitude = max(predire_tactique(historique).items(), key=lambda x: x[1])[0] if historique else None
    if habitude:
        nb = Counter(historique)[habitude]
        debut = f"Tu as joué « {TACTIQUES[habitude]['nom']} » {nb} fois sur {len(historique)}. "
    else:
        debut = "Je ne connais pas encore tes habitudes. "
    explication = (
        f"{debut}J'ai simulé {nombre * len(TACTIQUES)} matchs. "
        f"Ma meilleure réponse : « {meilleure['nom']} », qui gagne {meilleure['victoire']} % du temps."
    )
    return {
        "tactique": meilleure["tactique"],
        "rapport": rapport,
        "matchs_simules": nombre * len(TACTIQUES),
        "explication": explication,
    }
