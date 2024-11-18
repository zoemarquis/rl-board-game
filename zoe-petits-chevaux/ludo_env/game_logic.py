import numpy as np
from constants import *
from enum import Enum

class State(Enum):
    HOME = 0  # Le pion est dans sa maison, prêt à partir
    PATH = 1  # Le pion est en chemin
    SAFEZONE = 2  # Le pion est dans la zone protégée avant d'atteindre la destination
    SAFE = 3  # Le pion a atteint sa destination finale et ne bouge plus

    def get_state_from_position(self, relative_position : int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State.HOME
        elif relative_position < 57:
            return State.PATH
        elif relative_position < 63:
            return State.SAFEZONE
        else:
            return State.SAFE

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
        self.board = [[] for _ in range(NUM_PLAYERS)]
        for i in range(NUM_PLAYERS):
            self.board[i] = [0 for _ in range(TOTAL_SIZE)] # tableau de len TOTAL_SIZE
            self.board[i][0] = NB_PAWNS # on met les pions à HOME

    def get_pawns_info(self, player_id):
        pawns_info = []
        for i in range(TOTAL_SIZE):
            count_i = self.board[player_id][i]
            for _ in range(count_i):
                pawns_info.append({
                    "position": i,
                    "state": State.get_state_from_position(i)
                })  
        assert len(pawns_info) == NB_PAWNS, "Nombre de pions incorrect"

    def get_home_overview(self):
        home_overview = []
        for i in range(NUM_PLAYERS):
            for _ in range(self.board[i][0]):
                home_overview.append(i)
        return home_overview
    
    def get_goal_overview(self):
        goal_overview = []
        for i in range(NUM_PLAYERS):
            for _ in range(self.board[i][-1]):
                goal_overview.append(i)
        return goal_overview
    
    def get_safe_zone_overview(self):
        safe_zone_overview = [[] for _ in range(6)]
        for i in range(NUM_PLAYERS):
            for j in range(57, 63):
                for _ in range(self.board[i][j]):
                    safe_zone_overview[j-57].append(i)
        return safe_zone_overview

    def get_path_overview(self):
        # tout rabattre sur plateau du pion 0 pour "affichage"
        path_overview = [[] for _ in range(56)]
        for i in range(NUM_PLAYERS):
            for j in range(1, 57):
                for _ in range(self.board[i][j]):
                    if NUM_PLAYERS == 2:
                        indice = ((i*28)+j-1) % 56
                        path_overview[indice].append(i)
                    else : 
                        indice = ((i*14)+j-1) % 56
                        path_overview[indice].append(i)

    def print_board_overview(self):
        for i in range(NUM_PLAYERS):
            print("HOME : ", self.board[i][0])

        board_path = self.get_path_overview()
        for i in range(56//14):
            print(board_path[i*14:(i+1)*14])

        for i in range(NUM_PLAYERS):
            print("SAFEZONE : ", self.board[i][57:63])

        for i in range(NUM_PLAYERS):
            print("GOAL : ", self.board[i][-1])

    def dice_generator(self):
        return np.random.randint(1, 7)
    
    def move_pawn(self, player_id, pawn_position, dice_value, action): # ici pawn position ici c'est en absolu (1 à 56) (57 à 62): pas en relatif
        # TODO assert que c'est ok 

        # TODO à revoir logiqu avec les % des différents  avec relatif ce sera plus simple
        if action == Action.MOVE_OUT:
            assert self.board_home.count(player_id) > 0, "Pas de pion à sortir"
            self.board_home.remove(player_id)
            if player_id == 0:
                self.board_path[0].append(player_id)
            elif player_id == 1:
                if NUM_PLAYERS != 2:
                    self.board_path[14].append(player_id)
                else:
                    self.board_path[28].append(player_id)
            elif player_id == 2:
                self.board_path[28].append(player_id)
            elif player_id == 3:
                self.board_path[42].append(player_id)

        elif action == Action.MOVE_FORWARD:
            # on avance juste le pion de dice_value dans path (attention il doit rester dans limite)
            assert self.board_path[pawn_position].count(player_id) > 0, "Pas de pion à déplacer à cette position"
            # assert vérif pas kill TODO

            self.board_path[pawn_position - 1].remove(player_id)
            get_position_relative = (pawn_position + dice_value)%56
            self.board_path[get_position_relative].append(player_id)

        elif action == Action.ENTER_SAFEZONE:
            assert self.board_path[pawn_position].count(player_id) > 0, "Pas de pion à déplacer à cette position"
            # assert vérif pas kill TODO

            self.board_path[pawn_position - 1].remove(player_id)
            get_position_relative = 57
            self.board_safe_zone[get_position_relative].append(player_id)

        elif action == Action.REACH_GOAL:
            assert self.board_safe_zone[pawn_position].count(player_id) > 0, "Pas de pion à déplacer à cette position"
            # assert vérif pas kill TODO

            self.board_safe_zone[pawn_position - 57].remove(player_id)
            self.board_goal.append(player_id)

    def get_valid_actions_for_pawns(self, player_id, position, state, dice_value):
        # TODO : si on s'est fait die (au tour précédent : reward négatif ? est ce vrmt utile ?)

        valid_actions = []
        
        if state == State.HOME:
            if dice_value == 6:
                valid_actions.append(Action.MOVE_OUT)

        elif state == State.PATH:
            if position + dice_value < 56: # limite avant zone protégée
                valid_actions.append(Action.MOVE_FORWARD)

            elif position + dice_value >= 56:
                valid_actions.append(Action.ENTER_SAFEZONE)

            # est ce que tu tues un pion au passage ? -> alors ajouter kill
            if is_opponent_pawn_on(position+dice_value, player_id):
                valid_actions.append(Action.KILL)


        elif state == State.SAFEZONE:
            if position + dice_value <= 62:
                valid_actions.append(Action.MOVE_FORWARD)

            if position + dice_value >= 63:
                valid_actions.append(Action.REACH_GOAL)

        elif state == State.GOAL:
            pass # on peut recevoir des rewards pour pions déjà placés ?

        # on peut reward si on protége un pion (HOME + PATH POSSIBLE)
        if is_pawn_protected(player, position + dice_value):
            valid_actions.append(Action.PROTECT)

        return valid_actions
    

    def is_opponent_pawn_on(self, target_position, player):
        # TODO 
        pass
        for opponent in range(NUM_PLAYERS):
            if opponent != player:
                if target_position in self.board_path:
                    return True
        return False
    

    def is_pawn_threatened(player, position):
        # TODO
        pass

    def is_pawn_protected(player, position):
        # TODO
        pass

    def kill_pawn(self, player_id, position):
        # TODO
        pass







    def is_game_over(self):
        """
        Vérifie si un joueur a remporté la partie.
        """
        for player in range(NUM_PLAYERS):
            if all(state == State.GOAL for state in self.states[player]):
                return True
        return False


    def encode_possible_actions(self, possible_actions):
            action_vector = np.zeros(4, dtype=np.int32)  # Taille fixe pour 4 actions
            action_mapping = {"MOVE_OUT": 0, "MOVE": 1, "REACH_GOAL": 2, "NO_ACTION": 3}
            for action in possible_actions:
                action_vector[action_mapping[action]] = 1
            return action_vector

    def decode_possible_actions(self, action_vector):
        pass


    def avance(pion, de):
        # TODO
        pass

    def sortir_pion(pion):
        pass



    def get_valid_actions(self, player, dice_value) -> dict:
        """
        Calcule les actions possibles pour tous les pions d'un joueur.
        
        Parameters:
            - player (int): ID du joueur
            - dice_value (int): Résultat du dé
            
        Returns:
            - dict: Actions possibles par pion {pawn_index: [actions]}
        """
        valid_actions = {}
        for pawn_index in range(PAWNS_PER_PLAYER):
            position = self.board[player][pawn_index]
            state = self.states[player][pawn_index]
            valid_actions[pawn_index] = self.get_valid_actions_for_pawn(player, position, state, dice_value)
        return valid_actions