# Fléchettes · Étapes 3 et 4 (mercredi) — Le serveur arbitre le 301, puis l'IA apprend à viser

> Entre les deux : l'atelier débranché commun (`J3-ateliers-debranches.md`), avec les « fléchettes en papier ».

---

## Matin — Le serveur arbitre la partie de 301 (étape 3)

**Les règles du 301 :** on part de 301 et il faut arriver **exactement** à 0. Si une fléchette fait descendre
sous 0, c'est « bust » : toute la volée est annulée. Les pros doivent en plus finir sur un double.

### Prompt D3a — la cible et les règles côté serveur

```
Je travaille sur les fléchettes. On veut que ce soit le serveur Python qui compte les points.

Crée backend/app/flechettes/cible.py :
- les dimensions officielles et l'ordre des secteurs (les mêmes que dans cible.js)
- score(x, y) → points, libellé (« T20 », « D16 », « Bull 50 »…) et s'il s'agit d'un double (le bull 50 compte comme un double)
- appliquer(restant, coup, double_sortie) → (« ok » / « bust » / « gagne », nouveau score restant).
  Si on passe sous 0 : bust, le score ne change pas. Avec l'option double_sortie, il faut finir sur un double
  et on ne peut jamais rester à 1.

Dans routes.py : POST /api/flechettes/lancer reçoit l'endroit où la fléchette s'est plantée et le score restant,
et renvoie les points et le résultat. Refuse les coordonnées absurdes.
Ajoute des tests dans backend/tests/test_flechettes.py : le centre vaut 50, (0, 103) est le triple 20, (103, 0) le triple 6,
(0, 166) le double 20, hors de la cible vaut 0 ; et les règles du 301 (bust, finir sur un double…).
```

### Prompt D3b — une partie en solo

```
Côté site : une partie de 301 en solo. Chaque fléchette est envoyée au serveur, qui renvoie les points.
Affiche le score restant en grand et le numéro de la volée. Après 3 fléchettes (ou un bust), on enlève les fléchettes
et on passe à la volée suivante. En cas de bust, le score revient à ce qu'il était au début de la volée,
avec le message « 💥 Bust ! ». À 0 : « 🏆 301 terminé en 9 volées ! ». Supprime le calcul des points du navigateur :
c'est le serveur l'arbitre.
```

### Ce qu'on vérifie

- Finir une partie. Provoquer un bust exprès. **Combien de volées pour finir ?** (noter le record)
- **Commit.**

---

## Après-midi — L'IA apprend à viser (étape 4)

Après les « fléchettes en papier » du matin, l'élève a vu que **viser le triple 20 n'est pas toujours le mieux
quand on n'est pas précis**. L'IA va le découvrir toute seule, en simulant.

### Prompt D4a — le cerveau de l'IA

```
Je travaille sur les fléchettes. On veut un adversaire IA qui choisit intelligemment où viser.

Crée backend/app/flechettes/ia.py :
- chaque niveau a une précision : un « écart » en mm (Facile 38, Moyen 22, Difficile 11). Quand l'IA vise un point,
  sa fléchette arrive à côté, au hasard (loi normale avec cet écart).
- des « candidats » : environ 240 endroits de la cible que l'IA envisage de viser (des cercles autour du centre,
  tous les 9°)
- valeur_moyenne(visee, restant, ...) : on imagine des dizaines de lancers vers ce point avec l'écart de l'IA,
  et on calcule ce qu'il lui RESTERAIT en moyenne (un bust ne fait pas avancer ; finir la partie donne un bonus de 40)
- choisir_visee(...) : garde le candidat où il reste le moins en moyenne. Utilise les MÊMES lancers au hasard
  pour tous les candidats (pour comparer équitablement), et simule plus de lancers quand l'IA est imprécise
  (40 + 3 × écart), sinon la moyenne est trompeuse.
- jouer_volee(restant, double_sortie, niveau, rng) : 3 fléchettes (ou moins en cas de bust / victoire),
  avec pour chacune où elle visait, où elle est tombée, et une explication du type :
  « Il me reste 301. J'ai simulé 37 114 lancers avec ma précision (environ 38 mm d'écart). Je vise 16 :
    je gagne en moyenne 15 points. Viser le triple 20 ne me rapporterait que 13,5 en moyenne. »
- carte_de_chaleur(...) : pour une grille de points de la cible, combien on gagne en moyenne en visant là

Ajoute la route POST /api/flechettes/ia/volee (score restant, niveau) qui renvoie la volée et la carte de chaleur.
Commentaires en français, comme si on devait le présenter à notre classe.
```

### Prompt D4b — les tests

```
Ajoute des tests :
- un champion (écart 5 mm) vise le triple 20
- un joueur imprécis (écart 40 mm) ne vise PAS le triple 20… et on vérifie sur 2000 lancers que son choix rapporte vraiment plus
- avec 40 à faire et l'option double, l'IA vise le double 20 ; avec 50, le bull
- une volée respecte toujours les règles
- le niveau difficile finit une partie en moins de volées que le facile
```

### Prompt D4c — côté site

```
On joue maintenant contre l'IA : après notre volée, c'est son tour. On montre ses fléchettes une par une :
d'abord un cercle bleu en pointillés là où elle VISE, puis sa fléchette là où elle TOMBE.
Deux grands scores côte à côte (Toi / IA), le premier à 0 gagne. Un choix de niveau.
Une carte « Dans la tête de l'IA » avec son explication, et une case à cocher pour afficher sa carte de chaleur
sur la cible : seulement les meilleurs endroits, du jaune (bien) au rouge (le meilleur).
```

### Ce qu'on vérifie

- Comparer la carte de chaleur et les choix de l'IA en Facile et en Difficile : **où vise un débutant, où vise un champion ?**
  Faire le lien avec les fléchettes en papier du matin.
- **Commit.**

### Si ça coince

- L'IA met trop de temps : « Combien de lancers simule-t-elle par fléchette ? Mesure le temps et propose une solution. »
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
