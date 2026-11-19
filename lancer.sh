#!/usr/bin/env bash
# Lance le compagnon de stage. Les 4 jeux d'exemple sont dedans : entrée « La salle de jeux » de son menu.
#
#   ./lancer.sh                    → http://127.0.0.1:8000
#   ./lancer.sh --reseau           pareil, accessible depuis les postes des élèves (même réseau)
#   ./lancer.sh stop               arrête ce qui tourne encore (après une fenêtre fermée sans Ctrl+C, par exemple)
#
# Le script prépare tout seul ce qui manque : l'environnement virtuel Python (.venv), les dépendances,
# et les deux sites React (le compagnon et les jeux), reconstruits seulement si un fichier a changé.
# Ctrl+C arrête tout.

set -euo pipefail
RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPAGNON="$RACINE/compagnon-de-stage"
SOLUTION="$RACINE/solution/salle-de-jeux"
PORT_COMPAGNON="${PORT_COMPAGNON:-8000}"
# Le serveur des jeux d'exemple : le compagnon le lance lui-même sur ce port, pour lui seul
export SALLE_PORT="${SALLE_PORT:-8001}"

quoi="lancer"
hote="127.0.0.1"
for argument in "$@"; do
  case "$argument" in
    --reseau) hote="0.0.0.0" ;;
    stop) quoi="stop" ;;
    *) quoi="aide" ;;
  esac
done

