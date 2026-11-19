"""La salle de jeux d'exemple (les 4 jeux de la solution de référence), affichée DANS le compagnon.

Les élèves ne voient qu'un seul site, à une seule adresse. En coulisses :
- au démarrage, le compagnon lance lui-même le serveur des jeux, à côté de lui, invisible depuis l'extérieur ;
- le site des jeux est construit dans backend/dist-jeux et servi ici, sous /jeux/ ;
- quand un jeu appelle son serveur (/api/echecs/…, /api/coach/…), le compagnon transmet la question
  au serveur des jeux et renvoie sa réponse. On appelle ça un « proxy » : un intermédiaire.

Le code des jeux n'est pas modifié : c'est celui du dossier solution/salle-de-jeux du kit.
"""
import subprocess
import sys
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, Response

from app.config import SALLE_ACTIVE, SALLE_DIR, SALLE_PORT

DIST_JEUX = Path(__file__).resolve().parents[1] / "dist-jeux"
ADRESSE = f"http://127.0.0.1:{SALLE_PORT}"
JEUX_SERVIS = ("echecs", "coach", "penalty", "flechettes")

# Ajouté dans la page des jeux : les couleurs du compagnon, et le thème (sombre ou clair) choisi dans le compagnon
HABILLAGE = """<link rel="stylesheet" href="/jeux-theme.css">
<script>try { if (localStorage.getItem('compagnon-theme') === 'clair') document.documentElement.classList.add('theme-clair') } catch (e) {}</script>
"""

salle = APIRouter()
_serveur: subprocess.Popen | None = None


def installee() -> bool:
    """Les deux morceaux sont là : le serveur des jeux (Python) et leur site construit."""
    return SALLE_ACTIVE and (SALLE_DIR / "app" / "main.py").is_file() and (DIST_JEUX / "index.html").is_file()


def demarrer() -> None:
    """Lance le serveur des jeux comme un deuxième programme, qui n'écoute que sur cette machine (127.0.0.1)."""
    global _serveur
    if not installee():
        return
    _serveur = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(SALLE_PORT), "--log-level", "warning"],
        cwd=SALLE_DIR)


def arreter() -> None:
    global _serveur
    if _serveur is not None:
        _serveur.terminate()
        try:
            _serveur.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _serveur.kill()
        _serveur = None


def disponible() -> bool:
    return _serveur is not None and _serveur.poll() is None


async def transmettre(requete: Request) -> Response:
    if not disponible():
        raise HTTPException(404, "La salle de jeux n'est pas lancée.")
    try:
        async with httpx.AsyncClient(base_url=ADRESSE, timeout=60) as client:
            r = await client.request(requete.method, requete.url.path, params=requete.query_params,
                                     content=await requete.body(),
                                     headers={"content-type": requete.headers.get("content-type", "application/json")})
    except httpx.HTTPError:
        raise HTTPException(503, "Le serveur des jeux ne répond pas encore : réessaie dans quelques secondes.")
    return Response(r.content, r.status_code, media_type=r.headers.get("content-type"))


@salle.get("/api/sante")
async def sante(requete: Request):
    return await transmettre(requete)


for _jeu in JEUX_SERVIS:
    salle.add_api_route(f"/api/{_jeu}/{{chemin:path}}", transmettre, methods=["GET", "POST", "PUT", "DELETE"],
                        include_in_schema=False)


@salle.get("/jeux", include_in_schema=False)
@salle.get("/jeux/{chemin:path}", include_in_schema=False)
def site_des_jeux(chemin: str = ""):
    if not disponible():
        raise HTTPException(404, "La salle de jeux n'est pas lancée.")
    fichier = (DIST_JEUX / chemin).resolve()
    if chemin and DIST_JEUX.resolve() in fichier.parents and fichier.is_file():
        return FileResponse(fichier)
    page = (DIST_JEUX / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(page.replace("</head>", HABILLAGE + "</head>"))
