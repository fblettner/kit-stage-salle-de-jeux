# Catalogue des projets — à montrer aux élèves le lundi

Chaque élève choisit **un jeu** à construire pendant la semaine, contre une IA qu'il va programmer avec Claude.
Les deux élèves peuvent choisir **des jeux différents**… ou **le même** (voir en bas de page).
Tous les jeux finissent dans la même « salle de jeux » en ligne, avec un menu d'accueil.

Pour aider à choisir : faire jouer les élèves 5 minutes à chaque jeu de la **solution de référence**
(`solution/salle-de-jeux`, voir son README pour la lancer). Puis leur dire : « Vous allez construire le vôtre. »

---

## ♞ Échecs contre l'IA

**Ce que tu construis :** un échiquier où tu joues contre l'ordinateur, avec 3 niveaux, un mode débutant qui montre
les coups possibles, le choix de ta couleur et l'historique de la partie.

**Comment pense l'IA :** elle **calcule**. Elle imagine tous les coups possibles, puis les réponses, puis les réponses aux réponses…
et choisit le meilleur (l'algorithme **minimax**). Elle examine des milliers de positions par coup.

| | |
|---|---|
| Pour qui ? | ceux qui aiment la logique et la stratégie (pas besoin d'être fort aux échecs) |
| Ce qu'on apprend | algorithme, arbre de recherche, utiliser une librairie (on ne recode pas les règles) |
| Ce qui est spectaculaire | voir l'IA examiner 5 000 positions en une demi-seconde |
| Difficulté | ★★☆ |
| Le client change d'avis… | « les petits ne savent pas comment bougent les pièces » → le mode débutant |

---

## ⚽ Coach

**Ce que tu construis :** un jeu d'entraîneur de foot à 5. Tu recrutes tes joueurs (inventés) sur des cartes, avec un budget,
tu choisis ta tactique, et le match est simulé et commenté en direct, minute par minute. À la mi-temps, tu peux changer de tactique.

**Comment pense l'IA :** l'entraîneur adverse **simule** des centaines de matchs avec chacune de ses tactiques pour trouver
la meilleure contre ton équipe (méthode de **Monte-Carlo**), et il **apprend** tes habitudes d'un match à l'autre.

| | |
|---|---|
| Pour qui ? | les fans de foot, de FIFA Ultimate Team ou de Football Manager |
| Ce qu'on apprend | données, probabilités, simulation, **équilibrage** d'un jeu (un joueur trop fort et pas cher casse tout) |
| Ce qui est spectaculaire | « J'ai simulé 1 500 matchs. Ta tactique offensive ? Je joue la contre-attaque. » |
| Difficulté | ★★★ |
| Le client change d'avis… | « un vrai coach change de tactique à la mi-temps ! » |

---

## 🥅 Penalty Pro

**Ce que tu construis :** une séance de tirs au but. Tu vises à la souris où tu veux dans le but, puis tu arrêtes une jauge
de puissance au bon moment : plus c'est fort, plus c'est dur à arrêter… mais moins c'est précis (et ça peut passer au-dessus !).
Ensuite tu deviens gardien. 5 tirs chacun, puis mort subite.

**Comment pense l'IA :** le gardien **apprend** où tu tires : il compte tes tirs par zone, repère tes enchaînements
(« après un tir à gauche, il tire à droite ») et retient même l'endroit précis où tu vises d'habitude.

| | |
|---|---|
| Pour qui ? | les fans de foot qui veulent de l'action et de l'adresse |
| Ce qu'on apprend | animations, physique simple (trajectoire, hasard), probabilités, apprentissage à partir de données |
| Ce qui est spectaculaire | le panneau « Dans la tête du gardien » qui devine où tu vas tirer |
| Difficulté | ★★☆ |
| Le client change d'avis… | « les jeunes veulent aussi être gardien ! » |

---

## 🎯 Fléchettes

**Ce que tu construis :** une vraie cible, aux dimensions officielles, et une partie de 301 contre l'ordinateur.
Ta main tremble : le viseur bouge tout seul, il faut lancer au bon moment. Il faut arriver exactement à 0 (sinon « bust » !).

**Comment pense l'IA :** elle connaît sa propre précision et **simule** des milliers de lancers pour savoir où viser :
un champion vise le triple 20, mais un joueur imprécis a intérêt à viser ailleurs ! Une **carte de chaleur** montre
les meilleurs endroits. Et le conseiller **mesure ta précision** pour te dire où, toi, tu devrais viser.

| | |
|---|---|
| Pour qui ? | ceux qui aiment l'adresse, les maths « utiles » et les beaux dessins |
| Ce qu'on apprend | géométrie (angles, cercles), dessin SVG, simulation, décider sous incertitude |
| Ce qui est spectaculaire | la carte de chaleur, et le conseil personnalisé qui change selon le joueur |
| Difficulté | ★★★ |
| Le client change d'avis… | « les petits ratent tout, l'ordinateur pourrait les conseiller ! » |

---

## Et si les deux élèves choisissent le même jeu ?

C'est possible, et même intéressant. Deux formules au choix :

### Formule 1 — « Deux agences concurrentes » (recommandée)

Chacun construit **sa propre version** du jeu, dans son propre dossier, avec les mêmes prompts.
Vendredi, chacun présente sa version au client : on compare les choix (couleurs, réglages, niveau de l'IA)
et l'IA de l'un affronte… le joueur de l'autre.

Il suffit de donner un nom différent à chaque version, par exemple `flechettes_lea` et `flechettes_tom` :
dans les prompts, remplacer le nom du dossier, le préfixe de l'API (`/api/flechettes_lea`) et le préfixe CSS
(`.flechettes_lea-`). Le prompt du socle (mardi matin) crée directement les deux dossiers.

### Formule 2 — « Une équipe, deux métiers »

Les deux élèves construisent **ensemble un seul jeu**, mais avec des rôles différents :
- l'un est le **développeur front** (React : l'écran, les animations) ;
- l'autre est le **développeur back** (Python : le serveur, l'arbitre, l'IA, les tests).

Chaque prompt du parcours est déjà découpé en « côté serveur » / « côté site ». La clé de la réussite :
se mettre d'accord **avant** sur ce que le site envoie et ce que le serveur répond (le « contrat » de l'API).
C'est exactement comme dans une vraie équipe. À réserver à un duo qui aime travailler ensemble ;
le mardi après-midi, le développeur back prépare les données et les tests pendant que l'autre dessine l'écran.

---

## Résumé pour choisir

| Jeu | Thème | L'IA… | Difficulté |
|---|---|---|---|
| ♞ Échecs | réflexion | **calcule** (minimax) | ★★☆ |
| ⚽ Coach | foot, gestion | **simule** des matchs et **apprend** tes habitudes | ★★★ |
| 🥅 Penalty Pro | foot, adresse | **apprend** où tu tires | ★★☆ |
| 🎯 Fléchettes | adresse, maths | **simule** ses lancers et **mesure** ta précision | ★★★ |
