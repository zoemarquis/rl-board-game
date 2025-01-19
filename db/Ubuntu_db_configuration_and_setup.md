# Configuration et utilisation de la base de données `ludo_stats` (ubuntu)

# 1. Mise en place de PostgreSQL et préparation de l'environnement

## Installer PostgreSQL et ses outils
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

## Vérifier le statut du service PostgreSQL
```bash
sudo systemctl status postgresql
```

## Créer un utilisateur PostgreSQL
```bash
sudo -u postgres createuser --interactive
```

# ⚠️ Mettre 'username' comme username et entrez 'y' pour être superutilisateur

# 2. Création de la base de données

## Connectez-vous au terminal interactif de PostgreSQL
```bash
sudo -u postgres psql
```

# Définir 'password' par vos identifiants PostgreSQL.
```bash
\password username
```

# ⚠️ Mettre 'password' comme mot de passe.


## Créez la base de données
```bash
CREATE DATABASE ludo_stats;
```

## Quittez le terminal PostgreSQL
```bash
\q
```

# 3. Configuration du fichier secret

## Créez un fichier de configuration pour stocker l'URL de connexion
```bash
mkdir -p ./db/secret
echo 'DATABASE_URL = "postgresql://username:password@localhost:5432/ludo_stats"' > ./db/secret/config.py
```

# 4. Initialisation de la structure de la base de données

```bash
cd db
```

## Lancez le script Python pour créer les tables dans la base de données
```bash
python schema.py
```

# 5. Vérification de la connexion à la base de données

## Reconnectez-vous à PostgreSQL pour tester la base
```bash
sudo -u postgres psql
```

## Dans le terminal PostgreSQL, connectez-vous à la base
```bash
\c ludo_stats
```

## Affichez la liste des tables
```bash
\dt
```

# 6. Lancer les simulations de parties

## Exécutez le script Python pour simuler des parties et enregistrer les résultats dans la base
```bash
python ludo_stats_play.py
```

# 7. Exporter les données de la base de données

## Utilisez le script Python d'exportation pour sauvegarder les données au format CSV
```bash
python export.py
```

# 8. Gestion de la base de données

## Vider toutes les tables
```bash
sudo -u postgres psql -d ludo_stats -c "TRUNCATE TABLE action_stats, game, game_rule, is_rule_of, participant, player, set_of_rules;"
```

## Supprimer complètement la base de données si nécessaire
```bash
sudo -u postgres psql -c "DROP DATABASE ludo_stats;"
```
