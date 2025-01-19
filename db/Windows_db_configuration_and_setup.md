# Configuration et utilisation de la base de données `ludo_stats` (Windows)

## 1. Préparation de la base de données

### Installation de PostgreSQL
1. Installer PostgreSQL sur votre machine.
2. Créer un utilisateur PostgreSQL.

### Création de la base de données

Connectez vous au terminal interactif de PostgreSQL en exécutant la commande suivante dans un terminal :

```bash
psql -U postgres
```

Exécutez la commande suivante dans le terminal PostgreSQL pour créer la base :

```sql
CREATE DATABASE ludo_stats;
```

### Configuration du fichier secret
Créer un fichier `secret/config.py` dans le dossier `./db` contenant la ligne suivante :

```python
DATABASE_URL = "postgresql://username:password@localhost:5432/ludo_stats"
```

> ⚠️ **Remplacez `username` et `password`** par vos identifiants PostgreSQL.

### Initialisation de la structure de la base de données
Lancez le script `schema.py` pour créer les tables nécessaires dans la base de données :

```bash
cd db
python schema.py
```

## 2. Connexion à la base de données pour tester
Pour vérifier que la base a été correctement créée :

```bash
psql -U postgres
```

Puis, dans le terminal PostgreSQL :

```sql
\c ludo_stats
```

Un message confirmant la connexion à la base `ludo_stats` devrait s’afficher.

Vous pouvez ensuite exécuter des requêtes SQL sur les tables de la base.  
Pour afficher la liste des tables disponibles, utilisez la commande suivante : `\dt`.

---

## 3. Lancer les simulations de parties
Utilisez le script `ludo_stats_play.py` pour exécuter des simulations de parties entre agents et enregistrer les résultats dans la base de données :

```bash
python ludo_stats_play.py
```
---

## 4. Exporter les données de la base de données

Pour exporter les données de la base au format CSV, utilisez le script `export.py` :

```bash
python export.py
```
---

## 5. Gestion de la base de données
### Vider les tables

Pour réinitialiser la base en supprimant toutes les données :

```bash
truncate table action_stats, game, game_rule, is_rule_of, participant, player, set_of_rules;
```

### Supprimer la base de données
Pour supprimer complètement la base :

```sql
DROP DATABASE ludo_stats;
```
---