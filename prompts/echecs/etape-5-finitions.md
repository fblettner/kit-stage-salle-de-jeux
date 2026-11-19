# Échecs · Étape 5 (jeudi) — Finitions… et le client change d'avis

> Un prompt **par fonctionnalité**, on teste, on committe, puis on passe à la suivante.
> L'élève peut rédiger lui-même ces prompts : ceux-ci servent de modèle ou de secours.

---

### Prompt E5a — fin de partie

```
Je travaille sur le jeu d'échecs.
Quand la partie est finie, affiche un message clair en français :
« Échec et mat ! Vous avez gagné 🎉 », « Échec et mat… l'ordinateur a gagné », ou le type de match nul
(pat, répétition, pas assez de pièces). On ne doit plus pouvoir bouger les pièces.
Quand un roi est en échec, colorie sa case en rouge.
```

### Prompt E5b — choisir sa couleur et recommencer

```
Ajoute deux boutons « Jouer les Blancs » et « Jouer les Noirs » qui lancent une nouvelle partie.
Si on prend les Noirs, l'échiquier doit être retourné et c'est l'ordinateur qui commence.
Colorie en jaune les deux cases du dernier coup joué.
```

### Prompt E5c — mise en page et historique

```
Mets les réglages (niveau, boutons) et la liste des coups joués dans un panneau à droite de l'échiquier,
avec les « cartes » du style commun (classe carte). Les coups sont numérotés par paires (1. e4 e5, 2. Cf3 Cc6…).
Sur un petit écran, le panneau passe sous l'échiquier.
Mets les styles dans src/echecs/echecs.css avec des classes qui commencent par echecs-.
```

---

## 🎭 Le client change d'avis (en fin de matinée)

Tu reprends ton rôle de directeur de la Maison des jeunes :

> « Les animateurs adorent, mais les plus petits ne savent pas comment bougent les pièces.
> Il faudrait qu'en cliquant sur une pièce, on voie où elle peut aller. Et la démo n'a pas bougé ! »

Laisse l'élève réagir : qu'est-ce qu'on enlève pour tenir le délai ? C'est la réalité du métier.

### Prompt E5d — le mode débutant

```
Notre client veut un « mode débutant » (une case à cocher, activée par défaut) :
quand on clique sur une de nos pièces, on voit des petits points sur les cases où elle peut aller,
et un cercle sur les pièces qu'elle peut prendre. Un deuxième clic sur une de ces cases joue le coup.
Le glisser-déposer doit continuer à fonctionner.
```

---

## Chasse aux bugs (après-midi)

C'est l'autre élève qui teste le jeu d'échecs (et inversement). Idées :
cliquer très vite, changer de niveau en pleine partie, recommencer pendant que l'ordinateur réfléchit,
couper le serveur Python, promouvoir un pion, jouer sur téléphone…

```
On a trouvé un bug. Ce qu'on a fait : […]. Ce qui s'est passé : […].
Ce qui aurait dû se passer : […]. Trouve la cause, explique-la-nous, puis corrige.
```

**Commit** à la fin de la journée.
