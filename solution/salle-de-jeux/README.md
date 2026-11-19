# 🎮 La salle de jeux — solution de référence

Projet réalisé pendant un stage d'observation de 3e : une salle de jeux en ligne, avec des jeux
contre l'ordinateur et plusieurs façons de faire une IA. Les élèves choisissent un ou deux jeux du catalogue ;
cette solution de référence les contient **tous les quatre**.

| Jeu | Le principe | L'IA… | Où |
|---|---|---|---|
| ♞ **Échecs** | une partie contre l'ordinateur | **calcule** les coups à l'avance (minimax + élagage) | `backend/app/echecs/` |
| ⚽ **Coach** | recruter 5 joueurs (inventés), choisir sa tactique, suivre le match en direct | **simule** des centaines de matchs (Monte-Carlo) et **apprend** tes habitudes | `backend/app/coach/` |
| 🥅 **Penalty Pro** | viser à la souris, doser sa puissance, puis arrêter les tirs de l'IA | **apprend** où tu tires (fréquences, enchaînements, endroit précis) | `backend/app/penalty/` |
| 🎯 **Fléchettes** | une partie de 301, la main qui tremble | **simule** ses lancers pour savoir où viser selon sa précision ; le conseiller **mesure** la tienne | `backend/app/flechettes/` |

- **Front** : React + Vite. Échecs : `react-chessboard`, `chess.js`. Les autres jeux : CSS et SVG, sans librairie.
- **Back** : Python + FastAPI. Échecs : `python-chess`. Le serveur est l'**arbitre** de chaque jeu.

## Les étapes

Chaque jeu se construit en 4 étapes, en parallèle, chacun dans son dossier.

| Étape | ♞ Échecs | ⚽ Coach | 🥅 Penalty Pro | 🎯 Fléchettes |
|---|---|---|---|---|
| 1 — socle commun | le menu, un dossier par jeu | ← | ← | ← |
| 2 — l'affichage | l'échiquier | le mercato | viser et tirer | la cible |
| 3 — le serveur | l'IA joue au hasard | le match | l'arbitre | l'arbitre du 301 |
| 4 — la vraie IA | minimax | l'entraîneur IA | le gardien apprend | l'IA vise |
| 5 — finitions | finitions | la mi-temps | la séance | le conseiller |
| 6 — mise en ligne | build, FastAPI Cloud, Docker/OCI | ← | ← | ← |

## Lancer en local (2 terminaux)

Prérequis : Python 3.10+, Node.js 20+.

**Terminal 1 — le back**

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -U pip
pip install "fastapi[standard]" chess pytest httpx
fastapi dev                        # http://127.0.0.1:8000/docs pour voir l'API
```

**Terminal 2 — le front**

```bash
cd frontend
npm install
npm run dev                        # ouvrir http://localhost:5173
```

**Tests**

```bash
cd backend && pytest               # 47 tests (échecs 7, Coach 16, Penalty Pro 13, Fléchettes 11)
```

## Mise en ligne

### Option A — FastAPI Cloud (la plus simple)

```bash
cd frontend && npm run build       # crée backend/dist (le site compilé)
cd ../backend && fastapi deploy    # 1re fois : le navigateur s'ouvre pour se connecter
```

`backend/dist` est ignoré par Git mais envoyé sur FastAPI Cloud grâce à `backend/.fastapicloudignore`.

### Option B — VM OCI avec Docker

Voir `deploy/oci/` : `docker compose up -d --build` lance la salle de jeux derrière **Caddy**,
qui fournit HTTPS automatiquement (modifier le nom de domaine dans `Caddyfile`).

## Ne garder que les jeux choisis

Pour un projet avec seulement certains jeux : supprimer les dossiers des autres jeux
(`frontend/src/<jeu>`, `backend/app/<jeu>`, `backend/tests/test_<jeu>.py`), puis retirer leur ligne
dans la liste `JEUX` de `frontend/src/App.jsx` et leur `include_router` dans `backend/app/main.py`.

Tous les joueurs et clubs de Coach sont inventés.
