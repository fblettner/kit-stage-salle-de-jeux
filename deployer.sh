#!/usr/bin/env bash
# Met le compagnon de stage en ligne (avec les 4 jeux d'exemple). À lancer SUR LE SERVEUR, dans le dossier du kit.
#
#   ./deployer.sh                  premier déploiement : pose 3 questions (domaine, e-mail, mot de passe), construit,
#                                  demande le certificat HTTPS à Let's Encrypt et démarre
#   ./deployer.sh --maj            mise à jour : récupère la dernière version du kit, reconstruit, redémarre
#   ./deployer.sh --certificat     redemande le certificat HTTPS (perdu ou expiré), sans coupure
#   ./deployer.sh --sauvegarde     copie les carnets des élèves dans un fichier sauvegarde-<date>.db
#   ./deployer.sh --journal        affiche ce que disent les serveurs (Ctrl+C pour quitter)
#   ./deployer.sh --arret          arrête tout (les carnets sont conservés)
#
#   Ajouter --image à un déploiement ou à une mise à jour : télécharge l'image construite par GitHub
#   au lieu de la construire sur le serveur (plus rapide sur une petite machine).
#
# Avant : Docker installé, le domaine qui pointe vers ce serveur, les ports 80 et 443 ouverts,
# et le kit récupéré avec git clone. Le détail est dans compagnon-de-stage/README.md.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
DEPLOY="compagnon-de-stage/deploy"
ENV="$DEPLOY/.env"

quoi="deployer"
image="non"
for argument in "$@"; do
  case "$argument" in
    --maj) quoi="maj" ;;
    --certificat) quoi="certificat" ;;
    --sauvegarde) quoi="sauvegarde" ;;
    --journal) quoi="journal" ;;
    --arret) quoi="arret" ;;
    --image) image="oui" ;;
    *) quoi="aide" ;;
  esac
done

