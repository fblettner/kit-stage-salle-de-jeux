# Image Docker de la salle de jeux (utilisée pour le déploiement sur une VM OCI)
# Construction en 2 étapes : d'abord le site React, ensuite le serveur Python.

# --- Étape 1 : compiler le site React ---
FROM node:22-alpine AS front
WORKDIR /src/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# vite.config.js range le résultat dans ../backend/dist
RUN npm run build

# --- Étape 2 : le serveur Python qui sert l'API + le site ---
FROM python:3.12-slim
WORKDIR /app
COPY backend/pyproject.toml ./
# On installe les dépendances listées dans pyproject.toml (avec uv, rapide)
RUN pip install --no-cache-dir uv && uv pip install --system --no-cache -r pyproject.toml
COPY backend/app ./app
COPY --from=front /src/backend/dist ./dist

EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]
