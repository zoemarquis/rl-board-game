import numpy as np
from constants import *
from enum import Enum

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
        self.board_path = [[] for _ in range(BOARD_SIZE)] # faire + 1 -> 0 = HOME -> toujours order ?
        self.board_home = []
        for i in range(NUM_PLAYERS):
            self.board_home.extend([i] * NB_PAWNS)
        self.board_safe_zone = [[] for _ in range(SAFE_ZONE_SIZE)] # faire + 57 
        self.board_goal = [] # + 63 pour position

        # ou alors une liste pas pawn + une fonction qui retourne "get plateau overview"

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
                    "position": i + 1,
                    "state": State.PATH
                })
        for i in range(len(self.board_safe_zone)):
            count_safe_zone = self.board_safe_zone[i].count(player_id)
            for _ in range(count_safe_zone):
                player_pawns.append({
                    "position": i + 57,
                    "state": State.SAFEZONE
                })
        count_goal = self.board_goal.count(player_id)
        for _ in range(count_goal):
            player_pawns.append({
                "position": 63,
                "state": State.GOAL
            })
        assert len(player_pawns) == NB_PAWNS, "Nombre de pions incorrect"

    def get_plateau_player(self, player_id): # info que de ce joueur
        plateau = np.zeros(64, dtype=np.int32)
        count_home = self.board_home.count(player_id)
        plateau[0] += count_home
        if player_id == 0:
            for i in range(len(self.board_path)):
                count_path = self.board_path[i].count(player_id)
            plateau[i + i] += count_path
        elif player_id == 1:
            if NUM_PLAYERS != 2:
                ind_0 = 0
                ind_j = 14
                while ind_j < 56:
                    count_path = self.board_path[ind_0].count(player_id)
                    plateau[ind_j] += count_path
                    ind_0 += 1
                    ind_j += 1
                ind_j = 0
                while ind_j < 14:
                    count_path = self.board_path[ind_0].count(player_id)
                    plateau[ind_j] += count_path
                    ind_0 += 1
                    ind_j += 1
            else: # que 2 joueurs opposés
                ind_0 = 0
                ind_j = 28
                while ind_j < 56:
                    count_path = self.board_path[ind_0].count(player_id)
                    plateau[ind_j] += count_path
                    ind_0 += 1
                    ind_j += 1
                ind_j = 0
                while ind_j < 28:
                    count_path = self.board_path[ind_0].count(player_id)
                    plateau[ind_j] += count_path
                    ind_0 += 1
                    ind_j += 1
        elif player_id == 2:
            ind_0 = 0
            ind_j = 28
            while ind_j < 56:
                count_path = self.board_path[ind_0].count(player_id)
                plateau[ind_j] += count_path
                ind_0 += 1
                ind_j += 1
            ind_j = 0
            while ind_j < 28:
                count_path = self.board_path[ind_0].count(player_id)
                plateau[ind_j] += count_path
                ind_0 += 1
                ind_j += 1
        elif player_id == 3:    
            ind_0 = 0
            ind_j = 42
            while ind_j < 56:
                count_path = self.board_path[ind_0].count(player_id)
                plateau[ind_j] += count_path
                ind_0 += 1
                ind_j += 1
            ind_j = 0
            while ind_j < 42:
                count_path = self.board_path[ind_0].count(player_id)
                plateau[ind_j] += count_path
                ind_0 += 1
                ind_j += 1
        for i in range(len(self.board_safe_zone)):
            count_safe_zone = self.board_safe_zone[i].count(player_id)
            plateau[i + 57] += count_safe_zone
        count_goal = self.board_goal.count(player_id)
        plateau[63] += count_goal
        return plateau

    def get_overview(self):
        # indice 0 -> les joueurs 0 
        # indice 1 -> les joueurs 1 mais avec le bon décalage
        # indice 2 -> les joueurs 2 mais avec le bon décalage
        # indice 3 -> les joueurs 3 mais avec le bon décalage
        # TODO
        pass


    def get_plateau(player_id, nb_joueurs):
        # objectif pour tous les jouerus retourne un tableau de 0 à 63
        # le 0 pas commun pour tous les joueurs -> HOME
        # de 1 à 56 -> PATH -> commun (il va falloir faire des calculs)
        # de 57 à 62 -> SAFEZONE -> unique
        # 63 -> GOAL -> unique

        # si 2 joueurs : 
        # joueur 0 : case 1 = joueur 1 case 29
        # joueur 0 : case 2 = joueur 1 case 30

        # si 3 ou 4 joueures : 
        # joueur 0 : case 1, joueur 1 case 43 , joueur 2 case 29, joueur 3 case 18

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