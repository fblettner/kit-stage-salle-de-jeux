# Je suis bloqué — le guide de dépannage des élèves

> Ce fichier est affiché dans le compagnon de stage, page « Je suis bloqué ».
> Les blocs sans langage deviennent des prompts à copier.

Être bloqué, c'est **normal** : un développeur passe une bonne partie de ses journées à chercher pourquoi ça ne marche pas.
Ce qui fait la différence, c'est la méthode. La voici.

## L'échelle du dépannage

Monte les barreaux **dans l'ordre**. La plupart des problèmes se règlent avant le troisième.

1. **Lis le message d'erreur, en entier.** Il est en rouge dans le terminal, ou dans la console du navigateur (touche F12, onglet « Console »).
   Souvent, il dit exactement ce qui ne va pas, et dans quel fichier.
2. **Demande à Claude**, en lui donnant le message d'erreur complet (prompt ci-dessous).
3. **Demande à l'autre stagiaire.** Expliquer son problème à voix haute suffit souvent à trouver la solution. Les développeurs appellent ça « la méthode du canard en plastique ».
4. **Cherche ton symptôme** dans la liste plus bas.
5. **Reviens à ce qui marchait** (la machine à remonter le temps, plus bas).
6. **Appelle ton maître de stage** avec le bouton SOS : décris ce que tu voulais faire, ce qui se passe, et ce que tu as déjà essayé.
   S'il est occupé, **ne reste pas à attendre** : regarde « En attendant » tout en bas.

## Les prompts de dépannage

### Quand il y a un message d'erreur

```
J'ai une erreur. Voici ce que j'essayais de faire : [CE QUE TU VOULAIS FAIRE].
Voici le message d'erreur complet :
[COLLE ICI TOUT LE MESSAGE D'ERREUR]
Explique-moi d'abord la cause avec des mots simples. Ensuite seulement, corrige, et dis-moi comment vérifier que c'est réparé.
```

### Quand ça ne fait pas ce qu'on attend (sans message d'erreur)

```
Il y a un bug. Ce que j'ai fait : [TES GESTES, DANS L'ORDRE].
Ce qui s'est passé : [CE QUE TU AS VU].
Ce qui aurait dû se passer : [CE QUE TU ATTENDAIS].
Trouve la cause, explique-la-moi, puis corrige. Ne modifie que les fichiers de mon jeu.
```

### Quand tu ne comprends pas ce que Claude a fait

```
Je n'ai pas compris ce que tu viens de faire. Explique-le-moi comme à quelqu'un qui n'a jamais programmé :
quels fichiers tu as modifiés, à quoi sert chacun, et une comparaison de la vie de tous les jours pour l'idée principale.
```

### Quand Claude part dans une mauvaise direction

```
Stop. Ce n'est pas ce que je voulais. Annule ce que tu viens de modifier.
Ce que je veux vraiment : [EXPLIQUE AUTREMENT, AVEC UN EXEMPLE].
Avant de coder, redis-moi avec tes mots ce que tu as compris, et attends que je dise oui.
```

## Les pannes les plus courantes

### La page du site est blanche, ou affiche une erreur

- Ouvre la console du navigateur (F12, onglet « Console ») : la ligne rouge dit ce qui ne va pas. Copie-la à Claude.
- Vérifie que tes **deux** programmes tournent : un terminal avec `fastapi dev`, un autre avec `npm run dev`.
- Vérifie l'adresse : **http://localhost:5173** pendant le développement.

### Mes modifications n'apparaissent pas

- As-tu **enregistré** le fichier (Ctrl+S, ou Cmd+S sur Mac) ?
- Recharge la page (F5).
- Arrête et relance le serveur : clique dans son terminal, Ctrl+C, puis `fastapi dev`.

### Le terminal dit « command not found » ou « n'est pas reconnu »

- Es-tu dans le bon dossier ? `fastapi dev` se lance dans `backend`, `npm run dev` dans `frontend`. La commande `pwd` t'affiche où tu es.
- Pour Python, l'environnement est-il activé ? Tu dois voir `(.venv)` au début de la ligne. Sinon : `source .venv/bin/activate` (sous Windows : `.venv\Scripts\activate`).

### « Address already in use » ou « port déjà utilisé »

