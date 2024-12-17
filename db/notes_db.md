# Configuration et exécution de la base de données `ludo_stats`

## 1. Préparation de la base de données

### Installation de PostgreSQL
1. Installer PostgreSQL sur votre machine.
2. Créer un utilisateur

### Création de la base de données
Ouvrir un terminal et exécuter les commandes suivantes :

```bash
psql -U postgres
```

Ensuite, dans le terminal `psql` :

```sql
CREATE DATABASE ludo_stats;
```

### Configuration du fichier secret
Créer un fichier `secret/config.py`, dans le dossier `./db`, contenant la ligne suivante :

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/ludo_stats"
```

> ⚠️ **Remplacez `username` et `password`** par vos identifiants PostgreSQL.

### Initialisation de la base de données
Exécuter le script `schema.py` pour créer les tables dans la base de données :

```bash
python schema.py
```

### Connexion à la base de données pour tester
Vérifiez que la base de données a été correctement créée :

```bash
psql -U postgres
```

Puis, dans le terminal `psql` :

```sql
\c ludo_stats
```

Vous devriez voir un message confirmant la connexion à la base de données `ludo_stats`.

---

## 2. Exécution du code de simulation de parties

### Lancer les simulations de parties
Le script principal à exécuter est `ludo_stats_play.py`, situé dans le répertoire `./db`. Utilisez la commande suivante :

```bash
python ludo_stats_play.py
```

---

## 3. Configuration des agents

Les configurations des agents sont définies dans le fichier `config_game.py`. =

---

## 4. Importer et exporter les données de la base de données

- **Exporter la base de données en CSV** : Utilisez `export.py`.
- **Importer des données depuis un CSV** : Utilisez `import.py`.

---

## 5. TODO

- Voir dans les fichiers les TODO
- Description de game_rule utile ?
- Checker le nombre de parties jouées par les agents
- Checker contre qui jouent les agents

- Statistiques intéressantes
    - 1 conf avec différents types d'agents : mouvements choisis, qui gagne
    - 1 type d'agent différentes conf : nombre d'erreurs
    - 1 type d'agent, 1 conf mais steps entrainement différent : nombre erreurs, qui gagne, mouvements choisis

- Ajouter le type d'agent dans la BD
- Ecrire document qui résume tout ce que j'ai fais

