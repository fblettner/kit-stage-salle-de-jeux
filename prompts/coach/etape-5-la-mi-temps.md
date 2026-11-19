# Coach · Étape 5 (jeudi) — Finitions… et le client change d'avis

> Un prompt **par fonctionnalité**, on teste, on committe, puis on passe à la suivante.

---

## Matin — Revue et finitions

Ressortir la maquette du lundi. Qu'est-ce qui manque ? L'élève liste et priorise lui-même.
Idées fréquentes (à faire avec ses propres prompts) : afficher l'équipe sur un petit terrain,
une couleur de maillot pour son club, un bouton pour revoir le match, le meilleur buteur du match…

---

## 🎭 Le client change d'avis (en fin de matinée)

Tu reprends ton rôle de directeur de la Maison des jeunes :

> « Les jeunes adorent ! Mais ils râlent : quand ils perdent 2-0 à la mi-temps, ils ne peuvent rien faire.
> Un vrai coach, ça change de tactique à la mi-temps ! Et la démo n'a pas bougé ! »

Laisse l'élève réagir. Questions à faire émerger :
- Le moteur de match sait-il déjà simuler seulement une partie du match ? (oui : `minute_debut`, `minute_fin`, `score`)
- Et l'entraîneur IA, il peut changer de tactique aussi ? Sur quoi doit-il se baser ? (le score, le temps restant,
  et ce qu'il a vu de la 1re mi-temps)

💡 **Message clé :** quand on a bien découpé son code (le moteur d'un côté, l'IA de l'autre), une nouvelle demande
se fait vite. C'est le travail de l'architecte qui paie.

### Prompt F5a — la mi-temps

```
Notre client veut pouvoir changer de tactique à la mi-temps.

Côté serveur :
- /api/coach/match accepte minute_debut, minute_fin et le score de départ (pour jouer une seule mi-temps)
- /api/coach/entraineur accepte aussi minute_debut et le score : l'entraîneur IA simule seulement
  la fin du match, à partir du score actuel. (S'il perd à la mi-temps, il devrait prendre plus de risques !)
- ajoute un test : une seconde mi-temps commence bien avec le score de la première

Côté site :
- le match se joue en deux fois : minutes 1 à 45, puis un écran « mi-temps », puis 46 à 90
- à la mi-temps : les statistiques de la 1re période, et le choix de la tactique pour la 2e
- au moment de reprendre, l'entraîneur IA réfléchit à nouveau : il a vu notre tactique de 1re mi-temps
  (on l'ajoute à l'historique) et connaît le score
- les commentaires et les statistiques des deux mi-temps s'additionnent
```

### Ce qu'on vérifie

- Être mené à la mi-temps, passer en offensive : est-ce que ça change quelque chose ?
- Regarder la décision de l'IA à la mi-temps quand elle mène, et quand elle est menée. Est-ce logique ?

---

## Chasse aux bugs (après-midi)

C'est l'autre élève qui teste Coach (et inversement). Idées :
cliquer plusieurs fois sur « Coup d'envoi », couper le serveur Python pendant le match, revenir au menu en plein match,
changer de niveau entre deux matchs, recruter puis retirer très vite, jouer sur téléphone, envoyer une équipe
trop chère directement à l'API depuis **http://127.0.0.1:8000/docs** (le serveur doit refuser !)…

```
On a trouvé un bug. Ce qu'on a fait : […]. Ce qui s'est passé : […].
Ce qui aurait dû se passer : […]. Trouve la cause, explique-la-nous, puis corrige.
```

### Bonus : le tournoi

Chaque élève compose son équipe et affronte FC Python 🐍 en Difficile, 3 matchs. Qui prend le plus de points ?
Puis comparer avec l'IA des échecs : belle slide pour la démo.

**Commit** à la fin de la journée.

### Si ça coince

Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
