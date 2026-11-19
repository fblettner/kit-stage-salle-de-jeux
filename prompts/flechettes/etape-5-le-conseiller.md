# Fléchettes · Étape 5 (jeudi) — Finitions… et le client change d'avis

> Un prompt **par fonctionnalité**, on teste, on committe, puis on passe à la suivante.

---

## Matin — Revue et finitions

Ressortir la maquette du lundi. Qu'est-ce qui manque ? L'élève liste et priorise lui-même.

### Prompt D5a — les options de partie

```
Je travaille sur les fléchettes. Ajoute dans les réglages :
- trois boutons 101 / 301 / 501 pour lancer une nouvelle partie avec ce score de départ
- une case « Finir sur un double (comme les pros) », envoyée au serveur à chaque lancer
```

---

## 🎭 Le client change d'avis (en fin de matinée)

Tu reprends ton rôle de directeur de la Maison des jeunes :

> « Les petits se découragent : ils visent toujours le triple 20 et ratent tout. L'ordinateur, lui, sait où viser…
> Il ne pourrait pas les **conseiller** ? Et la démo n'a pas bougé ! »

Questions à faire émerger : le calcul de l'IA marche avec n'importe quelle précision… mais quelle est la précision
**du joueur** ? Comment la mesurer ? (en comparant où il visait et où sa fléchette est tombée !)

### Prompt D5b — le conseiller

```
Notre client veut un conseiller pour les joueurs.

Côté serveur, dans ia.py :
- estimer_ecart(lancers) : mesure la précision du joueur à partir de ses lancers précédents (où il visait, où c'est tombé).
  Tant qu'on a peu de lancers, on part d'une précision « moyenne » de 25 mm (comme si on avait déjà vu 3 lancers à 25 mm).
- une route POST /api/flechettes/conseil : reçoit le score restant, l'option double et les lancers du joueur ;
  estime sa précision, cherche où IL a intérêt à viser (même fonction que l'IA), et renvoie le conseil,
  une explication (« D'après tes 9 lancers, ta fléchette s'écarte d'environ 19 mm… vise T16 ») et sa carte de chaleur.
- un test : un joueur très précis a un écart estimé plus petit qu'un joueur imprécis.

Côté site : on garde en mémoire tous nos lancers (où on visait = la souris, où c'est tombé). Un bouton
« 💡 Où dois-je viser ? » affiche l'explication, un cercle jaune qui clignote là où viser, et notre carte de chaleur personnelle.
```

### Ce qu'on vérifie

- Lancer 10 fléchettes, demander conseil. Puis faire tester par quelqu'un de plus adroit (toi ?) : le conseil change-t-il ?
- **Message clé :** l'IA ne donne pas le même conseil à tout le monde : elle s'**adapte à la personne** grâce aux **données**
  qu'elle a mesurées. C'est le principe des applis de sport, des recommandations…

---

## Chasse aux bugs (après-midi)

C'est l'autre élève qui teste les fléchettes. Idées : cliquer très vite, cliquer pendant le tour de l'IA,
changer de partie en plein tour, couper le serveur, finir une partie avec et sans l'option double, jouer sur téléphone,
envoyer des coordonnées absurdes à l'API depuis **http://127.0.0.1:8000/docs**…

```
On a trouvé un bug. Ce qu'on a fait : […]. Ce qui s'est passé : […].
Ce qui aurait dû se passer : […]. Trouve la cause, explique-la-nous, puis corrige.
```

**Commit** à la fin de la journée.

### Si ça coince

Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
