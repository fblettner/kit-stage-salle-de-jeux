"""Les données du jeu Coach : les joueurs à recruter et les équipes de l'ordinateur.

Tous les joueurs et toutes les équipes sont INVENTÉS.

Chaque joueur a 4 caractéristiques, notées sur 100 :
- attaque   : qualité de tir
- defense   : qualité pour défendre (pour un gardien : les arrêts)
- technique : contrôle, passes → aide à garder le ballon
- vitesse   : utile surtout pour les contre-attaques

On joue au foot à 5 : 1 gardien + 4 joueurs de champ, avec un budget limité.
"""

BUDGET = 50  # en millions d'euros (fictifs !)
TAILLE_EQUIPE = 5

POSTES = {"G": "Gardien", "DEF": "Défenseur", "MIL": "Milieu", "ATT": "Attaquant"}

# Pour calculer la note globale, chaque caractéristique compte plus ou moins selon le poste
POIDS_PAR_POSTE = {
    "G": {"attaque": 0.0, "defense": 0.8, "technique": 0.2, "vitesse": 0.0},
    "DEF": {"attaque": 0.1, "defense": 0.5, "technique": 0.2, "vitesse": 0.2},
    "MIL": {"attaque": 0.2, "defense": 0.2, "technique": 0.4, "vitesse": 0.2},
    "ATT": {"attaque": 0.5, "defense": 0.0, "technique": 0.25, "vitesse": 0.25},
}


def note_globale(joueur: dict) -> int:
    poids = POIDS_PAR_POSTE[joueur["poste"]]
    return round(sum(joueur[carac] * p for carac, p in poids.items()))


def prix(joueur: dict) -> int:
    """Le prix dépend de la note : un très bon joueur coûte très cher."""
    return max(3, round((note_globale(joueur) - 55) * 0.8))


def _joueur(id, nom, poste, attaque, defense, technique, vitesse):
    j = {"id": id, "nom": nom, "poste": poste, "attaque": attaque, "defense": defense,
         "technique": technique, "vitesse": vitesse}
    j["note"] = note_globale(j)
    j["prix"] = prix(j)
    return j


# Les joueurs qu'on peut recruter
JOUEURS = [
    # Gardiens
    _joueur(1, "Hugo Lefort", "G", 10, 88, 62, 40),
    _joueur(2, "Samir Haddad", "G", 10, 80, 72, 45),
    _joueur(3, "Kevin Mbaye", "G", 10, 72, 52, 50),
    _joueur(4, "Léo Martin", "G", 10, 64, 56, 45),
    # Défenseurs
    _joueur(5, "Malik Traoré", "DEF", 38, 88, 62, 76),
    _joueur(6, "Théo Garnier", "DEF", 30, 84, 56, 58),
    _joueur(7, "Ibrahim Koné", "DEF", 42, 76, 58, 84),
    _joueur(8, "Lucas Petit", "DEF", 45, 70, 66, 64),
    _joueur(9, "Enzo Rossi", "DEF", 35, 66, 50, 70),
    _joueur(10, "Nathan Roux", "DEF", 50, 60, 60, 55),
    # Milieux
    _joueur(11, "Adam Chérif", "MIL", 72, 60, 92, 68),
    _joueur(12, "Jules Moreau", "MIL", 64, 72, 82, 60),
    _joueur(13, "Mamadou Diallo", "MIL", 60, 78, 74, 74),
    _joueur(14, "Rayan Belkacem", "MIL", 70, 55, 70, 86),
    _joueur(15, "Tom Girard", "MIL", 55, 60, 64, 58),
    # Attaquants
    _joueur(16, "Noah Fontaine", "ATT", 92, 25, 80, 86),
    _joueur(17, "Ilyes Mansour", "ATT", 86, 30, 84, 70),
    _joueur(18, "Gabriel Silva", "ATT", 80, 20, 66, 92),
    _joueur(19, "Moussa Camara", "ATT", 76, 40, 60, 70),
    _joueur(20, "Arthur Blanc", "ATT", 68, 35, 58, 62),
    _joueur(21, "Sacha Dumas", "ATT", 62, 30, 55, 80),
]

JOUEURS_PAR_ID = {j["id"]: j for j in JOUEURS}

# Les équipes de l'ordinateur, une par niveau (leurs joueurs ne sont pas à vendre)
EQUIPES_IA = {
    1: {
        "nom": "FC Bugs 🐛",
        "joueurs": [
            _joueur(101, "Bug", "G", 10, 60, 50, 40),
            _joueur(102, "Glitch", "DEF", 35, 62, 50, 55),
            _joueur(103, "Lag", "MIL", 52, 55, 58, 50),
            _joueur(104, "Crash", "ATT", 64, 25, 52, 60),
            _joueur(105, "Patch", "ATT", 60, 30, 50, 66),
        ],
    },
    2: {
        "nom": "Racing Pixel 👾",
        "joueurs": [
            _joueur(201, "Pixel", "G", 10, 70, 58, 45),
            _joueur(202, "Octet", "DEF", 38, 70, 56, 64),
            _joueur(203, "Kilo", "MIL", 58, 62, 70, 64),
            _joueur(204, "Méga", "ATT", 74, 30, 62, 72),
            _joueur(205, "Giga", "ATT", 66, 32, 58, 80),
        ],
    },
    3: {
        "nom": "FC Python 🐍",
        "joueurs": [
            _joueur(301, "Algo", "G", 10, 74, 60, 45),
            _joueur(302, "Boucle", "DEF", 40, 78, 58, 70),
            _joueur(303, "Fonction", "MIL", 60, 62, 76, 64),
            _joueur(304, "Variable", "MIL", 66, 58, 70, 80),
            _joueur(305, "Récursif", "ATT", 78, 28, 68, 76),
        ],
    },
}


def cout_equipe(joueurs: list[dict]) -> int:
    return sum(j["prix"] for j in joueurs)
