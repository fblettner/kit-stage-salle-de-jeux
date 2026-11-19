"""Le déroulé de la semaine : chaque activité pointe vers un morceau des fichiers .md du kit.

Les activités « ensemble » affichent aux stagiaires un pas-à-pas écrit pour eux :
la partie du fichier autonomie/parcours-eleves.md qui porte le même identifiant (« ## l3 · … »).

Le CONTENU (textes, prompts, cases à cocher) reste dans les fichiers .md : on les modifie là-bas.
Ici, on ne décrit que la STRUCTURE : quel jour, à quelle heure, quel morceau de quel fichier.

Une activité « perso » dépend du jeu du stagiaire : elle pointe vers une étape (2, 34 ou 5),
c'est-à-dire vers le bon fichier du dossier prompts/<jeu>/.
"""

JEUX = {
    "echecs": {
        "nom": "Échecs", "icone": "♞", "catalogue": "♞ Échecs",
        "fichiers": {2: "prompts/echecs/etape-2-l-echiquier.md", 34: "prompts/echecs/etapes-3-4-l-ordinateur-joue.md",
                     5: "prompts/echecs/etape-5-finitions.md"},
    },
    "coach": {
        "nom": "Coach", "icone": "⚽", "catalogue": "⚽ Coach",
        "fichiers": {2: "prompts/coach/etape-2-le-mercato.md", 34: "prompts/coach/etapes-3-4-le-match-et-l-entraineur-ia.md",
                     5: "prompts/coach/etape-5-la-mi-temps.md"},
    },
    "penalty": {
        "nom": "Penalty Pro", "icone": "🥅", "catalogue": "🥅 Penalty Pro",
        "fichiers": {2: "prompts/penalty/etape-2-viser-et-tirer.md", 34: "prompts/penalty/etapes-3-4-l-arbitre-et-le-gardien-ia.md",
                     5: "prompts/penalty/etape-5-la-seance.md"},
    },
    "flechettes": {
        "nom": "Fléchettes", "icone": "🎯", "catalogue": "🎯 Fléchettes",
        "fichiers": {2: "prompts/flechettes/etape-2-la-cible.md", 34: "prompts/flechettes/etapes-3-4-l-arbitre-et-l-ia.md",
                     5: "prompts/flechettes/etape-5-le-conseiller.md"},
    },
}

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
THEMES = [
    "Le besoin et le choix · casquette conseil",
    "L'architecture et les premiers écrans · architecte et développeur",
    "L'intelligence artificielle démystifiée",
    "Finitions et changements · le réel du métier",
    "Fusion, mise en ligne et démo",
]

J1, J2, J3, J5 = ("prompts/J1-le-besoin.md", "prompts/J2-architecture-et-socle.md",
                  "prompts/J3-ateliers-debranches.md", "prompts/J5-mise-en-ligne-et-demo.md")


def A(id, jour, debut, fin, titre, description, mode="ensemble", source=None, prompts_eleve=False,
      surprise=False, lien=None, idees=False, modele_prompt=None, bilan=False, routine=False):
    """bilan : la dernière activité du jour, où le stagiaire écrit son bilan pour son maître de stage.
    routine : la première activité « sur ordinateur » du jour : on y rappelle comment relancer le poste."""
    return {"id": id, "jour": jour, "debut": debut, "fin": fin, "titre": titre, "description": description,
            "mode": mode, "source": source, "prompts_eleve": prompts_eleve, "surprise": surprise, "lien": lien,
            "idees": idees, "modele_prompt": modele_prompt, "bilan": bilan, "routine": routine}


# Pour les finitions, l'élève écrit SES propres prompts : on lui donne un modèle à compléter.
MODELE_FINITION = """[PHRASE DE DÉPART]
Notre client voudrait une amélioration : [DÉCRIS CE QUE TU VEUX, CE QU'ON DOIT VOIR À L'ÉCRAN].
Avant de coder, explique-moi en 3 lignes ce que tu vas faire et quels fichiers tu vas modifier.
Ensuite, dis-moi comment tester."""


