"""Qui est connecté ? L'animateur (avec un mot de passe) ou un stagiaire (avec son code à 6 caractères)."""
import hmac
import secrets
import time

from fastapi import Depends, Header, HTTPException

from app.base import connexion, maintenant

# Lettres et chiffres faciles à recopier (pas de 0/O, 1/I/L)
ALPHABET_CODE = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"

_echecs_recents: dict[str, list[float]] = {}


def nouveau_code() -> str:
    return "".join(secrets.choice(ALPHABET_CODE) for _ in range(6))


def nouveau_jeton(role: str, stagiaire_id: int | None = None) -> str:
    jeton = secrets.token_urlsafe(32)
    with connexion() as db:
        db.execute("INSERT INTO sessions (jeton, role, stagiaire_id, cree_le) VALUES (?, ?, ?, ?)",
                   (jeton, role, stagiaire_id, maintenant()))
    return jeton


def freiner(cle: str) -> None:
    """Contre les essais en rafale : au-delà de 10 échecs en 5 minutes, on refuse pendant un moment."""
    now = time.monotonic()
    essais = [t for t in _echecs_recents.get(cle, []) if now - t < 300]
    _echecs_recents[cle] = essais
    if len(essais) >= 10:
        raise HTTPException(429, "Trop d'essais. Attends quelques minutes.")


def noter_echec(cle: str) -> None:
    _echecs_recents.setdefault(cle, []).append(time.monotonic())


def comparer(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode(), b.encode())


def session(authorization: str = Header(default="")) -> dict:
    jeton = authorization.removeprefix("Bearer ").strip()
    if not jeton:
        raise HTTPException(401, "Il faut se connecter.")
    with connexion() as db:
        ligne = db.execute("SELECT role, stagiaire_id FROM sessions WHERE jeton = ?", (jeton,)).fetchone()
    if not ligne:
        raise HTTPException(401, "Session expirée : reconnecte-toi.")
    return {"role": ligne["role"], "stagiaire_id": ligne["stagiaire_id"], "jeton": jeton}


def animateur(s: dict = Depends(session)) -> dict:
    if s["role"] != "animateur":
        raise HTTPException(403, "Réservé à l'animateur.")
    return s


def stagiaire(s: dict = Depends(session)) -> int:
    if s["role"] != "stagiaire":
        raise HTTPException(403, "Réservé aux stagiaires.")
    return s["stagiaire_id"]
