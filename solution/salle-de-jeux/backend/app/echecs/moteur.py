"""Le « cerveau » de l'ordinateur : l'algorithme minimax.

Idée générale, à expliquer avec un arbre au tableau :
1. L'ordinateur imagine TOUS les coups qu'il peut jouer.
2. Pour chacun, il imagine toutes les réponses possibles de l'adversaire,
   puis ses propres réponses… jusqu'à une certaine « profondeur ».
3. Arrivé au bout, il donne une NOTE à la position (qui a le plus de pièces ? qui est mieux placé ?).
4. Il remonte l'arbre en supposant que chaque joueur choisit le meilleur coup pour lui :
   l'ordinateur MAXimise la note, l'adversaire la MINimise. D'où le nom : minimax.

Plus la profondeur est grande, plus l'ordinateur est fort… et plus il met de temps.
"""
import random

import chess

# Valeur de chaque pièce, en « points » (un pion = 100)
VALEUR_PIECES = {
    chess.PAWN: 100,    # pion
    chess.KNIGHT: 320,  # cavalier
    chess.BISHOP: 330,  # fou
    chess.ROOK: 500,    # tour
    chess.QUEEN: 900,   # dame
    chess.KING: 0,      # roi : on ne peut pas le perdre, il ne compte pas dans le matériel
}

# Les 4 cases du centre : y avoir des pièces est un avantage
CENTRE = {chess.D4, chess.E4, chess.D5, chess.E5}
# Les 12 cases autour du centre : petit bonus aussi
AUTOUR_DU_CENTRE = {
    chess.C3, chess.D3, chess.E3, chess.F3,
    chess.C4, chess.F4, chess.C5, chess.F5,
    chess.C6, chess.D6, chess.E6, chess.F6,
}

GAGNE = 100_000  # note d'un échec et mat (énorme, pour qu'il passe avant tout le reste)

# Les niveaux de difficulté : profondeur de recherche + part de hasard
NIVEAUX = {
    1: {"nom": "Facile", "profondeur": 1, "hasard": 0.3},
    2: {"nom": "Moyen", "profondeur": 2, "hasard": 0.0},
    3: {"nom": "Difficile", "profondeur": 3, "hasard": 0.0},
}


def evaluer(plateau: chess.Board) -> int:
    """Donne une note à la position, du point de vue des BLANCS.

    Note positive : les blancs sont mieux. Note négative : les noirs sont mieux.
    """
    if plateau.is_checkmate():
        # Le joueur qui doit jouer est mat : il a perdu
        return -GAGNE if plateau.turn == chess.WHITE else GAGNE
    if plateau.is_game_over():
        return 0  # pat, répétition, matériel insuffisant… : match nul

    note = 0
    for case, piece in plateau.piece_map().items():
        valeur = VALEUR_PIECES[piece.piece_type]
        if case in CENTRE:
            valeur += 20
        elif case in AUTOUR_DU_CENTRE:
            valeur += 10
        note += valeur if piece.color == chess.WHITE else -valeur
    return note


def trier_coups(plateau: chess.Board) -> list[chess.Move]:
    """Regarde d'abord les captures : ça accélère beaucoup la recherche."""
    return sorted(plateau.legal_moves, key=plateau.is_capture, reverse=True)


def minimax(plateau: chess.Board, profondeur: int, alpha: int, beta: int, compteur: list[int]) -> int:
    """Renvoie la meilleure note atteignable depuis cette position.

    alpha et beta servent à « élaguer » : on arrête d'explorer une branche dès qu'on
    sait qu'elle est moins bonne qu'une autre déjà trouvée (élagage alpha-bêta).
    """
    compteur[0] += 1
    if profondeur == 0 or plateau.is_game_over():
        return evaluer(plateau)

    if plateau.turn == chess.WHITE:  # les blancs cherchent la note la plus HAUTE
        meilleure = -GAGNE * 10
        for coup in trier_coups(plateau):
            plateau.push(coup)
            meilleure = max(meilleure, minimax(plateau, profondeur - 1, alpha, beta, compteur))
            plateau.pop()
            alpha = max(alpha, meilleure)
            if beta <= alpha:
                break  # élagage : l'adversaire ne nous laissera jamais arriver ici
        return meilleure

    # les noirs cherchent la note la plus BASSE
    meilleure = GAGNE * 10
    for coup in trier_coups(plateau):
        plateau.push(coup)
        meilleure = min(meilleure, minimax(plateau, profondeur - 1, alpha, beta, compteur))
        plateau.pop()
        beta = min(beta, meilleure)
        if beta <= alpha:
            break
    return meilleure


def choisir_coup(plateau: chess.Board, niveau: int = 2) -> tuple[chess.Move, int]:
    """Choisit le coup de l'ordinateur.

    Renvoie le coup choisi et le nombre de positions examinées.
    """
    reglage = NIVEAUX.get(niveau, NIVEAUX[2])
    coups = list(plateau.legal_moves)

    # Au niveau facile, l'ordinateur joue parfois n'importe quoi (comme un débutant)
    if random.random() < reglage["hasard"]:
        return random.choice(coups), 1

    compteur = [0]
    joue_les_blancs = plateau.turn == chess.WHITE
    notes = []
    for coup in coups:
        plateau.push(coup)
        note = minimax(plateau, reglage["profondeur"] - 1, -GAGNE * 10, GAGNE * 10, compteur)
        plateau.pop()
        notes.append((note, coup))

    meilleure_note = max(n for n, _ in notes) if joue_les_blancs else min(n for n, _ in notes)
    # S'il y a plusieurs coups aussi bons, on en prend un au hasard : l'ordinateur varie son jeu
    meilleurs_coups = [coup for note, coup in notes if note == meilleure_note]
    return random.choice(meilleurs_coups), compteur[0]
