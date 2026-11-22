"""Les réglages de l'application, lus dans les variables d'environnement."""
import os
from pathlib import Path

# Le dossier du kit, qui contient les fichiers .md (prompts/, fiches/, guides/…).
# Par défaut : le dossier parent de compagnon-de-stage/, trois niveaux au-dessus de ce fichier.
# On ne calcule ce chemin par défaut QUE si la variable n'est pas définie : dans l'image Docker,
# ce fichier est dans /app/app, il n'y a pas trois niveaux au-dessus, et le calcul plantait au démarrage.
ICI = Path(__file__).resolve()
CONTENU_DIR = Path(os.environ["CONTENU_DIR"]) if os.environ.get("CONTENU_DIR") else ICI.parents[3]

# Le fichier de la base de données SQLite
DB_PATH = Path(os.environ.get("DB_PATH", Path(__file__).resolve().parents[1] / "donnees" / "compagnon.db"))

# Le mot de passe de l'animateur. À définir absolument en production !
MOT_DE_PASSE_ANIMATEUR = os.environ.get("ANIMATEUR_MOT_DE_PASSE", "")
MODE_DEV = os.environ.get("COMPAGNON_DEV", "") == "1"
if not MOT_DE_PASSE_ANIMATEUR and MODE_DEV:
    MOT_DE_PASSE_ANIMATEUR = "animateur"

FUSEAU = os.environ.get("FUSEAU", "Europe/Paris")

# La salle de jeux d'exemple (voir app/salle.py) : le dossier du serveur des jeux, et le port sur lequel
# le compagnon le lance, pour lui seul. SALLE=0 la désactive (les tests s'en passent).
SALLE_DIR = Path(os.environ.get("SALLE_DIR", CONTENU_DIR / "solution" / "salle-de-jeux" / "backend"))
SALLE_PORT = int(os.environ.get("SALLE_PORT", "8001"))
SALLE_ACTIVE = os.environ.get("SALLE", "1") != "0"
