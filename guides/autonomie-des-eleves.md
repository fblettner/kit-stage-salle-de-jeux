# L'autonomie des élèves : ce que le compagnon leur affiche

Le but : que chaque élève sache **toujours quoi faire ensuite** en regardant son écran, sans attendre que tu sois disponible.
Tu es là, mais tu n'es plus le passage obligé : tu peux aider l'un pendant que l'autre avance, répondre à un collègue,
ou simplement les regarder se débrouiller.

## Ce qu'ils ont sous les yeux

| Sur leur écran | D'où ça vient |
|---|---|
| Un **pas-à-pas pour chaque activité**, y compris les moments « ensemble » (interview, cahier des charges, schéma, socle, ateliers sur l'IA, fusion, mise en ligne, démo), avec des cases à cocher qui comptent dans l'avancement | `autonomie/parcours-eleves.md` |
| Les **prompts de leur jeu**, les vérifications, les conseils « Si ça coince » | `prompts/<jeu>/…` |
| **« Reprendre où j'en étais »** et **« Activité suivante »** : ils enchaînent seuls | — |
| La page **« Je suis bloqué »** : l'échelle du dépannage, les prompts de secours, les pannes courantes, quoi faire en attendant | `autonomie/depannage.md` |
| Le rappel **« relancer mon poste »** en tête de la première activité sur ordinateur, chaque matin | `autonomie/parcours-eleves.md`, partie « Routine du matin » |
| **« La salle de jeux »** dans le menu : les 4 jeux d'exemple, affichés dans le compagnon, pour jouer avant de choisir | le compagnon les démarre avec lui |
| Le **CLAUDE.md déjà rempli** avec leurs jeux, à télécharger (mardi matin) | `CLAUDE.md` du kit |
| Les commandes Git avec **leur** dépôt et **leurs** branches (mardi midi, fusion) | Réglages → adresse du dépôt |
| **Ton mot du jour**, en haut de leur journée | Réglages |
| Le **bilan du jour** à écrire en trois lignes, que tu lis sur ton tableau de bord | — |

Ta fiche d'animateur (tes notes, les réponses du client, « Laisse l'élève réagir… ») reste sur **ton** écran.
Dans « Le programme », le bouton **« Écran des élèves »** te montre exactement ce qu'ils lisent pour chaque activité.

## Deux moments où tu choisis

- **L'interview du client (lundi).** Soit tu joues le client, soit Claude le joue : leur écran propose un prompt « secret »
  (les réponses sont dedans, ils le copient sans le lire), et Claude fait ensuite le bilan des questions oubliées. Dis-leur lequel.
- **Le client change d'avis (jeudi).** La demande reste cachée chez eux tant que tu n'as pas cliqué « Déclencher », après avoir joué la scène.

## À renseigner dans les Réglages

- [ ] **L'adresse du dépôt Git** (privé, vide) : elle est recopiée dans leurs commandes de mardi midi et de la fusion.
- [ ] **Le mot du jour**, quand tu as quelque chose à leur dire à tous les deux.

Les textes des élèves leur demandent de **ne jamais taper de mot de passe** : si Git ou FastAPI Cloud en réclame un, ils t'appellent.
Pour que ça n'arrive pas, connecte Git au dépôt et fais `fastapi login` sur les postes avant.

## Adapter les textes

Tout ce que lisent les élèves est dans deux fichiers, modifiables comme le reste du kit :

- `autonomie/parcours-eleves.md` : une partie « ## identifiant · titre » par activité « ensemble » (le mode d'emploi est en tête du fichier).
- `autonomie/depannage.md` : la page « Je suis bloqué ».

Après une modification : `pytest` dans `compagnon-de-stage/backend` (un test vérifie que chaque activité a toujours son guide),
puis relance le compagnon.
