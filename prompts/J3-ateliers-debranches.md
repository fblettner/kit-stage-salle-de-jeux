# Jour 3 (milieu de matinée) — Comment « pense » une IA ? · atelier débranché, les deux élèves ensemble

> **Durée :** 1 h, sans ordinateur. **Matériel :** tableau, un échiquier, 2 dés, des feuilles de papier (pour les boulettes),
> une cible dessinée au tableau ou sur une grande feuille.
> C'est **le** moment clé de la semaine pour comprendre ce qu'est une IA de jeu.
> Les deux élèves font les trois parties, quel que soit leur jeu : chacun comprend ainsi l'IA de l'autre.
> Si le temps manque, garde en priorité la partie qui correspond à leurs jeux (voir le tableau final).

---

## Partie A — L'IA qui CALCULE : minimax (20 min) · ♞ Échecs

1. **Donner une note à une position.** On compte les pièces : pion 1, cavalier/fou 3, tour 5, dame 9.
2. **Regarder un coup en avance.** « Parmi mes coups, lequel donne la meilleure note ? »
   → l'ordinateur mange tout ce qu'il peut… y compris un pion protégé par une dame adverse !
3. **Regarder deux coups en avance.** Un petit arbre au tableau : mes coups, puis les réponses de l'adversaire.
   L'adversaire choisit **le pire pour moi** (MIN), moi **le meilleur pour moi** (MAX) → **minimax**.
4. **Le problème :** environ 30 coups possibles par position. 3 coups d'avance = 27 000 positions.
   → il faut **élaguer** (ne pas explorer les branches qu'on sait perdantes).

💡 Variante : le même raisonnement sur le **morpion**, que tout le monde connaît.

---

## Partie B — L'IA qui SIMULE (20 min) · ⚽ Coach, 🎯 Fléchettes

Quand il y a du **hasard**, on ne peut pas tout calculer. Alors on essaie… beaucoup de fois.

**Version « fléchettes en papier » :** dessine une cible au tableau (au moins le 20 et ses voisins, le 1 et le 5).
Chaque élève lance 10 boulettes en visant le **triple 20**, puis 10 en visant le **centre**. On compte les points.
Pour des lanceurs imprécis, viser le centre rapporte souvent plus ! Et pour un champion ? → **Ça dépend de ta précision.**
C'est exactement ce que fait l'IA des fléchettes : elle simule des milliers de lancers avec SA précision avant de choisir.

**Version « match aux dés » :** un match de 6 actions, un dé par action. Équipe offensive : 5 ou 6 = but pour elle, 1 = but encaissé.
Équipe défensive : 6 = but, jamais de but encaissé. Un seul match ne prouve rien ; 10 matchs de chaque, la tendance apparaît.
C'est ce que fait l'entraîneur IA de Coach, avec 1 500 matchs en moins d'une seconde.

→ On appelle ça la **méthode de Monte-Carlo** (du nom du casino… parce qu'on tire beaucoup au sort).

---

## Partie C — L'IA qui APPREND (20 min) · 🥅 Penalty Pro, ⚽ Coach, 🎯 le conseiller des fléchettes

1. **Tu joues 15 manches** de pierre-feuille-ciseaux contre chaque élève, en notant leurs choix en secret.
2. **Tu révèles ta feuille :** « Tu as joué pierre 7 fois sur 15. Et après avoir perdu, tu changes presque toujours. »
   Rejoue 10 manches en utilisant ces observations : tu devrais gagner plus souvent.
3. **Le lien avec les jeux :**
   - compter les choix = le gardien de Penalty Pro au niveau **Moyen** ;
   - repérer « après ça, il fait souvent ça » = le niveau **Difficile** ;
   - mesurer l'écart entre où on vise et où ça tombe = le **conseiller** des fléchettes ;
   - la parade : être **imprévisible**. C'est pour ça que les IA gardent un peu de hasard elles aussi.

---

## Conclusion au tableau (5 min)

| L'IA… | Comment | Dans nos jeux | Dans la vraie vie |
|---|---|---|---|
| **calcule** | imagine tous les coups possibles | ♞ Échecs | GPS (meilleur trajet), robots |
| **simule** | essaie des milliers de fois avec du hasard | ⚽ Coach, 🎯 Fléchettes | météo, prévisions sportives |
| **apprend** | observe des données et prédit | 🥅 Penalty Pro, ⚽ Coach, 🎯 conseiller | recommandations YouTube, anti-spam |

💡 **Message clé :** « Une IA, ce n'est pas magique : ce sont des règles de calcul écrites par des humains,
qu'on peut expliquer. Et on vient de les comprendre. »

### Prompt optionnel (Claude Desktop) pour approfondir

```
On est deux élèves de 3e. On a découvert trois idées pour faire une IA de jeu :
calculer à l'avance (minimax), simuler beaucoup de fois avec du hasard (Monte-Carlo),
et apprendre à partir des habitudes du joueur. Donne-nous des exemples de la vie de tous les jours
pour chacune, et explique ce qu'est le « machine learning » avec des mots simples.
```
