# Kit stage de 3e — « La salle de jeux : un jeu, une IA, de l'idée à la mise en ligne »

Kit pour accueillir deux collégiens de 3e pendant une semaine et leur faire vivre le cycle complet
d'un projet logiciel, avec les trois casquettes du métier : **conseil**, **architecte**, **développeur**.

Le projet : une **salle de jeux en ligne** avec un menu et des jeux contre l'ordinateur.
Chaque élève **choisit son projet** dans un catalogue de 4 jeux, chacun avec une IA différente.
Ils peuvent choisir deux jeux différents… ou le même.

| | ♞ Échecs | ⚽ Coach | 🥅 Penalty Pro | 🎯 Fléchettes |
|---|---|---|---|---|
| Le jeu | partie contre l'ordinateur | entraîneur de foot : mercato, tactique, match en direct | tirs au but : viser, doser sa puissance, puis garder | partie de 301, la main qui tremble |
| L'IA… | **calcule** (minimax) | **simule** des matchs, **apprend** tes habitudes | **apprend** où tu tires | **simule** ses lancers, **mesure** ta précision |
| Difficulté | ★★☆ | ★★★ | ★★☆ | ★★★ |

Le détail de chaque projet, et les deux formules quand les élèves choisissent le même jeu : `01-CATALOGUE-DES-PROJETS.md`.

## Contenu

```
00-LISEZ-MOI.md                     ← ce fichier : programme de la semaine et mode d'emploi
01-CATALOGUE-DES-PROJETS.md         ← à présenter aux élèves le lundi pour qu'ils choisissent
CLAUDE.md                           ← à copier à la racine du projet (consignes pour Claude), à compléter avec les jeux choisis
prompts/
  J1-le-besoin.md                   ← ensemble : interview client, choix des projets, cahier des charges, maquettes
  J2-architecture-et-socle.md       ← ensemble : schéma, découpage en modules, création du socle
  J3-ateliers-debranches.md         ← ensemble : comment pense une IA (calculer, simuler, apprendre)
  echecs/  coach/  penalty/  flechettes/   ← le parcours de chaque jeu, du mardi après-midi au jeudi :
    etape-2-….md                    ←   mardi après-midi : l'écran du jeu
    etapes-3-4-….md                 ←   mercredi : le serveur, puis la vraie IA (+ tests)
    etape-5-….md                    ←   jeudi : finitions, « le client change d'avis », chasse aux bugs
  J5-mise-en-ligne-et-demo.md       ← ensemble : fusion, FastAPI Cloud, démo OCI, présentation
guides/
  preparation-du-poste.md           ← checklist avant leur arrivée (2 postes)
  travailler-a-deux-avec-git.md     ← une branche par élève, la fusion, les reprises, le cas « même jeu »
  deploiement-fastapi-cloud.md      ← pas à pas + pièges
  deploiement-oci.md                ← VM, Docker, Caddy/HTTPS + pièges OCI
  autonomie-des-eleves.md           ← ce que le compagnon affiche aux élèves pour qu'ils avancent seuls
autonomie/
  parcours-eleves.md                ← les moments « ensemble », expliqués AUX ÉLÈVES, pas à pas
  depannage.md                      ← « Je suis bloqué » : l'échelle du dépannage, les prompts de secours
fiches/
  carnet-de-bord.md                 ← à imprimer, un par élève
  lexique.md                        ← à imprimer, un par élève
solution/salle-de-jeux/             ← solution de référence testée, avec LES 4 JEUX
compagnon-de-stage/                 ← l'appli web du stage : ton tableau de bord + un parcours guidé par élève
lancer.sh                           ← ./lancer.sh : démarre le compagnon, avec les 4 jeux d'exemple dans son menu (« La salle de jeux »)
deployer.sh                         ← ./deployer.sh : met le compagnon en ligne sur un serveur (Docker), puis --maj pour le mettre à jour
```

