# Déploiement sur une VM OCI (Docker + Caddy)

Version « entreprise », à faire en **démonstration** devant les élèves (après l'avoir répétée seul).
Fichiers utilisés : `Dockerfile` à la racine du projet, `deploy/oci/docker-compose.yml`, `deploy/oci/Caddyfile`.

```
Internet ──443──▶ [ VM OCI ]
                    ├── Caddy (HTTPS, certificat automatique) ──▶ conteneur « salle-de-jeux » :8000
                    └── conteneur « salle-de-jeux » = FastAPI (API des 2 jeux + site React compilé)
```

## 1. La VM (une fois, à préparer avant)

- Image **Ubuntu 24.04**, forme **Ampere A1 (ARM)** ou **AMD** : les images Docker utilisées existent pour les deux.
- **Security List / NSG** du sous-réseau : règles entrantes TCP **80** et **443** depuis `0.0.0.0/0` (le 22 est déjà ouvert).
- **Nom de domaine** : un enregistrement `A` (ex. `jeux.ton-domaine.fr`) vers l'IP publique de la VM.

> ⚠️ **Piège classique OCI :** les images Ubuntu d'Oracle ont aussi un pare-feu **iptables** qui bloque
> 80/443 même si la Security List est ouverte. À ouvrir sur la VM :
> ```bash
> sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
> sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
> sudo netfilter-persistent save
> ```

## 2. Installer Docker sur la VM

```bash
ssh ubuntu@<IP_PUBLIQUE>
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER      # puis se déconnecter / reconnecter
docker --version && docker compose version
```

## 3. Récupérer le projet et configurer le domaine

```bash
git clone <URL_DU_DEPOT> salle-de-jeux   # dépôt des élèves ou solution de référence
cd salle-de-jeux/deploy/oci
nano Caddyfile                          # remplacer jeux.example.com par ton domaine
```

## 4. Lancer

```bash
docker compose up -d --build
docker compose ps                       # les 2 conteneurs doivent être « running »
docker compose logs -f caddy            # voir Caddy obtenir le certificat HTTPS (Ctrl+C pour quitter)
```

Ouvrir `https://jeux.ton-domaine.fr` 🎉

## 5. Mettre à jour après une modification

```bash
cd ~/salle-de-jeux && git pull
cd deploy/oci && docker compose up -d --build
```

## Ce qu'il faut expliquer pendant la démo

- **SSH** : on pilote un ordinateur distant, sans écran, via des commandes.
- **Docker** : le `Dockerfile` est une recette. Étape 1 : un conteneur Node compile le site React.
  Étape 2 : un conteneur Python, qui ne contient que le strict nécessaire, sert l'API et le site.
  « Ça marche sur ma machine » devient « ça marche partout ».
- **Caddy / reverse proxy** : le « portier » qui reçoit les visiteurs, gère le HTTPS et transmet au jeu.
  Le jeu lui-même n'est pas exposé directement sur Internet.
- **Sécurité en couches** : Security List OCI → iptables → seul Caddy exposé → conteneur.

## Dépannage

| Symptôme | Piste |
|---|---|
| Le site ne répond pas du tout | Security List **et** iptables (voir encadré), DNS (`dig +short jeux.ton-domaine.fr`) |
| Erreur de certificat | Le DNS ne pointe pas encore vers la VM : attendre, puis `docker compose restart caddy` |
| `502 Bad Gateway` | Le conteneur `salle-de-jeux` est arrêté : `docker compose logs salle-de-jeux` |
| Build très long sur la VM | Normal la 1re fois (téléchargement des images) |
