"""Le compagnon de stage : l'API + le site React (une fois construit dans dist/)."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app import base, salle as salle_de_jeux
from app.routes import anim, api
from app.salle import salle


@asynccontextmanager
async def demarrage(app: FastAPI):
    base.initialiser()
    salle_de_jeux.demarrer()     # les 4 jeux d'exemple, lancés à côté (voir app/salle.py)
    yield
    salle_de_jeux.arreter()


app = FastAPI(title="Compagnon de stage", lifespan=demarrage)
app.include_router(api)
app.include_router(anim)
app.include_router(salle)

DIST = Path(__file__).resolve().parents[1] / "dist"
if DIST.exists():
    app.frontend("/", directory=DIST)
