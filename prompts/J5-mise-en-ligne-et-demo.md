# Jour 5 — Fusion, mise en ligne et démo · les deux élèves ensemble

> **Objectif du jour :** réunir les deux jeux, publier la salle de jeux sur Internet, montrer la version « entreprise » sur OCI, présenter le projet.

---

## Atelier 0 — La fusion (si elle n'a pas été faite jeudi soir, 20 min)

Sur ton poste, devant les deux élèves (détails dans `guides/travailler-a-deux-avec-git.md`) :

```bash
git switch main
git pull
git merge <jeu A>     # on ramène le travail de l'élève A (ex. git merge flechettes)
git merge <jeu B>     # puis celui de l'élève B
```

Comme chacun est resté dans son dossier, il ne devrait y avoir **aucun conflit**.
C'est le bon moment pour montrer **pourquoi** l'architecture du mardi matin était importante.
Lancer `pytest` (tous les tests des deux jeux) et jouer aux deux jeux depuis le menu.

---

## Atelier 1 — Préparer la version en ligne (30 min)

Expliquer la différence **développement / production** : en dev, deux programmes tournent (Vite et Python).
En ligne, on veut **un seul** programme : le site React est « compilé » en fichiers simples que Python sert lui-même.

### Prompt 11

```
On veut mettre la salle de jeux en ligne sur FastAPI Cloud, avec un seul programme.
On a le droit de modifier les fichiers communs pour cette étape.
1. Vérifie que « npm run build » range le site compilé dans backend/dist (réglage build.outDir de vite.config.js)
2. Dans backend/app/main.py, sers ce dossier avec app.frontend("/", directory=...) — seulement s'il existe,
   pour que le développement continue de fonctionner sans build. Les routes /api doivent rester prioritaires.
3. Ajoute backend/dist au .gitignore (on ne versionne pas un fichier généré)
   MAIS crée un fichier backend/.fastapicloudignore contenant « !dist/ » pour qu'il soit quand même envoyé au déploiement.
Explique-nous pourquoi on « compile » le site avant de le mettre en ligne.
```

### Vérifier en local, comme en production

```bash
cd frontend && npm run build
cd ../backend && fastapi run      # puis ouvrir http://127.0.0.1:8000 : la salle complète, sans Vite
```

---

## Atelier 2 — Mise en ligne sur FastAPI Cloud (30 min)

Voir `guides/deploiement-fastapi-cloud.md`. En résumé :

```bash
cd backend
fastapi deploy        # 1re fois : connexion via le navigateur (TON compte), puis choix du nom de l'appli
```

Quand l'URL s'affiche : les élèves l'ouvrent **sur leur téléphone** et jouent chacun au jeu de l'autre.

💡 **Points à expliquer :** l'adresse en `https://` (le cadenas), le fait que le programme tourne
maintenant sur un ordinateur d'un centre de données, et non plus sur le tien.

---

## Atelier 3 — La version « entreprise » sur OCI (démonstration, 30 min)

C'est **toi** qui fais, eux qui regardent. Voir `guides/deploiement-oci.md`.

À montrer et à expliquer : la **machine virtuelle**, la connexion **SSH**, **Docker** (la « boîte »),
**Caddy** et le **nom de domaine** (HTTPS), le **pare-feu**.

Puis comparer les deux options avec eux, comme un architecte devant un client :

| | FastAPI Cloud | VM OCI |
|---|---|---|
| Mise en place | 1 commande | 1 à 2 h |
| Maintenance (mises à jour, sécurité) | gérée par le service | à notre charge |
| Contrôle, personnalisation | limité | total |
| Coût | selon l'offre | selon la VM (offres gratuites possibles) |

**Question à leur poser :** « Pour la Maison des jeunes, vous conseilleriez quoi ? Et pour une banque ? »

---

## Atelier 4 — La démo (après-midi)

Les élèves présentent la salle de jeux (15-20 min) à tes collègues, comme une vraie démo client :
1. le besoin du client (le cahier des charges du lundi) — *ensemble*
2. l'architecture : front / back / API, et le découpage en deux modules — *ensemble*
3. **le jeu de l'élève A** et comment pense son IA (calcule, simule ou apprend ?) — *élève A*
4. **le jeu de l'élève B**, avec le panneau « Dans la tête de l'IA » — *élève B*
   (même jeu pour les deux ? montrer les deux versions côte à côte : qu'est-ce qui diffère ?)
5. **démo en direct** sur l'URL publique : faire jouer un collègue !
6. ce qu'ils ont appris, ce qui a été difficile, ce qu'ils ajouteraient — *chacun*

### Prompt optionnel (Claude Desktop) pour préparer la présentation

```
On doit présenter notre projet de salle de jeux ([NOS JEUX], contre l'IA)
à des professionnels, en 15 minutes, à deux.
Voici ce qu'on a fait cette semaine : [résumé des élèves].
Aide-nous à préparer le plan de la présentation et ce que chacun va dire,
avec des phrases simples.
```

---

## Atelier 5 — Le rapport de stage

Les élèves s'appuient sur leur carnet de bord (`fiches/carnet-de-bord.md`).
**Ils l'écrivent eux-mêmes** : Claude peut relire, pas rédiger à leur place.

```
Voici un passage de mon rapport de stage. Ne le réécris pas : signale-moi seulement
les fautes d'orthographe et les phrases pas claires, et explique pourquoi.
[TEXTE]
```
