"""Le moteur de match : il simule un match minute par minute, avec des probabilités.

À chaque minute :
1. On tire au sort quelle équipe a le ballon. L'équipe la plus technique l'a plus souvent.
2. L'équipe qui a le ballon peut se créer une occasion. Plus son attaque est forte
   par rapport à la défense adverse, plus c'est probable.
3. Sur une occasion, un joueur tire. Il marque plus souvent s'il est bon en attaque
   et si le gardien adverse est moins bon.
4. L'équipe qui n'a PAS le ballon peut lancer une contre-attaque (si elle joue « contre-attaque »).

Comme tout repose sur le hasard, deux matchs ne se ressemblent jamais… mais la meilleure
équipe gagne plus souvent. Exactement comme dans la réalité !
"""
import random

# Chaque tactique modifie les forces de l'équipe (en points sur 100)
TACTIQUES = {
    "defensive": {
        "nom": "Défensive", "emoji": "🧱",
        "description": "Tout le monde défend. On encaisse peu… mais on marque peu.",
        "attaque": -10, "defense": 14, "possession": -6,
    },
    "equilibree": {
        "nom": "Équilibrée", "emoji": "⚖️",
        "description": "Ni trop, ni trop peu.",
        "attaque": 0, "defense": 0, "possession": 0,
    },
    "offensive": {
        "nom": "Offensive", "emoji": "🔥",
        "description": "Tout le monde attaque ! Attention aux contres.",
        "attaque": 12, "defense": -12, "possession": 4,
    },
    "pressing": {
        "nom": "Pressing", "emoji": "🏃",
        "description": "On récupère le ballon très haut. Fatigant : moins efficace après la 60e minute.",
        "attaque": 6, "defense": 4, "possession": 12,
    },
    "contre": {
        "nom": "Contre-attaque", "emoji": "⚡",
        "description": "On laisse le ballon à l'adversaire, puis on file au but avec nos joueurs rapides.",
        "attaque": -4, "defense": 6, "possession": -12,
    },
}

FATIGUE_PRESSING = 14  # perte de force après la 60e minute pour le pressing


def borner(valeur: float, mini: float, maxi: float) -> float:
    return max(mini, min(maxi, valeur))


def forces_equipe(joueurs: list[dict]) -> dict:
    """Résume une équipe en 5 notes : attaque, défense, technique, vitesse et gardien."""
    gardien = next(j for j in joueurs if j["poste"] == "G")
    champ = [j for j in joueurs if j["poste"] != "G"]

    def moyenne(carac):
        return sum(j[carac] for j in champ) / len(champ)

    return {
        "attaque": moyenne("attaque"),
        "defense": moyenne("defense"),
        "technique": moyenne("technique"),
        "vitesse": moyenne("vitesse"),
        "gardien": gardien["defense"],
    }


def _tactique_a_la_minute(nom: str, minute: int) -> dict:
    t = dict(TACTIQUES[nom])
    if nom == "pressing" and minute > 60:
        for carac in ("attaque", "defense", "possession"):
            t[carac] -= FATIGUE_PRESSING
    return t


def _choisir_tireur(joueurs, carac, rng):
    """Les meilleurs dans la caractéristique tirent plus souvent."""
    champ = [j for j in joueurs if j["poste"] != "G"]
    return rng.choices(champ, weights=[j[carac] ** 2 for j in champ])[0]


