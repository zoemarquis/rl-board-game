# ce fichier gère toute la logique du jeu / les règles du jeu
import numpy as np
from enum import Enum

BOARD_SIZE = 56
SAFE_ZONE_SIZE = 6
NUM_PLAYERS = 2  # pour le moment, après il en aura 4
NB_CHEVAUX = 2  # idem
TOTAL_SIZE = BOARD_SIZE + SAFE_ZONE_SIZE + 2  # HOME + GOAL

# 0 : HOME
# 1-56 : PATH
# 57-62 : SAFEZONE
# 63 : GOAL


class State(Enum):
    ECURIE = 0
    CHEMIN = 1
    # PIED_ESCALIER = 2
    ESCALIER = 2
    OBJECTIF = 3

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State.ECURIE
        elif relative_position < 57:
            return State.CHEMIN
        # elif relative_position == 57:
        #     return State.PIED_ESCALIER
        elif relative_position < 63:
            return State.ESCALIER
        else:
            return State.OBJECTIF


class Action(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1  # Sortir de la maison
    MOVE_FORWARD = 2  # Avancer le long du chemin
    ENTER_SAFEZONE = 3  # Entrer dans la zone protégée
    MOVE_IN_SAFE_ZONE = 4  # Avancer dans la zone protégée
    REACH_GOAL = 5  # Atteindre l'objectif final
    KILL = 6  # Tuer un pion adverse
    # TODO :
    # REACH PIED ESCALIER
    # ESCALADER ou ESCALADER_1, ESCALADER_2 ... ?


REWARD_TABLE_MOVE_OUT = {
    Action.NO_ACTION: -1,
    Action.MOVE_OUT: 20,
    Action.MOVE_FORWARD: 5,
    Action.ENTER_SAFEZONE: 15,
    Action.MOVE_IN_SAFE_ZONE: 1,
    Action.REACH_GOAL: 10,
    Action.KILL: 30,
    # Action.PROTECT: 20,
    # 
    # Action.DIE: -20 # TODO -> reward pas d'action enfaite, on le subit pendant un tour
}  # faudrait que les sommes répartis soient égales

DEFAULT_ACTION_ORDER = {
    0, # ça veut dire rien de possible
    1, # d'abord essayer de sortir
    3, 8, # sauver le pion
    5, 10, # atteindre l'objectif
    2, 7, # avancer
    4, 9, # avancer dans la safezone
    6, 11 # tuer un pion
}


class GameLogic:
    def __init__(self):
        self.init_board()

    def init_board(self):
        self.board = [
            [] for _ in range(NUM_PLAYERS)
        ]  # chaque joueur à son propre board de 0 (home) à 63 (goal)
        for i in range(NUM_PLAYERS):
            self.board[i] = [0 for _ in range(TOTAL_SIZE)]
            self.board[i][0] = NB_CHEVAUX  # on met les pions dans l'écurie
        self.tour = 0

    def get_pawns_info(self, player_id):
        pawns_info = []
        for i in range(TOTAL_SIZE):
            count_i = self.board[player_id][i]
            for _ in range(count_i):
                pawns_info.append(
                    {"position": i, "state": State.get_state_from_position(i)}
                )
        assert len(pawns_info) == NB_CHEVAUX, "Nombre de pions incorrect"
        return pawns_info

    def get_ecurie_overview(self):
        """
        retourne une liste contenant chaque pion dans son écurie

        exemple: [0, 0, 1, 1] si 2 pions du joueur 0 et du joueur 1 sont dans leur écurie
        """
        ecurie_overview = []
        for i in range(NUM_PLAYERS):
            for _ in range(self.board[i][0]):
                ecurie_overview.append(i)
        return ecurie_overview

    def get_goal_overview(self):
        """
        retourne une liste contenant chaque pion dans son goal

        exemple: [0, 0, 1, 1] si 2 pions du joueur 0 et du joueur 1 sont dans leur goal
        """
        goal_overview = []
        for i in range(NUM_PLAYERS):
            for _ in range(self.board[i][-1]):
                goal_overview.append(i)
        return goal_overview
    def get_escalier_overview(self):
        """
        retourne une liste contenant chaque pion dans sa safezone
        """
        escalier_overview = [[] for _ in range(6)]
        for i in range(NUM_PLAYERS):
            for j in range(57, 63):
                for _ in range(self.board[i][j]):
                    escalier_overview[j - 57].append(i)
        return escalier_overview

    def get_str_game_overview(self):
        """
        affiche le plateau de jeu avec les pions de chaque joueur dans leur écurie, sur le chemin (vu par le joueur 0), leur escalier, leur goal
        """
        str_game_overview = ""
        for i in range(NUM_PLAYERS):
            str_game_overview += f"ECURIE {i} : {self.board[i][0]}\n"

        str_game_overview += "chemin vu par joueur 0 : \n"
        chemin = self.get_chemin_pdv_2_joueurs(0) if NUM_PLAYERS == 2 else self.get_chemin_pdv(0)
        for i in range(56 // 14):
            # print(i * 14 + 1, " -> ", (i + 1) * 14)
            str_game_overview += f"{chemin[i * 14 : (i + 1) * 14]}\n"

        for i in range(NUM_PLAYERS):
            str_game_overview += f"ESCALIER {i} : {self.board[i][57:63]}\n"

        for i in range(NUM_PLAYERS):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview

    
    
    def get_board_pour_voir_ou_sont_adversaires_sur_mon_plateau(self, player_id):
        assert NUM_PLAYERS == 2, "fonction pas implémenté pour plus de joueur"
        # plateau = [-1 for _ in range(TOTAL_SIZE)] # -1 mais j'ai mis 0 pour low... donc le modele n'apprend pas
        chemin = self.get_chemin_pdv_2_joueurs(player_id) 
        chemin_len = [len(lst) for lst in chemin]
        chemin_my = [lst.count(player_id) for lst in chemin]
        chemin_cpt = [a - b for a, b in zip(chemin_len, chemin_my)]
        return chemin_cpt
    
    def get_str_player_overview(self, player_id):
        str_game_overview = ""
        for i in range(NUM_PLAYERS):
            str_game_overview += f"ECURIE {i} : {self.board[i][0]}\n"

        str_game_overview += f"chemin vu par joueur {player_id} : \n"
        chemin = self.get_chemin_pdv_2_joueurs(player_id) if NUM_PLAYERS == 2 else self.get_chemin_pdv(player_id)
        for i in range(56 // 14):
            # print(i * 14 + 1, " -> ", (i + 1) * 14)
            str_game_overview += f"{chemin[i * 14 : (i + 1) * 14]}\n"

        for i in range(NUM_PLAYERS):
            str_game_overview += f"ESCALIER {i} : {self.board[i][57:63]}\n"

        for i in range(NUM_PLAYERS):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview



    
    def get_overview_of(self, other_player_id):
        # return self.board[other_player_id]
        # TODO vérifier ce truc là 
        board = [0 for _ in range(TOTAL_SIZE)]
        # mettre tous les home ensemble, puis les safe zone, puis les goal
        # ensuite calculer pour les path
        count_all_home = self.get_ecurie_overview()
        count_self_home = count_all_home.count(other_player_id)
        board[0] = count_self_home
        
        count_all_goal = self.get_goal_overview()
        count_self_goal = count_all_goal.count(other_player_id)
        board[-1] = count_self_goal
        
        safe_zone = self.get_escalier_overview()
        for i in range(6):
            count_all_safe = safe_zone[i]
            count_self_safe = count_all_safe.count(other_player_id)
            board[i + 57] = count_self_safe
        
        path_zone = self.get_chemin_pdv_2_joueurs(other_player_id) if NUM_PLAYERS == 2 else self.get_chemin_pdv(other_player_id)
        path_board = [0 for _ in range(56)]
        for i in range(56):
            count_all_path = path_zone[i]
            count_self_path = count_all_path.count(other_player_id)
            path_board[i] = count_self_path
        # shift path board pour matcher avec le bon joueur
        if other_player_id == 0:
            board[1:57] = path_board
        elif other_player_id == 1:
            if NUM_PLAYERS != 2:
                board[15:57] = path_board[:42]
                board[1:15] = path_board[42:]
            else:
                board[29:57] = path_board[:28]
                board[1:29] = path_board[28:]
        elif other_player_id == 2:
            board[29:57] = path_board[:28]
            board[1:29] = path_board[28:]
        elif other_player_id == 3:
            board[43:57] = path_board[:14]
            board[1:43] = path_board[14:]
        return board


    def get_instruction_for_player(self, player_id):
        str_instruction = ""    
        str_instruction += f"Joueur {player_id} : \n"
        str_instruction += "0 : ne rien faire\n"
        str_instruction += "1 : sortir pion\n"
        infos = self.get_pawns_info(player_id)
        str_instruction += f"pion 0 case {infos[0]['position']}\n"
        str_instruction += "2 : avancer pion 0\n"
        str_instruction += "3 : entrer escalier pion 0\n"
        str_instruction += "4 : avancer dans escalier pion 0\n"
        str_instruction += "5 : atteindre objectif pion 0\n"
        str_instruction += "6 : tuer adversaire pion 0\n"
        str_instruction += f"pion 1 case {infos[1]['position']}\n"
        str_instruction += "7 : avancer pion 1\n"
        str_instruction += "8 : entrer escalier pion 1\n"  
        str_instruction += "9 : avancer dans escalier pion 1\n"
        str_instruction += "10 : atteindre objectif pion 1\n"
        str_instruction += "11 : tuer adversaire pion 1\n"
        return str_instruction
    

    def dice_generator(self):
        valeur = np.random.randint(1, 7)  # TODO : fix avec une seed pour les tests
        return valeur

    def get_pawns_on_position(self, player_id, target_position_relative): # TODO check cette fonction
        if player_id == 0:
            indice = target_position_relative - 1
        elif player_id == 2:
            indice = (target_position_relative - 1 + 28) % 56
        elif player_id == 3:
            indice = (target_position_relative - 1 + 42) % 56
            
        if NUM_PLAYERS == 2:
            if player_id == 1:
                indice = (target_position_relative - 1 + 28) % 56
            return self.get_chemin_pdv_2_joueurs(player_id)[indice]
        elif NUM_PLAYERS == 3 or NUM_PLAYERS == 4:  
            if player_id == 1:     
                indice = (target_position_relative - 1 + 14) % 56
            return self.get_chemin_pdv(player_id)[indice]
        else:
            raise ValueError(
                "get_pawns_on_position pas bien implémenté"
            )

    def is_opponent_pawn_on(self, player_id, target_position_relative):
        # TODO : tester tout ça
        case = self.get_pawns_on_position(player_id, target_position_relative)
        # si il y a autre chose que moi meme sur la case return true
        for i in range(NUM_PLAYERS):
            if i != player_id and case.count(i) > 0:
                return True
        return False

    def is_pawn_threatened(
        self, player, position
    ):  # si un pion est menacé par un autre pion adverse -> quelquun dans les 6 cases avant (HOME d'un autre joueur compte)
        # TODO
        # retourne combien de pions sont menacés ?
        return False

    def is_pawn_protected(
        self, player, position
    ):  # si un pion est protégé par un autre pion allié -> quelquun dans les 6 cases avant (HOME d'un autre joueur compte)
        # TODO
        return False

    # Savoir la position d'un joueur dans la perspective d'un autre joueur
    def get_relative_position(self, from_player, to_player, position):
        offset = (to_player - from_player) * (56 // NUM_PLAYERS)
        return (position + offset) % 56

    # Tuer un pion adverse si on arrive sur sa case
    # Supprimer le pion de sa case et le renvoyer à l'écurie
    def kill_pawn(self, player_id, position):
        for other_player in range(NUM_PLAYERS):
            if other_player != player_id:
                relative_position = self.get_relative_position(player_id, other_player, position)
                num_pawns_to_kill = self.board[other_player][relative_position]
                if num_pawns_to_kill > 0:
                    self.board[other_player][relative_position] -= num_pawns_to_kill
                    self.board[other_player][0] += num_pawns_to_kill




    def is_winner(self):
        """
        Vérifie si un joueur a remporté la partie.
        """
        for player_id in range(NUM_PLAYERS):
            if self.board[player_id][-1] == NB_CHEVAUX:
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
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"
        assert old_position + dice_value < 57, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def avance_pion_safe_zone(self, player_id, old_position, dice_value):
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"
        assert old_position + dice_value < 63, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def securise_pion_goal(self, player_id, old_position, dice_value):
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"
        assert old_position + dice_value >= 63, "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][-1] += 1

    def move_pawn(self, player_id, old_position, dice_value, action):
        target_position = old_position + dice_value
        if action == Action.MOVE_OUT:
            self.sortir_pion(player_id, dice_value)
        elif action == Action.MOVE_FORWARD:
            self.avance_pion_path(player_id, old_position, dice_value)
        elif action == Action.ENTER_SAFEZONE or action == Action.MOVE_IN_SAFE_ZONE:
            self.avance_pion_safe_zone(player_id, old_position, dice_value)
        elif action == Action.REACH_GOAL:
            self.securise_pion_goal(player_id, old_position, dice_value)
        elif action == Action.KILL:
            self.kill_pawn(player_id, target_position)
            self.avance_pion_path(player_id, old_position, dice_value)
        elif action == Action.NO_ACTION:
            pass
        else:
            raise ValueError("Action non valide")

    def get_valid_actions_for_pawns(self, player_id, position, state, dice_value):
        # TODO : si on s'est fait die (au tour précédent : reward négatif ? est ce vrmt utile ?)
        valid_actions = []
        if state == State.ECURIE:
            if dice_value == 6:
                valid_actions.append(Action.MOVE_OUT)
        elif state == State.CHEMIN and self.is_opponent_pawn_on(player_id, position + dice_value):
            valid_actions.append(Action.KILL)
        elif state == State.CHEMIN:
            if position + dice_value < 57:  # limite avant zone protégée
                valid_actions.append(Action.MOVE_FORWARD)
            elif position + dice_value >= 57:
                valid_actions.append(Action.ENTER_SAFEZONE)
            # est ce que tu tues un pion au passage ? -> alors ajouter kill
            # TODO ajouter ces moves là
            # if self.is_opponent_pawn_on(player_id, position+dice_value):
            #     valid_actions.append(Action.KILL)
            # if self.is_pawn_protected(player_id, position + dice_value): # on peut reward ça aussi
            #     valid_actions.append(Action.PROTECT)
        elif state == State.ESCALIER:
            if position + dice_value <= 62:
                valid_actions.append(Action.MOVE_IN_SAFE_ZONE)
            if position + dice_value >= 63:
                valid_actions.append(Action.REACH_GOAL)
        elif state == State.OBJECTIF:
            pass
            # valid_actions.append(Action.NO_ACTION) # est ce qu'on peut ne rien faire ?
        return valid_actions
        # TODO : ne pas inclure les no action, seulement au global si toutes les listes sont vides

    def get_valid_actions(self, player_id, dice_value):
        all_vide = True
        valid_actions = [[] for _ in range(NB_CHEVAUX)]
        infos = self.get_pawns_info(player_id)
        for i in range(NB_CHEVAUX):
            tmp = self.get_valid_actions_for_pawns(
                player_id, infos[i]["position"], infos[i]["state"], dice_value
            )
            if tmp != []:
                all_vide = False
            valid_actions[i] = tmp
        if all_vide:
            valid_actions.append(Action.NO_ACTION)
        else:
            valid_actions.append(False)  # en indice NB_PAWNS
        return valid_actions

    def encode_action(self, pawn_id, action_type):
        if action_type == Action.NO_ACTION:
            return 0
        if action_type == Action.MOVE_OUT:
            return 1
        # 0 : no action
        # 1 : sortir pion
        # 2 ou 6 : move forward
        return pawn_id * (len(Action) - 2) + action_type.value

    def encode_valid_actions(self, valid_actions):
        if valid_actions[NB_CHEVAUX] == Action.NO_ACTION:
            return [0]
        valid_actions = valid_actions[:NB_CHEVAUX] 
        encoded_actions = []
        for i, actions in enumerate(valid_actions):
            for action in actions:
                encoded_actions.append(self.encode_action(i, action))
        return list(set(encoded_actions))

    def decode_action(self, action):  # TODO : adapter à la version du jeu ?
        if action == 0:
            return 0, Action.NO_ACTION
        if action == 1:
            return 0, Action.MOVE_OUT
        
        if action == 2:
            return 0, Action.MOVE_FORWARD
        if action == 3:
            return 0, Action.ENTER_SAFEZONE
        if action == 4:
            return 0, Action.MOVE_IN_SAFE_ZONE
        if action == 5:
            return 0, Action.REACH_GOAL
        if action == 6:
            return 0, Action.KILL

        if action == 7:
            return 1, Action.MOVE_FORWARD
        if action == 8:
            return 1, Action.ENTER_SAFEZONE
        if action == 9:
            return 1, Action.MOVE_IN_SAFE_ZONE
        if action == 10:
            return 1, Action.REACH_GOAL
        if action == 11:
            return 1, Action.KILL

        else:
            raise ValueError("Action non valide")

    def get_reward(self, action):  # TODO
        return REWARD_TABLE_MOVE_OUT[action]

    # ------------------ Fonctions d'affichage ------------------

    

    def get_player_order(self, perspective_player):
        """
        Retourne l'ordre des joueurs selon la perspective
        """
        if NUM_PLAYERS == 2:
            if perspective_player == 0:
                return [0, 1]
            elif perspective_player == 1:
                return [1, 0]

        elif NUM_PLAYERS == 3:
            if perspective_player == 0:
                return [0, 1, 2]
            elif perspective_player == 1:
                return [1, 2, 0]
            elif perspective_player == 2:
                return [2, 0, 1]

        elif NUM_PLAYERS == 4:
            if perspective_player == 0:
                return [0, 1, 2, 3]
            elif perspective_player == 1:
                return [1, 2, 3, 0]
            elif perspective_player == 2:
                return [2, 3, 0, 1]
            elif perspective_player == 3:
                return [3, 0, 1, 2]

        else:
            raise ValueError("Nombre de joueurs incorrect.")

    def get_chemin_pdv(self, perspective_player):
        """
        Retourne un chemin relatif à la perspective d'un joueur donné (le joueur qui regarde)
        """
        assert NUM_PLAYERS != 2, "Nombre de joueurs incorrect."

        chemin = [[] for _ in range(56)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, 57):  # Cases du plateau
                for _ in range(self.board[p][j]):
                    # Calcul de l'indice selon l'ordre des joueurs et l'offset
                    indice = ((i * 14) + j - 1) % 56
                    chemin[indice].append(p)
            i = (i + 1) % NUM_PLAYERS

        return chemin

    def get_chemin_pdv_2_joueurs(self, perspective_player):
        """
        Retourne un chemin relatif à la perspective d'un joueur donné (le joueur qui regarde)
        """
        assert NUM_PLAYERS == 2, "Nombre de joueurs incorrect."

        chemin = [[] for _ in range(56)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, 57):
                for _ in range(self.board[p][j]):
                    # Calcul de l'indice
                    indice = ((i * 28) + j - 1) % 56
                    chemin[indice].append(p)
            i = (i + 1) % NUM_PLAYERS

        return chemin

    def get_adversaires_overview_plateau(self, player_id):
        assert NUM_PLAYERS == 2, "fonction pas implémenté pour plus de joueur"
        # result = [] TODO faire pour tous les joueurs
        other_player_id = 1 if player_id == 0 else 0
        return self.get_overview_of(other_player_id)
            
    def get_str_adversaires_overview_plateau(self, player_id):
        str_game_overview = ""
        for i in range(NUM_PLAYERS):
            if i != player_id:
                str_game_overview += f"JOUEUR {i} : {self.get_overview_of(i)}\n"
        return str_game_overview
    

    def debug_action(self, encoded_valid_actions):
        for action in DEFAULT_ACTION_ORDER:
            if action in encoded_valid_actions:
                return action

    # TODO : ajouter une fonction pour se voir avec son POV + 1 pour ses joueur, 0 pour les autres, 
    # # où du moins avec un plateau sans mes pions mais où je vois où sont tous les autres par rapport à ma vision