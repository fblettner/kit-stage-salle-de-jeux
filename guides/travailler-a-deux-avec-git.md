# Travailler à deux avec Git

Deux élèves, deux postes, un seul projet. L'organisation retenue est celle d'une vraie équipe,
en version simplifiée : **une branche par élève**, fusionnée à la fin.

```
main          ──●(socle)──────────────────────────────●(fusion)──●(déploiement)
                  \                                   /    /
<jeu A>            ●── étape 2 ── 3 ── 4 ── 5 ───────┘    /
                    \                                    /
<jeu B>              ●── étape 2 ── 3 ── 4 ── 5 ────────┘
```

Dans les exemples ci-dessous, l'élève A fait les **fléchettes** et l'élève B **Penalty Pro**. Remplace par vos jeux.

## Mardi midi — mise en place (≈ 15 min, par toi)

1. Sur ton poste, une fois le socle commité sur `main` :
   ```bash
   # créer un dépôt PRIVÉ vide sur GitHub/GitLab, puis :
   git remote add origin <URL_DU_DEPOT>
   git push -u origin main
   ```
2. Sur le 2e poste (VS Code + Claude connecté à ton compte) :
   ```bash
   git clone <URL_DU_DEPOT> salle-de-jeux
   ```
   puis installer les dépendances (voir le README : `.venv` + `pip install …`, `npm install`).
3. Chaque élève crée sa branche **sur son poste**, du nom de son jeu :
   ```bash
   git switch -c flechettes    # poste de l'élève A
   git switch -c penalty       # poste de l'élève B
   ```

## Pendant la semaine

- Chaque élève **committe** après chaque étape qui marche (Claude le propose).
- En fin de journée, il **pousse** sa branche : `git push -u origin flechettes`. C'est aussi une sauvegarde.
- Chaque poste fait tourner **sa propre copie** du serveur et du site : pas d'interférence.
- Les fichiers communs (`App.jsx`, `index.css`, `main.py`…) ne doivent pas bouger.
  Si un élève en a vraiment besoin, on en discute à trois : c'est une décision d'architecte !

## Jeudi soir (ou vendredi matin) — la fusion, devant les élèves

```bash
git switch main
git pull
git fetch origin
git merge origin/flechettes -m "Fusion des fléchettes"
git merge origin/penalty -m "Fusion de Penalty Pro"
git push
```

Comme chaque jeu est resté dans son dossier, la fusion se fait **sans conflit**.
Lancer ensuite `pytest` (tous les fichiers de tests) et tester les deux jeux depuis le menu.

> Variante plus « pro » : faire une **pull request** par branche sur GitHub/GitLab,
> et que chaque élève relise celle de l'autre avant de fusionner. Une belle illustration de la revue de code.

## Le cas « même jeu »

**Formule « deux agences concurrentes »** (chacun sa version) : au moment du socle (mardi matin), on crée deux dossiers
distincts, par exemple `flechettes_lea` et `flechettes_tom`, avec leurs préfixes d'API (`/api/flechettes_lea`)
et de CSS (`.flechettes_lea-`). Chaque élève remplace le nom dans ses prompts. Tout le reste est identique : une branche chacun,
une fusion sans conflit, et deux tuiles dans le menu.

**Formule « une équipe, deux métiers »** (un seul jeu, l'un au site, l'autre au serveur) : une seule branche du nom du jeu,
sur laquelle les deux élèves committent, en se partageant les fichiers : `frontend/src/<jeu>/` pour l'un,
`backend/app/<jeu>/` et `backend/tests/` pour l'autre. Ils font `git pull` avant de commencer et `git push` après chaque commit.
C'est l'occasion de vivre un petit conflit Git… et d'apprendre à le résoudre avec Claude.

## En cas de pépin sur un seul jeu

On peut ramener **un seul dossier** à l'un de ses commits précédents, sans toucher à l'autre jeu.
D'où l'intérêt d'un commit après chaque étape qui marche :

```bash
git log --oneline -- frontend/src/flechettes backend/app/flechettes     # la liste des commits du jeu, du plus récent au plus ancien
git checkout <numéro du commit> -- frontend/src/flechettes backend/app/flechettes backend/tests/test_flechettes.py
```

Si le jeu n'a jamais marché à cette étape, compare avec la solution de référence (`solution/salle-de-jeux`, même dossier) et fais corriger par Claude.

## Et si on n'a qu'un seul poste ?

C'est possible : les deux élèves travaillent sur la même branche `main`, en alternant
(un élève pilote pendant que l'autre teste le jeu de l'autre). Moins d'autonomie, mais plus simple.
