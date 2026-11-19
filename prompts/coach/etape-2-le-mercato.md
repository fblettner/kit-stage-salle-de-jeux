# Coach · Étape 2 (mardi après-midi) — Le mercato

> Toujours commencer la séance Claude par : **« Je travaille sur le jeu Coach. »**
> Ressortir la maquette papier du lundi : c'est elle qui guide l'écran.

---

## Avant de coder (15 min, sans ordinateur) : inventer les joueurs

Sur une feuille, l'élève invente quelques joueurs (noms **inventés**, pas de vrais joueurs) et leur donne
4 notes sur 100 : **attaque, défense, technique, vitesse**. Pour un gardien, la « défense » représente les arrêts.

Questions à lui poser :
- « Combien doit coûter un attaquant noté 90 ? Et un défenseur noté 60 ? »
- « Si le meilleur joueur coûte presque rien, que se passe-t-il ? » → tout le monde le prend, le jeu est cassé.
  C'est l'**équilibrage**, un vrai métier dans le jeu vidéo.

---

### Prompt F2a — les données (côté serveur)

```
Je travaille sur le jeu Coach (dossiers backend/app/coach et frontend/src/coach).
C'est un jeu d'entraîneur de foot à 5 : on recrute 1 gardien et 4 joueurs de champ avec un budget de 50 M€.

Crée backend/app/coach/joueurs.py avec :
- une vingtaine de joueurs INVENTÉS (4 gardiens, 6 défenseurs, 5 milieux, 6 attaquants),
  chacun avec un id, un nom, un poste (G, DEF, MIL, ATT) et 4 notes sur 100 :
  attaque, defense (pour un gardien : ses arrêts), technique, vitesse.
  Voici quelques joueurs que j'ai inventés : [COLLER LES JOUEURS DE LA FEUILLE]
- une note globale calculée selon le poste (un attaquant est surtout jugé sur l'attaque, un défenseur sur la défense…)
- un prix calculé à partir de la note globale : un joueur noté 85 doit coûter environ 25 M€,
  un joueur noté 60 environ 4 M€ (minimum 3 M€)

Dans backend/app/coach/routes.py, ajoute une route GET /api/coach/joueurs qui renvoie
le budget, la taille de l'équipe et la liste des joueurs.
Explique-nous comment tu as calculé la note globale et le prix.
```

### Ce qu'on vérifie

- Ouvrir **http://127.0.0.1:8000/docs** et appeler `/api/coach/joueurs` : la liste s'affiche en JSON.
  « C'est ça, des **données** : ce que le serveur sait et envoie au navigateur. »
- Les prix sont-ils logiques ? Peut-on se payer un « dream team » ? (il ne faut pas !)

---

### Prompt F2b — l'écran du mercato

```
Côté site (frontend/src/coach), on veut l'écran du mercato dans Coach.jsx :
- au démarrage, on récupère les joueurs avec GET /api/coach/joueurs
- chaque joueur est affiché comme une carte façon album de vignettes (composant CarteJoueur.jsx) :
  note globale en gros, poste, initiales dans un rond, nom, les 4 notes, le prix.
  Fond doré si la note est de 80 ou plus, argenté à partir de 70, bronze sinon.
- des boutons pour filtrer par poste (Tous, Gardiens, Défenseurs, Milieux, Attaquants)
- cliquer sur une carte recrute le joueur (une coche verte), recliquer le retire
- on ne peut pas recruter : un 2e gardien, plus de 5 joueurs, un joueur trop cher pour le budget restant,
  ni 4 joueurs de champ sans gardien. Les cartes impossibles sont grisées, avec la raison au survol.
  Mets ces règles dans un fichier equipe.js.
- à droite : le nom du club (modifiable), le budget dépensé avec une barre,
  les petites cartes de l'équipe, et les forces de l'équipe en jauges
  (moyennes d'attaque, défense, technique, vitesse des joueurs de champ + note du gardien)
- un bouton « Valider l'équipe » actif seulement quand l'équipe est complète et dans le budget
- styles dans coach.css, avec des classes qui commencent par coach-
```

### Ce qu'on vérifie

- Essayer de tricher : 2 gardiens, 6 joueurs, dépasser le budget… Tout doit être refusé avec une explication.
- Faire tester l'autre élève : « Quelle équipe tu ferais avec 50 M€ ? » Comparer les choix : **il n'y a pas une seule bonne réponse**,
  c'est ce qui rend le jeu intéressant.
- **Commit** (« Coach : le mercato »).

### Si ça coince

- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.

### Bonus si en avance

```
Ajoute 3 joueurs que j'ai inventés : [noms et notes]. Vérifie que leur prix est cohérent avec les autres.
```
