import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from datetime import datetime
from schema import Player, Participant, Game, SetOfRules, IsRuleOf, GameRule

Session = sessionmaker(bind=create_engine(DATABASE_URL))


class PlayerToInsert:
    def __init__(
        self,
        name: str,
        is_human: bool,
        turn_order: int,
        nb_moves: int,
        is_winner: bool,
        score: int = None,
        player_id: int = None,
    ):
        assert name is not None, "name must be provided"
        assert is_human is not None, "is_human must be provided"
        if player_id is None:
            assert is_human == True, "player_id must be provided if is_human is False"
        else:
            assert (
                is_human == False
            ), "player_id must not be provided if is_human is True"
        assert 1 <= turn_order <= 4, "turn_order must be between 1 and 4"
        if is_human is True:
            assert score is None, "score must be None if is_human is True"
        else:
            assert score is not None, "score must be provided if is_human is False"
        assert nb_moves >= 1, "nb_moves must be greater than or equal to 1"

        self.player_id = player_id
        self.name = name
        self.is_human = is_human
        self.turn_order = turn_order
        self.score = score
        self.nb_moves = nb_moves
        self.is_winner = is_winner

    def get_or_create_human_player(self, session) -> int:
        if not self.is_human:
            raise ValueError("This method is for human players only.")

        player = (
            session.query(Player)
            .filter(Player.name == self.name, Player.is_human == True)
            .first()
        )

        if player is None:
            # Si le joueur n'existe pas, on l'ajoute
            player = Player(name=self.name, is_human=self.is_human)
            session.add(player)
            print(f"Joueur ajouté : {player.name}")
        else:
            print(f"Joueur existant : {player.name}")
        return player.player_id


class SetOfRulesToInsert:
    def __init__(self, rules_ids: list[int], set_of_rules_id: int = None):
        if len(rules_ids) == 0:
            assert (
                set_of_rules_id is not None
            ), "set_of_rules_id must be provided if rules_ids is empty"
        self.set_of_rules_id = set_of_rules_id
        self.rules_ids = rules_ids

    def get_or_create_set_of_rules(self, session) -> int:
        if self.set_of_rules_id is not None:
            return self.set_of_rules_id

        # test s'il existe déjà une combinaison de ces règles
        existing_set_of_rules = (
            session.query(SetOfRules)
            .join(IsRuleOf)
            .filter(IsRuleOf.rule_id.in_(self.rules_ids))
            .group_by(SetOfRules.set_of_rules_id)
            .having(func.count(SetOfRules.set_of_rules_id) == len(self.rules_ids))
            .first()
        )
        if existing_set_of_rules:
            print(f"Un set de règles existant contient déjà ces règles.")
            return existing_set_of_rules.set_of_rules_id

        # vérif que les règles existent
        for rule_id in self.rules_ids:
            rule = session.query(GameRule).filter(GameRule.rule_id == rule_id).first()
            if rule is None:
                raise ValueError(f"La règle {rule_id} n'existe pas.")

        # si pas de combinaison existante, on crée un nouveau set de règles
        new_set_of_rules = SetOfRules()
        session.add(new_set_of_rules)
        # on crée les liens entre les règles et le set de règles
        for rule_id in self.rules_ids:
            is_rule_of = IsRuleOf(
                set_of_rules_id=new_set_of_rules.set_of_rules_id, rule_id=rule_id
            )
            session.add(is_rule_of)
        print(f"Nouveau set de règles créé : {new_set_of_rules.set_of_rules_id}")
        return new_set_of_rules.set_of_rules_id


class ParticipantToInsert:
    def __init__(self, game_id: int, player: PlayerToInsert):
        self.game_id = game_id
        self.player_id = player.player_id
        self.turn_order = player.turn_order
        self.score = player.score
        self.nb_moves = player.nb_moves
        self.is_winner = player.is_winner

    def create_participant(self, session) -> int:
        participant = (
            session.query(Participant)
            .filter(
                Participant.game_id == self.game_id,
                Participant.player_id == self.player_id,
            )
            .first()
        )
        if participant is None:
            participant = Participant(
                game_id=self.game_id,
                player_id=self.player_id,
                turn_order=self.turn_order,
                score=self.score,
                nb_moves=self.nb_moves,
                is_winner=self.is_winner,
            )
            session.add(participant)
            print(
                f"Participant ajouté : {participant.player_id} pour le jeu {participant.game_id}"
            )
        else:
            raise ValueError("Participant déjà existant.")
        return participant.player_id


def store_final_game_data(
    rules: SetOfRulesToInsert,
    players: list[PlayerToInsert],
):
    with Session() as session:
        set_of_rules_id = rules.get_or_create_set_of_rules(session)
        game = Game(
            set_of_rules_id=set_of_rules_id,
            played_at=datetime.now(),
            nb_participants=len(players),
        )
        session.add(game)
        game_id = game.game_id
        for player in players:
            player.get_or_create_human_player(session)
            participant = ParticipantToInsert(game_id, player)
            participant.create_participant(session)

        session.commit()
        print("Données enregistrées.")
