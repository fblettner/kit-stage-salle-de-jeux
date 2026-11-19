# Penalty Pro · Étape 5 (jeudi) — Finitions… et le client change d'avis

> Un prompt **par fonctionnalité**, on teste, on committe, puis on passe à la suivante.

---

## Matin — Revue et finitions

Ressortir la maquette du lundi. Qu'est-ce qui manque ? L'élève liste et priorise lui-même
(idées : un son de foule, la trace du ballon, des statistiques de ses tirs, un bouton « Recommencer »…).

---

## 🎭 Le client change d'avis (en fin de matinée)

Tu reprends ton rôle de directeur de la Maison des jeunes :

> « Les jeunes adorent tirer… mais ils veulent aussi jouer **gardien** ! Et faire une vraie séance de tirs au but,
> comme en Coupe du monde. Et la démo n'a pas bougé ! »

Questions à faire émerger : le code du gardien peut-il servir à un **tireur** IA ? (oui : prédire où le joueur plonge,
puis viser ailleurs). Qui gagne une séance ? (5 tirs chacun, arrêt dès que l'écart ne peut plus être rattrapé, puis mort subite.)

### Prompt P5a — l'IA tireur

```
Notre client veut que le joueur puisse aussi être gardien.

Côté serveur, dans ia.py :
- choisir_tir(historique_plongeons, niveau, rng) : le tireur IA prédit où le joueur va plonger (même fonction predire),
  puis vise la zone où il a le plus de chances de marquer. Pour savoir si une zone est risquée, il SIMULE
  200 tirs vers cette zone avec la fonction trajectoire et compte combien restent dans le cadre.
  Chance de marquer = (1 − probabilité que le joueur plonge là) × (part des tirs cadrés).
  Il vise près des poteaux, avec une puissance qui dépend du niveau (0,55 / 0,75 / 0,8).
- une route POST /api/penalty/arret : reçoit où le joueur plonge et ses plongeons précédents ;
  le tireur décide AVANT de regarder le plongeon.
- un test : si le joueur plonge toujours en bas à gauche, l'IA ne tire jamais là.
```

### Prompt P5b — la séance de tirs au but

```
Côté site : une vraie séance. Le joueur tire, puis il devient gardien (maillot orange) et clique où il veut plonger,
puis il retire, etc. Mets les règles dans regles.js : 5 tirs chacun, on s'arrête dès que l'écart ne peut plus
être rattrapé, puis mort subite. Ajoute un tableau des scores (une ligne « Toi », une ligne « IA », avec ⚽ ou ❌),
un badge « Mort subite ! », le message de fin et un bouton « Nouvelle séance ».
Dans la carte « Dans la tête de l'IA », affiche ce que pensait le gardien OU le tireur selon le moment.
```

---

## Chasse aux bugs (après-midi)

C'est l'autre élève qui teste Penalty Pro. Idées : cliquer très vite plusieurs fois, changer de niveau en pleine séance,
cliquer « Nouvelle séance » pendant un tir, couper le serveur, arriver à 5-5, jouer sur téléphone,
envoyer une cible hors du but directement à l'API depuis **http://127.0.0.1:8000/docs** (le serveur doit refuser !)…

```
On a trouvé un bug. Ce qu'on a fait : […]. Ce qui s'est passé : […].
Ce qui aurait dû se passer : […]. Trouve la cause, explique-la-nous, puis corrige.
```

**Commit** à la fin de la journée.

### Si ça coince

Bloqué plus de 20 minutes : revenir au dernier commit qui marchait (page « Je suis bloqué » du compagnon, « La machine à remonter le temps »), puis refaire l'étape prompt par prompt.
