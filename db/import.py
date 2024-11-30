import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from schema import (
    Player,
    Participant,
    Game,
    SetOfRules,
    IsRuleOf,
    GameRule,
    create_engine,
)

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


def import_participants_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            participant = Participant(
                game_id=row["game_id"],
                player_id=row["player_id"],
                turn_order=row["turn_order"],
                score=row["score"],
                nb_moves=row["nb_moves"],
                is_winner=row["is_winner"],
            )
            session.add(participant)

        session.commit()
        print(f"{len(df)} participants import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


def import_games_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            game = Game(
                game_id=row["game_id"],
                set_of_rules_id=row["set_of_rules_id"],
                played_at=row["played_date"],
                nb_participants=row["nb_participants"],
            )
            session.add(game)

        session.commit()
        print(f"{len(df)} games import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


def import_set_of_rules_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            set_of_rules = SetOfRules(
                set_of_rules_id=row["set_of_rules_id"],
                name=row["name"],
                description=row["description"],
            )
            session.add(set_of_rules)

        session.commit()
        print(f"{len(df)} set of rules import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


def import_is_rule_of_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            is_rule_of = IsRuleOf(
                set_of_rules_id=row["set_of_rules_id"],
                game_rule_id=row["game_rule_id"],
            )
            session.add(is_rule_of)

        session.commit()
        print(f"{len(df)} is rule of import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


def import_game_rule_from_csv(file_path):
    session = Session()
    try:
        df = pd.read_csv(file_path)

        for _, row in df.iterrows():
            game_rule = GameRule(
                game_rule_id=row["game_rule_id"],
                name=row["name"],
                description=row["description"],
            )
            session.add(game_rule)

        session.commit()
        print(f"{len(df)} game rule import successfully")

    except IntegrityError as e:
        print(f"Integrity error during import: {e}")
        session.rollback()
    except Exception as e:
        print(f"Error during import: {e}")
        session.rollback()
    finally:
        session.close()


import_players_from_csv("data/players.csv")
import_participants_from_csv("data/participants.csv")
import_games_from_csv("data/games.csv")
import_set_of_rules_from_csv("data/set_of_rules.csv")
import_is_rule_of_from_csv("data/is_rule_of.csv")
import_game_rule_from_csv("data/game_rule.csv")
