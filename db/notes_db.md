# Installation de postgreSQL
# Création d'un utilisateur
# Création de la base de données
Terminal :
psql -U postgres
> CREATE DATABASE ludo_stats;

Création d'un fichier secret/config.py avec la ligne suivante dedans :
postgresql://username:password@localhost:5432/ludo_stats <-- CHANGER USERNAME ET PASSSWORD

Exécution du script dans le terminal :
python schema.py

# Connection à la BD pour tester :
postgres=# \c ludo_stats
You are now connected to database "ludo_stats" as user "postgres".

# Lancer le code dans ./db
python ludo_stats_play.py

--> Les configs de parties sont définies dans config_game.py


TODO :
- Voir dans les fichiers les TODO
- Voir comment enregistrer la BD pour la partager
- Description de game_rule utile ?
- Gérer correctement les players et participants