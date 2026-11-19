# Penalty Pro · Étape 2 (mardi après-midi) — Viser et tirer

> Toujours commencer la séance Claude par : **« Je travaille sur Penalty Pro. »**
> Ressortir la maquette papier du lundi : c'est elle qui guide l'écran.

---

### Prompt P2a — le but et le viseur

```
Je travaille sur Penalty Pro (dossier frontend/src/penalty).

On veut dessiner le jeu dans PenaltyPro.jsx, avec le dessin du but dans un composant Cage.jsx :
- un but vu de face (poteaux blancs, filet), 3 fois plus large que haut, posé sur une pelouse rayée,
  avec le point de penalty dessous
- un petit gardien dessiné simplement en SVG (tête, maillot bleu, bras levés, gants blancs), debout au milieu
- un ballon (l'émoji ⚽) sur le point de penalty
- quand la souris passe sur le but, un viseur jaune (un rond avec une croix) suit la souris
- on repère une position dans le but par x (0 = poteau gauche, 1 = poteau droit)
  et y (0 = la barre, 1 = le sol)
- un clic dans le but choisit la cible : le viseur reste à cet endroit

Styles dans penalty.css, avec des classes qui commencent par penalty-.
Pour l'instant tout se passe dans le navigateur : on ne touche pas au serveur Python.
Explique-nous comment on transforme la position de la souris en x et y entre 0 et 1.
```

### Prompt P2b — la jauge de puissance et le tir

```
Après avoir choisi la cible, une jauge de puissance apparaît sous le but : un curseur fait des allers-retours
de 0 à 1 (environ 1,3 seconde pour un aller-retour), sur une barre qui va du vert (précis) au rouge (puissant).
Un deuxième clic arrête la jauge et tire. Anime la jauge avec requestAnimationFrame.

Pour l'instant, calcule le résultat dans le navigateur :
- le gardien plonge au hasard au centre d'une des 6 zones du but (3 colonnes × 2 lignes)
- si la puissance dépasse 0,85 et qu'on vise le haut du but, le ballon passe au-dessus
- sinon, le gardien arrête le ballon s'il est assez près : on calcule la distance entre la cible et l'endroit
  où il plonge (en multipliant l'écart horizontal par 3, car le but est 3 fois plus large que haut),
  et sa « portée » vaut 0,22 + 0,33 × (1 − puissance) : plus le tir est fort, moins il va loin
- le ballon s'envole vers la cible et le gardien plonge (animations CSS), puis un message :
  « BUUUT ! ⚽ », « Arrêté par le gardien 🧤 » ou « Au-dessus de la barre ! 😬 »
- un compteur « Buts : 3 / 5 »
```

### Ce qu'on vérifie

- Tirer 10 fois au milieu, puis 10 fois dans les coins. Puis fort, puis doucement. Qu'est-ce qui marche le mieux ?
  **Il n'y a pas une seule bonne réponse** : c'est un choix entre puissance et précision, comme un vrai tireur.
- Tester sur une fenêtre étroite (téléphone) : le viseur suit-il le doigt ?
- **Commit** (« Penalty Pro : viser et tirer »).

### Si ça coince

- La jauge est saccadée ou continue de tourner après le tir : « Explique-nous comment on arrête requestAnimationFrame. »
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.

### Bonus si en avance

```
On aimerait que le maillot du gardien soit aux couleurs de [club préféré de l'élève].
```