Le programme tourne déjà dans un autre terminal. Retrouve ce terminal et arrête-le (Ctrl+C), ou ferme tous les terminaux
(l'icône poubelle) et relance les deux programmes.

### Des erreurs en rouge après `npm run dev` ou `npm install`

Dans le dossier `frontend`, relance `npm install`, puis `npm run dev`. Si l'erreur revient, copie-la à Claude.

### Un test est rouge après `pytest`

C'est une bonne nouvelle : le test a fait son travail, il a trouvé un problème **avant** les joueurs.
Copie à Claude le nom du test et le message, et demande-lui d'expliquer ce que le test vérifiait.

### Claude me demande une permission

- Lire ou modifier un fichier **de ton projet**, lancer `pytest` ou `npm` : tu peux accepter, après avoir lu ce qu'il propose.
- Supprimer des fichiers, installer un logiciel sur l'ordinateur, modifier un fichier **en dehors** du projet, taper un mot de passe : **refuse**, et demande à ton maître de stage.
- Modifier un fichier **commun** (`App.jsx`, `index.css`, `main.py`…) : parles-en d'abord à l'autre stagiaire, ce fichier est à vous deux.

### Claude ne répond plus, ou dit qu'une limite est atteinte

Ça arrive : fais une pause de quelques minutes. Si ça dure, continue **sans lui** : teste ton jeu à la main et note les bugs,
remplis ton carnet de bord, relis le lexique, teste le jeu de l'autre. Préviens ton maître de stage avec le bouton SOS.

### On me demande un mot de passe, un e-mail, ou de créer un compte

**N'écris rien.** Ferme la fenêtre et préviens ton maître de stage avec le bouton SOS. Tu n'as jamais à créer de compte pendant le stage.

### Plus d'Internet

Préviens ton maître de stage. En attendant : les maquettes, le schéma, le carnet de bord et les tests à la main se font sans Internet.

## La machine à remonter le temps

Ton jeu marchait, et après une modification plus rien ne marche ? Git garde une « photo » de chaque commit.

**1. Regarde ce qui a changé depuis la dernière photo :**

```bash
git status
```

**2. Demande à Claude de revenir en arrière proprement :**

```
Mon jeu marchait au dernier commit et il ne marche plus. Montre-moi ce qui a changé depuis le dernier commit,
explique-moi ce qui a pu casser, puis propose-moi soit de corriger, soit de revenir au dernier commit pour les fichiers de mon jeu.
Attends ma réponse avant de faire quoi que ce soit.
```

**3. La règle d'or pour ne plus avoir peur :** un **commit après chaque étape qui marche**.
Plus tu prends de photos, moins tu perds de travail quand quelque chose casse.

Si une étape entière est cassée et que tu n'en sors pas : fais un commit de ce que tu as (même cassé, on ne perd rien),
puis préviens ton maître de stage avec le bouton SOS.

## Les règles d'or

- **La règle des 20 minutes :** bloqué depuis 20 minutes sur le même problème ? Change de barreau sur l'échelle. On ne reste pas seul face à un mur.
- **On ne tape jamais de mot de passe, on ne crée jamais de compte, on n'installe rien** sur l'ordinateur.
- **On reste dans son dossier.** Les fichiers communs se modifient à deux, d'accord tous les deux.
- **On vérifie tout ce que Claude produit.** Chaque prompt est suivi d'un test : c'est toi le responsable de ton jeu, pas lui.
- **Un commit à chaque étape qui marche.**
- **On fait des pauses** : 10 minutes le matin, 10 minutes l'après-midi, loin de l'écran.

## En attendant

Tu as appelé ton maître de stage et tu ne peux vraiment pas avancer sur ton étape ? Il y a toujours quelque chose d'utile à faire :

- **Teste le jeu de l'autre stagiaire** et note les bugs dans la page « Bugs ».
- **Remplis ton carnet de bord** : c'est du temps gagné pour ton rapport de stage.
- **Révise le lexique** : choisis 5 mots et explique-les à l'autre, sans regarder.
- **Passe à l'activité suivante** si elle ne dépend pas de celle qui bloque, et reviens plus tard.
- **Prépare la démo** de vendredi : que vas-tu montrer de ton jeu ? Qu'est-ce que tu diras sur son IA ?

## J'ai fini en avance

- Regarde s'il y a un **« Bonus si en avance »** en bas de la fiche de ton étape.
- **Écris tes propres prompts** : une amélioration à la fois, on teste, on committe.
- **Aide l'autre stagiaire**… sans prendre son clavier : pose-lui des questions, c'est lui le responsable de son jeu.
- **Joue contre ton IA** aux trois niveaux et note ce qui te semble trop facile ou trop dur.
