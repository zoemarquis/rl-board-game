import numpy as np
from constants import *
from enum import Enum

class State(Enum):
    HOME = 0  # Le pion est dans sa maison, prêt à partir
    PATH = 1  # Le pion est en chemin
    SAFEZONE = 2  # Le pion est dans la zone protégée avant d'atteindre la destination
    GOAL = 3  # Le pion a atteint sa destination finale et ne bouge plus

    @staticmethod
    def get_state_from_position(relative_position : int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State.HOME
        elif relative_position < 57:
            return State.PATH
        elif relative_position < 63:
            return State.SAFEZONE
        else:
            return State.GOAL

class Action(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1  # Sortir de la maison
    MOVE_FORWARD = 2  # Avancer le long du chemin
    ENTER_SAFEZONE = 3  # Entrer dans la zone protégée
    REACH_GOAL = 4  # Atteindre l'objectif final
    # PROTECT = 4  # Protéger un pion allié
    # KILL = 5  # Tuer un pion adverse
    # DIE = 6  # Se faire tuer

action_table = {
    State.HOME: [Action.MOVE_OUT],
    State.PATH: [Action.MOVE_FORWARD, Action.ENTER_SAFEZONE],
    State.SAFEZONE: [Action.REACH_GOAL],
    State.GOAL: []  # Aucun mouvement autorisé
}


REWARD_TABLE = {
    Action.MOVE_OUT: 50,
    Action.MOVE_FORWARD: 5,
    Action.ENTER_SAFEZONE: 10,
    Action.REACH_GOAL: 50,
    # Action.PROTECT: 20,
    # Action.KILL: 30,
    # Action.DIE: -20 # TODO -> reward pas d'action enfaite, on le subit pendant un tour
}
# La table des récompenses est bien définie. 
# Tu peux envisager d'utiliser une fonction pour calculer les récompenses 
# dynamiquement selon des critères plus complexes (comme l’état du jeu).

class GameLogic:

    def __init__(self):
        self.init_board()

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
        return pawns_info

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
        return path_overview


    def print_board_overview(self):
        for i in range(NUM_PLAYERS):
            print(f"HOME {i} : {self.board[i][0]}")

        board_path = self.get_path_overview()
        for i in range(56//14):
            print(i*14, " -> ", (i+1)*14)
            print(board_path[i*14:(i+1)*14 ])

        for i in range(NUM_PLAYERS):
            print(f"SAFEZONE {i}: {self.board[i][57:63]}")

        for i in range(NUM_PLAYERS):
            print(f"GOAL {i} : {self.board[i][-1]}")

        print()


    def get_adversaire_relative_overview(self, player_id):
        board = [0 for _ in range(TOTAL_SIZE)]
        # mettre tous les home ensemble, puis les safe zone, puis les goal
        # ensuite calculer pour les path
        count_all_home = self.get_home_overview()
        count_self_home = count_all_home.count(player_id)
        board[0] = count_self_home

        count_all_goal = self.get_goal_overview()
        count_self_goal = count_all_goal.count(player_id)
        board[-1] = count_self_goal

        safe_zone = self.get_safe_zone_overview()
        for i in range(6):
            count_all_safe = safe_zone[i]
            count_self_safe = count_all_safe.count(player_id)
            board[i+57] = count_self_safe
        
        path_zone = self.get_path_overview()
        path_board = [0 for _ in range(56)]
        for i in range(56):
            count_all_path = path_zone[i]
            count_self_path = count_all_path.count(player_id)
            path_board[i] = count_self_path
        # shift path board pour matcher avec le bon joueur
        if player_id == 0:
            board[1:57] = path_board
        elif player_id == 1:
            if NUM_PLAYERS != 2:
                board[15:57] = path_board[:42]
                board[1:15] = path_board[42:]
            else:
                board[29:57] = path_board[:28]
                board[1:29] = path_board[28:]
        elif player_id == 2:
            board[29:57] = path_board[:28]
            board[1:29] = path_board[28:]
        elif player_id == 3:
            board[43:57] = path_board[:14]
            board[1:43] = path_board[14:]
        # TODO print pour etre sur 
        return board

    def dice_generator(self):
        valeur = np.random.randint(1, 7) # TODO : fix avec une seed pour les tests
        print("jeté de dé : ", valeur)
        return valeur
    
    def get_pawns_on_position(self, player_id, target_position_relative):
        if player_id == 0:
            return self.get_path_overview()[target_position_relative - 1]
        elif player_id == 1:
            if NUM_PLAYERS != 2:
                indice = (target_position_relative - 1+ 14) % 56
                return self.get_path_overview()[indice]
            else:
                indice = target_position_relative - 1 + 28
                return self.get_path_overview()[indice]
        elif player_id == 2:
            indice = target_position_relative - 1 + 28
            return self.get_path_overview()[indice]
        elif player_id == 3:
            indice = target_position_relative - 1 + 42
            return self.get_path_overview()[indice]
        # TODO print pour check tout ça

    def is_opponent_pawn_on(self, player_id, target_position_relative):
        case = self.get_pawns_on_position(player_id, target_position_relative)
        # si il y a autre chose que moi meme sur la case return true
        for i in range(NUM_PLAYERS):
            if i != player_id and case.count(i) > 0:
                return True
        return False

    def is_pawn_threatened(player, position): # si un pion est menacé par un autre pion adverse -> quelquun dans les 6 cases avant (HOME d'un autre joueur compte)
        # TODO
        # retourne combien de pions sont menacés ?
        pass

    def is_pawn_protected(player, position): # si un pion est protégé par un autre pion allié -> quelquun dans les 6 cases avant (HOME d'un autre joueur compte)
        # TODO
        pass

    def kill_pawn(self, player_id, position):
        # TODO pour tous les pions sur la case -> retourne HOME
        pass
    
    def is_winner(self):
        """
        Vérifie si un joueur a remporté la partie.
        """
        for player_id in range(NUM_PLAYERS):
            print(f"player {player_id} : {self.board[player_id][-1]}")
            if self.board[player_id][-1] == NB_PAWNS:
                return player_id
        return -1
    
    def is_game_over(self):
        """
        Vérifie si la partie est terminée.
        """
        if self.is_winner() != -1:
            return True
        return False
    
    def sortir_pion(self, player_id, dice_value):
        assert dice_value == 6, "Le dé n'est pas un 6"
        assert self.board[player_id][0] > 0, "Pas de pion à sortir"
        self.board[player_id][0] -= 1
        self.board[player_id][1] += 1

    def avance_pion_path(self, player_id, old_position, dice_value):
        assert self.board[player_id][old_position] > 0, "Pas de pion à déplacer à cette position"
        assert old_position + dice_value < 57, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def avance_pion_safe_zone(self, player_id, old_position, dice_value):
        print("avance pion safe zone")
        print(f"old position : {old_position}")
        print(f"dice value : {dice_value}")
        assert self.board[player_id][old_position] > 0, "Pas de pion à déplacer à cette position"
        assert old_position + dice_value < 63, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def securise_pion_goal(self, player_id, old_position, dice_value):
        assert self.board[player_id][old_position] > 0, "Pas de pion à déplacer à cette position"
        assert old_position + dice_value >= 63, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][-1] += 1

    def move_pawn(self, player_id, old_position, dice_value, action):
        print("move pawn action : ", action)
        if action == Action.MOVE_OUT:
            self.sortir_pion(player_id, dice_value)
        elif action == Action.MOVE_FORWARD:
            self.avance_pion_path(player_id, old_position, dice_value)
        elif action == Action.ENTER_SAFEZONE:
            self.avance_pion_safe_zone(player_id, old_position, dice_value)
        elif action == Action.REACH_GOAL:
            self.securise_pion_goal(player_id, old_position, dice_value)
        elif action == Action.NO_ACTION:
            pass
        else:
            raise ValueError("Action non valide")
        # PROTECT, KILL, DIE 

    def get_valid_actions_for_pawns(self, player_id, position, state, dice_value):
        # print(state)
        # TODO : si on s'est fait die (au tour précédent : reward négatif ? est ce vrmt utile ?)
        valid_actions = []
        if state == State.HOME:
            if dice_value == 6:
                valid_actions.append(Action.MOVE_OUT)
            # else :
            #     valid_actions.append(Action.NO_ACTION) # est ce qu'on peut ne rien faire ?
        elif state == State.PATH:
            if position + dice_value < 56: # limite avant zone protégée
                valid_actions.append(Action.MOVE_FORWARD)
            elif position + dice_value >= 56:
                valid_actions.append(Action.ENTER_SAFEZONE)
            # est ce que tu tues un pion au passage ? -> alors ajouter kill
            if self.is_opponent_pawn_on(player_id, position+dice_value):
                valid_actions.append(Action.KILL)
            if self.is_pawn_protected(player_id, position + dice_value): # on peut reward ça aussi
                valid_actions.append(Action.PROTECT)
        elif state == State.SAFEZONE:
            if position + dice_value <= 62:
                valid_actions.append(Action.MOVE_FORWARD)
            if position + dice_value >= 63:
                valid_actions.append(Action.REACH_GOAL)
        elif state == State.GOAL:
            pass
            # valid_actions.append(Action.NO_ACTION) # est ce qu'on peut ne rien faire ? 
        return valid_actions
        # TODO : ne pas inclure les no action, seulement au global si toutes les listes sont vides
    
    def get_valid_actions(self, player_id, dice_value):
        all_vide = True
        valid_actions = [ [] for _ in range(NB_PAWNS)]
        infos = self.get_pawns_info(player_id)
        for i in range(NB_PAWNS):
            tmp = self.get_valid_actions_for_pawns(player_id, infos[i]["position"], infos[i]["state"], dice_value)
            if tmp != []:
                all_vide = False
            valid_actions[i] = (tmp)
        if all_vide:
            valid_actions.append(Action.NO_ACTION)
        else: 
            valid_actions.append(False) # en indice NB_PAWNS 
        return valid_actions
    

    def encode_action(self, pawn_id, action_type):
        if action_type == Action.NO_ACTION:
            return 0
        return pawn_id * len(Action) + Action(action_type).value
    
    def encode_valid_actions(self, valid_actions):
        if valid_actions[NB_PAWNS] == Action.NO_ACTION:
            return [0]
        valid_actions = valid_actions[:NB_PAWNS]
        encoded_actions = []
        for i, actions in enumerate(valid_actions):
            for action in actions:
                encoded_actions.append(self.encode_action(i, action))
        print("valid actions : ", valid_actions)
        print("encoded actions : ", encoded_actions)
        return encoded_actions

    def decode_action(self, action):
        if action == 0:
            return 0, Action.NO_ACTION
        pawn_id, action_type = divmod(action, len(Action))
        print("pawn_id : ", pawn_id)
        print("action_type : ", action_type)
        return pawn_id, Action(action_type)



# Remarques : 
# Pense à ajouter des tests unitaires pour couvrir des cas comme :
# Un joueur tente de bouger un pion alors que ce dernier est bloqué.
# Deux pions ennemis entrent en collision sur une même case.
# Si le jeu doit évoluer, envisager l’utilisation d’une classe dédiée à chaque joueur, encapsulant les informations liées à ses pions et états.