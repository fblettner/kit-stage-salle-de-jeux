# Jour 2 (matin) — L'architecture et le socle commun · les deux élèves ensemble

> **Objectif :** comprendre comment un site est organisé, et créer ensemble le « socle » sur lequel chacun construira son jeu.
> **L'après-midi**, chaque élève passe aux prompts de son jeu : `prompts/<jeu>/etape-2-….md`.

---

## Atelier 1 — Le schéma au tableau (30 min, sans ordinateur)

Dessine avec eux, en partant de leur vécu (« quand vous allez sur YouTube, il se passe quoi ? ») :

```text
 [ Navigateur ]  ── question ──▶  [ Serveur ]
   le FRONT      ◀── réponse ───    le BACK
   React             (API)         Python
  ce qu'on voit                 ce qui calcule
                                  ├── IA du jeu de l'élève A
                                  └── IA du jeu de l'élève B
```

Analogie du **restaurant** : la salle (front) où le client est servi, la cuisine (back) où l'on prépare,
et le serveur qui fait passer les commandes selon un menu précis (l'API).

### La casquette architecte : comment travailler à deux sans se gêner ?

Pose-leur la question avant de donner la réponse. Puis dessine :

```text
salle-de-jeux/
├── commun : le menu, les couleurs, le serveur   ← on le fait ENSEMBLE ce matin
├── <jeu A>/  ← le dossier de l'élève A   (ex. flechettes/)
└── <jeu B>/  ← le dossier de l'élève B   (ex. penalty/)
```

💡 **Message clé :** en entreprise, plusieurs développeurs travaillent sur le même logiciel.
On découpe en « modules » et on se met d'accord sur ce qui est commun **avant** de se séparer.

### Prompt optionnel dans Claude Desktop, pour illustrer

```
Explique à deux élèves de 3e, avec l'exemple d'un restaurant, ce que sont
le « front », le « back » et une « API » dans un site web.
Puis explique pourquoi, quand deux développeurs travaillent sur le même site,
on découpe le code en modules séparés.
```

---

## Atelier 2 — Découverte des outils (30 min)

Montre rapidement : VS Code (les fichiers à gauche), le terminal, Git (« une machine à remonter le temps »),
et le panneau Claude dans VS Code.

**Avant de commencer :** crée un dossier vide `salle-de-jeux`, ouvre-le dans VS Code, `git init`,
et copie dedans le fichier **`CLAUDE.md` du kit**. Complétez ensemble la ligne « Les jeux de NOTRE projet »
avec les choix d'hier. Explique : « c'est la fiche de consignes qu'on donne à Claude, comme on briefe
un nouveau collègue ». Lisez-la ensemble.

---

## Atelier 3 — Créer le socle (un seul poste, les deux élèves)

### Prompt 1 — à coller dans Claude (VS Code)

Remplacer les **[crochets]** par les jeux choisis. Noms de dossier possibles : `echecs`, `coach`, `penalty`, `flechettes`
(ou `flechettes_lea` et `flechettes_tom` si les deux élèves font chacun leur version du même jeu).

```
Lis le fichier CLAUDE.md pour comprendre notre projet.

On travaille tous les deux sur le socle COMMUN de la salle de jeux, avec deux jeux :
[JEU A, dossier xxx] et [JEU B, dossier yyy]. On veut :

Côté serveur (dossier backend) :
- un serveur Python FastAPI avec une route GET /api/sante qui répond un petit message en français
- un dossier par jeu dans app/ ([xxx] et [yyy]), chacun avec un fichier routes.py
  contenant un APIRouter (préfixe /api/[xxx] et /api/[yyy]) et une route GET /statut
  qui répond « en construction 🚧 »
- main.py branche ces deux routeurs
- un pyproject.toml avec [tool.fastapi] entrypoint = "app.main:app"

Côté site (dossier frontend, créé avec Vite + React) :
- un menu d'accueil « 🎮 La salle de jeux » avec une grande tuile cliquable par jeu (une icône, un titre, une phrase)
- cliquer sur une tuile affiche le jeu, avec un bouton « ← Menu » pour revenir
- chaque jeu est un composant dans son dossier (src/[xxx]/ et src/[yyy]/),
  qui pour l'instant affiche juste le message de sa route /statut
- la liste des jeux est un simple tableau dans App.jsx : ajouter un jeu = ajouter une ligne
- les styles communs (couleurs, boutons, « cartes ») dans index.css
- Vite redirige les appels /api vers le serveur Python sur le port 8000

Explique-nous chaque fichier créé en une phrase, puis dis-nous comment lancer les deux parties.
```

### Ce qu'on vérifie

- Terminal 1 : `cd backend` → créer l'environnement virtuel → `fastapi dev`. Ouvrir **http://127.0.0.1:8000/docs** :
  les élèves testent l'API en cliquant sur « Try it out ». Moment très parlant.
- Terminal 2 : `cd frontend` → `npm install` → `npm run dev` → ouvrir **http://localhost:5173**.
- Le menu s'affiche, chaque tuile mène à « en construction », le bouton Menu ramène à l'accueil.
- **Commit** (« Socle commun : menu et un dossier par jeu »).

💡 **Expérience à faire :** arrêter le serveur Python et recharger la page. Que se passe-t-il ? Pourquoi ?

### Si ça coince

Bloqué plus de 20 minutes : comparer avec le socle de la solution de référence (dossier `solution/salle-de-jeux`), fichier par fichier, avec Claude.

---

## Atelier 4 — Chacun son poste

Voir `guides/travailler-a-deux-avec-git.md`. En résumé :

1. Tu pousses le socle sur un dépôt distant (GitHub/GitLab privé).
2. Sur le 2e poste, on clone le dépôt.
3. Chaque élève crée **sa branche**, du nom de son jeu : par exemple `git switch -c flechettes`.
4. Dans Claude, chaque élève commence par : **« Je travaille sur [son jeu] »** (ex. « sur les fléchettes »).
   Le `CLAUDE.md` demande alors à Claude de ne toucher qu'aux fichiers de ce jeu.

L'après-midi, chacun suit les prompts de son jeu : `prompts/<jeu>/etape-2-….md`.
