# Échecs · Étape 2 (mardi après-midi) — L'échiquier

> Toujours commencer la séance Claude par : **« Je travaille sur le jeu d'échecs. »**

---

### Prompt E2

```
Je travaille sur le jeu d'échecs (dossier frontend/src/echecs).

On veut afficher un échiquier dans JeuEchecs.jsx et pouvoir jouer à deux, chacun son tour.
Utilise la librairie react-chessboard (version 5) pour dessiner l'échiquier
et chess.js pour vérifier que les coups respectent les règles.
Si un coup est interdit, la pièce doit revenir à sa place.
Affiche au-dessus de l'échiquier à qui c'est le tour de jouer (Blancs ou Noirs).

Pour l'instant, on ne touche pas au serveur Python.
Explique-nous pourquoi on utilise une librairie au lieu de coder les règles nous-mêmes.
```

### Ce qu'on vérifie

- Tester un coup interdit (un pion qui recule, un fou qui avance tout droit…).
- Tester un roque, une prise. Demander : « combien de temps pour coder toutes les règles nous-mêmes ? »
- **Commit** (« Échecs : échiquier jouable à deux »).

### Si ça coince

- L'échiquier ne s'affiche pas ou erreur dans la console du navigateur (F12) :
  ```
  L'échiquier ne s'affiche pas. Voici l'erreur de la console du navigateur : [COLLER]
  Attention, react-chessboard v5 prend ses réglages dans une seule prop options={{...}}.
  ```
- Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.

### Bonus si en avance

```
On aimerait que les cases de l'échiquier aient d'autres couleurs : [couleurs choisies].
```
