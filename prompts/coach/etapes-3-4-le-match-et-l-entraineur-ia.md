# Coach · Étapes 3 et 4 (mercredi) — Le match, puis l'entraîneur IA

> Entre les deux : l'atelier débranché commun (`J3-ateliers-debranches.md`), avec le « match aux dés ».

---

## Matin — Le moteur de match (étape 3)

### Prompt F3a — simuler un match avec des probabilités

```
Je travaille sur le jeu Coach. On veut que le serveur simule un match, minute par minute.

Crée backend/app/coach/simulateur.py :
- 5 tactiques, avec un nom, un emoji, une phrase d'explication et des bonus/malus (en points sur 100) :
  Défensive (attaque -10, défense +14, possession -6), Équilibrée (rien),
  Offensive (attaque +12, défense -12, possession +4),
  Pressing (attaque +6, défense +4, possession +12, mais -14 partout après la 60e minute : c'est fatigant),
  Contre-attaque (attaque -4, défense +6, possession -12, mais permet des contre-attaques).
- les forces d'une équipe : moyennes de ses joueurs de champ (attaque, défense, technique, vitesse) + la note du gardien
- une fonction simuler(equipe_a, tactique_a, equipe_b, tactique_b, minute_debut=1, minute_fin=90, score=(0, 0)) ;
  à chaque minute :
  1. on tire au sort qui a le ballon : l'équipe la plus technique l'a plus souvent (entre 20 % et 80 %)
  2. l'équipe qui a le ballon peut se créer une occasion (environ 7 % de chances, plus si son attaque
     dépasse la défense adverse)
  3. sur une occasion, un joueur tire (les meilleurs attaquants plus souvent) ; il marque environ
     une fois sur trois, plus si son attaque dépasse la note du gardien. Sinon : arrêt, tir à côté ou poteau.
  4. si l'équipe qui n'a pas le ballon joue la contre-attaque, elle peut partir en contre
     (plus souvent si elle est rapide et si l'adversaire attaque beaucoup)
  Chaque événement a un commentaire en français : « ⚽ BUUUT de … ! (1-0) », « 🧤 Parade de … »…
  La fonction renvoie le score, la liste des événements et les statistiques (possession, tirs, tirs cadrés).
- on peut lui donner un générateur de hasard avec une « graine » pour que le même match se rejoue à l'identique (utile pour les tests)

Ajoute dans backend/app/coach/joueurs.py trois équipes de l'ordinateur, une par niveau, avec des joueurs
aux noms de robots ou d'informatique (FC Bugs pour Facile, Racing Pixel pour Moyen, FC Python pour Difficile).

Explique-nous pourquoi, avec du hasard, la meilleure équipe gagne quand même plus souvent.
```

### Prompt F3b — les routes et les tests

```
Dans routes.py, ajoute :
- GET /api/coach/tactiques et GET /api/coach/adversaires
- POST /api/coach/match : reçoit les identifiants des 5 joueurs, la tactique et le niveau.
  Le serveur VÉRIFIE l'équipe (5 joueurs, 1 gardien, budget respecté, pas de doublon) et renvoie une erreur 400
  claire sinon. Pour l'instant, l'ordinateur choisit sa tactique AU HASARD. Renvoie aussi cette tactique.

Puis ajoute des tests avec pytest dans backend/tests/test_coach.py :
- un match rejoué avec la même graine donne exactement le même résultat
- le score correspond au nombre de buts commentés
- sur 300 matchs simulés, une bonne équipe bat la plus faible équipe de l'ordinateur plus d'une fois sur deux
- les matchs entre deux équipes offensives ont plus de buts qu'entre deux équipes défensives
- l'API refuse une équipe trop chère, et une équipe avec 2 gardiens
Lance les tests et explique-nous le résultat.
```

💡 **Message clé sur la vérification côté serveur :** « Le navigateur est chez l'utilisateur : n'importe qui peut
le modifier. Le serveur doit donc tout revérifier lui-même. C'est une règle de base de la sécurité. »

### Prompt F3c — le match à l'écran

```
Côté site, après « Valider l'équipe » :
1. Un écran « vestiaire » : notre équipe face à celle de l'ordinateur (petites cartes), le choix du niveau,
   et les 5 tactiques sous forme de gros boutons avec leur explication. Un bouton « ⚽ Coup d'envoi ! ».
2. Un écran « match » : le serveur simule les 90 minutes d'un coup, puis on les AFFICHE petit à petit,
   comme un direct (environ 0,2 seconde par minute) : un tableau d'affichage (noms des clubs, score),
   une barre qui avance avec la minute, et les commentaires qui apparaissent au fur et à mesure
   (les plus récents en haut, les buts surlignés en vert pour nous et en rouge pour l'ordinateur).
   Ajoute un petit terrain vu de dessus où le ballon se déplace vers le but de l'équipe qui domine.
   Un bouton « ⏩ Accélérer ».
3. À la fin : Victoire / Match nul / Défaite, les statistiques, la tactique jouée par l'ordinateur,
   et des boutons « Revanche » et « Changer d'équipe ».
Mets l'affichage du match dans Match.jsx et le choix de tactique dans ChoixTactique.jsx.
```