dire() { printf '\n\033[1;34m▶ %s\033[0m\n' "$*"; }
erreur() { printf '\n\033[1;31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

if [[ "$quoi" == "aide" ]]; then
  sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 1
fi

# Qui écoute sur un port ? (affiche les numéros de processus, rien si le port est libre)
qui_ecoute() { lsof -nP -tiTCP:"$1" -sTCP:LISTEN 2>/dev/null || true; }

arreter() {
  local port pids
  for port in "$PORT_COMPAGNON" "$SALLE_PORT"; do
    pids="$(qui_ecoute "$port")"
    if [[ -n "$pids" ]]; then
      echo "  port $port : arrêt du processus $(echo $pids)"
      kill $pids 2>/dev/null || true
    fi
  done
}

if [[ "$quoi" == "stop" ]]; then
  dire "Arrêt du compagnon"
  arreter
  echo "  C'est arrêté."
  exit 0
fi

# Un port déjà pris = un ancien lancement qui tourne encore : le nouveau ne pourrait pas démarrer,
# et on continuerait à voir l'ANCIENNE version sans comprendre pourquoi.
verifier_port() {
  [[ -z "$(qui_ecoute "$1")" ]] || erreur "Le port $1 est déjà utilisé : un ancien lancement tourne encore.
  Arrête-le avec :  ./lancer.sh stop     puis relance."
}

command -v python3 >/dev/null || erreur "Python 3 est introuvable (il faut Python 3.10 ou plus)."
command -v npm >/dev/null || erreur "npm est introuvable (il faut Node.js 20 ou plus)."

# L'adresse de ce poste sur le réseau local, pour la donner aux élèves
adresse_reseau() {
  ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || hostname -I 2>/dev/null | awk '{print $1}' || echo "<adresse-de-ce-poste>"
}

# Vrai si le site doit être (re)construit : pas encore construit, ou un fichier source plus récent que la construction
a_reconstruire() {   # $1 : le dossier frontend   $2 : le fichier index.html construit   $3… : d'autres fichiers à surveiller
  local front="$1" construit="$2"; shift 2
  [[ ! -f "$construit" ]] && return 0
  [[ -n "$(find "$front/src" "$front/public" "$front/index.html" "$front/package.json" "$@" -newer "$construit" -print -quit 2>/dev/null)" ]]
}

# L'environnement virtuel : une « boîte » Python réservée à un projet, avec ses propres paquets
preparer_python() {   # $1 : le dossier backend   $2… : les paquets à installer
  local back="$1"; shift
  if [[ ! -x "$back/.venv/bin/fastapi" || "$back/pyproject.toml" -nt "$back/.venv/installe" ]]; then
    dire "Python : installation des paquets dans ${back#$RACINE/}/.venv"
    [[ -d "$back/.venv" ]] || python3 -m venv "$back/.venv"
    "$back/.venv/bin/pip" install --quiet --upgrade pip
    (cd "$back" && .venv/bin/pip install --quiet "$@")
    touch "$back/.venv/installe"
  fi
}

preparer_npm() {   # $1 : le dossier frontend
  if [[ ! -d "$1/node_modules" ]]; then
    dire "Site : installation des paquets dans ${1#$RACINE/}"
    (cd "$1" && npm install --no-audit --no-fund)
  fi
}

preparer_compagnon() {
  preparer_python "$COMPAGNON/backend" -e ".[dev]"
  preparer_npm "$COMPAGNON/frontend"
  if a_reconstruire "$COMPAGNON/frontend" "$COMPAGNON/backend/dist/index.html"; then
    dire "Compagnon : construction du site"
    (cd "$COMPAGNON/frontend" && npm run build)
  fi
}

# Les 4 jeux d'exemple, construits pour vivre à l'adresse /jeux/ du compagnon (le code de la solution n'est pas modifié)
preparer_jeux() {
  preparer_npm "$SOLUTION/frontend"
  local sortie="$COMPAGNON/backend/dist-jeux"
  if a_reconstruire "$SOLUTION/frontend" "$sortie/index.html"; then
    dire "Salle de jeux : construction du site"
    (cd "$SOLUTION/frontend" && npx vite build --base=/jeux/ --outDir "$sortie" --emptyOutDir)
  fi
}

mot_de_passe() {
  # Sans mot de passe choisi, on est en mode développement : le mot de passe animateur est « animateur ».
  # Sur le réseau, tout le monde pourrait l'essayer : on exige alors un vrai mot de passe.
  if [[ -z "${ANIMATEUR_MOT_DE_PASSE:-}" ]]; then
    [[ "$hote" == "0.0.0.0" ]] && erreur "Avec --reseau, choisis un mot de passe animateur :
  ANIMATEUR_MOT_DE_PASSE='une phrase de quatre mots' ./lancer.sh --reseau"
    export COMPAGNON_DEV=1
    echo "  Mot de passe animateur (mode développement) : animateur"
  fi
  return 0
}

# Le serveur lancé (son numéro de processus), pour l'arrêter proprement à la fin
PID=""
tout_arreter() {
  trap - INT TERM EXIT
  [[ -n "$PID" ]] && kill "$PID" 2>/dev/null
  wait 2>/dev/null
  printf '\n  Tout est arrêté.\n'
  exit 0
}
trap tout_arreter INT TERM

verifier_port "$PORT_COMPAGNON"; verifier_port "$SALLE_PORT"
mot_de_passe
preparer_jeux
preparer_compagnon

(cd "$COMPAGNON/backend" && exec .venv/bin/fastapi run app/main.py --host "$hote" --port "$PORT_COMPAGNON") &
PID=$!

# On attend que le compagnon ET les jeux répondent avant d'annoncer l'adresse
for essai in $(seq 1 80); do
  curl -sf -o /dev/null "http://127.0.0.1:$PORT_COMPAGNON/api/sante" && break
  kill -0 "$PID" 2>/dev/null || erreur "Le serveur s'est arrêté au démarrage : regarde le message au-dessus."
  sleep 0.5
done

dire "C'est prêt :  http://127.0.0.1:$PORT_COMPAGNON"
[[ "$hote" == "0.0.0.0" ]] && echo "  Depuis les postes des élèves (même réseau) :  http://$(adresse_reseau):$PORT_COMPAGNON"
echo "  Les 4 jeux d'exemple : entrée « La salle de jeux » du menu."
echo "  Ctrl+C pour tout arrêter."

# On reste là tant que le serveur tourne
while kill -0 "$PID" 2>/dev/null; do sleep 1; done
tout_arreter