ACTIVITES = [
    # --- Lundi ---
    A("l1", 0, "09:00", "10:30", "Accueil et découverte du métier",
      "Visite de l'entreprise, puis ton maître de stage te présente son métier : développeur, architecte, consultant."),
    A("l2", 0, "10:30", "12:00", "Installation aux postes",
      "On découvre l'ordinateur sur lequel tu vas travailler toute la semaine.",
      source={"fichier": "guides/preparation-du-poste.md"}),
    A("l3", 0, "13:30", "14:15", "L'interview du client",
      "Ton maître de stage joue un client : le directeur d'une Maison des jeunes. Pose-lui des questions et note ses réponses !",
      source={"fichier": J1, "depuis": "Atelier 1", "jusqua": "Atelier 2"}),
    A("l4", 0, "14:15", "15:00", "Le catalogue : choisis ton projet",
      "Joue aux 4 jeux d'exemple, lis le catalogue, puis choisis TON projet dans l'onglet « Mon projet ».",
      source={"fichier": J1, "depuis": "Atelier 2", "jusqua": "Atelier 3"}, lien="projet"),
    A("l5", 0, "15:00", "15:45", "Le cahier des charges",
      "Avec Claude, on transforme les notes de l'interview en document clair pour le client.",
      source={"fichier": J1, "depuis": "Atelier 3", "jusqua": "Atelier 4"}, prompts_eleve=True),
    A("l6", 0, "15:45", "16:30", "Les maquettes papier",
      "Dessine sur une feuille l'écran de ton jeu, puis ensemble le menu d'accueil. Garde-la : elle servira jeudi.",
      source={"fichier": J1, "depuis": "Atelier 4"}, lien="carnet", bilan=True),
    # --- Mardi ---
    A("m1", 1, "09:00", "09:45", "Le schéma : front, back, API",
      "Au tableau : comment fonctionne un site, et comment travailler à deux sans se gêner.",
      source={"fichier": J2, "depuis": "Atelier 1", "jusqua": "Atelier 2"}),
    A("m2", 1, "09:45", "10:30", "Découverte des outils",
      "VS Code, le terminal, Git, et la fiche de consignes pour Claude (le fichier CLAUDE.md).",
      source={"fichier": J2, "depuis": "Atelier 2", "jusqua": "Atelier 3"}),
    A("m3", 1, "10:30", "11:30", "Le socle commun",
      "Ensemble, sur un seul poste : on crée le menu de la salle de jeux et un dossier pour chaque jeu.",
      source={"fichier": J2, "depuis": "Atelier 3", "jusqua": "Atelier 4"}, prompts_eleve=True),
    A("m4", 1, "11:30", "12:00", "Chacun son poste",
      "Chacun récupère le projet sur son ordinateur et crée sa branche Git, du nom de son jeu.",
      source={"fichier": J2, "depuis": "Atelier 4"}),
    A("m5", 1, "13:30", "15:30", "Étape 2 : l'écran de ton jeu",
      "Tu construis l'affichage de ton jeu avec Claude. Suis les prompts un par un et coche ce que tu as vérifié.",
      mode="perso", source={"etape": 2}),
    A("m6", 1, "15:30", "16:30", "Présentation et carnet de bord",
      "Montre ton écran à l'autre stagiaire, teste le sien, puis remplis ton carnet de bord.", lien="carnet", bilan=True),
    # --- Mercredi ---
    A("w1", 2, "09:00", "10:15", "Étape 3 : le serveur",
      "Le serveur Python entre en jeu. Pour l'instant, l'ordinateur joue (ou décide) au hasard.",
      mode="perso", source={"etape": 34, "depuis": "Matin", "jusqua": "Après-midi"}, routine=True),
    A("w2", 2, "10:15", "11:30", "Atelier : comment « pense » une IA ?",
      "Sans ordinateur : calculer (minimax), simuler (avec des dés ou des boulettes de papier), apprendre (pierre-feuille-ciseaux).",
      source={"fichier": J3}),
    A("w3", 2, "13:30", "15:45", "Étape 4 : la vraie IA",
      "Tu programmes l'intelligence artificielle de ton jeu, avec 3 niveaux et des tests automatiques.",
      mode="perso", source={"etape": 34, "depuis": "Après-midi"}),
    A("w4", 2, "15:45", "16:30", "Le duel",
      "Chacun affronte l'IA du jeu de l'autre. Note tes résultats dans ton carnet !", lien="carnet", bilan=True),
    # --- Jeudi ---
    A("j1", 3, "09:00", "09:30", "Revue avec les maquettes",
      "Ressors ta maquette de lundi : que manque-t-il ? Fais la liste de tes idées ci-dessous et classe-les : "
      "par quoi commencer ?", idees=True, routine=True),
    A("j2", 3, "09:30", "11:00", "Étape 5 : les finitions",
      "Tu améliores ton jeu. Un prompt par amélioration, on teste, on committe.",
      mode="perso", source={"etape": 5, "jusqua": "🎭"}, idees=True, modele_prompt=MODELE_FINITION),
    A("j3", 3, "11:00", "12:00", "🎭 Le client change d'avis",
      "Le client a une nouvelle demande… Elle apparaîtra ici quand ton maître de stage la déclenchera.",
      mode="perso", source={"etape": 5, "depuis": "🎭", "jusqua": "Chasse"}, surprise=True),
    A("j4", 3, "13:30", "15:30", "Chasse aux bugs",
      "Tu deviens testeur du jeu de l'autre stagiaire. Note chaque bug dans l'onglet « Bugs ».",
      mode="perso", source={"etape": 5, "depuis": "Chasse"}, lien="bugs"),
    A("j5", 3, "15:30", "16:30", "Tournoi et fusion",
      "Tournoi contre les IA, puis on réunit les deux jeux dans le même projet (la « fusion » Git).",
      source={"fichier": "guides/travailler-a-deux-avec-git.md", "depuis": "Jeudi soir", "jusqua": "Le cas"}, bilan=True),
    # --- Vendredi ---
    A("v1", 4, "09:00", "09:45", "Fusion et version en ligne",
      "On vérifie que les deux jeux marchent ensemble, puis on prépare la version à mettre en ligne.",
      source={"fichier": J5, "depuis": "Atelier 0", "jusqua": "Atelier 2"}, prompts_eleve=True, routine=True),
    A("v2", 4, "09:45", "10:30", "Mise en ligne !",
      "Le jeu part sur Internet. Ouvre l'adresse sur ton téléphone et note-la dans ton carnet.",
      source={"fichier": J5, "depuis": "Atelier 2", "jusqua": "Atelier 3"}),
    A("v3", 4, "10:30", "12:00", "La version « entreprise »",
      "Démonstration : une machine virtuelle, Docker, un nom de domaine, HTTPS. Quelle solution conseiller au client ?",
      source={"fichier": J5, "depuis": "Atelier 3", "jusqua": "Atelier 4"}),
    A("v4", 4, "13:30", "14:30", "Préparer la démo",
      "Préparez la présentation à deux voix : le besoin, l'architecture, chaque jeu et son IA, la démo en direct.",
      source={"fichier": J5, "depuis": "Atelier 4", "jusqua": "Atelier 5"}, prompts_eleve=True),
    A("v5", 4, "14:30", "15:30", "La démo devant l'équipe",
      "C'est votre moment : présentez votre salle de jeux et faites jouer le public !"),
    A("v6", 4, "15:30", "16:30", "Carnet de bord et rapport de stage",
      "Termine ton carnet de bord, puis imprime-le : il t'aidera pour ton rapport de stage.",
      source={"fichier": J5, "depuis": "Atelier 5"}, prompts_eleve=True, lien="carnet", bilan=True),
]

ACTIVITES_PAR_ID = {a["id"]: a for a in ACTIVITES}
