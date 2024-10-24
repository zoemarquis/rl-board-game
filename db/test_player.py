from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Player  # Assurez-vous d'importer votre modèle Player
from secret.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

players = session.query(Player).all()

for player in players:
    print(
        f"ID: {player.player_id}, Name: {player.name}, Type: {player.is_human}, "
        f"Strategy: {player.strategy}, Description: {player.description}, "
        f"Difficulty: {player.difficulty},"
        f"Registration Date: {player.registration_date}"
    )

session.close()
