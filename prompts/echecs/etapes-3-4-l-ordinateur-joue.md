# Échecs · Étapes 3 et 4 (mercredi) — L'ordinateur joue, puis réfléchit

> Entre les deux : l'atelier débranché commun (`J3-ateliers-debranches.md`).

---

## Matin — Un ordinateur qui joue au hasard (étape 3)

### Prompt E3

```
Je travaille sur le jeu d'échecs. Nous voulons jouer contre l'ordinateur, nous jouons les Blancs.

Côté serveur (backend/app/echecs/routes.py) :
- ajoute une route POST /api/echecs/coup-ia qui reçoit la position de la partie au format FEN
- utilise la librairie python-chess pour lister les coups autorisés
- pour l'instant, l'ordinateur choisit un coup AU HASARD et le renvoie au format UCI (ex. "e7e5")
- si la position est invalide ou la partie terminée, renvoie une erreur 400 avec un message en français

Côté React (JeuEchecs.jsx) :
- après chaque coup du joueur, envoie la position au serveur et joue le coup reçu
- affiche « L'ordinateur réfléchit… » pendant l'attente
- on ne doit pas pouvoir jouer pendant que l'ordinateur réfléchit

Explique-nous ce qu'est le format FEN avec la position de départ en exemple.
```

### Ce qu'on vérifie

- Dans **http://127.0.0.1:8000/docs**, envoyer une FEN à la main et voir le coup proposé.
- Jouer une partie : l'ordinateur est nul. **Question :** « comment toi, tu choisis un coup ? »
  → noter les réponses (prendre des pièces, protéger son roi…). On les réutilise cet après-midi.
- **Commit.**

---

## Après-midi — Coder minimax (étape 4)

### Prompt E4a — le cerveau

```
Je travaille sur le jeu d'échecs. On a compris le principe de minimax.
On veut remplacer le coup au hasard par une vraie IA.

Crée un fichier backend/app/echecs/moteur.py avec :
1. une fonction evaluer(plateau) qui donne une note à la position du point de vue des Blancs :
   valeur des pièces (pion 100, cavalier 320, fou 330, tour 500, dame 900)
   + un petit bonus pour les pièces au centre de l'échiquier.
   Un échec et mat vaut une note énorme.
2. une fonction minimax avec élagage alpha-bêta
3. une fonction choisir_coup(plateau, niveau) avec 3 niveaux :
   Facile = profondeur 1 avec 30 % de coups au hasard, Moyen = profondeur 2, Difficile = profondeur 3.
   Elle renvoie aussi le nombre de positions examinées.

Écris des commentaires en français qui expliquent l'idée, comme si on devait la présenter à notre classe.
Modifie la route /api/echecs/coup-ia pour qu'elle reçoive aussi le niveau
et renvoie le nombre de positions examinées.
```

### Prompt E4b — les tests

```
Ajoute des tests automatiques avec pytest dans backend/tests/test_echecs.py pour vérifier que :
- le coup choisi est toujours autorisé
- l'ordinateur prend une dame qu'on lui offre gratuitement
- l'ordinateur trouve un échec et mat en un coup quand il y en a un
- le niveau difficile répond en moins de 5 secondes
Puis lance les tests et explique-nous le résultat.
```

💡 **Message clé :** « Un test, c'est un contrôle automatique qu'on relance à chaque modification.
On ne fait pas confiance au code, même écrit par une IA : on vérifie. »

### Prompt E4c — côté React

```
Ajoute un menu pour choisir le niveau (Facile, Moyen, Difficile) et envoie-le au serveur.
Sous l'échiquier, affiche « L'ordinateur a examiné X positions ».
```

### Ce qu'on vérifie

- Comparer le nombre de positions examinées entre Facile, Moyen et Difficile. **Faire le lien avec l'arbre du matin.**
- Faire jouer l'autre élève (le « client-testeur ») en Moyen. Qui gagne ?
- **Commit.**

### Si ça coince

- Trop lent : « Le niveau difficile est trop lent. Examine les captures en premier pour que l'élagage soit plus efficace. »
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
