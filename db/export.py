import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from secret.config import DATABASE_URL

import pandas as pd
from sqlalchemy.orm import sessionmaker
from schema import Player, create_engine

# Créez une session
Session = sessionmaker(bind=create_engine(DATABASE_URL))


def export_players_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        players = session.query(Player).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "player_id": player.player_id,
                    "name": player.name,
                    "type": player.is_human,
                    "strategy": player.strategy,
                    "description": player.description,
                    "difficulty": player.difficulty,
                    "registration_date": player.registration_date,
                }
                for player in players
            ]
        )

        # Exporter vers un fichier CSV
        df.to_csv(file_path, index=False)
        print(f"Exportation réussie vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        session.close()


# Exemple d'utilisation
export_players_to_csv("data/players.csv")
