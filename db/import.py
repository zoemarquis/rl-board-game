import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from secret.config import DATABASE_URL


import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.schema import Player, create_engine

# Créez une session
Session = sessionmaker(bind=create_engine(DATABASE_URL))


def import_players_from_csv(file_path):
    session = Session()
    try:
        # Lire le fichier CSV
        df = pd.read_csv(file_path)

        # Parcourir chaque ligne du DataFrame et ajouter des instances de Player
        for index, row in df.iterrows():
            player = Player(
                name=row["name"],
                is_human=row[
                    "is_human"
                ],  # Assurez-vous que la valeur est compatible avec l'Enum
                strategy=row["strategy"],
                description=row["description"],
                difficulty=row["difficulty"],
            )
            session.add(player)

        # Committer les changements à la base de données
        session.commit()
        print(f"{len(df)} joueurs ont été importés avec succès.")

    except IntegrityError as e:
        print(f"Erreur d'intégrité lors de l'importation : {e}")
        session.rollback()  # Annuler les changements en cas d'erreur
    except Exception as e:
        print(f"Erreur lors de l'importation : {e}")
        session.rollback()  # Annuler les changements en cas d'erreur
    finally:
        session.close()  # Fermer la session


# Exemple d'utilisation
import_players_from_csv("data/players.csv")
