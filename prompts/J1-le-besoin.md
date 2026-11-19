# Jour 1 — Comprendre le besoin et choisir son projet (casquette « conseil ») · les deux élèves ensemble

> **Outil :** Claude Desktop (ou claude.ai), sur ton compte. Les élèves dictent, tu tapes ou tu leur laisses le clavier.
> **Objectif du jour :** passer d'une demande floue d'un client à un cahier des charges clair, et choisir chacun son projet.

---

## Atelier 1 — L'interview du client (sans Claude, 45 min)

Tu joues **le client** : le directeur de la Maison des jeunes du quartier.
Demande initiale, volontairement floue :

> « J'aimerais une salle de jeux sur Internet pour nos jeunes : des jeux où on joue contre l'ordinateur.
> Ici, ce qui marche le mieux, c'est le club d'échecs, le foot et le tournoi de fléchettes du vendredi. »

Les élèves doivent te poser des questions et noter les réponses. Questions à faire émerger (ne les donne pas !) :

| Question à faire émerger | Ta réponse de client |
|---|---|
| Qui va l'utiliser ? | Des jeunes de 10 à 16 ans, certains débutants |
| Quels jeux, exactement ? | « Je ne sais pas, c'est vous les spécialistes : proposez-moi ! » (→ atelier 2) |
| Contre qui on joue ? | Contre l'ordinateur, ils n'ont pas toujours un partenaire |
| Sur quel appareil ? | Ordinateur surtout, et le téléphone si possible |
| Faut-il un compte / mot de passe ? | Non, surtout pas |
| Plusieurs niveaux ? | Oui ! Les débutants se découragent si l'ordi est trop fort |
| Comment on passe d'un jeu à l'autre ? | Un menu d'accueil, simple |
| Combien de temps pour le faire ? | Pour vendredi, c'est la démo devant le conseil d'administration |

💡 **Message clé :** un bon informaticien commence par **écouter et questionner**, pas par coder.

---

## Atelier 2 — Le catalogue : chacun choisit son projet (45 min)

1. Lance la **solution de référence** (voir `solution/salle-de-jeux/README.md`) et laisse les élèves jouer
   5 minutes à chaque jeu : ♞ Échecs, ⚽ Coach, 🥅 Penalty Pro, 🎯 Fléchettes.
   « Ce sont des exemples. Vous allez construire LE VÔTRE, avec vos idées. »
2. Lis avec eux `01-CATALOGUE-DES-PROJETS.md` : ce qu'on construit, comment pense l'IA, la difficulté.
3. **Chacun choisit.** Même jeu ou jeux différents : les deux marchent (voir les deux formules en bas du catalogue).
4. Note les choix : ils serviront à compléter le `CLAUDE.md` demain matin.

💡 **Message clé :** en conseil, on présente des **options** au client avec leurs avantages et leurs inconvénients,
puis on décide ensemble. Ici, les élèves sont à la fois les consultants et ceux qui décident.

---

## Atelier 3 — Le cahier des charges avec Claude (30 min)

### Prompt à copier dans Claude Desktop

```
Bonjour Claude ! On est deux élèves de 3e en stage dans une entreprise d'informatique.
Notre maître de stage joue le rôle d'un client : le directeur d'une Maison des jeunes.

Voici les notes de notre interview du client :
[COLLER ICI LES NOTES DES ÉLÈVES]

On a 4 jours pour faire une « salle de jeux » en ligne, avec des jeux contre l'ordinateur.
Voici les jeux qu'on a choisis : [EX. : « des fléchettes (Tom) et Penalty Pro, des tirs au but (Léa) »].

Aide-nous à écrire un cahier des charges simple :
1. Le but du projet en 2 phrases
2. Les utilisateurs (qui sont-ils ?)
3. Ce qui est COMMUN à tous les jeux (menu, style, mise en ligne…)
4. Pour chaque jeu : les fonctionnalités « indispensables » / « bien si on a le temps » / « plus tard »
5. Ce qu'on ne fera PAS (pour être clairs avec le client)
6. Les questions qu'on a oublié de poser au client

Écris simplement : on découvre le métier.
Présente-le comme un document qu'on pourrait montrer au client.
```

### Ce qu'on vérifie ensemble

- Le point 6 : les élèves retournent voir le client (toi) pour y répondre.
- Est-ce que tout ce qui est « indispensable » tient en 4 jours ? Fais-leur couper si besoin.
- Chacun devient « responsable » de son jeu et « client-testeur » du jeu de l'autre.

---

## Atelier 4 — Les maquettes papier (30 min, sans Claude)

Sur une feuille A4 chacun dessine **l'écran de son jeu**, puis ensemble **le menu d'accueil**.
Que voit-on ? Où sont les boutons ? Qu'est-ce qui s'affiche quand la partie est finie ?

💡 **Message clé :** dessiner coûte 5 minutes ; recoder un écran mal pensé coûte des heures.

Garde les maquettes : elles serviront à vérifier le résultat le jeudi.
