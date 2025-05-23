import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from secret.config import DATABASE_URL

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from datetime import datetime
from schema import Player, Participant, Game, SetOfRules, IsRuleOf, GameRule, ActionStats
import rules

racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game"))
sys.path.append(racine_dir)
from ludo_env.action import Action_NO_EXACT, Action_EXACT, Action_EXACT_ASCENSION

Session = sessionmaker(bind=create_engine(DATABASE_URL))


class PlayerToInsert:
    def __init__(
        self,
        name: str,
        is_human: bool,
        turn_order: int,
        nb_moves: int,
        is_winner: bool,
        reward_action_agent: int = None,
        reward_rectified: int = None,
        player_id: int = None,
        nb_train_steps: int = None,
        nb_actions_interdites: int = 0,
        strategy: str = None,
        nb_pawns_in_goal: int = 0,
    ):
        assert name is not None, "name must be provided"
        assert is_human is not None, "is_human must be provided"
        assert 1 <= turn_order <= 4, "turn_order must be between 1 and 4"
        if is_human is True:
            assert reward_action_agent is None, "score must be None if is_human is True"
        else:
            assert reward_action_agent is not None, "score must be provided if is_human is False"
        assert nb_moves >= 1, "nb_moves must be greater than or equal to 1"

        self.player_id = player_id
        self.name = name
        self.is_human = is_human
        self.turn_order = turn_order
        self.reward_action_agent = reward_action_agent
        self.reward_rectified = reward_rectified
        self.nb_moves = nb_moves
        self.is_winner = is_winner
        self.nb_train_steps = nb_train_steps
        self.nb_actions_interdites = nb_actions_interdites
        self.strategy = strategy
        self.nb_pawns_in_goal = nb_pawns_in_goal

    def get_or_create_human_player(self, session) -> int:
        if not self.is_human:
            raise ValueError("This method is for human players only.")

        player = (
            session.query(Player)
            .filter(Player.name == self.name, Player.is_human == True)
            .first()
        )
        if not player:
            player = Player(name=self.name, is_human=self.is_human)
            session.add(player)
            session.commit()
            print(f"Joueur ajouté : {player.name}")
        else:
            print(f"Joueur existant : {player.name}")
        self.player_id = player.player_id
        return self.player_id

class SetOfRulesToInsert:
    def __init__(self, rules_ids: list[int], set_of_rules_id: int = None, num_config: int = None):
        if len(rules_ids) == 0:
            assert (
                set_of_rules_id is not None
            ), "set_of_rules_id must be provided if rules_ids is empty"
        self.set_of_rules_id = set_of_rules_id
        self.rules_ids = rules_ids
        self.num_config = num_config

    def get_or_create_set_of_rules(self, session) -> int:
        if self.set_of_rules_id is not None:
            return self.set_of_rules_id

        # test s'il existe déjà une combinaison de ces règles
        existing_set_of_rules = (
            session.query(SetOfRules)
            .join(IsRuleOf)
            .filter(IsRuleOf.game_rule_id.in_(self.rules_ids))
            .group_by(SetOfRules.set_of_rules_id)
            .having(func.count(SetOfRules.set_of_rules_id) == len(self.rules_ids))
            .first()
        )
        if existing_set_of_rules:
            print(f"Un set de règles existant contient déjà ces règles.")
            return existing_set_of_rules.set_of_rules_id

        # vérif que les règles existent
        for rule_id in self.rules_ids:
            rule = session.query(GameRule).filter(GameRule.game_rule_id == rule_id).first()
            if rule is None:
                # si la règle existe pas, on l'ajoute
                rule_name = rules.ALL_RULES.get(rule_id, f"Règle inconnue {rule_id}")
                rule = GameRule(
                    game_rule_id=rule_id,
                    name=rule_name,
                    description=f"Description de {rule_name}",
                )
                session.add(rule)
                print(f"Règle créée : ID={rule_id}, Name={rule_name}")

        session.commit()

        # si pas de combinaison existante, on crée un nouveau set de règles (avec name et description par défaut)
        new_set_of_rules = SetOfRules(
            name=",".join(map(str, self.rules_ids)),
            description=rules.generate_rule_description(self.rules_ids, rules.ALL_RULES),
            num_config=self.num_config,
        )
        session.add(new_set_of_rules)
        session.commit()

        # on crée les liens entre les règles et le set de règles
        for rule_id in self.rules_ids:
            is_rule_of = IsRuleOf(
                set_of_rules_id=new_set_of_rules.set_of_rules_id, game_rule_id=rule_id
            )
            session.add(is_rule_of)
        session.commit()

        print(f"Nouveau set de règles créé : {new_set_of_rules.set_of_rules_id}")
        return new_set_of_rules.set_of_rules_id


