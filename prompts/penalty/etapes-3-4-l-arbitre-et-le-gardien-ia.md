# Penalty Pro · Étapes 3 et 4 (mercredi) — Le serveur arbitre, puis le gardien apprend

> Entre les deux : l'atelier débranché commun (`J3-ateliers-debranches.md`), avec le pierre-feuille-ciseaux.

---

## Matin — Le serveur est l'arbitre (étape 3)

**Question pour lancer la séance :** « Dans un jeu en ligne, si c'est le navigateur qui décide s'il y a but,
qu'est-ce qui empêche un petit malin de tricher ? » → c'est le **serveur** qui doit arbitrer.

### Prompt P3a — la physique du tir

```
Je travaille sur Penalty Pro. On veut que ce soit le serveur Python qui décide de tout.

Crée backend/app/penalty/physique.py :
- trajectoire(cible, puissance, rng) : le ballon n'arrive jamais exactement sur la cible. On ajoute une erreur
  au hasard (loi normale) qui grandit avec la puissance : écart = 0,015 + 0,06 × puissance².
  L'erreur verticale est 1,5 fois plus grande. Si la puissance dépasse 0,8, le ballon monte un peu
  (y diminue de (puissance − 0,8) × 0,7). Le ballon ne peut pas passer sous le sol.
- distance(a, b) entre deux points du but, en tenant compte du fait que le but est 3 fois plus large que haut
- portee_gardien(puissance) = 0,22 + 0,33 × (1 − puissance)
- arbitrer(impact, plongeon, puissance) → « dehors » (bien à côté), « poteau » (à moins de 0,03 du cadre),
  « arret » (assez près du gardien) ou « but »

Dans routes.py : POST /api/penalty/tir reçoit la cible (x et y entre 0 et 1, sinon refus) et la puissance (entre 0 et 1).
Pour l'instant, le gardien plonge au hasard au centre d'une des 6 zones. Renvoie l'impact du ballon,
l'endroit du plongeon et le résultat.
Explique-nous ce qu'est une « loi normale » avec un exemple de la vie courante.
```

### Prompt P3b — les tests et le site

```
Ajoute des tests avec pytest dans backend/tests/test_penalty.py :
- un tir fort est en moyenne au moins 3 fois moins précis qu'un tir doux
- un tir à pleine puissance en lucarne passe souvent au-dessus (plus de 40 % du temps)
- un gardien bien placé arrête presque tous les tirs lents, mais beaucoup moins les tirs forts
- quelques cas simples pour l'arbitre (en plein sur le gardien = arrêt, très au-dessus = dehors…)
- l'API refuse une cible en dehors du but

Puis côté site : au deuxième clic, on envoie la cible et la puissance au serveur, et on anime le ballon
jusqu'à l'impact renvoyé (qui peut être au-dessus de la barre ou sur le poteau). Ajoute le message « 💥 Sur le poteau ! ».
```

### Ce qu'on vérifie

- Dans **http://127.0.0.1:8000/docs**, envoyer la même cible 5 fois : l'impact change (le hasard).
- Lancer les tests. **Commit.**

---

## Après-midi — Le gardien apprend (étape 4)

Après le pierre-feuille-ciseaux du matin, l'élève a compris l'idée : **observer, compter, prédire.**

### Prompt P4a — le cerveau du gardien

```
Je travaille sur Penalty Pro. On veut que le gardien APPRENNE où le joueur tire.

Crée backend/app/penalty/ia.py :
1. zone_de(point) : dans quelle des 6 zones est ce point (haut/bas × gauche/centre/droite)
2. predire(historique, niveau) : la probabilité de chaque zone pour le prochain tir, et une phrase d'explication.
   - Facile : 1 chance sur 6 partout
   - Moyen : on compte les tirs précédents par zone (en partant de 1 pour chaque zone)
     → « Tu as choisi en haut à gauche 3 fois sur 5. »
   - Difficile : on regarde aussi ce que le joueur a fait APRÈS son dernier choix, les autres fois ;
     ces enchaînements comptent 3 fois plus → « Après en bas à gauche, tu as choisi en haut à droite 2 fois sur 2. »
3. choisir_plongeon(historique_tirs, niveau, rng) : au hasard en Facile ; sinon la zone la plus probable
   (au hasard parmi les quasi ex aequo), et le gardien plonge vers l'endroit PRÉCIS où le joueur vise
   d'habitude dans cette zone (la moyenne de ses tirs précédents dans la zone).
   Important : cette fonction ne reçoit PAS le tir en cours. Le gardien ne peut pas tricher.

La route /api/penalty/tir reçoit maintenant l'historique des cibles précédentes et le niveau.
Le gardien décide AVANT que le serveur regarde le tir. Renvoie aussi la prédiction et l'explication.
Commentaires en français, comme si on devait le présenter à notre classe.
```

### Prompt P4b — les tests

```
Ajoute des tests :
- au niveau Moyen, si j'ai tiré 3 fois en haut à gauche, le gardien plonge en haut à gauche, à l'endroit où je vise
- au niveau Difficile, si j'alterne bas-gauche / haut-droite et que je viens de tirer en bas à gauche,
  le gardien plonge en haut à droite (alors que le niveau Moyen se trompe)
- les probabilités font toujours 100 %
- la fonction du gardien ne reçoit même pas le tir en cours (on vérifie la liste de ses paramètres avec inspect)
```

### Prompt P4c — côté site

```
Ajoute le choix du niveau du gardien, et une carte « Dans la tête du gardien » : un petit but avec les 6 zones
colorées en orange plus ou moins fort selon la probabilité (avec le % écrit dedans) et son explication
(composant PenseeIA.jsx).
```

### Ce qu'on vérifie

- **Le duel :** l'autre élève tire 10 fois en Moyen, puis 10 fois en Difficile. Combien de buts ?
- **Piéger l'IA :** une fois qu'on a compris comment le gardien pense, peut-on le battre ?
- **Commit.**

### Si ça coince

- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
