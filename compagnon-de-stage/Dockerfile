# Le compagnon de stage en une seule image : le site React construit + le serveur Python + les fichiers .md du kit.
# À construire DEPUIS LA RACINE DU KIT (le dossier qui contient prompts/, fiches/, guides/) :
#   docker build -f compagnon-de-stage/Dockerfile -t compagnon-de-stage .

# 1) On construit le site React
FROM node:22-slim AS site
WORKDIR /site
COPY compagnon-de-stage/frontend/package*.json ./
RUN npm ci
COPY compagnon-de-stage/frontend/ ./
RUN npx vite build --outDir /site/dist

# 1 bis) On construit le site des 4 jeux d'exemple, pour l'adresse /jeux/ du compagnon
FROM node:22-slim AS jeux
WORKDIR /jeux
COPY solution/salle-de-jeux/frontend/package*.json ./
RUN npm ci
COPY solution/salle-de-jeux/frontend/ ./
RUN npx vite build --base=/jeux/ --outDir /jeux/dist

# 2) Le serveur Python
FROM python:3.12-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY compagnon-de-stage/backend/pyproject.toml ./
RUN uv pip install --system -r pyproject.toml
COPY compagnon-de-stage/backend/app ./app
COPY --from=site /site/dist ./dist
# La salle de jeux d'exemple : son site, et son serveur que le compagnon lance à côté de lui (app/salle.py)
COPY --from=jeux /jeux/dist ./dist-jeux
COPY solution/salle-de-jeux/backend/app /salle/app
# Les contenus du stage : l'appli lit directement les fichiers .md du kit
COPY *.md /contenu/
COPY prompts /contenu/prompts
COPY fiches /contenu/fiches
COPY guides /contenu/guides
COPY autonomie /contenu/autonomie
ENV CONTENU_DIR=/contenu \
    SALLE_DIR=/salle \
    DB_PATH=/donnees/compagnon.db \
    FUSEAU=Europe/Paris
RUN useradd --create-home compagnon && mkdir -p /donnees && chown compagnon /donnees
USER compagnon
VOLUME /donnees
EXPOSE 8000
CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--proxy-headers"]