### Ce qu'on vérifie

- Jouer 3 matchs avec la même équipe : les résultats changent, c'est le hasard. Mais est-ce que ça « ressemble » à du foot ?
  Les élèves deviennent **testeurs** : trop de buts ? pas assez ? On ajuste les chiffres ensemble.
- **Question :** « Ta tactique a-t-elle de l'importance ? Comment le prouver ? » → en jouant beaucoup de matchs…
  ce que l'IA va faire cet après-midi !
- **Commit.**

---

## Après-midi — L'entraîneur IA (étape 4)

Après le « match aux dés » du matin, l'élève a compris l'idée : **simuler beaucoup de fois, compter, choisir.**

### Prompt F4a — le cerveau de l'entraîneur

```
Je travaille sur le jeu Coach. On veut un vrai entraîneur adverse, dans backend/app/coach/ia.py.

Il ne connaît PAS la tactique que le joueur va choisir. Alors :
1. Il APPREND : une fonction predire_tactique(historique) donne la probabilité de chaque tactique du joueur
   d'après les tactiques qu'il a jouées aux matchs précédents (on compte, en partant de 1 pour chaque tactique).
2. Il SIMULE : une fonction choisir_tactique(...) essaie chacune de ses 5 tactiques, simule à chaque fois
   des dizaines de matchs contre l'équipe du joueur (en tirant au sort la tactique du joueur selon la prédiction),
   compte les victoires, nuls et défaites, et garde la tactique qui rapporte le plus de points en moyenne
   (3 pour une victoire, 1 pour un nul). C'est la méthode de Monte-Carlo.
3. Les niveaux : Facile = tactique au hasard, aucune simulation ;
   Moyen = suppose que le joueur joue sa tactique habituelle, 100 matchs simulés par tactique ;
   Difficile = tient compte de toutes ses habitudes, 300 matchs simulés par tactique.
4. Il renvoie sa tactique, un « rapport » (pour chaque tactique : % de victoires, nuls, défaites, points)
   et une phrase d'explication du type « Tu as joué Offensive 3 fois sur 4. J'ai simulé 1500 matchs.
   Ma meilleure réponse : Contre-attaque, qui gagne 48 % du temps. »

Ajoute une route POST /api/coach/entraineur qui reçoit l'équipe du joueur, l'historique de ses tactiques et le niveau,
mais SURTOUT PAS sa tactique pour ce match : si on essaie de la lui envoyer, le serveur doit refuser (extra="forbid").
La route /api/coach/match reçoit maintenant la tactique choisie par l'entraîneur.
Commentaires en français, comme si on devait le présenter à notre classe.
```

### Prompt F4b — les tests

```
Ajoute des tests dans backend/tests/test_coach.py pour vérifier que :
- si le joueur a joué 3 fois offensif, la prédiction dit « offensive »
- dans le rapport, victoires + nuls + défaites font 100 % (aux arrondis près), et la tactique choisie est
  bien celle qui rapporte le plus de points
- contre un joueur qui joue toujours offensif, la tactique choisie par l'entraîneur difficile gagne plus souvent
  que la moyenne des 5 tactiques
- la contre-attaque punit le jeu offensif
- l'API /entraineur refuse qu'on lui envoie la tactique du joueur
```

### Prompt F4c — côté site

```
Au coup d'envoi, on demande D'ABORD sa tactique à l'entraîneur IA (/entraineur), PUIS on lance le match (/match).
On garde en mémoire l'historique de nos tactiques d'un match à l'autre.
Dans le panneau de droite, ajoute une carte « Dans la tête de l'entraîneur adverse » (composant RapportIA.jsx) :
sa tactique choisie, une barre par tactique (rouge = victoire de l'IA, gris = nul, vert = défaite de l'IA)
et son explication. Dans le vestiaire, affiche les tactiques qu'il a déjà vues (leurs emojis).
```

### Ce qu'on vérifie

- **Le duel :** l'autre élève joue 3 matchs de suite avec la même tactique. Regarder le rapport évoluer :
  l'IA s'adapte ! Puis changer brusquement de tactique : on la prend à contre-pied.
- Comparer Moyen et Difficile : le nombre de matchs simulés, les choix.
- **Commit.**

### Si ça coince

- Trop lent : « Le niveau difficile met trop de temps. Combien de matchs simule-t-il ? Mesure le temps et propose une solution. »
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