dire() { printf '\n\033[1;34m▶ %s\033[0m\n' "$*"; }
erreur() { printf '\n\033[1;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

if [[ "$quoi" == "aide" ]]; then
  sed -n '2,16p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 1
fi

command -v docker >/dev/null || erreur "Docker est introuvable. Installe-le :  curl -fsSL https://get.docker.com | sudo sh"
docker compose version >/dev/null 2>&1 || erreur "« docker compose » est introuvable (il vient avec les versions récentes de Docker)."
docker info >/dev/null 2>&1 || erreur "Docker ne répond pas. Ton compte a-t-il le droit de l'utiliser ?
  sudo usermod -aG docker \$USER    puis déconnecte-toi et reconnecte-toi."

compose() { docker compose -f "$DEPLOY/docker-compose.yml" "$@"; }

# Les réglages du serveur (le domaine, l'e-mail pour le certificat, le mot de passe animateur) vivent dans un fichier .env
# qui reste sur le serveur : il n'est jamais envoyé sur GitHub.
preparer_env() {
  [[ -f "$ENV" ]] && return 0
  dire "Premier déploiement : trois questions"
  local domaine email mot_de_passe
  read -r -p "  Le nom de domaine (ex. stage.ton-domaine.fr) : " domaine
  [[ "$domaine" =~ ^[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]] || erreur "« $domaine » ne ressemble pas à un nom de domaine."
  read -r -p "  Ton e-mail (Let's Encrypt prévient si le certificat va expirer) : " email
  [[ "$email" =~ ^[^@[:space:]]+@[^@[:space:]]+\.[A-Za-z]{2,}$ ]] || erreur "« $email » ne ressemble pas à une adresse e-mail."
  read -r -s -p "  Le mot de passe animateur (une phrase de 4-5 mots) : " mot_de_passe; echo
  [[ ${#mot_de_passe} -ge 12 ]] || erreur "Trop court : au moins 12 caractères (une phrase de quelques mots, c'est très bien)."
  [[ "$mot_de_passe" != *$'\n'* && "$mot_de_passe" != *"'"* ]] || erreur "Pas d'apostrophe dans le mot de passe, s'il te plaît."
  ( umask 077; printf "DOMAINE=%s\nEMAIL_CERTIFICAT=%s\nANIMATEUR_MOT_DE_PASSE='%s'\n" "$domaine" "$email" "$mot_de_passe" > "$ENV" )
  echo "  Enregistré dans $ENV (lisible par toi seul)."
}

lire_env() { sed -n "s/^$1=//p" "$ENV" | tr -d "\"'"; }
domaine() { lire_env DOMAINE; }

# Le certificat HTTPS. Let's Encrypt vérifie qu'on possède le domaine en venant lire un fichier
# que certbot dépose dans un dossier servi par nginx (port 80) : le domaine doit donc déjà pointer vers ce serveur.
certificat_present() {
  compose run --rm --no-deps --entrypoint sh certbot -c "test -f /etc/letsencrypt/live/$(domaine)/fullchain.pem" >/dev/null 2>&1
}
demander_certificat() {
  local email; email="$(lire_env EMAIL_CERTIFICAT)"
  [[ -n "$email" ]] || erreur "Ajoute EMAIL_CERTIFICAT=ton@adresse dans $ENV (Let's Encrypt en a besoin)."
  compose run --rm --no-deps --entrypoint certbot certbot certonly --webroot -w /var/www/certbot \
    --cert-name "$(domaine)" -d "$(domaine)" --email "$email" --agree-tos --no-eff-email --non-interactive
}
premier_certificat() {
  certificat_present && return 0
  dire "Demande du certificat HTTPS pour $(domaine)"
  # Le vrai portier ne peut pas démarrer sans certificat : un portier provisoire répond à Let's Encrypt sur le port 80
  compose stop nginx-proxy 2>/dev/null || true
  compose --profile init up -d nginx-init
  sleep 3
  demander_certificat || { compose --profile init rm -sf nginx-init >/dev/null 2>&1; erreur "Let's Encrypt a refusé. Vérifie que $(domaine) pointe vers ce serveur (dig +short $(domaine)) et que le port 80 est ouvert."; }
  compose --profile init rm -sf nginx-init
}

# Construit (ou télécharge) l'image, démarre, puis attend que le compagnon ET les jeux répondent
demarrer() {
  if [[ "$image" == "oui" ]]; then
    dire "Téléchargement de l'image construite par GitHub"
    compose pull compagnon
  else
    dire "Construction de l'image (quelques minutes la première fois)"
    compose build compagnon
  fi
  premier_certificat
  dire "Démarrage"
  compose up -d --no-build
  # Le compagnon vient peut-être de changer d'adresse dans le réseau Docker : nginx la relit
  compose exec -T nginx-proxy nginx -s reload >/dev/null 2>&1 || true
  dire "Vérification"
  local essai
  for essai in $(seq 1 60); do
    if compose exec -T compagnon python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/sante', timeout=2)" 2>/dev/null; then
      dire "C'est en ligne :  https://$(domaine)"
      echo "  Mise à jour : ./deployer.sh --maj      Sauvegarde : ./deployer.sh --sauvegarde"
      return 0
    fi
    sleep 2
  done
  erreur "Le compagnon ne répond pas. Regarde ce qu'il dit :  ./deployer.sh --journal"
}

case "$quoi" in
  deployer)
    preparer_env
    demarrer
    ;;
  maj)
    [[ -f "$ENV" ]] || erreur "Pas encore déployé ici : lance d'abord  ./deployer.sh"
    dire "Récupération de la dernière version du kit"
    git pull --ff-only
    demarrer
    ;;
  certificat)
    [[ -f "$ENV" ]] || erreur "Pas encore déployé ici : lance d'abord  ./deployer.sh"
    dire "Certificat HTTPS pour $(domaine)"
    demander_certificat
    compose exec -T nginx-proxy nginx -s reload
    echo "  Certificat à jour. Il se renouvelle ensuite tout seul."
    ;;
  sauvegarde)
    fichier="sauvegarde-$(date +%F-%Hh%M).db"
    dire "Sauvegarde des carnets"
    # On passe par la fonction « backup » de SQLite : la copie est propre même si un élève écrit au même moment
    compose exec -T compagnon python -c "import sqlite3; s=sqlite3.connect('/donnees/compagnon.db'); s.backup(sqlite3.connect('/donnees/sauvegarde.db'))"
    compose cp compagnon:/donnees/sauvegarde.db "./$fichier"
    echo "  Fichier créé : $fichier  (il contient les prénoms et les écrits des élèves : ne le publie pas)"
    ;;
  journal)
    compose logs -f --tail 100
    ;;
  arret)
    dire "Arrêt"
    compose down
    echo "  Arrêté. Les carnets sont conservés ; ./deployer.sh pour redémarrer."
    ;;
esac