> 🧭 **Le compagnon de stage** (`compagnon-de-stage/README.md`) met tout ce kit en ligne : ton écran animateur
> (programme heure par heure, fiches complètes, demandes d'aide, carnets) et un écran par élève (sa journée, ses prompts
> prêts à copier et adaptés à SON jeu, ses cases à cocher, son carnet de bord, la chasse aux bugs, le bouton 🆘).
> Les fichiers .md restent la source : si tu modifies un prompt ici, l'appli l'affiche après un redéploiement.
>
> 🟣 **Des élèves autonomes.** Chaque activité affiche aux élèves un pas-à-pas écrit pour eux, y compris les ateliers
> que tu animes, et la page « Je suis bloqué » les aide à se dépanner seuls. Voir `guides/autonomie-des-eleves.md`.

## Les outils : qui fait quoi

- **Claude Desktop** : les ateliers de réflexion (cahier des charges, architecture, préparation de la démo).
- **VS Code + Claude**, **un poste par élève** : tout le développement et le déploiement.
- **Ton compte, tes sessions** : Claude.ai est réservé aux 18 ans et plus. Les élèves dictent et décident ;
  le clavier peut passer de main en main, mais les sessions restent les tiennes.

## Le principe pédagogique

1. **Ensemble pour les décisions, séparés pour la réalisation.** Besoin, architecture, IA débranchée, mise en ligne : à deux.
   Développement : chacun son jeu, sa branche Git, son dossier.
2. **Chacun est responsable de son jeu et client-testeur du jeu de l'autre.**
3. **Chaque prompt est suivi d'un test.** On ne fait pas confiance au code, même écrit par une IA : on vérifie.
4. **Un commit à chaque étape qui marche.** Si une séance déraille : on ramène le dossier de son jeu à l'étape de la solution.
5. **Les prompts du kit sont un filet de sécurité.** À partir du mercredi, encourage les élèves à écrire leurs propres prompts.
6. **Le même rythme pour tous les jeux** : quel que soit le choix, l'étape 2 est le mardi après-midi, les étapes 3 et 4
   le mercredi, l'étape 5 le jeudi. Les moments communs restent synchronisés.

## Programme de la semaine

Horaires indicatifs (9h-12h / 13h30-16h30), à adapter. 👥 = les deux élèves ensemble, 🅰 🅱 = chacun sur son poste, dans le parcours de son jeu.

### Lundi — Le besoin et le choix · casquette conseil
| Horaire | | Atelier | Outil |
|---|---|---|---|
| 9h00 | 👥 | Accueil, visite, présentation de ton métier (dev / architecte / conseil) et d'un projet réel | — |
| 10h30 | 👥 | Installation aux postes | — |
| 13h30 | 👥 | **Interview du client** (tu joues le directeur de la Maison des jeunes) | papier |
| 14h15 | 👥 | **Le catalogue** : jouer aux 4 jeux de la solution, **chacun choisit son projet** | solution, catalogue |
| 15h00 | 👥 | **Cahier des charges** | Claude Desktop |
| 15h45 | 👥 | **Maquettes papier** : le menu + l'écran de chaque jeu | papier |

### Mardi — L'architecture et les premiers écrans · casquettes architecte et développeur
| Horaire | | Atelier | Prompts |
|---|---|---|---|
| 9h00 | 👥 | Schéma front / back / API · **découper en modules** pour travailler à deux | J2 |
| 9h45 | 👥 | VS Code, terminal, Git ; compléter et lire le `CLAUDE.md` | J2 |
| 10h30 | 👥 | **Le socle commun** : le menu, un dossier par jeu | J2 · prompt 1 |
| 11h30 | 👥 | Mise en place des 2 postes et des 2 branches | guide Git |
| 13h30 | 🅰 🅱 | **Étape 2 : l'écran du jeu** (échiquier · mercato · but et jauge · cible) | `<jeu>/etape-2` |
| 15h30 | 👥 | Chacun présente son écran à l'autre ; carnet de bord | — |

