import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from db.schema import Player, create_engine

Session = sessionmaker(bind=create_engine(DATABASE_URL))


def import_players_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            player = Player(
                name=row["name"],
                is_human=row["is_human"],
                strategy=row["strategy"],
                description=row["description"],
                difficulty=row["difficulty"],
            )
            session.add(player)

        session.commit()
        print(f"{len(df)} players import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


import_players_from_csv("data/players.csv")
