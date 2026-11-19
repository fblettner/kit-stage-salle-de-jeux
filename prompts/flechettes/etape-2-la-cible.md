# Fléchettes · Étape 2 (mardi après-midi) — La cible et la main qui tremble

> Toujours commencer la séance Claude par : **« Je travaille sur les fléchettes. »**

---

## Avant de coder (15 min) : observer une vraie cible

Montrer une photo de cible (ou une vraie !) et faire découvrir les règles : 20 secteurs, l'anneau des triples,
celui des doubles, le centre (« bull ») à 50, l'anneau autour à 25. Le maximum en 3 fléchettes ? (180 = 3 × triple 20)

**Question de géométrie :** 20 secteurs pour faire un tour complet… combien de degrés par secteur ? (360 / 20 = 18°)
C'est ce calcul qui permettra à l'ordinateur de savoir dans quel secteur est une fléchette.

---

### Prompt D2a — dessiner la cible

```
Je travaille sur les fléchettes (dossier frontend/src/flechettes).

On veut dessiner une vraie cible de fléchettes en SVG, dans un composant Cible.jsx, avec les dimensions officielles
(en mm, depuis le centre) rangées dans un fichier cible.js :
centre (bull) 6,35 mm ; anneau du 25 : 15,9 mm ; anneau des triples de 99 à 107 mm ; anneau des doubles de 162 à 170 mm.
Les 20 secteurs, dans le sens des aiguilles d'une montre en partant du haut :
20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5. Chaque secteur fait 18°, le 20 est centré en haut.
Couleurs : secteurs alternés noir et crème, anneaux alternés rouge et vert, centre rouge, anneau du 25 vert,
les numéros en blanc tout autour sur un fond noir.

Explique-nous comment on dessine un « morceau d'anneau » avec un chemin SVG (path).
Styles dans flechettes.css, avec des classes qui commencent par flechettes-.
```

### Prompt D2b — viser, trembler, lancer

```
On veut pouvoir lancer des fléchettes :
- on repère un point de la cible en mm depuis le centre, avec y vers le HAUT (attention : en SVG, y va vers le bas)
- quand la souris est sur la cible, un viseur jaune la suit… mais la main TREMBLE : le viseur décrit une petite courbe
  autour de la souris (environ 14 mm, avec des sinus, animé avec requestAnimationFrame)
- un clic lance la fléchette là où est le viseur À CE MOMENT-LÀ : il faut lancer au bon moment !
- une fonction score(x, y) dans cible.js calcule les points : bull 50, 25, triple, double, simple ou « Raté »
  (on trouve le secteur avec l'angle, grâce à Math.atan2)
- on dessine la fléchette plantée, on affiche « T20 : 60 points »
- une volée = 3 fléchettes : on affiche les 3 résultats, le total, et le record de la meilleure volée
Pour l'instant tout se passe dans le navigateur : on ne touche pas au serveur Python.
```

### Ce qu'on vérifie

- Viser le centre : les points affichés sont-ils justes ? Viser le triple 20, le double 6, le 11…
- Qui fait la meilleure volée ? L'autre élève, toi… **Petit concours !**
- **Commit** (« Fléchettes : la cible et la main qui tremble »).

### Si ça coince

- Les secteurs sont décalés : « Le 20 n'est pas en haut / les numéros ne correspondent pas aux secteurs. Explique pourquoi et corrige. »
  (C'est presque toujours une histoire de sens de l'axe y ou de décalage de 9°.)
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
