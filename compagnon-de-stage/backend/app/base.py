"""La base de données SQLite : un seul fichier, gardé dans un volume Docker."""
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS stagiaires (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prenom TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    jeu TEXT,
    dossier TEXT,
    cree_le TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    jeton TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    stagiaire_id INTEGER REFERENCES stagiaires(id) ON DELETE CASCADE,
    cree_le TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coches (
    stagiaire_id INTEGER NOT NULL REFERENCES stagiaires(id) ON DELETE CASCADE,
    cle TEXT NOT NULL,
    fait INTEGER NOT NULL,
    maj TEXT NOT NULL,
    PRIMARY KEY (stagiaire_id, cle)
);
CREATE TABLE IF NOT EXISTS reponses (
    stagiaire_id INTEGER NOT NULL REFERENCES stagiaires(id) ON DELETE CASCADE,
    cle TEXT NOT NULL,
    texte TEXT NOT NULL,
    maj TEXT NOT NULL,
    PRIMARY KEY (stagiaire_id, cle)
);
CREATE TABLE IF NOT EXISTS aides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stagiaire_id INTEGER NOT NULL REFERENCES stagiaires(id) ON DELETE CASCADE,
    activite TEXT NOT NULL,
    message TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'ouverte',
    reponse TEXT NOT NULL DEFAULT '',
    cree_le TEXT NOT NULL,
    maj TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS bugs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    auteur_id INTEGER NOT NULL REFERENCES stagiaires(id) ON DELETE CASCADE,
    cible_id INTEGER REFERENCES stagiaires(id) ON DELETE CASCADE,
    action TEXT NOT NULL,
    resultat TEXT NOT NULL,
    attendu TEXT NOT NULL,
    corrige INTEGER NOT NULL DEFAULT 0,
    cree_le TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS surprises (
    stagiaire_id INTEGER NOT NULL REFERENCES stagiaires(id) ON DELETE CASCADE,
    activite TEXT NOT NULL,
    PRIMARY KEY (stagiaire_id, activite)
);
CREATE TABLE IF NOT EXISTS reglages (
    cle TEXT PRIMARY KEY,
    valeur TEXT NOT NULL
);
"""


def maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def initialiser() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connexion() as db:
        db.executescript(SCHEMA)
        # Une base créée avec une version précédente n'a pas encore cette colonne : on l'ajoute.
        colonnes = {l["name"] for l in db.execute("PRAGMA table_info(stagiaires)")}
        if "vu_le" not in colonnes:
            db.execute("ALTER TABLE stagiaires ADD COLUMN vu_le TEXT")   # la dernière fois que son écran a parlé au serveur


@contextmanager
def connexion():
    """Une connexion par requête ; les changements sont enregistrés à la fin (commit)."""
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def lire_reglage(db, cle: str, defaut: str = "") -> str:
    ligne = db.execute("SELECT valeur FROM reglages WHERE cle = ?", (cle,)).fetchone()
    return ligne["valeur"] if ligne else defaut


def ecrire_reglage(db, cle: str, valeur: str) -> None:
    db.execute("INSERT INTO reglages (cle, valeur) VALUES (?, ?) ON CONFLICT(cle) DO UPDATE SET valeur = excluded.valeur",
               (cle, valeur))