class ParticipantToInsert:
    def __init__(self, game_id: int, player: PlayerToInsert, nb_actions_interdites: int = 0):
        self.game_id = game_id
        self.player_id = player.player_id
        self.turn_order = player.turn_order
        self.reward_action_agent = player.reward_action_agent
        self.reward_rectified = player.reward_rectified
        self.nb_moves = player.nb_moves
        self.is_winner = player.is_winner
        self.nb_actions_interdites = nb_actions_interdites
        self.nb_pawns_in_goal = player.nb_pawns_in_goal

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
                reward_action_agent=self.reward_action_agent,
                reward_rectified=self.reward_rectified,
                nb_moves=self.nb_moves,
                is_winner=self.is_winner,
                nb_actions_interdites=self.nb_actions_interdites,
                nb_pawns_in_goal=self.nb_pawns_in_goal,
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
    actions_stats_by_player: dict,
    nb_pawns: int,
    num_config: int,
):
    with Session() as session:
        rules.num_config = num_config
        set_of_rules_id = rules.get_or_create_set_of_rules(session)
        
        game = Game(
            set_of_rules_id=set_of_rules_id,
            nb_participants=len(players),
            nb_pawns=nb_pawns,
        )
        session.add(game)
        session.commit()
        game_id = game.game_id

        num_player_game = 1
        for player in players:
            if player.is_human:
                player_id = player.get_or_create_human_player(session)
            else:
                
                db_player = session.query(Player).filter(Player.name == player.name).first()
                
                # Ajout de l'agent s'il n'est pas déjà dans la BD
                if not db_player:
                    db_player = Player(
                        name=player.name, 
                        is_human=False, 
                        strategy=player.strategy,
                        nb_train_steps=player.nb_train_steps                        
                    )
                    session.add(db_player)
                    session.commit()
                
                player_id = db_player.player_id

            stats = actions_stats_by_player.get(player.turn_order - 1, {})

            
            action_stats = ActionStats(
                # Actions demandées
                nb_no_action_d = stats["requested"].get('Action_NO_EXACT.NO_ACTION', 0) + stats["requested"].get('Action_EXACT.NO_ACTION', 0) + stats["requested"].get('Action_EXACT_ASCENSION.NO_ACTION', 0),
                nb_move_out_d = stats["requested"].get('Action_NO_EXACT.MOVE_OUT', 0) + stats["requested"].get('Action_EXACT.MOVE_OUT', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MOVE_OUT', 0),
                nb_move_out_and_kill_d = stats["requested"].get('Action_NO_EXACT.MOVE_OUT_AND_KILL', 0) + stats["requested"].get('Action_EXACT.MOVE_OUT_AND_KILL', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL', 0),
                nb_move_forward_d = stats["requested"].get('Action_NO_EXACT.MOVE_FORWARD', 0) + stats["requested"].get('Action_EXACT.MOVE_FORWARD', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MOVE_FORWARD', 0),
                nb_get_stuck_behind_d = stats["requested"].get('Action_NO_EXACT.GET_STUCK_BEHIND', 0) + stats["requested"].get('Action_EXACT.GET_STUCK_BEHIND', 0) + stats["requested"].get('Action_EXACT_ASCENSION.GET_STUCK_BEHIND', 0),
                nb_enter_safezone_d = stats["requested"].get('Action_NO_EXACT.ENTER_SAFEZONE', 0) + stats["requested"].get('Action_EXACT.ENTER_SAFEZONE', 0) + stats["requested"].get('Action_EXACT_ASCENSION.ENTER_SAFEZONE', 0),
                nb_move_in_safe_zone_d = stats["requested"].get('Action_NO_EXACT.MOVE_IN_SAFE_ZONE', 0) + stats["requested"].get('Action_EXACT.MOVE_IN_SAFE_ZONE', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MOVE_IN_SAFE_ZONE', 0),
                nb_reach_goal_d = stats["requested"].get('Action_NO_EXACT.REACH_GOAL', 0) + stats["requested"].get('Action_EXACT.REACH_GOAL', 0) + stats["requested"].get('Action_EXACT_ASCENSION.REACH_GOAL', 0),
                nb_kill_d = stats["requested"].get('Action_NO_EXACT.KILL', 0) + stats["requested"].get('Action_EXACT.KILL', 0) + stats["requested"].get('Action_EXACT_ASCENSION.KILL', 0),
                nb_reach_pied_escalier_d = stats["requested"].get('Action_NO_EXACT.REACH_PIED_ESCALIER', 0) + stats["requested"].get('Action_EXACT.REACH_PIED_ESCALIER', 0) + stats["requested"].get('Action_EXACT_ASCENSION.REACH_PIED_ESCALIER', 0),
                nb_avance_recule_pied_escalier_d = stats["requested"].get('Action_NO_EXACT.AVANCE_RECULE_PIED_ESCALIER', 0) + stats["requested"].get('Action_EXACT.AVANCE_RECULE_PIED_ESCALIER', 0) + stats["requested"].get('Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER', 0),
                nb_marche_1_d = stats["requested"].get('Action_NO_EXACT.MARCHE_1', 0) + stats["requested"].get('Action_EXACT.MARCHE_1', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_1', 0),
                nb_marche_2_d = stats["requested"].get('Action_NO_EXACT.MARCHE_2', 0) + stats["requested"].get('Action_EXACT.MARCHE_2', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_2', 0),
                nb_marche_3_d = stats["requested"].get('Action_NO_EXACT.MARCHE_3', 0) + stats["requested"].get('Action_EXACT.MARCHE_3', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_3', 0),
                nb_marche_4_d = stats["requested"].get('Action_NO_EXACT.MARCHE_4', 0) + stats["requested"].get('Action_EXACT.MARCHE_4', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_4', 0),
                nb_marche_5_d = stats["requested"].get('Action_NO_EXACT.MARCHE_5', 0) + stats["requested"].get('Action_EXACT.MARCHE_5', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_5', 0),
                nb_marche_6_d = stats["requested"].get('Action_NO_EXACT.MARCHE_6', 0) + stats["requested"].get('Action_EXACT.MARCHE_6', 0) + stats["requested"].get('Action_EXACT_ASCENSION.MARCHE_6', 0),
                
                # Actions réalisées
                nb_no_action_e = stats["realized"].get('Action_NO_EXACT.NO_ACTION', 0) + stats["realized"].get('Action_EXACT.NO_ACTION', 0) + stats["realized"].get('Action_EXACT_ASCENSION.NO_ACTION', 0),
                nb_move_out_e = stats["realized"].get('Action_NO_EXACT.MOVE_OUT', 0) + stats["realized"].get('Action_EXACT.MOVE_OUT', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MOVE_OUT', 0),
                nb_move_out_and_kill_e = stats["realized"].get('Action_NO_EXACT.MOVE_OUT_AND_KILL', 0) + stats["realized"].get('Action_EXACT.MOVE_OUT_AND_KILL', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL', 0),
                nb_move_forward_e = stats["realized"].get('Action_NO_EXACT.MOVE_FORWARD', 0) + stats["realized"].get('Action_EXACT.MOVE_FORWARD', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MOVE_FORWARD', 0),
                nb_get_stuck_behind_e = stats["realized"].get('Action_NO_EXACT.GET_STUCK_BEHIND', 0) + stats["realized"].get('Action_EXACT.GET_STUCK_BEHIND', 0) + stats["realized"].get('Action_EXACT_ASCENSION.GET_STUCK_BEHIND', 0),
                nb_enter_safezone_e = stats["realized"].get('Action_NO_EXACT.ENTER_SAFEZONE', 0) + stats["realized"].get('Action_EXACT.ENTER_SAFEZONE', 0) + stats["realized"].get('Action_EXACT_ASCENSION.ENTER_SAFEZONE', 0),
                nb_move_in_safe_zone_e = stats["realized"].get('Action_NO_EXACT.MOVE_IN_SAFE_ZONE', 0) + stats["realized"].get('Action_EXACT.MOVE_IN_SAFE_ZONE', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MOVE_IN_SAFE_ZONE', 0),
                nb_reach_goal_e = stats["realized"].get('Action_NO_EXACT.REACH_GOAL', 0) + stats["realized"].get('Action_EXACT.REACH_GOAL', 0) + stats["realized"].get('Action_EXACT_ASCENSION.REACH_GOAL', 0),
                nb_kill_e = stats["realized"].get('Action_NO_EXACT.KILL', 0) + stats["realized"].get('Action_EXACT.KILL', 0) + stats["realized"].get('Action_EXACT_ASCENSION.KILL', 0),
                nb_reach_pied_escalier_e = stats["realized"].get('Action_NO_EXACT.REACH_PIED_ESCALIER', 0) + stats["realized"].get('Action_EXACT.REACH_PIED_ESCALIER', 0) + stats["realized"].get('Action_EXACT_ASCENSION.REACH_PIED_ESCALIER', 0),
                nb_avance_recule_pied_escalier_e = stats["realized"].get('Action_NO_EXACT.AVANCE_RECULE_PIED_ESCALIER', 0) + stats["realized"].get('Action_EXACT.AVANCE_RECULE_PIED_ESCALIER', 0) + stats["realized"].get('Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER', 0),
                nb_marche_1_e = stats["realized"].get('Action_NO_EXACT.MARCHE_1', 0) + stats["realized"].get('Action_EXACT.MARCHE_1', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_1', 0),
                nb_marche_2_e = stats["realized"].get('Action_NO_EXACT.MARCHE_2', 0) + stats["realized"].get('Action_EXACT.MARCHE_2', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_2', 0),
                nb_marche_3_e = stats["realized"].get('Action_NO_EXACT.MARCHE_3', 0) + stats["realized"].get('Action_EXACT.MARCHE_3', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_3', 0),
                nb_marche_4_e = stats["realized"].get('Action_NO_EXACT.MARCHE_4', 0) + stats["realized"].get('Action_EXACT.MARCHE_4', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_4', 0),
                nb_marche_5_e = stats["realized"].get('Action_NO_EXACT.MARCHE_5', 0) + stats["realized"].get('Action_EXACT.MARCHE_5', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_5', 0),
                nb_marche_6_e = stats["realized"].get('Action_NO_EXACT.MARCHE_6', 0) + stats["realized"].get('Action_EXACT.MARCHE_6', 0) + stats["realized"].get('Action_EXACT_ASCENSION.MARCHE_6', 0),
            )

            session.add(action_stats)
            session.commit()

            participant = Participant(
                game_id=game_id,
                player_id=player_id,
                turn_order=player.turn_order,
                reward_action_agent=player.reward_action_agent,
                reward_rectified=player.reward_rectified,
                nb_moves=player.nb_moves,
                is_winner=player.is_winner,
                nb_actions_interdites = player.nb_actions_interdites,
                action_stats=action_stats.stat_id,
                nb_pawns_in_goal = player.nb_pawns_in_goal
            )
            participant.num_player_game = num_player_game
            session.add(participant)
            num_player_game += 1

        session.commit()
        print(f"Données enregistrées avec l'ID (game) : {game_id}")
