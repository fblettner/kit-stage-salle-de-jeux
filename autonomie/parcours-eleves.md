# Le parcours des élèves — les moments « ensemble », expliqués pas à pas

> Ce fichier est lu par le compagnon de stage : chaque partie « ## identifiant · titre » s'affiche sur l'écran des élèves,
> pour qu'ils sachent toujours quoi faire, même pendant les moments animés par le maître de stage.
> L'identifiant (l1, m3, w2…) est celui de l'activité dans `compagnon-de-stage/backend/app/programme.py` : ne le change pas.
>
> Ce qu'on peut écrire ici :
> - un bloc de code **sans langage** devient un prompt à copier ; avec le langage `secret`, un prompt caché
>   (l'élève le copie sans le lire) ; avec `bash`, une commande ;
> - un titre « ### Ce qu'on vérifie » suivi d'une liste devient des cases à cocher ;
> - `[[PROMPTS]]` est remplacé par les prompts de la fiche de l'animateur (pas de copier-coller entre deux fichiers) ;
> - `[[CLAUDE_MD]]` est remplacé par le fichier CLAUDE.md déjà rempli, à télécharger ;
> - `{{url_depot}}` vient des Réglages ; `{{dossier}}`, `{{dossier_autre}}`
>   et `{{prenom_autre}}` viennent des choix des élèves.

---

## Routine du matin

**Avant de commencer, 5 minutes pour remettre le poste en route :**

1. Ouvre **VS Code** : ton projet `salle-de-jeux` doit s'afficher (sinon : Fichier → Ouvrir le dossier).
2. Ouvre **deux terminaux** (menu Terminal → Nouveau terminal) et relance les deux programmes :

```bash
cd backend
source .venv/bin/activate      # sous Windows : .venv\Scripts\activate
fastapi dev
```

```bash
cd frontend
npm run dev
```

3. Ouvre **http://localhost:5173** : ton jeu s'affiche comme hier soir ? Parfait.
4. Dans le panneau Claude, commence une **nouvelle conversation** avec ta phrase de départ (elle est rappelée en haut de chaque étape).

Si quelque chose ne redémarre pas, va voir la page **« Je suis bloqué »** dans le menu : tout y est expliqué.

---

## l1 · Accueil et découverte du métier

Ton maître de stage vous fait visiter l'entreprise et vous présente son métier. Écoutez, posez des questions, prenez des notes.
Ensuite, votre première mission : **mener l'enquête sur les métiers de l'informatique**, comme des journalistes.

### 1. L'enquête (45 min)

Demandez à une ou deux personnes de l'équipe si elles ont **10 minutes** pour répondre à vos questions
(on demande toujours avant, et on remercie après). Posez ces 5 questions et notez les réponses sur une feuille :

1. C'est quoi ton métier, expliqué simplement ?
2. À quoi ressemble une journée normale ?
3. Qu'est-ce que tu préfères ? Qu'est-ce qui est difficile ?
4. Quelles études as-tu faites ?
5. Est-ce que tu utilises l'intelligence artificielle dans ton travail ? Pour quoi faire ?

### 2. Les trois casquettes (20 min)

Cette semaine, vous allez porter trois casquettes : **consultant** (comprendre le client),
**architecte** (organiser le logiciel) et **développeur** (le construire).
Ouvrez Claude Desktop et demandez-lui de vous les expliquer :

```
Bonjour Claude ! On est deux élèves de 3e en stage dans une entreprise d'informatique.
Explique-nous simplement, avec une comparaison de la vie de tous les jours pour chacun,
la différence entre ces trois métiers : consultant, architecte logiciel, développeur.
Puis pose-nous 3 questions pour vérifier qu'on a compris.
```

### Ce qu'on vérifie

- On a interviewé au moins une personne et noté ses réponses.
- Chacun sait expliquer avec ses mots la différence entre consultant, architecte et développeur.
- On a noté « Le métier de mon tuteur, en 3 phrases » dans le carnet de bord (ou ce qu'on en sait pour l'instant).

---

## l2 · Installation aux postes

Chacun s'installe à **son** poste : c'est le tien pour toute la semaine.
On vérifie ensemble que tout est prêt, comme un pilote avant le décollage.

### 1. Trois outils à repérer

- **VS Code** : l'atelier du développeur. À gauche les fichiers, au milieu le code, en bas le terminal.
- **Le terminal** (menu Terminal → Nouveau terminal) : on y écrit des commandes au clavier, au lieu de cliquer.
- **Le panneau Claude** (l'icône Claude dans VS Code) : c'est là que tu donneras tes consignes.

### 2. Le contrôle avant décollage

Dans le terminal, tape ces trois commandes, une par une. Chacune doit répondre par un numéro de version :

```bash
python3 --version
node --version
git --version
```

Sous Windows, si `python3` ne répond pas, essaie `python --version`.

### Ce qu'on vérifie

- VS Code s'ouvre et j'ai trouvé le terminal.
- Les trois commandes répondent par un numéro (Python 3.10 ou plus, Node 20 ou plus).
- Le panneau Claude s'ouvre dans VS Code. **S'il demande un mot de passe ou de créer un compte : je n'écris rien**, et j'envoie un message avec le bouton SOS.
- Je suis connecté au compagnon de stage avec mon code, sur mon poste.

Une commande répond « command not found » ? Note laquelle et appelle ton maître de stage avec le bouton **SOS**.
En attendant, continue avec l'autre poste, à deux.

---

## l3 · L'interview du client

Le client, c'est le directeur de la Maison des jeunes. Votre travail de consultants : **lui poser les bonnes questions**.
Le rôle du client est joué par ton maître de stage, ou par **Claude** : c'est ton maître de stage qui vous dit lequel.

### 1. Si c'est Claude qui joue le client

Ouvrez Claude Desktop, démarrez une nouvelle conversation et collez ce prompt **sans le lire** :
il contient les réponses du client. Le lire, c'est comme regarder la fin du film avant le début !

```secret
Tu vas jouer un rôle pour deux élèves de 3e en stage dans une entreprise d'informatique.
Tu es M. Martin, le directeur de la Maison des jeunes du quartier. Tu n'es pas informaticien.
Les élèves sont des consultants : ils t'interviewent pour comprendre ton besoin.

Commence par cette demande, volontairement floue, et rien d'autre :
« Bonjour ! J'aimerais une salle de jeux sur Internet pour nos jeunes : des jeux où on joue contre l'ordinateur.
Ici, ce qui marche le mieux, c'est le club d'échecs, le foot et le tournoi de fléchettes du vendredi. »

Règles du jeu :
- Tu réponds UNIQUEMENT à la question posée, en 1 ou 2 phrases, avec des mots simples. Tu ne donnes jamais
  une information qu'on ne t'a pas demandée. Tu ne proposes pas de questions.
- Si une question est floue, demande aux élèves de la préciser, comme un vrai client.
- Tu restes dans ton rôle tant que les élèves n'écrivent pas « FIN DE L'INTERVIEW ».

Ce que tu sais (à ne révéler que si on te le demande) :
- Qui va l'utiliser : des jeunes de 10 à 16 ans, certains débutants.
- Quels jeux exactement : « Je ne sais pas, c'est vous les spécialistes : proposez-moi ! »
- Contre qui on joue : contre l'ordinateur, ils n'ont pas toujours un partenaire.
- Sur quel appareil : ordinateur surtout, et le téléphone si possible.
- Faut-il un compte ou un mot de passe : non, surtout pas.
- Plusieurs niveaux de difficulté : oui ! Les débutants se découragent si l'ordinateur est trop fort.
- Comment passer d'un jeu à l'autre : un menu d'accueil, simple.
- Le délai : pour vendredi, c'est la démonstration devant le conseil d'administration.
- Le budget, la publicité, les achats dans le jeu : pas de budget, pas de publicité, tout est gratuit.
- Pour toute autre question : invente une réponse simple et cohérente avec le reste.

Quand les élèves écrivent « FIN DE L'INTERVIEW », sors de ton rôle et fais le bilan en tant que formateur :
1. les bonnes questions qu'ils ont posées ;
2. les questions importantes qu'ils ont oubliées (parmi la liste ci-dessus), et pourquoi elles comptent ;
3. un conseil pour leur prochaine interview. Sois encourageant.
```

### 2. Mener l'interview (30 min)

- **Une question à la fois.** L'un pose la question, l'autre note la réponse sur une feuille, puis on échange les rôles.
- Le client ne dit que ce qu'on lui demande : à vous de penser à tout ! Qui ? Quoi ? Où ? Quand ? Comment ? Combien ?
- Avec Claude : quand vous n'avez plus d'idée de question, écrivez `FIN DE L'INTERVIEW`, il vous dira ce que vous avez oublié.
  Vous pouvez alors poser les questions oubliées (demandez-lui de reprendre son rôle).

💡 **À retenir :** un bon informaticien commence par **écouter et questionner**, pas par coder.

### Ce qu'on vérifie

- On a posé au moins 8 questions et noté toutes les réponses sur papier.
- On sait qui va utiliser la salle de jeux, sur quel appareil, et pour quelle date.
- On a complété nos notes avec les questions qu'on avait oubliées.
- On garde nos notes : on en aura besoin pour le cahier des charges.

---

## l4 · Le catalogue : choisis ton projet

Le client a dit : « proposez-moi ! ». Un consultant présente des **options**, avec leurs avantages et leurs inconvénients.
Ici, vous êtes à la fois les consultants et ceux qui décident.

### 1. Jouer aux 4 jeux d'exemple (20 min)

Dans le menu de gauche, cliquez sur **« La salle de jeux »**.

Jouez **5 minutes à chaque jeu**, tous les deux : ♞ Échecs, ⚽ Coach, 🥅 Penalty Pro, 🎯 Fléchettes.
Ce sont des exemples : vous allez construire **le vôtre**, avec vos idées.
Pendant que vous jouez, demandez-vous : comment l'ordinateur décide-t-il de ce qu'il fait ?

### 2. Lire les fiches et choisir (25 min)

Dans le menu, ouvre **« Mon projet »** : chaque jeu a sa fiche (ce qu'on construit, comment pense l'IA, la difficulté).
Lis-les en entier, discutez-en, puis **chacun choisit**. Même jeu ou jeux différents : les deux marchent.

Un conseil : choisis le jeu qui te donne envie, pas le plus facile. Tu vas passer trois jours dessus !

### Ce qu'on vérifie

- J'ai joué aux 4 jeux.
- J'ai lu les 4 fiches en entier.
- J'ai choisi mon jeu dans « Mon projet » et écrit pourquoi.
- Je sais quel jeu a choisi {{prenom_autre}}.

---

## l5 · Le cahier des charges

Le **cahier des charges**, c'est le document qui dit noir sur blanc ce qu'on va faire… et ce qu'on ne fera pas.
Le client le lit, il est d'accord, et tout le monde sait où on va.

### 1. Demander à Claude de le rédiger avec vous

Dans Claude Desktop, **nouvelle conversation**. Copiez le prompt ci-dessous, et remplacez la partie entre crochets
par vos notes de l'interview (tapez-les telles quelles, même en vrac).

[[PROMPTS]]

### 2. Relire comme des professionnels (15 min)

Ne dites pas « c'est bon » tout de suite. Lisez le document en entier, à voix haute, à tour de rôle :

- **Le point 6** (les questions oubliées) : retournez voir le client et posez-les-lui.
  Puis donnez ses réponses à Claude pour qu'il mette le document à jour.
- **Les « indispensables »** : est-ce que tout tient en 4 jours ? Si la liste est trop longue, demandez à Claude
  d'en déplacer dans « bien si on a le temps ». Savoir **couper** fait partie du métier.
- Une phrase que vous ne comprenez pas ? Demandez à Claude de la réécrire plus simplement.

### 3. Garder le document

Demandez à Claude : « Donne-nous la version finale ». Copiez-la dans un fichier ou imprimez-la :
vous la ressortirez **jeudi** (la revue) et **vendredi** (la démo).

### Ce qu'on vérifie

- On a répondu aux questions du point 6 avec le client.
- Les fonctionnalités « indispensables » de chaque jeu tiennent en 4 jours.
- Chacun sait de quel jeu il est **responsable**, et qu'il sera le **client-testeur** du jeu de l'autre.
- Le document final est gardé (fichier ou papier).

---

## l6 · Les maquettes papier

Pas d'ordinateur pour cette activité : une feuille A4, un crayon, une gomme.

1. **Chacun dessine l'écran de son jeu** (15 min). Que voit-on ? Où sont les boutons ? Où choisit-on le niveau ?
   Qu'est-ce qui s'affiche quand la partie est finie ? Où l'IA explique-t-elle ce qu'elle a « pensé » ?
2. **Échangez vos feuilles** (5 min). L'autre te dit ce qu'il ne comprend pas : s'il hésite, un vrai joueur hésitera aussi.
3. **Ensemble, dessinez le menu d'accueil** (10 min) : le titre, une tuile par jeu.

💡 **À retenir :** dessiner coûte 5 minutes ; recoder un écran mal pensé coûte des heures.

Écris ton prénom sur ta maquette et **garde-la précieusement** : elle guidera ton écran demain, et on vérifiera jeudi.

### Ce qu'on vérifie

- Ma maquette montre l'écran du jeu, les boutons, le choix du niveau et l'écran de fin.
- L'autre stagiaire a compris ma maquette sans que je lui explique.
- On a dessiné le menu d'accueil ensemble.

---

## m1 · Le schéma : front, back, API

Sans ordinateur pour commencer : une grande feuille pour deux.

### 1. Que se passe-t-il quand tu ouvres un site ? (10 min)

Quand tu regardes une vidéo en ligne, deux ordinateurs se parlent : le tien, et un autre, très loin, qu'on appelle un **serveur**.

```text
 [ Navigateur ]  ── question ──▶  [ Serveur ]
   le FRONT      ◀── réponse ───    le BACK
   React             (API)         Python
  ce qu'on voit                 ce qui calcule
```

Pense à un **restaurant** :
- la **salle** où le client est servi, c'est le **front** (ce qu'on voit, dans le navigateur) ;
- la **cuisine** où l'on prépare, c'est le **back** (ce qui calcule, sur le serveur) ;
- le **serveur** qui porte les commandes, avec un menu précis, c'est l'**API** : la liste de ce qu'on a le droit de demander.

Demandez à Claude Desktop de vous l'expliquer avec ses mots, puis posez-lui vos questions :

[[PROMPTS]]

### 2. À vous de dessiner (10 min)

Recopiez le schéma sur votre feuille et complétez-le : dans la cuisine, ajoutez **l'IA du jeu de chacun**.
Puis répondez à l'oral : dans votre jeu, qu'est-ce qui se passe dans la salle ? Et dans la cuisine ?

### 3. La question de l'architecte (10 min)

Vous êtes deux à construire le même site. **Comment faire pour ne pas se gêner ?**
Cherchez une réponse à deux pendant 3 minutes avant de regarder.

<details>
<summary>Voir la réponse de l'architecte</summary>

On découpe le projet en **modules** : une partie commune qu'on fait ensemble, et **un dossier par jeu**.

<pre>
salle-de-jeux/
├── commun : le menu, les couleurs, le serveur   ← on le fait ENSEMBLE ce matin
├── {{dossier}}/        ← ton dossier
└── {{dossier_autre}}/  ← le dossier de {{prenom_autre}}
</pre>

En entreprise, plusieurs développeurs travaillent sur le même logiciel. On se met d'accord sur ce qui est commun
**avant** de se séparer : ensuite, chacun reste dans son dossier.

</details>

### Ce qu'on vérifie

- Je sais dire ce que sont le front, le back et l'API avec l'exemple du restaurant.
- Notre schéma montre le navigateur, le serveur et l'IA de chaque jeu.
- Je sais pourquoi chaque jeu aura son propre dossier.
- J'ai recopié le schéma dans mon carnet de bord (page du mardi).

---

## m2 · Découverte des outils

On s'installe sur **un seul poste**, à deux, pour créer le projet. Celui qui n'a pas le clavier lit les consignes à voix haute.

### 1. Le tour de l'atelier (10 min)

- **VS Code** : à gauche, la liste des fichiers ; au milieu, leur contenu ; en bas, le terminal.
- **Le terminal** : on y tape des commandes. Menu Terminal → Nouveau terminal.
- **Git** : une **machine à remonter le temps**. À chaque étape qui marche, on prend une « photo » du projet (un *commit*).
  Si on casse tout, on revient à la dernière photo.
- **Le panneau Claude** : notre collègue. On lui écrit ce qu'on veut, il propose, **on vérifie**.

### 2. Créer le projet (10 min)

Dans VS Code : Fichier → Ouvrir le dossier → créez un **nouveau dossier vide** appelé `salle-de-jeux` et ouvrez-le.
Puis, dans le terminal :

```bash
git init
```

Git répond qu'il a créé un dépôt vide : la machine à remonter le temps est branchée.

### 3. La fiche de consignes pour Claude (10 min)

Quand un nouveau collègue arrive, on le briefe : le projet, les règles de l'équipe, comment on se parle.
Pour Claude, ce brief est un fichier : **CLAUDE.md**. Le voici, déjà rempli avec vos jeux.

[[CLAUDE_MD]]

Téléchargez-le et glissez-le dans le dossier `salle-de-jeux` (il doit apparaître dans la liste de gauche de VS Code).
Puis **lisez-le ensemble, en entier** : c'est vous les chefs de projet, vous devez savoir ce que vous demandez.

### Ce qu'on vérifie

- Le dossier `salle-de-jeux` est ouvert dans VS Code et `git init` a répondu sans erreur.
- Le fichier `CLAUDE.md` est dans le dossier, avec **nos** jeux écrits dedans.
- On a lu le CLAUDE.md en entier. On sait expliquer la règle « le serveur est l'arbitre » et la règle « l'IA ne triche jamais ».

---

## m3 · Le socle commun

Toujours **sur un seul poste, à deux**. Le socle, ce sont les fondations de la maison : le menu, les couleurs,
le serveur, et un dossier vide pour chaque jeu. On le construit ensemble avant de se séparer.

### 1. Le prompt

Copiez ce prompt dans le panneau Claude de VS Code. Les noms de vos jeux et de vos dossiers sont déjà remplis : vérifiez-les.

[[PROMPTS]]

Claude va créer beaucoup de fichiers et vous demander plusieurs fois la permission : lisez ce qu'il propose avant d'accepter.
Pendant qu'il travaille (2 à 5 minutes), regardez les fichiers apparaître à gauche.

### 2. Lancer les deux programmes

Claude vous donne les commandes à la fin. En général, il faut **deux terminaux** :

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate      # sous Windows : .venv\Scripts\activate
pip install "fastapi[standard]"
fastapi dev
```

```bash
cd frontend
npm install
npm run dev
```

Une commande affiche une erreur ? Copiez **tout** le message d'erreur dans Claude et demandez-lui d'expliquer la cause.

### 3. L'expérience

Arrêtez le serveur Python (cliquez dans son terminal, puis Ctrl+C) et rechargez la page du site.
Que se passe-t-il ? Pourquoi ? Relancez-le ensuite avec `fastapi dev`.

### 4. La première photo

Demandez à Claude : « Fais un commit avec le message "Socle commun : menu et un dossier par jeu" ».

### Ce qu'on vérifie

- **http://127.0.0.1:8000/docs** s'ouvre : on a testé une route en cliquant sur « Try it out » puis « Execute ».
- **http://localhost:5173** affiche le menu « La salle de jeux » avec une tuile par jeu.
- Chaque tuile mène à « en construction 🚧 » et le bouton « ← Menu » ramène à l'accueil.
- On a fait l'expérience du serveur arrêté et on sait expliquer ce qui s'est passé.
- Le commit est fait.

---

## m4 · Chacun son poste

Le socle est prêt. Maintenant, chacun le récupère sur **son** poste et crée sa **branche** :
une copie de travail à son nom, pour avancer sans toucher au travail de l'autre.

### 1. Sur le poste où vous avez créé le socle : envoyer le projet

```bash
git remote add origin {{url_depot}}
git push -u origin main
```

Le projet est maintenant aussi rangé sur un serveur Git : c'est une sauvegarde, et le moyen de le partager.

### 2. Sur l'autre poste : récupérer le projet

Dans le terminal de VS Code :

```bash
git clone {{url_depot}} salle-de-jeux
```

Puis Fichier → Ouvrir le dossier → `salle-de-jeux`. Il faut installer les outils du projet sur ce poste aussi.
Demandez à Claude :

```
Je viens de récupérer le projet avec git clone sur un nouveau poste.
Lis le CLAUDE.md, puis aide-moi à installer ce qu'il faut et à lancer le serveur et le site.
Donne-moi les commandes une par une et attends que je te dise si ça a marché.
```

### 3. Sur chaque poste : créer sa branche

Chacun sur son poste, avec le nom de **son** dossier (le tien : `{{dossier}}`) :

```bash
git switch -c {{dossier}}
```

### Ce qu'on vérifie

- Les deux postes affichent le menu de la salle de jeux sur http://localhost:5173.
- Sur mon poste, la commande `git branch` montre une étoile devant `{{dossier}}`.
- Je sais que je ne modifie que les fichiers de **mon** jeu.

Si Git demande un identifiant ou un mot de passe : **n'écrivez rien**, et appelez votre maître de stage avec le bouton SOS.

---

## m6 · Présentation et carnet de bord

1. **Montre ton écran à {{prenom_autre}}** (10 min chacun). Explique ce que tu as construit et ce qui a été difficile.
   Compare avec ta maquette de lundi : qu'est-ce qui est pareil, qu'est-ce qui a changé ?
2. **Teste son écran.** Dis-lui deux choses que tu trouves réussies, et une chose à améliorer. C'est ça, un client-testeur.
3. **Range ton travail :** demande à Claude « Fais un commit de ce qui marche, puis pousse ma branche ».
4. **Remplis ton carnet de bord** (page du mardi), puis écris ton bilan du jour ci-dessous.

### Ce qu'on vérifie

- J'ai présenté mon écran et testé celui de l'autre.
- Mon travail est commité et poussé.
- Mon carnet du mardi est rempli.

---

## w2 · Atelier : comment « pense » une IA ?

Une heure **sans ordinateur**. Il vous faut : des feuilles, deux crayons, 2 dés si vous en avez.
C'est le moment le plus important de la semaine : après ça, vous saurez expliquer l'IA de votre jeu.
Faites les trois parties, quel que soit votre jeu : chacun comprendra ainsi l'IA de l'autre.

### Partie A — L'IA qui CALCULE (20 min) · ♞ Échecs

Jouez une partie de **morpion** normale. Puis rejouez-en une, mais cette fois, avant chaque coup,
celui qui joue doit dire à voix haute : « si je joue là, tu joueras là, alors je… ».

C'est exactement ce que fait une IA qui calcule :
- elle imagine **ses** coups possibles et choisit le **meilleur pour elle** (MAX) ;
- pour chacun, elle imagine la réponse de l'adversaire, qui choisit **le pire pour elle** (MIN).

On appelle ça le **minimax**. Petit exercice, sur votre feuille : l'IA a 2 coups possibles.
Après le coup A, l'adversaire peut lui laisser 3 points ou 8 points. Après le coup B, 5 points ou 6 points. Que joue l'IA ?

<details>
<summary>Voir la réponse</summary>

L'adversaire choisit toujours le pire pour l'IA : après A il lui laisse 3, après B il lui laisse 5.
L'IA joue donc **B** (5 vaut mieux que 3), même si le plus gros score, 8, était du côté de A.
Une IA qui calcule ne rêve pas : elle suppose que l'adversaire joue bien.

</details>

Aux échecs, il y a environ 30 coups possibles à chaque tour. Calculez : combien de positions à regarder pour 3 coups d'avance ?
(30 × 30 × 30.) C'est pour ça que l'ordinateur doit aussi **élaguer** : abandonner vite les pistes perdantes.

### Partie B — L'IA qui SIMULE (20 min) · ⚽ Coach, 🎯 Fléchettes

Quand il y a du **hasard**, on ne peut pas tout calculer. Alors on essaie… beaucoup de fois.

**Les fléchettes en papier.** Dessinez une grande cible sur une feuille posée par terre : un centre, et tout autour
des parts numérotées, avec le 20 entouré du 1 et du 5. Dans la part du 20, dessinez une petite zone « triple » (60 points).
Faites des boulettes de papier. Chacun lance **10 boulettes en visant le triple 20**, puis **10 en visant le centre** (50 points).
Comptez les points des deux séries.

Alors, il vaut mieux viser où ? **Ça dépend de ta précision** : c'est ce que calcule l'IA des fléchettes.
Elle simule des milliers de lancers avec SA précision avant de choisir où viser.

**Le match aux dés** (si vous avez des dés). Un match dure 6 actions, on lance un dé par action.
Équipe offensive : 5 ou 6 = but marqué, 1 = but encaissé. Équipe défensive : 6 = but marqué, jamais de but encaissé.
Jouez 1 match de chaque : ça ne prouve rien. Jouez-en 10 de chaque : la tendance apparaît.
L'entraîneur IA de Coach fait pareil, avec 1 500 matchs en moins d'une seconde.

On appelle ça la **méthode de Monte-Carlo** (le nom d'un casino… parce qu'on tire beaucoup au sort).

### Partie C — L'IA qui APPREND (20 min) · 🥅 Penalty Pro, ⚽ Coach

1. Jouez **15 manches de pierre-feuille-ciseaux**. Après chaque manche, chacun note **en secret** ce que l'autre a joué
   et s'il a gagné ou perdu.
2. Chacun étudie sa feuille 2 minutes : qu'est-ce que l'autre joue le plus souvent ? Que fait-il après avoir perdu ?
3. Rejouez **10 manches** en utilisant ce que vous avez observé. Qui gagne plus souvent qu'avant ?

Le lien avec vos jeux :
- **compter** les choix de l'autre, c'est le gardien de Penalty Pro au niveau Moyen ;
- repérer « après ça, il fait souvent ça », c'est le niveau Difficile ;
- la parade : être **imprévisible**. C'est pour ça que les IA gardent un peu de hasard, elles aussi.

### Conclusion

Recopiez et complétez ce tableau sur une feuille, puis vérifiez avec le prompt ci-dessous si vous voulez aller plus loin.

| L'IA… | Comment elle fait | Dans quel jeu de la salle | Un exemple dans la vraie vie |
|---|---|---|---|
| **calcule** | | | |
| **simule** | | | |
| **apprend** | | | |

💡 **À retenir :** une IA, ce n'est pas magique. Ce sont des règles de calcul écrites par des humains, qu'on peut expliquer.
Et vous venez de les comprendre.

[[PROMPTS]]

### Ce qu'on vérifie

- On a fait les trois parties (calculer, simuler, apprendre).
- J'ai trouvé la réponse de l'exercice du minimax et je sais l'expliquer.
- On a rempli le tableau de conclusion.
- Je sais dire laquelle de ces trois idées utilise l'IA de **mon** jeu, et j'ai rempli la page du mercredi de mon carnet.

---

## w4 · Le duel

1. **Échangez vos places.** Chacun joue au jeu de l'autre, contre son IA : 3 parties en Facile, 3 en Moyen, 3 en Difficile.
2. Note tes résultats. L'IA de l'autre est-elle vraiment plus forte quand on monte de niveau ? Regarde ce qu'elle « explique ».
3. **Fais un retour à {{prenom_autre}}** : deux choses réussies, une chose à améliorer.
4. Reviens à ton poste : demande à Claude « Fais un commit de ce qui marche, puis pousse ma branche ».
5. Remplis ton carnet (page du mercredi), puis ton bilan du jour ci-dessous.

### Ce qu'on vérifie

- J'ai joué contre l'IA de l'autre aux trois niveaux et noté mes résultats.
- J'ai donné mon retour à l'autre, et écouté le sien.
- Mon travail est commité et poussé.

---

## j1 · Revue avec les maquettes

Ressors ta **maquette de lundi** et le **cahier des charges**. Pose ta maquette à côté de ton écran et compare, point par point.

1. Entoure sur ta maquette ce qui **manque** encore à l'écran.
2. Écris ta liste d'améliorations dans la zone ci-dessus, **une idée par ligne**.
3. **Classe-les** : en premier ce qui est « indispensable » dans le cahier des charges, ensuite ce qui est « bien si on a le temps ».
4. Montre ta liste à {{prenom_autre}} : est-il d'accord avec ton ordre ? Un client-testeur a son mot à dire.

Tu as environ 1 h 30 de finitions ce matin : compte 20 à 30 minutes par amélioration. **3 idées bien faites valent mieux que 8 commencées.**

### Ce qu'on vérifie

- J'ai comparé mon écran avec ma maquette.
- Ma liste est écrite et classée, les indispensables en premier.
- L'autre stagiaire a vu ma liste.

---

## j5 · Tournoi et fusion

### 1. Le tournoi (20 min)

Chacun joue 3 parties contre l'IA de chaque jeu, au niveau Difficile. Qui bat le plus souvent les IA ?

### 2. La fusion (30 min)

Depuis mardi, vous travaillez chacun sur votre branche. Il est temps de **réunir les deux jeux** dans la branche principale, `main`.

**D'abord, chacun sur son poste**, on range et on envoie son travail :

```bash
git status
git push -u origin {{dossier}}
```

Si `git status` affiche des fichiers modifiés, demande d'abord à Claude : « Fais un commit de ce qui marche ».

**Ensuite, à deux sur un seul poste** :

```bash
git switch main
git pull
git fetch origin
git merge origin/{{dossier}} -m "Fusion de {{dossier}}"
git merge origin/{{dossier_autre}} -m "Fusion de {{dossier_autre}}"
git push
```

Comme chacun est resté dans son dossier, la fusion doit se faire **sans conflit**.
C'est pour ça que l'architecture de mardi matin était importante !

Git parle de « conflit » ? Pas de panique, ça arrive à tous les développeurs. Demandez à Claude :

```
On vient de fusionner nos deux branches et Git annonce un conflit.
Explique-nous ce qu'est un conflit, montre-nous les fichiers concernés,
puis propose une solution en nous expliquant ce que tu gardes de chaque côté. Ne supprime le travail de personne.
```

### 3. Vérifier

Relancez le serveur et le site, puis jouez aux deux jeux depuis le menu. Dans le terminal du dossier `backend` :

```bash
pytest
```

### Ce qu'on vérifie

- Les deux branches sont poussées.
- Sur `main`, le menu affiche les deux jeux et les deux fonctionnent.
- `pytest` affiche tous les tests en vert.

Pas le temps de finir ? Aucun problème : la fusion est aussi prévue demain matin.

---

## v1 · Fusion et version en ligne

Si la fusion n'a pas été faite hier, commencez par elle : retournez à l'activité **« Tournoi et fusion »** de jeudi.

### 1. Développement et production

Depuis mardi, **deux** programmes tournent sur votre poste : le site (Vite) et le serveur (Python). C'est pratique pour développer.
En ligne, on veut **un seul** programme : on « compile » le site en fichiers simples, et c'est Python qui les sert.

À deux sur un seul poste, sur la branche `main` :

[[PROMPTS]]

### 2. Tester comme en production

Arrêtez vos deux programmes (Ctrl+C dans chaque terminal), puis :

```bash
cd frontend
npm run build
cd ../backend
fastapi run
```

Ouvrez **http://127.0.0.1:8000** : toute la salle de jeux doit fonctionner, sans Vite.

### Ce qu'on vérifie

- `npm run build` se termine sans erreur.
- La salle de jeux complète fonctionne sur http://127.0.0.1:8000 (les deux jeux, contre l'IA).
- On sait expliquer la différence entre « développement » et « production ».
- Le commit est fait et poussé.

---

## v2 · Mise en ligne !

Le grand moment : votre salle de jeux part sur Internet.

Dans le terminal, dans le dossier `backend` :

```bash
fastapi deploy
```

- La commande demande un **nom** pour l'application : choisissez-le ensemble (sans espace ni accent).
- Après une ou deux minutes, une **adresse en https://** s'affiche. C'est la vôtre !

⚠️ Si une page de connexion s'ouvre et demande un e-mail ou un mot de passe : **n'écrivez rien et ne créez pas de compte**.
Appelez votre maître de stage : c'est lui qui se connecte.

### Quand l'adresse s'affiche

1. Ouvrez-la **sur vos téléphones** et jouez chacun au jeu de l'autre.
2. Regardez le **cadenas** à côté de l'adresse : `https` veut dire que personne ne peut lire ce qui circule entre le téléphone et le serveur.
3. Votre programme ne tourne plus sur votre poste : il tourne sur un ordinateur dans un **centre de données**. Éteignez `fastapi run` pour vérifier !

### Ce qu'on vérifie

- L'adresse fonctionne sur un téléphone.
- Les deux jeux marchent en ligne, contre l'IA.
- J'ai noté l'adresse dans mon carnet de bord.

---

## v3 · La version « entreprise »

Vous venez de mettre en ligne en **une commande**. Dans une grande entreprise, on fait souvent autrement :
on loue une machine et on installe tout soi-même. Vous en utilisez un exemple depuis lundi : **ce compagnon de stage** tourne comme ça.

### 1. Les six mots à connaître (15 min)

| Le mot | Ce que c'est | Comme… |
|---|---|---|
| **Machine virtuelle (VM)** | un ordinateur qu'on loue dans un centre de données | louer un local vide |
| **SSH** | la façon de piloter cette machine à distance, au clavier | la clé du local |
| **Docker** | une « boîte » qui contient le programme et tout ce qu'il lui faut | un food-truck : tout est dedans, on le gare où on veut |
| **Nom de domaine** | l'adresse facile à retenir, à la place d'une suite de chiffres | l'enseigne sur la rue |
| **HTTPS (avec Caddy)** | le cadenas : ce qui circule est chiffré | une enveloppe fermée au lieu d'une carte postale |
| **Pare-feu** | il ne laisse entrer que ce qu'on a autorisé | le vigile à l'entrée |

Demandez à Claude Desktop de vous raconter le voyage complet :

```
On est deux élèves de 3e. On vient de mettre un site en ligne avec une seule commande.
Notre maître de stage, lui, met des sites en ligne sur une machine virtuelle, avec Docker, Caddy et un nom de domaine.
Raconte-nous, étape par étape et avec des comparaisons simples, ce qui se passe entre le moment
où quelqu'un tape l'adresse du site sur son téléphone et le moment où la page s'affiche.
```

### 2. Le conseil de l'architecte (20 min)

Un architecte compare les options avant de conseiller son client :

| | Une commande (FastAPI Cloud) | Une machine à soi (VM) |
|---|---|---|
| Mise en place | 1 commande | 1 à 2 heures |
| Mises à jour, sécurité | le service s'en occupe | c'est à nous de le faire |
| Liberté de tout régler | limitée | totale |
| Coût | selon l'offre | selon la machine |

Discutez-en à deux, puis écrivez votre réponse sur une feuille (vous la présenterez à la démo) :

1. Pour la **Maison des jeunes**, vous conseillez quoi ? Pourquoi ?
2. Et pour une **banque** ? Pourquoi ?

### Ce qu'on vérifie

- Je sais expliquer les six mots avec mes propres comparaisons.
- On a écrit notre conseil pour la Maison des jeunes et pour la banque, avec une raison à chaque fois.

---

## v4 · Préparer la démo

Cet après-midi, vous présentez votre salle de jeux comme une **vraie démo client** : 15 minutes, à deux voix.

### 1. Le plan

1. **Le besoin du client** (le cahier des charges de lundi) — *ensemble*
2. **L'architecture** : front, back, API, et le découpage en deux modules (votre schéma) — *ensemble*
3. **Mon jeu** et comment pense son IA : elle calcule, elle simule ou elle apprend ? — *chacun le sien*
4. **La démo en direct** sur l'adresse publique : faites jouer quelqu'un du public !
5. **Le client a changé d'avis** jeudi : comment on a réagi
6. Ce qu'on a appris, ce qui a été difficile, ce qu'on ajouterait — *chacun*

Claude peut vous aider à organiser, mais c'est **vous** qui parlez :

[[PROMPTS]]

### 2. Répéter (au moins deux fois)

- Chronométrez : 15 minutes, pas plus.
- Ouvrez **avant** tout ce qu'il faut : l'adresse du site, le schéma, le cahier des charges.
- Prévoyez le pire : si Internet lâche, que montrez-vous ? (la version sur votre poste, avec `fastapi run`.)
- Pas de phrases apprises par cœur : des mots-clés sur une feuille suffisent.

### Ce qu'on vérifie

- On sait qui dit quoi, dans quel ordre.
- On a répété deux fois, chronomètre en main.
- Tout est ouvert et prêt sur le poste de démo.
- On a un plan B si Internet ne marche pas.

---

## v5 · La démo devant l'équipe

C'est votre moment. Trois conseils de professionnels :

- **Parlez au public**, pas à l'écran.
- Un bug en direct ? Souriez, dites « ça, c'est noté pour la prochaine version », et continuez. Ça arrive à tout le monde.
- **Faites jouer quelqu'un** : c'est ce dont les gens se souviennent.

À la fin, demandez au public : « Qu'est-ce que vous amélioreriez ? » et notez les réponses.

### Ce qu'on vérifie

- On a présenté notre salle de jeux.
- Quelqu'un du public a joué.
- On a noté les réactions et les idées du public.

---

## v6 · Carnet de bord et rapport de stage

1. **Termine ton carnet de bord** : la page du vendredi et le bilan de la semaine.
2. **Imprime-le** (bouton « Imprimer » en haut du carnet) : c'est la base de ton rapport de stage.
3. **Commence ton rapport.** C'est **toi** qui l'écris : Claude peut relire, pas rédiger à ta place.
   Quand tu as écrit un passage, tu peux lui demander une relecture :

[[PROMPTS]]

4. Écris ton **bilan du jour** ci-dessous : c'est aussi ton message de fin de stage pour ton maître de stage.
5. Range ton poste, et **remercie** les personnes qui t'ont accueilli cette semaine.

### Ce qu'on vérifie

- Mon carnet de bord est complet et imprimé.
- J'ai noté l'adresse de notre salle de jeux pour la montrer à ma famille et à mon collège.
- J'ai dit merci.
