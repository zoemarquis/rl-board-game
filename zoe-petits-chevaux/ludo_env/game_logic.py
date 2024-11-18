import numpy as np
from constants import *

class State(Enum):
    HOME = 0  # Le pion est dans sa maison, prêt à partir
    PATH = 1  # Le pion est en chemin
    SAFEZONE = 2  # Le pion est dans la zone protégée avant d'atteindre la destination
    SAFE = 3  # Le pion a atteint sa destination finale et ne bouge plus

class Action(Enum):
    MOVE_OUT = 0  # Sortir de la maison
    MOVE_FORWARD = 1  # Avancer le long du chemin
    REACH_GOAL = 3  # Atteindre l'objectif final
    ENTER_SAFEZONE = 2  # Entrer dans la zone protégée
    PROTECT = 4  # Protéger un pion allié
    KILL = 4  # Tuer un pion adverse
    DIE = 5  # Se faire tuer
    NO_ACTION = 6  # Ne rien faire : TODO est ce que c'est utile ? possible ? on a le droit de ne pas bouger si on a la possibilité ?

action_table = {
    State.HOME: [Action.MOVE_OUT],
    State.PATH: [Action.MOVE_FORWARD, Action.ENTER_SAFEZONE],
    State.SAFEZONE: [Action.REACH_GOAL],
    State.SAFE: []  # Aucun mouvement autorisé
}

REWARD_TABLE = {
    Action.MOVE_OUT: 50,
    Action.MOVE_FORWARD: 5,
    Action.ENTER_SAFEZONE: 10,
    Action.REACH_GOAL: 50,
    Action.PROTECT: 20,
    Action.KILL: 30,
    Action.DIE: -20 # TODO -> reward pas d'action enfaite, on le subit pendant un tour
}


class GameLogic:

    def init_board(self):
        self.board_path = [[] for _ in range(BOARD_SIZE)]
        self.board_home = []
        for i in range(NUM_PLAYERS):
            self.board_home.extend([i] * NB_PAWNS)
        self.board_safe_zone = [[] for _ in range(SAFE_ZONE_SIZE)]
        self.board_goal = []


    def get_pawns_info(self, player_id):
        player_pawns = []
        count_home = self.board_home.count(player_id)
        for _ in range(count_home):
            player_pawns.append({
                "position": 0,
                "state": State.HOME
            })
        for i in range(len(self.board_path)):
            count_path = self.board_path[i].count(player_id)
            for _ in range(count_path):
                player_pawns.append({
                    "position": i,
                    "state": State.PATH
                })
        for i in range(len(self.board_safe_zone)):
            if player_id in self.board_safe_zone[i]:
                player_pawns.append({
                    "position": i,
                    "state": State.SAFEZONE
                })

        assert len(player_pawns) == NB_PAWNS, "Nombre de pions incorrect"


    def get_plateau_player(self, player_id):
        # en 0 : ceux en home
        # de 1 à 56 -> path
        # de 57 à 62 -> safezone
        # à 63 goal
        pass



    def dice_generator(self):
        return np.random.randint(1, 7)

    def get_valid_actions(self, board, player, dice_value) -> list[Action]:
        
        if dice_value == 6:
            # espace d'actions est alors 
            # sortir un pion
            # avancer un pion déjà sur le plateau
        else: 
            # espace d'actions est alors
            # avancer un pion déjà sur le plateau
            # si il y en a, sinon pass

        # TODO

    def get_invalid_actions(self, board, player, dice_value):
        # retourne liste de toutes les actions invalides en fonction du 

        # TODO -> pas obligatoire ?

    def get_deplacement(self, board, pieces, current_player, dice_value):

        # TODO

    def is_valid_move(self, board, pieces, current_player, piece_index, x, y, rotation, horizontal_flip, vertical_flip):

        # TODO

    def get_valid_actions(self, board, pieces, current_player):

        # TODO

    def is_game_over(self, board, pieces):
        for player in range(NUM_PLAYERS):
            for pawn in range(PAWNS_PER_PLAYER):
                if pieces[player][piece][0] != BOARD_SIZE:
                    return False
        # pour l'instant : est ce que le joueur a atteint la case == BOARD SIZE

        # TODO : tous les pions d'un joueur sont sur la case finale



# brouillon: 

    def is_opponent_pawn_on(target_position, player):
        # TODO 
        pass

    def is_pawn_threatened(player, position):
        # TODO
        pass

    def is_pawn_protected(player, position):
        # TODO
        pass
    

    def get_valid_actions_for_pawns(dice, player, position, state):
        # TODO : si on s'est fait die (au tour précédent : reward négatif ? est ce vrmt utile ?)

        valid_actions = []
        
        if state == State.HOME:
            if dice == 6:
                valid_actions.append(Action.MOVE_OUT)

        elif state == State.PATH:
            if position + dice <= 56: # limite avant zone protégée
                valid_actions.append(Action.MOVE_FORWARD)

            elif position + dice == 57:
                valid_actions.append(Action.ENTER_SAFEZONE)

            # est ce que tu tues un pion au passage ? -> alors ajouter kill
            if is_opponent_pawn_on(position+dice, player):
                valid_actions.append(Action.KILL)


        elif state == State.SAFEZONE:
            if position + dice <= 62:
                valid_actions.append(Action.MOVE_FORWARD)

            if position + dice >= 63:
                valid_actions.append(Action.REACH_GOAL)

        elif state == State.GOAL:
            pass # on peut recevoir des rewards pour pions déjà placés ?

        # on peut reward si on protége un pion (HOME + PATH POSSIBLE)
        if is_pawn_protected(player, position + dice):
            valid_actions.append(Action.PROTECT)

        return valid_actions
    

def get_valid_action_for_player(dice, player, player_pawns):
        actions_for_pawns = {}
        
        for i, pawn in enumerate(player_pawns):
            valid_actions = get_valid_actions_for_pawns(dice, player, pawn["position"], pawn["state"]) # TODO get that
            actions_for_pawns[i] = valid_actions

        # TODO : si tout vide -> passer son tour -> reward -1 ?
        return actions_for_pawns




def calculate_rewards(action, board, player_id, strategy):
    # si un pion a subit un DIE pendant le dernier tour -> reward négatif global ?
    pawn_index, target_position = action

    # TODO : ici on va pouvoir implémneter les différents agents 

    pass


def encode_possible_actions(self, possible_actions):
        action_vector = np.zeros(4, dtype=np.int32)  # Taille fixe pour 4 actions
        action_mapping = {"MOVE_OUT": 0, "MOVE": 1, "REACH_GOAL": 2, "NO_ACTION": 3}
        for action in possible_actions:
            action_vector[action_mapping[action]] = 1
        return action_vector

def decode_possible_actions(self, action_vector):
    pass