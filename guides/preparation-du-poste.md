# Préparer les postes avant l'arrivée des élèves

À faire **la semaine d'avant**, pour ne pas perdre la première matinée en installations.

## Deux postes de travail

Idéalement **un poste par élève** (à partir du mardi après-midi, chacun développe son jeu).
Sur **chaque** poste :

- [ ] **VS Code** avec l'extension **Claude Code**, connectée à **ton** compte
- [ ] **Git** configuré (`git config --global user.name` / `user.email`)
- [ ] **Python 3.10+** (`python3 --version`)
- [ ] **Node.js 20+** (`node --version`), npm fourni avec
- [ ] Un navigateur avec les **outils de développement** (F12) : on s'en sert pour lire les erreurs

Sur ton poste en plus : **Claude Desktop** (jours 1, 2 et 5 : cahier des charges, schémas, présentation).

> Un seul poste ? C'est jouable, voir la fin de `travailler-a-deux-avec-git.md`.

## Comptes

- [ ] **Claude** : ton compte. Les conditions d'utilisation de Claude.ai réservent le service aux **18 ans et plus** :
      les élèves dictent et décident, la session reste la tienne (une fenêtre VS Code par poste).
- [ ] **Un dépôt Git distant privé** (GitHub/GitLab) pour partager le socle et les deux branches
- [ ] **FastAPI Cloud** : connexion testée (`fastapi deploy` une fois avec la solution de référence)
- [ ] **OCI** : une VM prête (voir `deploiement-oci.md`), un nom de domaine ou sous-domaine qui pointe dessus

## Répétition générale (≈ 3-4 h, fortement recommandé)

1. Crée un dossier vide, copie le `CLAUDE.md` du kit, et déroule les prompts :
   le socle (J2), puis **le parcours des jeux choisis** (`prompts/<jeu>/`), puis le J5.
   Avant que les élèves aient choisi, joue au moins aux 4 jeux de la solution pour pouvoir les présenter.
   Note ce qui coince et ajuste les prompts si besoin.
2. Essaie la fusion des deux branches et un déploiement FastAPI Cloud + OCI.
3. Garde la **solution de référence** (dossier `solution/salle-de-jeux`) sous la main :
   quand un élève est bloqué, tu peux comparer son code avec celui du même jeu.

## Le jour J

- Les deux postes **côte à côte**, si possible avec un grand écran pour les moments communs.
- Chaque élève est **responsable** de son jeu et **client-testeur** du jeu de l'autre.
  Le mercredi et le jeudi, demande-leur régulièrement de jouer au jeu de l'autre et de lui faire des retours.
- **Ton rythme :** pendant que Claude travaille sur un poste (1 à 3 min), passe à l'autre.
  Les prompts sont écrits pour que chaque élève puisse avancer seul 15-20 minutes.
- Le **carnet de bord** et le **lexique** imprimés (`fiches/`), un par élève.
- Un tableau blanc, un échiquier physique, 2 dés et une feuille pour le « match aux dés » du mercredi.

## Pourquoi VS Code + Claude plutôt que tout dans Claude Desktop ?

| | VS Code + Claude Code | Claude Desktop seul |
|---|---|---|
| Voir les fichiers se créer, lire le code | ✅ | partiel |
| Lancer l'appli en local et tester dans le navigateur | ✅ | ❌ |
| Git : commits, branches, fusion, retour arrière | ✅ | ❌ |
| Déployer avec `fastapi deploy` | ✅ (terminal) | ❌ |
| Réfléchir, rédiger, schématiser | possible | ✅ idéal |

→ **Claude Desktop** pour les ateliers « conseil » et « architecture », **VS Code** pour développer et déployer.
