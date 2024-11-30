import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from secret.config import DATABASE_URL

import pandas as pd
from sqlalchemy.orm import sessionmaker
from schema import (
    Player,
    Participant,
    Game,
    SetOfRules,
    IsRuleOf,
    GameRule,
    create_engine,
)

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
                    "is_human": player.is_human,
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


def export_participants_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        participants = session.query(Participant).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "game_id": participant.game_id,
                    "player_id": participant.player_id,
                    "turn_order": participant.turn_order,
                    "score": participant.score,
                    "nb_moves": participant.nb_moves,
                    "is_winner": participant.is_winner,
                }
                for participant in participants
            ]
        )

        # Exporter vers un fichier CSV
        df.to_csv(file_path, index=False)
        print(f"Exportation réussie vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        session.close()


def export_games_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        games = session.query(Game).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "game_id": game.game_id,
                    "set_of_rules_id": game.set_of_rules_id,
                    "played_at": game.played_at,
                    # TODO : to add ?"duration": game.duration,
                    "nb_participants": game.nb_participants,
                }
                for game in games
            ]
        )

        # Exporter vers un fichier CSV
        df.to_csv(file_path, index=False)
        print(f"Exportation réussie vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        session.close()


def export_set_of_rules_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        set_of_rules = session.query(SetOfRules).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "set_of_rules_id": set_of_rule.set_of_rules_id,
                    "name": set_of_rule.name,
                    "description": set_of_rule.description,
                }
                for set_of_rule in set_of_rules
            ]
        )

        # Exporter vers un fichier CSV
        df.to_csv(file_path, index=False)
        print(f"Exportation réussie vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        session.close()


def export_is_rule_of_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        is_rule_of = session.query(IsRuleOf).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "set_of_rules_id": is_rule_of.set_of_rules_id,
                    "game_rule_id": is_rule_of.game_rule_id,
                }
                for is_rule_of in is_rule_of
            ]
        )

        # Exporter vers un fichier CSV
        df.to_csv(file_path, index=False)
        print(f"Exportation réussie vers {file_path}")
    except Exception as e:
        print(f"Erreur lors de l'exportation : {e}")
    finally:
        session.close()


def export_game_rules_to_csv(file_path):
    session = Session()
    try:
        # Récupérer les données de la base de données
        game_rules = session.query(GameRule).all()

        # Convertir les données en DataFrame
        df = pd.DataFrame(
            [
                {
                    "game_rule_id": game_rule.game_rule_id,
                    "name": game_rule.name,
                    "description": game_rule.description,
                }
                for game_rule in game_rules
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
export_participants_to_csv("data/participants.csv")
export_games_to_csv("data/games.csv")
export_set_of_rules_to_csv("data/set_of_rules.csv")
export_is_rule_of_to_csv("data/is_rule_of.csv")
export_game_rules_to_csv("data/game_rules.csv")
