# ce fichier gère toute la logique du jeu / les règles du jeu
import numpy as np

from ludo_env.action import Action
from ludo_env.state import State
from ludo_env.reward import REWARD_TABLE_MOVE_OUT, DEFAULT_ACTION_ORDER

BOARD_SIZE = 56
SAFE_ZONE_SIZE = 6
TOTAL_SIZE = BOARD_SIZE + SAFE_ZONE_SIZE + 2  # HOME + GOAL


class GameLogic:
    def __init__(self, num_players, nb_chevaux, mode_fin_partie="tous_pions"):
        self.num_players = num_players
        self.nb_chevaux = nb_chevaux
        self.mode_fin_partie = mode_fin_partie
        self.init_board()

    def init_board(self):
        """
        Initialisation du plateau de jeu

        Chaque joueur a son propre board de 0 (ecurie) à 63 (objectif)
        Pour chaque joueur :
            - 0 : ECURIE
            - 1-56 : CHEMIN
            - 57-62 : ESCALIER
            - 63 : OBJECTIF
        """
        self.board = [[] for _ in range(self.num_players)]
        for i in range(self.num_players):
            self.board[i] = [0 for _ in range(TOTAL_SIZE)]
            self.board[i][0] = self.nb_chevaux  # on met les pions dans l'écurie
        self.tour = 0  # TODO : compter les tours pour les stats

    def get_pawns_info(self, player_id):
        """
        Retourne une liste : pour chaque pion du joueur retourne un dictionnaire avec sa position et son état
        """
        pawns_info = []
        for i in range(TOTAL_SIZE):
            count_i = self.board[player_id][i]
            for _ in range(count_i):
                pawns_info.append(
                    {"position": i, "state": State.get_state_from_position(i)}
                )
        assert len(pawns_info) == self.nb_chevaux, "Nombre de pions incorrect"
        return pawns_info

    def get_ecurie_overview(self):
        """
        Retourne une liste contenant tous les pions dans leur écurieÒ

        exemple: [0, 0, 1, 1] si 2 pions du joueur 0 et du joueur 1 sont dans leur écurie
        """
        ecurie_overview = []
        for i in range(self.num_players):
            for _ in range(self.board[i][0]):
                ecurie_overview.append(i)
        return ecurie_overview

    def get_objectif_overview(self):
        """
        retourne une liste contenant tous les pions dans leur objectif

        exemple: [0, 0, 1, 1] si 2 pions du joueur 0 et du joueur 1 sont dans leur goal
        """
        goal_overview = []
        for i in range(self.num_players):
            for _ in range(self.board[i][-1]):
                goal_overview.append(i)
        return goal_overview

    def get_escalier_overview(self):
        """
        retourne une liste contenant chaque pion dans sa safezone
        """
        escalier_overview = [[] for _ in range(6)]
        for i in range(self.num_players):
            for j in range(57, 63):
                for _ in range(self.board[i][j]):
                    escalier_overview[j - 57].append(i)
        return escalier_overview

    def get_str_game_overview(self):
        """
        affiche le plateau de jeu avec les pions de chaque joueur dans leur écurie,
        sur le chemin (vu par le joueur 0), leur escalier, leur objectif
        """
        str_game_overview = ""
        for i in range(self.num_players):
            str_game_overview += f"ECURIE {i} : {self.board[i][0]}\n"

        str_game_overview += "chemin vu par joueur 0 : \n"
        chemin = (
            self.get_chemin_pdv_2_joueurs(0)
            if self.num_players == 2
            else self.get_chemin_pdv(0)
        )
        for i in range(56 // 14):
            str_game_overview += f"{chemin[i * 14 : (i + 1) * 14]}\n"

        for i in range(self.num_players):
            str_game_overview += f"ESCALIER {i} : {self.board[i][57:63]}\n"

        for i in range(self.num_players):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview

    def get_opponent_positions_on_my_board(self, player_id):
        # TODO : multi joueurs
        # TODO : tests sur ça en 2 3 et 4 joueurs
        assert (
            self.num_players == 2
        ), "fonction get_opponent_positions_on_my_board pas implémenté pour plus de joueur"
        chemin = self.get_chemin_pdv_2_joueurs(player_id)
        chemin_len = [len(lst) for lst in chemin]
        chemin_my = [lst.count(player_id) for lst in chemin]
        chemin_cpt = [a - b for a, b in zip(chemin_len, chemin_my)]
        return chemin_cpt

    def get_str_player_overview(self, player_id):
        str_game_overview = ""
        for i in range(self.num_players):
            str_game_overview += f"ECURIE {i} : {self.board[i][0]}\n"

        str_game_overview += f"chemin vu par joueur {player_id} : \n"
        chemin = (
            self.get_chemin_pdv_2_joueurs(player_id)
            if self.num_players == 2
            else self.get_chemin_pdv(player_id)
        )
        for i in range(56 // 14):
            # print(i * 14 + 1, " -> ", (i + 1) * 14)
            str_game_overview += f"{chemin[i * 14 : (i + 1) * 14]}\n"

        for i in range(self.num_players):
            str_game_overview += f"ESCALIER {i} : {self.board[i][57:63]}\n"

        for i in range(self.num_players):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview

    def get_overview_of(self, other_player_id):
        # mettre tous les home ensemble, puis les safe zone, puis les goal
        # ensuite calculer pour les path

        # TODO vérifier ce truc là
        board = [0 for _ in range(TOTAL_SIZE)]
        count_all_home = self.get_ecurie_overview()
        count_self_home = count_all_home.count(other_player_id)
        board[0] = count_self_home

        count_all_goal = self.get_objectif_overview()
        count_self_goal = count_all_goal.count(other_player_id)
        board[-1] = count_self_goal

        safe_zone = self.get_escalier_overview()
        for i in range(6):
            count_all_safe = safe_zone[i]
            count_self_safe = count_all_safe.count(other_player_id)
            board[i + 57] = count_self_safe

        path_zone = (
            self.get_chemin_pdv_2_joueurs(other_player_id)
            if self.num_players == 2
            else self.get_chemin_pdv(other_player_id)
        )
        path_board = [0 for _ in range(56)]
        for i in range(56):
            count_all_path = path_zone[i]
            count_self_path = count_all_path.count(other_player_id)
            path_board[i] = count_self_path
        # shift path board pour matcher avec le bon joueur
        if other_player_id == 0:
            board[1:57] = path_board
        elif other_player_id == 1:
            if self.num_players != 2:
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

    """
    AFFICHAGE CHARLOTTE (NE PAS EFFACER MERCI)

    def get_instruction_for_player(self, player_id, dice_roll):
        str_instruction = f"Joueur {player_id} : \n"

        valid_actions = self.get_valid_actions(player_id, dice_roll)
        encoded_valid_actions = self.encode_valid_actions(valid_actions)

        if 0 in encoded_valid_actions:
            str_instruction += "0 : ne rien faire\n"
        if 1 in encoded_valid_actions:
            str_instruction += "1 : sortir pion\n"

        infos = self.get_pawns_info(player_id)

        for i in range(len(infos)):
            str_instruction += f"pion {i} case {infos[i]['position']}\n"
            if self.encode_action(i, Action.MOVE_FORWARD) in encoded_valid_actions:
                str_instruction += f"{2 + i * 5} : avancer pion {i}\n"
            if self.encode_action(i, Action.ENTER_SAFEZONE) in encoded_valid_actions:
                str_instruction += f"{3 + i * 5} : entrer escalier pion {i}\n"
            if self.encode_action(i, Action.MOVE_IN_SAFE_ZONE) in encoded_valid_actions:
                str_instruction += f"{4 + i * 5} : avancer dans escalier pion {i}\n"
            if self.encode_action(i, Action.REACH_GOAL) in encoded_valid_actions:
                str_instruction += f"{5 + i * 5} : atteindre objectif pion {i}\n"
            if self.encode_action(i, Action.KILL) in encoded_valid_actions:
                str_instruction += f"{6 + i * 5} : tuer adversaire pion {i}\n"

        return str_instruction





    """

    def get_instruction_for_player(self, player_id, dice_roll):
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

    def get_pawns_on_position(
        self, player_id, target_position_relative
    ):  # TODO check cette fonction pour multi joueurs
        if player_id == 0:
            indice = target_position_relative - 1
        elif player_id == 2:
            indice = (target_position_relative - 1 + 28) % 56
        elif player_id == 3:
            indice = (target_position_relative - 1 + 42) % 56

        if self.num_players == 2:
            if player_id == 1:
                indice = (target_position_relative - 1 + 28) % 56
            return self.get_chemin_pdv_2_joueurs(player_id)[indice]
        elif self.num_players == 3 or self.num_players == 4:
            if player_id == 1:
                indice = (target_position_relative - 1 + 14) % 56
            return self.get_chemin_pdv(player_id)[indice]
        else:
            raise ValueError("get_pawns_on_position pas bien implémenté")

    def is_opponent_pawn_on(self, player_id, target_position_relative):
        assert target_position_relative in range(1, 57), f"Position incorrecte {target_position_relative}"
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, target_position_relative
                )
                if self.board[other_player][relative_position] > 0:
                    return True
        return False
    
    def is_there_pawn_to_kill(self, player_id, target_position):
        assert target_position in range(1, 57), "Position incorrecte"
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, target_position
                )
                if self.board[other_player][relative_position] > 0:
                    return True
        return False

    def is_there_pawn_between_my_position_and_target_position(self, player_id, old_position, target_position):
        assert target_position in range(1, 57), f"Position incorrecte {target_position}"
        # TODO : mettre un if si on veut autoriser le doublement ici par exemple ?
        # TODO le représenter sous une autre forme d'action ?
        for pos in range(old_position + 1, target_position):
            if self.is_opponent_pawn_on(player_id, pos) or self.board[player_id][pos] > 0: # autre ou moi meme
                return True
        # if self.board[player_id][target_position] > 0:
        #     return True
        return False
    
    def get_dice_value_because_of_obstacle(self, player_id, old_position, target_position):
        assert target_position in range(1, 57), f"Position incorrecte {target_position}"
        dice_value = 0
        for pos in range(old_position + 1, target_position):
            if self.is_opponent_pawn_on(player_id, pos) or self.board[player_id][pos] > 0:
                return dice_value
            dice_value += 1
        if self.board[player_id][target_position] > 0:
            return dice_value
        raise ValueError(f"Pas d'obstacle. Player id : {player_id} Old position :{old_position} target position : {target_position} État du plateau : {self.board}")



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
        if position == 0 or position >= 57:
            raise ValueError("Position incorrecte")

        # Décalage de 28
        if self.num_players == 2:
            offset = (to_player - from_player) * 28
        # Décalage de 14 (pour 3 c'est comme si on avait 4 joueurs et 1 pas utilisé)
        elif self.num_players == 3 or self.num_players == 4:
            offset = (from_player - to_player) * 14
        else:
            raise ValueError("Nombre de joueurs non supporté")
        result = (position + offset) % 56
        if result == 0:
            return 56
        return result

    # Tuer un pion adverse si on arrive sur sa case
    # Supprimer le pion de sa case et le renvoyer à l'écurie
    def kill_pawn(self, player_id, position):
        assert position in range(1, 57), "Position incorrecte"
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, position
                )
                num_pawns_to_kill = self.board[other_player][relative_position]
                if num_pawns_to_kill > 0:
                    self.board[other_player][relative_position] -= num_pawns_to_kill
                    self.board[other_player][0] += num_pawns_to_kill

    def is_winner(self):
        """
        Vérifie si un joueur a remporté la partie.
        """
        if self.mode_fin_partie == "tous_pions":
            for player_id in range(self.num_players):
                if self.board[player_id][-1] == self.nb_chevaux:
                    return player_id
        elif self.mode_fin_partie == "un_pion":
            for player_id in range(self.num_players):
                if self.board[player_id][-1] == 1:
                    return player_id
        else:
            raise ValueError("Mode de fin de partie non supporté")
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

        if self.is_opponent_pawn_on(player_id, 1):
            self.kill_pawn(player_id, 1)

        self.board[player_id][0] -= 1
        self.board[player_id][1] += 1

    def avance_pion_path(self, player_id, old_position, dice_value):
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"

        # target_position = old_position + dice_value
        # chemin_observation = self.get_observation_my_chemin(player_id)
        # print(f"Chemin observation : {chemin_observation}")
        
        # # TODO : Mettre un if ici si on veut autoriser le doublement
        # # Empêcher de doubler un pion et reculer
        # for position in range(old_position + 1, min(target_position + 1, 57)):
        #     #print(f"Position : {position}")
        #     #print(f"chemin_observation[position] : {chemin_observation[position]}")
        #     if chemin_observation[position-1] == -1 or chemin_observation[position-1] == 1:
        #         print(f"Target : {target_position}")
        #         #if position == target_position and other_player != player_id:
        #         #    print(f"KILL possible à la position {position}")
        #         #    break
        #         #else:
        #         new_position = 2*position - dice_value - old_position
        #         #print(f"Chemin bloqué par un pion à la position {position}")
        #         if new_position < 1:
        #             new_position = 1

        #         self.board[player_id][old_position] -= 1
        #         self.board[player_id][new_position] += 1
        #         return

        # # TODO : Gérer le cas quand un joueur est entre un pion et l'escalier
        # # et que le pion a un dé le faisant arriver après l'escalier
        # # --> le code doit être changer dans les actions possibles

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
        if action == Action.MOVE_OUT:
            self.sortir_pion(player_id, dice_value)
        elif action == Action.MOVE_OUT_AND_KILL:
            self.kill_pawn(player_id, 1)
            self.sortir_pion(player_id, dice_value)
        elif action == Action.GET_STUCK_BEHIND:
            target_position = old_position + dice_value
            if target_position >= 57:
                target_position = 56
            valeur_de_avec_obstacle = self.get_dice_value_because_of_obstacle(player_id, old_position, target_position  )
            self.avance_pion_path(player_id, old_position, valeur_de_avec_obstacle)
        elif action == Action.MOVE_FORWARD:
            self.avance_pion_path(player_id, old_position, dice_value)
        elif action == Action.ENTER_SAFEZONE or action == Action.MOVE_IN_SAFE_ZONE:
            self.avance_pion_safe_zone(player_id, old_position, dice_value)
        elif action == Action.REACH_GOAL:
            self.securise_pion_goal(player_id, old_position, dice_value)
        elif action == Action.KILL:
            self.kill_pawn(player_id, old_position + dice_value)
            self.avance_pion_path(player_id, old_position, dice_value)
        elif action == Action.NO_ACTION:
            pass
        else:
            raise ValueError("Action non valide")

    def get_valid_actions_for_pawns(self, player_id, position, state, dice_value):
        target_position = position + dice_value

        valid_actions = []
        if state == State.ECURIE:
            if dice_value == 6:
                if self.is_opponent_pawn_on(player_id, 1): 
                    valid_actions.append(Action.MOVE_OUT_AND_KILL)
                else: 
                    # version où on autorise plusieurs pions du même joueur dans la même case
                    # if self.board[player_id][1] == 0: # si il y a déjà un de mes chevaux sur la case alors je ne peux pas sortir un autre
                    valid_actions.append(Action.MOVE_OUT)

        elif state == State.CHEMIN:
            if target_position < 57:  # limite avant zone protégée

                obstacle = self.is_there_pawn_between_my_position_and_target_position(player_id, position, target_position)
                if obstacle:
                    nb_cases_avancer = self.get_dice_value_because_of_obstacle(player_id, position, target_position)
                    if nb_cases_avancer > 0:
                        valid_actions.append(Action.GET_STUCK_BEHIND)
                else: 
                    if self.is_there_pawn_to_kill(player_id, target_position):
                        valid_actions.append(Action.KILL)
                    else: 
                        valid_actions.append(Action.MOVE_FORWARD)

            elif target_position >= 57:
                obstacle = self.is_there_pawn_between_my_position_and_target_position(player_id, position, 56)
                # TODO ZOE TESTER LE 56 ICI 
                if obstacle:
                    nb_cases_avancer = self.get_dice_value_because_of_obstacle(player_id, position, 56)
                    if nb_cases_avancer > 0:
                        valid_actions.append(Action.GET_STUCK_BEHIND)
                else:
                    valid_actions.append(Action.ENTER_SAFEZONE)

        elif state == State.ESCALIER:
            if target_position <= 62:
                # TODO ZOE : mis de coté : if self.board[player_id][target_position] == 0: # si il y a déjà un de mes chevaux sur la case alors je ne peux pas avancer
                valid_actions.append(Action.MOVE_IN_SAFE_ZONE)
            if target_position >= 63:
                valid_actions.append(Action.REACH_GOAL)
                
        elif state == State.OBJECTIF:
            pass

        return valid_actions

    def get_valid_actions(self, player_id, dice_value):
        all_vide = True
        valid_actions = [[] for _ in range(self.nb_chevaux)]
        infos = self.get_pawns_info(player_id)
        for i in range(self.nb_chevaux):
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
        elif action_type == Action.MOVE_OUT:
            return 1
        elif action_type == Action.MOVE_OUT_AND_KILL:
            return 2
        return pawn_id * (len(Action) - 3) + action_type.value

    def encode_valid_actions(self, valid_actions):
        if valid_actions[self.nb_chevaux] == Action.NO_ACTION:
            return [0]
        valid_actions = valid_actions[: self.nb_chevaux]
        encoded_actions = []
        for i, actions in enumerate(valid_actions):
            for action in actions:
                encoded_actions.append(self.encode_action(i, action))
        return list(set(encoded_actions))

    def decode_action(self, action):  
        if action == 0:
            return 0, Action.NO_ACTION
        elif action == 1:
            return 0, Action.MOVE_OUT
        elif action == 2:
            return 0, Action.MOVE_OUT_AND_KILL
        
        pawn_id = (action - 3) // (len(Action) - 3)
        if action < len(Action):    
            action_type = action
        else:
            action_type = (action - 3) % (len(Action) - 3) + 3
        return pawn_id, Action(action_type)


    def get_reward(self, action): 
        return REWARD_TABLE_MOVE_OUT[action]

    # ------------------ Fonctions d'affichage ------------------

    def get_player_order(self, perspective_player):
        """
        Retourne l'ordre des joueurs selon la perspective
        """
        if self.num_players == 2:
            if perspective_player == 0:
                return [0, 1]
            elif perspective_player == 1:
                return [1, 0]

        elif self.num_players == 3:
            if perspective_player == 0:
                return [0, 1, 2]
            elif perspective_player == 1:
                return [1, 2, 0]
            elif perspective_player == 2:
                return [2, 0, 1]

        elif self.num_players == 4:
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
        assert self.num_players > 2, "Nombre de joueurs incorrect."

        chemin = [[] for _ in range(56)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, 57):  # Cases du plateau
                for _ in range(self.board[p][j]):
                    relative_position = self.get_relative_position(
                        p, perspective_player, j
                    ) 
                    relative_position_chemin = relative_position - 1 # 1 à 56 -> 0 à 55
                    # Calcul de l'indice selon l'ordre des joueurs et l'offset
                    chemin[relative_position_chemin].append(p)
            i = (i + 1) % self.num_players

        # TODO : vérifier ça fonctionnel

        return chemin

    def get_chemin_pdv_2_joueurs(self, perspective_player):
        """
        Retourne un chemin relatif à la perspective d'un joueur donné (le joueur qui regarde)
        """
        assert self.num_players == 2, "Nombre de joueurs incorrect."

        chemin = [[] for _ in range(56)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, 57):
                for _ in range(self.board[p][j]):
                    relative_position = self.get_relative_position(
                        p, perspective_player, j
                    )
                    relative_position_chemin = relative_position - 1
                    chemin[relative_position_chemin].append(p)
            i = (i + 1) % self.num_players

        return chemin

    # def get_adversaires_overview_plateau(self, player_id):
    #     assert self.num_players == 2, "fonction pas implémenté pour plus de joueur"
    #     # result = [] TODO faire pour tous les joueurs
    #     other_player_id = 1 if player_id == 0 else 0
    #     return self.get_overview_of(other_player_id)

    def get_str_adversaires_overview_plateau(self, player_id):
        str_game_overview = ""
        for i in range(self.num_players):
            if i != player_id:
                str_game_overview += f"JOUEUR {i} : {self.get_overview_of(i)}\n"
        return str_game_overview

    def debug_action(self, encoded_valid_actions):
        for action in DEFAULT_ACTION_ORDER:
            if action in encoded_valid_actions:
                return action
        assert False, "Erreur : Aucune action possible dans la liste d'actions par défaut"

    # TODO : ajouter une fonction pour se voir avec son POV + 1 pour ses joueur, 0 pour les autres,
    # # où du moins avec un plateau sans mes pions mais où je vois où sont tous les autres par rapport à ma vision


    def get_observation_my_ecurie(self, player_id) -> int:
        return self.board[player_id][0]
    
    def get_observation_my_chemin(self, player_id):
        chemin = self.get_chemin_pdv(player_id) if self.num_players > 2 else self.get_chemin_pdv_2_joueurs(player_id)
        
        other_player_ids = [0, 1, 2, 3]
        other_player_ids.remove(player_id)

        result = [0 for _ in range(56)]
        for i in range(56):
            # assert len(chemin[i]) <= 1, "Erreur dans la logique du jeu"
            if player_id in chemin[i]:
                assert set(chemin[i]) == {player_id}, "Erreur dans la logique du jeu"
                result[i] = len(chemin[i])
            else :
                for other_player_id in other_player_ids:
                    if other_player_id in chemin[i]:
                        assert set(chemin[i]) == {other_player_id}, "Erreur dans la logique du jeu"
                        result[i] = -(len(chemin[i]))
                        break
        return result
    
    def get_observation_my_escalier(self, player_id):
        return self.board[player_id][57:63]
    
    def get_observation_my_goal(self, player_id) -> int:
        return self.board[player_id][-1]