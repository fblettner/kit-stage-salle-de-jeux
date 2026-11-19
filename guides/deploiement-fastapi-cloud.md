# Déploiement sur FastAPI Cloud

Le principe : le serveur Python sert **à la fois** l'API (`/api/...`) et le site React compilé (`backend/dist`).
Un seul programme à déployer, une seule commande.

## Prérequis (déjà en place à l'étape 6)

- `backend/pyproject.toml` liste les dépendances et contient :
  ```toml
  [tool.fastapi]
  entrypoint = "app.main:app"
  ```
- `frontend/vite.config.js` : `build.outDir = '../backend/dist'`
- `backend/app/main.py` : `app.frontend("/", directory=...)` si le dossier `dist` existe
- `.gitignore` contient `backend/dist/` **et** `backend/.fastapicloudignore` contient `!dist/`

> ⚠️ **Piège important :** la commande de déploiement n'envoie pas les fichiers ignorés par Git.
> Sans le `!dist/` du fichier `.fastapicloudignore`, l'API serait en ligne… mais pas le site.
> (Vérifié sur `fastapi-cloud-cli` 0.26.)

## Déployer

```bash
# 1. Compiler le site
cd frontend
npm run build                 # → backend/dist

# 2. Envoyer
cd ../backend
source .venv/bin/activate     # Windows : .venv\Scripts\activate
fastapi deploy
```

- **Première fois :** si tu n'es pas connecté, le navigateur s'ouvre pour l'authentification,
  puis la commande te demande de créer ou choisir l'application (choisis un nom, ex. `salle-de-jeux-stage`).
  Un dossier `.fastapicloud/` est créé : il mémorise l'application (il s'ignore tout seul dans Git).
- **Les fois suivantes :** `npm run build` puis `fastapi deploy`, c'est tout.
- À la fin, l'URL publique s'affiche (du type `https://<nom>.fastapicloud.dev`).

## Vérifications après déploiement

- `https://<url>/` → le menu de la salle de jeux s’affiche
- `https://<url>/api/sante` → `{"statut":"ok", ...}`
- `https://<url>/docs` → la documentation de l'API (sympa à montrer aux élèves)
- Jouer à chaque jeu depuis un téléphone, en niveau Difficile

## Si ça ne marche pas

| Symptôme | Cause probable |
|---|---|
| `/api/sante` OK mais page blanche ou 404 sur `/` | `dist` absent : refaire `npm run build`, vérifier `.fastapicloudignore` |
| Erreur au démarrage « module chess introuvable » | `chess` manquant dans les `dependencies` de `pyproject.toml` |
| Ancienne version du site | `npm run build` oublié avant `fastapi deploy` |
| La commande ne trouve pas l'application | `entrypoint` absent de `[tool.fastapi]` |

Les journaux de l'application sont consultables depuis le tableau de bord FastAPI Cloud.
