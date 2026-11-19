"""Le serveur (le « back ») de la salle de jeux.

Ce fichier est COMMUN à tous les jeux : il démarre le serveur et branche
les routes de chaque jeu. Chaque jeu vit dans son propre dossier :
    app/echecs/      → le jeu d'échecs
    app/coach/       → Coach, le jeu d'entraîneur de foot
    app/penalty/     → Penalty Pro, les tirs au but
    app/flechettes/  → les fléchettes

En production, il sert aussi les pages du site (le dossier dist/).
"""
from pathlib import Path

from fastapi import FastAPI

from app.coach.routes import routeur as routeur_coach
from app.echecs.routes import routeur as routeur_echecs
from app.flechettes.routes import routeur as routeur_flechettes
from app.penalty.routes import routeur as routeur_penalty

app = FastAPI(title="La salle de jeux")


@app.get("/api/sante")
def sante():
    """Permet de vérifier que le serveur est bien allumé."""
    return {"statut": "ok", "message": "Le serveur de la salle de jeux est prêt !"}


# On « branche » les routes de chaque jeu
app.include_router(routeur_echecs)
app.include_router(routeur_coach)
app.include_router(routeur_penalty)
app.include_router(routeur_flechettes)

# Le site React compilé (créé par "npm run build" dans le dossier frontend).
# Les routes /api ci-dessus restent prioritaires.
DOSSIER_SITE = Path(__file__).resolve().parent.parent / "dist"
if DOSSIER_SITE.is_dir():
    app.frontend("/", directory=str(DOSSIER_SITE))
