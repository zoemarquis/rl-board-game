from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Player  # Assurez-vous d'importer votre modèle Player
from secret.config import DATABASE_URL

# Créer une connexion à la base de données
engine = create_engine(DATABASE_URL)

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()

# Récupérer tous les joueurs de la table player
players = session.query(Player).all()

# Afficher les informations des joueurs
for player in players:
    print(f"ID: {player.player_id}, Name: {player.name}, Type: {player.type}, "
          f"Strategy: {player.strategy}, Description: {player.description}, "
          f"Difficulty: {player.difficulty},"
          f"Registration Date: {player.registration_date}")

# Fermer la session
session.close()
