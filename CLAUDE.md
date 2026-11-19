# Projet : la salle de jeux (stage de 3e)

## Contexte

Ce projet est réalisé pendant un **stage d'observation de 3e**. Deux collégiens (14-15 ans),
sans expérience de programmation, découvrent le métier de développeur avec leur maître de stage.
Ce sont eux qui te donnent les consignes. Ils veulent **comprendre** ce que tu fais, pas seulement obtenir un résultat.

La salle de jeux est un site avec un menu et des jeux contre l'ordinateur. Chaque jeu a son dossier
et chaque élève travaille sur un jeu (parfois le même, chacun dans sa version) :
- **Échecs** (`echecs`) : l'IA *calcule* les coups à l'avance (minimax).
- **Coach** (`coach`) : jeu d'entraîneur de foot ; l'IA *simule* des centaines de matchs pour choisir sa tactique et *apprend* les habitudes du joueur.
- **Penalty Pro** (`penalty`) : tirs au but avec visée et jauge de puissance ; le gardien IA *apprend* où le joueur tire.
- **Fléchettes** (`flechettes`) : partie de 301 ; l'IA *simule* ses lancers pour savoir où viser selon sa précision.

**Les jeux de NOTRE projet :** [à compléter : par exemple « Échecs (Léa) et Fléchettes (Tom) »]

Au début de chaque séance, l'élève te dit sur quel jeu il travaille. **Ne modifie que les fichiers de ce jeu.**

## Comment t'adresser à eux

- Réponds **en français**, avec des mots simples. Quand tu utilises un mot technique
  (API, composant, fonction, requête, probabilité…), explique-le en une phrase, avec une comparaison de la vie courante si possible.
- Avance **par petites étapes** : une fonctionnalité à la fois, puis on teste avant de continuer.
- Avant de coder, annonce en 2-3 lignes **ce que tu vas faire et pourquoi**.
- Après avoir codé, résume **quels fichiers tu as modifiés** et dis **comment tester** (quoi ouvrir, sur quoi cliquer).
- Quand quelque chose ne marche pas, explique la cause simplement avant de corriger : les erreurs font partie du métier.
- Si une consigne est floue, pose **une** question courte plutôt que de deviner.
- Propose un **commit Git** à la fin de chaque étape qui fonctionne, avec un message en français
  qui commence par le nom du jeu (ex. « Fléchettes : l'IA choisit où viser »).
  Ne pousse jamais sans qu'on te le demande.

## Règles pour le code

- Code **simple et lisible** avant tout : noms de variables et de fonctions **en français**
  (`partie`, `coupsPossibles`, `choisir_visee`), commentaires en français qui expliquent le « pourquoi ».
- Pas d'optimisation prématurée, pas d'abstraction inutile, pas de TypeScript, pas de librairie CSS ni de librairie de jeu.
- **Chaque jeu reste dans son dossier** : `frontend/src/<jeu>/`, `backend/app/<jeu>/`, `backend/tests/test_<jeu>.py`.
  Les fichiers communs (`App.jsx`, `index.css`, `main.py`, `vite.config.js`, `pyproject.toml`) ne se modifient
  **qu'après avoir demandé**, car ils concernent les deux élèves.
- Les classes CSS d'un jeu commencent par son nom (`.echecs-…`, `.coach-…`, `.penalty-…`, `.flechettes-…`).
- **Le serveur est l'arbitre** : c'est lui qui applique les règles et calcule les résultats. Il ne fait pas
  confiance au navigateur et vérifie ce qu'il reçoit.
- **L'IA ne triche jamais** : elle ne reçoit pas le choix en cours du joueur, seulement ses choix précédents.
- **L'IA reste compréhensible** : des calculs qu'on peut expliquer (compter, faire des moyennes, simuler avec du hasard,
  minimax). Pas de librairie de machine learning, pas de moteur externe (pas de Stockfish).
- **Échecs :** ne réinvente pas les règles, utilise `chess.js` (front) et `python-chess` (back).
- **Coach :** les joueurs et les clubs sont **inventés** (pas de vrais joueurs, clubs ou logos).
- Demande avant d'ajouter une nouvelle dépendance (npm ou pip).
- Ne mets jamais de mot de passe, clé ou jeton dans le code.

## Architecture

```
frontend/                   React + Vite (port 5173 en dev). Les appels /api vont vers le back (proxy).
  src/App.jsx               COMMUN : le menu de la salle de jeux (une ligne par jeu dans la liste JEUX)
  src/index.css             COMMUN : couleurs, boutons, cartes
  src/echecs/               JeuEchecs.jsx (react-chessboard v5 : réglages dans options={{...}}, chess.js)
  src/coach/                Coach.jsx (les étapes du jeu), Mercato.jsx, Match.jsx, RapportIA.jsx…
  src/penalty/              PenaltyPro.jsx, Cage.jsx (le dessin du but), PenseeIA.jsx, regles.js
  src/flechettes/           Flechettes.jsx, Cible.jsx (le dessin SVG), cible.js (les dimensions)
backend/                    Python + FastAPI (port 8000 en dev)
  app/main.py               COMMUN : démarre le serveur et branche les routes des jeux
  app/echecs/               routes.py (/api/echecs/...), moteur.py (minimax)
  app/coach/                routes.py (/api/coach/...), joueurs.py, simulateur.py, ia.py (Monte-Carlo)
  app/penalty/              routes.py (/api/penalty/...), physique.py (trajectoire, arbitre), ia.py (gardien et tireur)
  app/flechettes/           routes.py (/api/flechettes/...), cible.py (points, règles du 301), ia.py (où viser)
  tests/                    un fichier de tests par jeu (pytest)
```

## Commandes utiles

```bash
# Back (dans backend/, environnement virtuel activé)
fastapi dev          # lance le serveur (http://127.0.0.1:8000/docs pour tester l'API)
pytest               # lance tous les tests
pytest tests/test_flechettes.py    # seulement les tests d'un jeu

# Front (dans frontend/)
npm run dev          # lance le site (http://localhost:5173)
npm run build        # prépare la version en ligne dans backend/dist

# Mise en ligne (dans backend/, après npm run build)
fastapi deploy
```