def simuler(equipe_a: list[dict], tactique_a: str, equipe_b: list[dict], tactique_b: str,
            minute_debut: int = 1, minute_fin: int = 90, score=(0, 0),
            rng: random.Random | None = None, commentaires: bool = True) -> dict:
    """Simule le match de minute_debut à minute_fin. L'équipe A est celle du joueur."""
    rng = rng or random.Random()
    forces = {"a": forces_equipe(equipe_a), "b": forces_equipe(equipe_b)}
    joueurs = {"a": equipe_a, "b": equipe_b}
    tactiques = {"a": tactique_a, "b": tactique_b}
    gardiens = {cote: next(j for j in joueurs[cote] if j["poste"] == "G") for cote in "ab"}
    buts = {"a": score[0], "b": score[1]}
    tirs = {"a": 0, "b": 0}
    cadres = {"a": 0, "b": 0}
    minutes_possession = {"a": 0, "b": 0}
    evenements = []
    possession = []  # qui a le ballon à chaque minute (pour la barre de domination)

    def noter(minute, cote, type_, texte):
        if commentaires:
            evenements.append({"minute": minute, "equipe": cote, "type": type_, "texte": texte})

    def tir(minute, cote, tireur, bonus=0.0):
        adverse = "b" if cote == "a" else "a"
        tirs[cote] += 1
        chance = borner(0.28 + (tireur["attaque"] - forces[adverse]["gardien"]) / 200 + bonus, 0.08, 0.6)
        if rng.random() < chance:
            buts[cote] += 1
            cadres[cote] += 1
            noter(minute, cote, "but", f"⚽ BUUUT de {tireur['nom']} ! ({buts['a']}-{buts['b']})")
            return
        issue = rng.random()
        if issue < 0.55:
            cadres[cote] += 1
            noter(minute, cote, "arret", f"🧤 Parade de {gardiens[adverse]['nom']} devant {tireur['nom']} !")
        elif issue < 0.85:
            noter(minute, cote, "rate", f"{tireur['nom']} frappe… à côté !")
        else:
            noter(minute, cote, "poteau", f"💥 {tireur['nom']} trouve le poteau !")

    if minute_debut == 1:
        noter(0, None, "info", "Coup d'envoi !")

    for minute in range(minute_debut, minute_fin + 1):
        t = {cote: _tactique_a_la_minute(tactiques[cote], minute) for cote in "ab"}

        # 1. Qui a le ballon ?
        avantage = (forces["a"]["technique"] + t["a"]["possession"]) - (forces["b"]["technique"] + t["b"]["possession"])
        cote = "a" if rng.random() < borner(0.5 + avantage / 150, 0.2, 0.8) else "b"
        adverse = "b" if cote == "a" else "a"
        minutes_possession[cote] += 1
        possession.append(cote)

        # 2. L'équipe qui a le ballon se crée-t-elle une occasion ?
        ecart = (forces[cote]["attaque"] + t[cote]["attaque"]) - (forces[adverse]["defense"] + t[adverse]["defense"])
        if rng.random() < borner(0.075 + ecart / 350, 0.015, 0.2):
            tir(minute, cote, _choisir_tireur(joueurs[cote], "attaque", rng))

        # 3. Contre-attaque de l'équipe qui n'a pas le ballon ?
        if tactiques[adverse] == "contre":
            espace = 0.02 if tactiques[cote] in ("offensive", "pressing") else 0.0
            vitesse = forces[adverse]["vitesse"] - forces[cote]["defense"] - t[cote]["defense"]
            if rng.random() < borner(0.012 + espace + vitesse / 1200, 0.004, 0.06):
                rapide = _choisir_tireur(joueurs[adverse], "vitesse", rng)
                noter(minute, adverse, "contre", f"⚡ Contre-attaque éclair de {rapide['nom']}…")
                tir(minute, adverse, rapide, bonus=0.06)

        if minute == 45:
            noter(45, None, "info", f"Mi-temps : {buts['a']}-{buts['b']}")
    if minute_fin == 90:
        noter(90, None, "info", f"Coup de sifflet final : {buts['a']}-{buts['b']}")

    return {
        "score": [buts["a"], buts["b"]],
        "evenements": evenements,
        "possession": possession,
        "stats": {
            "possession": [minutes_possession["a"], minutes_possession["b"]],
            "tirs": [tirs["a"], tirs["b"]],
            "cadres": [cadres["a"], cadres["b"]],
        },
    }