### Mercredi — L'intelligence artificielle démystifiée
| Horaire | | Atelier | Prompts |
|---|---|---|---|
| 9h00 | 🅰 🅱 | **Étape 3 : le serveur** (le serveur répond ou arbitre ; l'IA joue encore au hasard) | `<jeu>/etapes-3-4` |
| 10h15 | 👥 | **Ateliers débranchés** : calculer, simuler, apprendre | J3 |
| 13h30 | 🅰 🅱 | **Étape 4 : la vraie IA**, 3 niveaux, tests automatiques | `<jeu>/etapes-3-4` |
| 15h45 | 👥 | **Le duel** : chacun affronte l'IA de l'autre jeu | — |

### Jeudi — Finitions et changements · le réel du métier
| Horaire | | Atelier | Prompts |
|---|---|---|---|
| 9h00 | 👥 | Revue avec les maquettes ; chacun liste et priorise ses tâches | — |
| 9h30 | 🅰 🅱 | Finitions | `<jeu>/etape-5` |
| 11h00 | 🅰 🅱 | 🎭 **Le client change d'avis** (une demande différente pour chaque jeu, voir le catalogue) | `<jeu>/etape-5` |
| 13h30 | 👥 | **Chasse aux bugs croisée** : chacun teste le jeu de l'autre | `<jeu>/etape-5` |
| 15h30 | 👥 | Tournoi · **fusion des deux branches** (si le temps le permet) | guide Git |

### Vendredi — Fusion, mise en ligne et démo
| Horaire | | Atelier | Prompts |
|---|---|---|---|
| 9h00 | 👥 | Fusion (si pas faite jeudi) · build de production · test en local | J5 · prompt 11 |
| 9h45 | 👥 | **Mise en ligne FastAPI Cloud**, test sur leurs téléphones | J5 |
| 10h30 | 👥 | **Démo OCI** (toi) : VM, SSH, Docker, Caddy, nom de domaine ; comparaison | J5 |
| 13h30 | 👥 | Préparation de la présentation à deux voix | J5 |
| 14h30 | 👥 | **Démo devant tes collègues** | — |
| 15h30 | 👥 | Carnet de bord, début du rapport de stage | — |

## Avant le stage

Voir `guides/preparation-du-poste.md`. Le plus important : **jouer aux 4 jeux de la solution** (pour les présenter lundi),
puis, dès que les élèves ont choisi (ou si tu peux le deviner), **dérouler toi-même le parcours de leurs jeux**
(2 à 3 h par jeu) et faire un déploiement d'essai.
Si tu utilises le compagnon de stage : le déployer, créer les deux comptes, imprimer les fiches d'accès
et faire la répétition générale avec « Forcer le jour » (voir `compagnon-de-stage/README.md`).
Renseigne aussi dans les Réglages l'adresse du dépôt Git (`guides/autonomie-des-eleves.md`).

## La solution de référence

Dossier `solution/salle-de-jeux` : le projet complet, avec **les 4 jeux** (React + Vite, FastAPI ;
échecs avec python-chess et minimax ; Coach avec un moteur de match et un entraîneur Monte-Carlo ;
Penalty Pro avec une physique simple et un gardien qui apprend ; fléchettes avec une cible officielle,
une IA qui simule ses lancers et un conseiller ; Dockerfile ; FastAPI Cloud et OCI).

Vérifications faites : le code compile et passe le contrôle de code ; 47 tests backend
(échecs 7, Coach 16, Penalty Pro 13, Fléchettes 11, dont des tests statistiques vérifiés sur plusieurs tirages) ;
un test d'interface par jeu (une partie complète, et la vérification que l'IA ne reçoit jamais le choix en cours) ;
chaque jeu joué dans un vrai navigateur, sur ordinateur et téléphone ; build de production servi par FastAPI.

Pour y jouer tout de suite : `./lancer.sh`, puis l'entrée « La salle de jeux » du menu du compagnon. Le `README.md` de la solution explique
comment la lancer à la main, et comment n'y garder que les jeux choisis.
