import os
import pandas as pd
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from schema import Base, Player, Participant, Game, SetOfRules, IsRuleOf, GameRule, ActionStats

from secret.config import DATABASE_URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def export_table_to_csv(session, table_class, file_path):
    try:

        inspector = inspect(session.bind)
        table_name = table_class.__tablename__
        columns = [col["name"] for col in inspector.get_columns(table_name)]

        query = session.query(table_class).all()

        df = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in query])

        df.to_csv(file_path, index=False)
        print(f"Exportation réussie de {table_name} vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation de {table_class.__tablename__} : {e}")


def export_all_tables_to_csv(output_dir):
    session = Session()
    try:
        tables = {
            "player": Player,
            "participant": Participant,
            "game": Game,
            "set_of_rules": SetOfRules,
            "is_rule_of": IsRuleOf,
            "game_rule": GameRule,
            "action_stats": ActionStats,
            # INFO : Ajouter les nouvelles tables ici
        }

        for table_name, table_class in tables.items():
            file_path = os.path.join(output_dir, f"{table_name}.csv")
            export_table_to_csv(session, table_class, file_path)
    except Exception as e:
        print(f"Erreur lors de l'exportation des tables : {e}")
    finally:
        session.close()


if __name__ == "__main__":
    output_directory = "data"
    os.makedirs(output_directory, exist_ok=True)

    export_all_tables_to_csv(output_directory)
