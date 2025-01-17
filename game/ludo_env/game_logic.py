# ce fichier gère toute la logique du jeu / les règles du jeu
import numpy as np

from .action import Action_NO_EXACT, Action_EXACT, Action_EXACT_ASCENSION
from .state import State_NO_EXACT, State_EXACT
from .reward import get_reward_table, get_default_action_order, AgentType

BOARD_SIZE = 56
SAFE_ZONE_SIZE = 6

ONE_PLAYER_BOARD_SIZE = BOARD_SIZE // 4  # 14
TWO_PLAYERS_BOARD_SIZE = BOARD_SIZE // 2  # 28
THIRD_PLAYER_IDX = 3 * ONE_PLAYER_BOARD_SIZE  # 42

N_FIRST_STEP = BOARD_SIZE + 1  # 57
N_LAST_STEP = BOARD_SIZE + SAFE_ZONE_SIZE  # 62
FINAL_POSITION = BOARD_SIZE + SAFE_ZONE_SIZE + 1  # 63

TOTAL_SIZE = BOARD_SIZE + SAFE_ZONE_SIZE + 2  # HOME + GOAL


class GameLogic:
    def __init__(
        self,
        num_players,
        nb_chevaux,
        mode_fin_partie="tous",
        mode_pied_escalier="not_exact",
        mode_ascension="sans_contrainte",
        mode_protect="désactivé",
        agent_type=AgentType.BALANCED,
    ):
        self.num_players = num_players
        self.nb_chevaux = nb_chevaux
        self.mode_fin_partie = mode_fin_partie
        self.mode_ascension = mode_ascension
        self.mode_pied_escalier = mode_pied_escalier
        self.mode_protect = mode_protect
        self.agent_type = agent_type
        if mode_ascension == "avec_contrainte" and mode_pied_escalier == "not_exact":
            raise ValueError("Mode d'ascension avec contrainte non supporté")
        self.init_board()

    def get_state(self):
        if self.mode_pied_escalier == "not_exact":
            return State_NO_EXACT
        elif self.mode_pied_escalier == "exact":
            return State_EXACT
        else:
            raise ValueError("Mode de pied d'escalier non supporté")

    def get_action(self):
        if self.mode_ascension == "avec_contrainte":
            return Action_EXACT_ASCENSION
        elif self.mode_pied_escalier == "not_exact":
            return Action_NO_EXACT
        elif self.mode_pied_escalier == "exact":
            return Action_EXACT
        else:
            raise ValueError("Mode de pied d'escalier non supporté")
        
    def init_board(self):
        """
        Initialisation du plateau de jeu

        Chaque joueur a son propre board de 0 (ecurie) à 63 (objectif)
        Pour chaque joueur :
            - 0 : ECURIE
            - 1-BOARD_SIZE : CHEMIN
            - 57-62 : ESCALIER
            - 63 : OBJECTIF
        """
        self.board = [[] for _ in range(self.num_players)]
        for i in range(self.num_players):
            self.board[i] = [0 for _ in range(TOTAL_SIZE)]
            self.board[i][0] = self.nb_chevaux  # on met les pions dans l'écurie
        self.tour = 0  # compter les tours pour les stats

    def get_pawns_info(self, player_id):
        """
        Retourne une liste : pour chaque pion du joueur retourne un dictionnaire avec sa position et son état
        """
        pawns_info = []
        for i in range(TOTAL_SIZE):
            count_i = self.board[player_id][i]
            for _ in range(count_i):
                pawns_info.append(
                    {
                        "position": i,
                        "state": self.get_state().get_state_from_position(i),
                    }
                )
        assert len(pawns_info) == self.nb_chevaux, "Nombre de pions incorrect"
        return pawns_info
    
    def get_pawns_in_goal(self, player_id):
        pawns_info = self.get_pawns_info(player_id)
        return sum(1 for pawn in pawns_info if pawn["state"] == State_NO_EXACT.OBJECTIF or pawn["state"] == State_EXACT.OBJECTIF)

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

    def get_ecurie_player(self, player_id):
        ecurie = []
        for _ in range(self.board[player_id][0]):
            ecurie.append(player_id)

        return len(ecurie)

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
        escalier_overview = [[] for _ in range(SAFE_ZONE_SIZE)]
        for i in range(self.num_players):
            for j in range(N_FIRST_STEP, FINAL_POSITION):
                for _ in range(self.board[i][j]):
                    escalier_overview[j - N_FIRST_STEP].append(i)
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
        for i in range(BOARD_SIZE // ONE_PLAYER_BOARD_SIZE):
            str_game_overview += f"{chemin[i * ONE_PLAYER_BOARD_SIZE: (i + 1) * ONE_PLAYER_BOARD_SIZE]}\n"

        for i in range(self.num_players):
            str_game_overview += (
                f"ESCALIER {i} : {self.board[i][N_FIRST_STEP:FINAL_POSITION]}\n"
            )

        for i in range(self.num_players):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview

    def get_opponent_positions_on_my_board(self, player_id):
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
        for i in range(BOARD_SIZE // ONE_PLAYER_BOARD_SIZE):
            str_game_overview += f"{chemin[i * ONE_PLAYER_BOARD_SIZE: (i + 1) * ONE_PLAYER_BOARD_SIZE]}\n"

        for i in range(self.num_players):
            str_game_overview += (
                f"ESCALIER {i} : {self.board[i][N_FIRST_STEP:FINAL_POSITION]}\n"
            )

        for i in range(self.num_players):
            str_game_overview += f"OBJECTIF {i} : {self.board[i][-1]}\n"

        return str_game_overview

    def get_overview_of(self, other_player_id):
        # mettre tous les home ensemble, puis les safe zone, puis les goal
        # ensuite calculer pour les path

        board = [0 for _ in range(TOTAL_SIZE)]
        count_all_home = self.get_ecurie_overview()
        count_self_home = count_all_home.count(other_player_id)
        board[0] = count_self_home

        count_all_goal = self.get_objectif_overview()
        count_self_goal = count_all_goal.count(other_player_id)
        board[-1] = count_self_goal

        safe_zone = self.get_escalier_overview()
        for i in range(SAFE_ZONE_SIZE):
            count_all_safe = safe_zone[i]
            count_self_safe = count_all_safe.count(other_player_id)
            board[i + N_FIRST_STEP] = count_self_safe

        path_zone = (
            self.get_chemin_pdv_2_joueurs(other_player_id)
            if self.num_players == 2
            else self.get_chemin_pdv(other_player_id)
        )
        path_board = [0 for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            count_all_path = path_zone[i]
            count_self_path = count_all_path.count(other_player_id)
            path_board[i] = count_self_path
        # shift path board pour matcher avec le bon joueur
        if other_player_id == 0:
            board[1:N_FIRST_STEP] = path_board
        elif other_player_id == 1:
            if self.num_players != 2:
                board[ONE_PLAYER_BOARD_SIZE + 1 : N_FIRST_STEP] = path_board[
                    :THIRD_PLAYER_IDX
                ]
                board[1 : ONE_PLAYER_BOARD_SIZE + 1] = path_board[THIRD_PLAYER_IDX:]
            else:
                board[TWO_PLAYERS_BOARD_SIZE + 1 : N_FIRST_STEP] = path_board[
                    :TWO_PLAYERS_BOARD_SIZE
                ]
                board[1 : TWO_PLAYERS_BOARD_SIZE + 1] = path_board[
                    TWO_PLAYERS_BOARD_SIZE:
                ]
        elif other_player_id == 2:
            board[TWO_PLAYERS_BOARD_SIZE + 1 : N_FIRST_STEP] = path_board[
                :TWO_PLAYERS_BOARD_SIZE
            ]
            board[1 : TWO_PLAYERS_BOARD_SIZE + 1] = path_board[TWO_PLAYERS_BOARD_SIZE:]
        elif other_player_id == 3:
            board[THIRD_PLAYER_IDX + 1 : N_FIRST_STEP] = path_board[
                :ONE_PLAYER_BOARD_SIZE
            ]
            board[1 : THIRD_PLAYER_IDX + 1] = path_board[ONE_PLAYER_BOARD_SIZE:]
        return board

    def dice_generator(self):
        valeur = np.random.randint(1, 7)  
        return valeur

    def get_pawns_on_position(
        self, player_id, target_position_relative
    ): 
        if player_id == 0:
            indice = target_position_relative - 1
        elif player_id == 2:
            indice = (
                target_position_relative - 1 + TWO_PLAYERS_BOARD_SIZE
            ) % BOARD_SIZE
        elif player_id == 3:
            indice = (target_position_relative - 1 + THIRD_PLAYER_IDX) % BOARD_SIZE

        if self.num_players == 2:
            if player_id == 1:
                indice = (
                    target_position_relative - 1 + TWO_PLAYERS_BOARD_SIZE
                ) % BOARD_SIZE
            return self.get_chemin_pdv_2_joueurs(player_id)[indice]
        elif self.num_players == 3 or self.num_players == 4:
            if player_id == 1:
                indice = (
                    target_position_relative - 1 + ONE_PLAYER_BOARD_SIZE
                ) % BOARD_SIZE
            return self.get_chemin_pdv(player_id)[indice]
        else:
            raise ValueError("get_pawns_on_position pas bien implémenté")

    def is_opponent_pawn_on(self, player_id, target_position_relative):
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, target_position_relative
                )
                if self.board[other_player][relative_position] > 0:
                    return self.board[other_player][relative_position]
        return 0

    def get_dice_value_because_of_obstacle(
        self, player_id, old_position, target_position
    ):
        assert target_position in range(
            1, N_FIRST_STEP
        ), f"Position incorrecte {target_position}"
        dice_value = 0
        for pos in range(old_position + 1, target_position):
            if (
                self.is_opponent_pawn_on(player_id, pos)
                or self.board[player_id][pos] > 0
            ):
                return dice_value
            dice_value += 1
        if self.board[player_id][target_position] > 0:
            return dice_value
        raise ValueError(
            f"Pas d'obstacle. Player id : {player_id} Old position :{old_position} target position : {target_position} État du plateau : {self.board}"
        )

    # Savoir la position d'un joueur dans la perspective d'un autre joueur
    def get_relative_position(self, from_player, to_player, position):
        if position == 0 or position >= N_FIRST_STEP:
            raise ValueError("Position incorrecte")

        # Décalage de 28
        if self.num_players == 2:
            offset = (to_player - from_player) * TWO_PLAYERS_BOARD_SIZE
        # Décalage de 14 (pour 3 c'est comme si on avait 4 joueurs et 1 pas utilisé)
        elif self.num_players == 3 or self.num_players == 4:
            offset = (from_player - to_player) * ONE_PLAYER_BOARD_SIZE
        else:
            raise ValueError("Nombre de joueurs non supporté")
        result = (position + offset) % BOARD_SIZE
        if result == 0:
            return BOARD_SIZE
        return result

    # Tuer un pion adverse si on arrive sur sa case
    # Supprimer le pion de sa case et le renvoyer à l'écurie
    def kill_pawn(self, player_id, position):
        assert position in range(1, N_FIRST_STEP), "Position incorrecte"  
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, position
                )
                num_pawns_to_kill = self.board[other_player][relative_position]
                if num_pawns_to_kill > 0:
                    if self.mode_protect == "activé" and num_pawns_to_kill > 1:
                        raise ValueError(
                            "Mode protect activé, impossible de tuer plus d'un pion"
                        )
                    self.board[other_player][relative_position] -= num_pawns_to_kill
                    self.board[other_player][0] += num_pawns_to_kill

    def is_winner(self):
        """
        Vérifie si un joueur a remporté la partie.
        """
        if self.mode_fin_partie == "tous":
            for player_id in range(self.num_players):
                if self.board[player_id][-1] == self.nb_chevaux:
                    return player_id
        elif self.mode_fin_partie == "un":
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

        assert (
            old_position + dice_value < N_FIRST_STEP
        ), "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def avance_recule(self, player_id, old_position, dice_value):
        assert (
            old_position + dice_value > BOARD_SIZE
        ), "Déplacement pas conforme à la position"
        get_distance_avant = BOARD_SIZE - old_position
        recule_de = dice_value - get_distance_avant
        get_position_apres = BOARD_SIZE - recule_de
        assert (
            old_position < get_position_apres
        ), f"Déplacement pas conforme à la position, {old_position} < {get_position_apres}, dice_value : {dice_value}"
        self.board[player_id][old_position] -= 1
        self.board[player_id][get_position_apres] += 1

    def avance_pion_safe_zone(self, player_id, old_position, dice_value):
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"
        assert (
            old_position + dice_value < FINAL_POSITION
        ), "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][old_position + dice_value] += 1

    def securise_pion_goal(self, player_id, old_position, dice_value):
        assert (
            self.board[player_id][old_position] > 0
        ), "Pas de pion à déplacer à cette position"
        assert (
            old_position + dice_value >= FINAL_POSITION
        ), "Déplacement pas conforme à la position"
        self.board[player_id][old_position] -= 1
        self.board[player_id][-1] += 1

    def is_there_pawn_to_kill(self, player_id, target_position):
        assert target_position in range(
            1, N_FIRST_STEP
        ), "Position incorrecte" 
        for other_player in range(self.num_players):
            if other_player != player_id:
                relative_position = self.get_relative_position(
                    player_id, other_player, target_position
                )
                if self.board[other_player][relative_position] > 0:
                    return True
        return False

    def is_there_pawn_between_my_position_and_target_position(
        self, player_id, old_position, target_position
    ):
        assert target_position in range(
            1, N_FIRST_STEP
        ), f"Position incorrecte {target_position}"  
        for pos in range(old_position + 1, target_position):
            if (
                self.is_opponent_pawn_on(player_id, pos)
                or self.board[player_id][pos] > 0
            ):  # autre ou moi meme
                return True
            if pos == target_position - 1 and self.is_opponent_pawn_on(player_id, pos):
                return True  # si c'est un de mes pions sur la case d'arrivée c'est autorisé
        return False

    def move_pawn(self, player_id, old_position, dice_value, action):
        if self.get_action() == Action_NO_EXACT:
            if action == Action_NO_EXACT.MOVE_OUT:
                self.sortir_pion(player_id, dice_value)
            elif action == Action_NO_EXACT.MOVE_OUT_AND_KILL:
                self.kill_pawn(player_id, 1)
                self.sortir_pion(player_id, dice_value)
            elif action == Action_NO_EXACT.GET_STUCK_BEHIND: 
                target_position = old_position + dice_value
                if target_position >= N_FIRST_STEP:
                    target_position = BOARD_SIZE
                valeur_de_avec_obstacle = self.get_dice_value_because_of_obstacle(
                    player_id, old_position, target_position
                )
                self.avance_pion_path(player_id, old_position, valeur_de_avec_obstacle)
            elif action == Action_NO_EXACT.MOVE_FORWARD:
                self.avance_pion_path(player_id, old_position, dice_value)
            elif (
                action == Action_NO_EXACT.ENTER_SAFEZONE
                or action == Action_NO_EXACT.MOVE_IN_SAFE_ZONE
            ):
                self.avance_pion_safe_zone(player_id, old_position, dice_value)
            elif action == Action_NO_EXACT.REACH_GOAL:
                self.securise_pion_goal(player_id, old_position, dice_value)
            elif action == Action_NO_EXACT.KILL:
                self.kill_pawn(player_id, old_position + dice_value)
                self.avance_pion_path(player_id, old_position, dice_value)
            elif action == Action_NO_EXACT.NO_ACTION:
                pass

            else:
                raise ValueError("Action non valide")

        elif self.get_action() == Action_EXACT:
            if action == Action_EXACT.MOVE_OUT:
                self.sortir_pion(player_id, dice_value)
            elif action == Action_EXACT.MOVE_OUT_AND_KILL:
                self.kill_pawn(player_id, 1)
                self.sortir_pion(player_id, dice_value)

            elif action == Action_EXACT.GET_STUCK_BEHIND:  
                target_position = old_position + dice_value
                if target_position >= N_FIRST_STEP:
                    target_position = BOARD_SIZE
                valeur_de_avec_obstacle = self.get_dice_value_because_of_obstacle(
                    player_id, old_position, target_position
                )
                self.avance_pion_path(player_id, old_position, valeur_de_avec_obstacle)

            elif action == Action_EXACT.KILL:
                self.kill_pawn(player_id, old_position + dice_value)
                self.avance_pion_path(player_id, old_position, dice_value)
            elif (
                action == Action_EXACT.MOVE_FORWARD
                or action == Action_EXACT.REACH_PIED_ESCALIER
            ):
                self.kill_pawn(player_id, old_position + dice_value)

                self.avance_pion_path(player_id, old_position, dice_value)
            elif action == Action_EXACT.AVANCE_RECULE_PIED_ESCALIER:
                self.avance_recule(player_id, old_position, dice_value)
            elif action == Action_EXACT.MOVE_IN_SAFE_ZONE:
                self.avance_pion_safe_zone(player_id, old_position, dice_value)
            elif action == Action_EXACT.REACH_GOAL:
                self.securise_pion_goal(player_id, old_position, dice_value)
            elif action == Action_EXACT.NO_ACTION:
                pass
            else:
                raise ValueError("Action non valide")

            pass

        elif self.get_action() == Action_EXACT_ASCENSION:
            if action == Action_EXACT_ASCENSION.MOVE_OUT:
                self.sortir_pion(player_id, dice_value)
            elif action == Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL:
                self.kill_pawn(player_id, 1)
                self.sortir_pion(player_id, dice_value)

            elif action == Action_EXACT_ASCENSION.GET_STUCK_BEHIND: 
                target_position = old_position + dice_value
                if target_position >= N_FIRST_STEP:
                    target_position = BOARD_SIZE
                valeur_de_avec_obstacle = self.get_dice_value_because_of_obstacle(
                    player_id, old_position, target_position
                )
                self.avance_pion_path(player_id, old_position, valeur_de_avec_obstacle)

            elif action == Action_EXACT_ASCENSION.KILL:
                self.kill_pawn(player_id, old_position + dice_value)
                self.avance_pion_path(player_id, old_position, dice_value)
            elif (
                action == Action_EXACT_ASCENSION.MOVE_FORWARD
                or action == Action_EXACT_ASCENSION.REACH_PIED_ESCALIER
            ):
                # ici on doit aussi mettre le kill pcq avec reach pied escalier on peut tuer un pion adverse
                self.kill_pawn(player_id, old_position + dice_value)

                self.avance_pion_path(player_id, old_position, dice_value)
            elif action == Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER:
                self.avance_recule(player_id, old_position, dice_value)

            elif action == Action_EXACT_ASCENSION.MARCHE_1:
                assert dice_value == 1, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)
            elif action == Action_EXACT_ASCENSION.MARCHE_2:
                assert dice_value == 2, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)
            elif action == Action_EXACT_ASCENSION.MARCHE_3:
                assert dice_value == 3, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)
            elif action == Action_EXACT_ASCENSION.MARCHE_4:
                assert dice_value == 4, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)
            elif action == Action_EXACT_ASCENSION.MARCHE_5:
                assert dice_value == 5, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)
            elif action == Action_EXACT_ASCENSION.MARCHE_6:
                assert dice_value == 6, "Déplacement pas conforme à la position"
                self.avance_pion_safe_zone(player_id, old_position, 1)

            elif action == Action_EXACT_ASCENSION.REACH_GOAL:
                assert (
                    dice_value == 6
                ), "Déplacement pas conforme à la position"  
                self.securise_pion_goal(player_id, old_position, dice_value)
            elif action == Action_EXACT_ASCENSION.NO_ACTION:
                pass
            else:
                raise ValueError("Action non valide")

        else:
            raise ValueError("Action non valide")

    def get_valid_actions_for_pawns(self, player_id, position, state, dice_value):
        target_position = position + dice_value

        valid_actions = []
        if self.get_state() == State_NO_EXACT and self.get_action() == Action_NO_EXACT:
            if state == State_NO_EXACT.ECURIE:
                if dice_value == 6:
                    nb_opp_pawns = self.is_opponent_pawn_on(player_id, 1)
                    if nb_opp_pawns > 0:
                        if self.mode_protect == "activé" and nb_opp_pawns > 1:
                            pass  # si protect : ne peut pas kill
                        else:  # soit protect désactivé, soit un seul pion adverse -> kill
                            valid_actions.append(Action_NO_EXACT.MOVE_OUT_AND_KILL)
                    else:  # pas d'adversaire
                        valid_actions.append(Action_NO_EXACT.MOVE_OUT)

            elif state == State_NO_EXACT.CHEMIN: 
                if target_position < N_FIRST_STEP:  # limite avant zone protégée
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, target_position
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, target_position
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(Action_NO_EXACT.GET_STUCK_BEHIND)
                    else:
                        nb_opp_pawns = self.is_opponent_pawn_on(
                            player_id, target_position
                        )
                        if nb_opp_pawns > 0:
                            if self.mode_protect == "activé" and nb_opp_pawns > 1:
                                pass  # ne peut pas kill si + d'un adversaire
                            else:
                                valid_actions.append(Action_NO_EXACT.KILL)
                        else:
                            valid_actions.append(Action_NO_EXACT.MOVE_FORWARD)
                elif target_position >= N_FIRST_STEP:
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, BOARD_SIZE
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, BOARD_SIZE
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(Action_NO_EXACT.GET_STUCK_BEHIND)
                    else:
                        valid_actions.append(Action_NO_EXACT.ENTER_SAFEZONE)

            elif state == State_NO_EXACT.ESCALIER:
                if target_position <= N_LAST_STEP:
                    valid_actions.append(Action_NO_EXACT.MOVE_IN_SAFE_ZONE)
                if target_position >= FINAL_POSITION:
                    valid_actions.append(Action_NO_EXACT.REACH_GOAL)

            elif state == State_NO_EXACT.OBJECTIF:
                pass

        elif self.get_state() == State_EXACT and self.get_action() == Action_EXACT:
            if state == State_EXACT.ECURIE:
                if dice_value == 6:
                    nb_opp_pawns = self.is_opponent_pawn_on(player_id, 1)
                    if nb_opp_pawns > 0:
                        if self.mode_protect == "activé" and nb_opp_pawns > 1:
                            pass  # si protect ne peut pas kill
                        else:  # soit protect désactivé, soit un seul pion adverse -> kill
                            valid_actions.append(Action_EXACT.MOVE_OUT_AND_KILL)
                    else:  # pas d'adversaire
                        valid_actions.append(Action_EXACT.MOVE_OUT)

            elif state == State_EXACT.CHEMIN:
                if target_position < BOARD_SIZE:
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, target_position
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, target_position
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(Action_EXACT.GET_STUCK_BEHIND)
                    else:
                        nb_opp_pawns = self.is_opponent_pawn_on(
                            player_id, target_position
                        )
                        if nb_opp_pawns > 0:
                            if self.mode_protect == "activé" and nb_opp_pawns > 1:
                                pass  # ne peut pas kill si + d'un adversaire
                            else:
                                valid_actions.append(Action_EXACT.KILL)
                        else:
                            valid_actions.append(Action_EXACT.MOVE_FORWARD)

                elif target_position == BOARD_SIZE:
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, BOARD_SIZE
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, BOARD_SIZE
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(Action_EXACT.GET_STUCK_BEHIND)
                    else:
                        # if self.is_opponent_pawn_on(player_id, target_position):
                        #     valid_actions.append(Action_EXACT.KILL)
                        nb_opp_pawns = self.is_opponent_pawn_on(
                            player_id, target_position
                        )
                        if nb_opp_pawns > 0:
                            if self.mode_protect == "activé" and nb_opp_pawns > 1:
                                pass  # ne peut pas kill si + d'un adversaire
                            else:
                                valid_actions.append(Action_EXACT.KILL)
                        else:
                            valid_actions.append(Action_EXACT.REACH_PIED_ESCALIER)

                else:  # > BOARD_SIZE
                    # pour chacune des cases entre moi et l'escalier : est ce qu'il y a un pion adverse ou un pion à moi ?
                    # si oui -> get stuck si dé > 1
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, BOARD_SIZE
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, BOARD_SIZE
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(Action_EXACT.GET_STUCK_BEHIND)
                    else:  # si non -> on s'assure qu'on ne reculera pas
                        distance_avant = BOARD_SIZE - position
                        recule_de = dice_value - distance_avant
                        position_apres = BOARD_SIZE - recule_de
                        if position_apres > position:
                            valid_actions.append(
                                Action_EXACT.AVANCE_RECULE_PIED_ESCALIER
                            )

            elif state == State_EXACT.PIED_ESCALIER:
                valid_actions.append(Action_EXACT.MOVE_IN_SAFE_ZONE)

            elif state == State_EXACT.ESCALIER:
                if target_position <= N_LAST_STEP:
                    valid_actions.append(Action_EXACT.MOVE_IN_SAFE_ZONE)
                if target_position >= FINAL_POSITION:
                    valid_actions.append(Action_EXACT.REACH_GOAL)

            elif state == State_EXACT.OBJECTIF:
                pass

        elif (
            self.get_state() == State_EXACT
            and self.get_action() == Action_EXACT_ASCENSION
        ):
            if state == State_EXACT.ECURIE:
                if dice_value == 6:
                    nb_opp_pawns = self.is_opponent_pawn_on(player_id, 1)
                    if nb_opp_pawns > 0:
                        if self.mode_protect == "activé" and nb_opp_pawns > 1:
                            pass  # si protect ne peut pas kill
                        else:  # soit protect désactivé, soit un seul pion adverse -> kill
                            valid_actions.append(
                                Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL
                            )
                    else:  # pas d'adversaire
                        valid_actions.append(Action_EXACT_ASCENSION.MOVE_OUT)

            elif state == State_EXACT.CHEMIN:
                if target_position < BOARD_SIZE:
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, target_position
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, target_position
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(
                                Action_EXACT_ASCENSION.GET_STUCK_BEHIND
                            )
                    else:
                        nb_opp_pawns = self.is_opponent_pawn_on(
                            player_id, target_position
                        )
                        if nb_opp_pawns > 0:
                            if self.mode_protect == "activé" and nb_opp_pawns > 1:
                                pass  # ne peut pas kill si + d'un adversaire
                            else:
                                valid_actions.append(Action_EXACT_ASCENSION.KILL)
                        else:
                            valid_actions.append(Action_EXACT_ASCENSION.MOVE_FORWARD)

                elif target_position == BOARD_SIZE:
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, BOARD_SIZE
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, BOARD_SIZE
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(
                                Action_EXACT_ASCENSION.GET_STUCK_BEHIND
                            )
                    else:
                        # if self.is_opponent_pawn_on(player_id, target_position):
                        #     valid_actions.append(Action_EXACT_ASCENSION.KILL)
                        nb_opp_pawns = self.is_opponent_pawn_on(
                            player_id, target_position
                        )
                        if nb_opp_pawns > 0:
                            if self.mode_protect == "activé" and nb_opp_pawns > 1:
                                pass  # ne peut pas kill si + d'un adversaire
                            else:
                                valid_actions.append(Action_EXACT_ASCENSION.KILL)
                        else:
                            valid_actions.append(
                                Action_EXACT_ASCENSION.REACH_PIED_ESCALIER
                            )

                else:  # > BOARD_SIZE
                    obstacle = (
                        self.is_there_pawn_between_my_position_and_target_position(
                            player_id, position, BOARD_SIZE
                        )
                    )
                    if obstacle:
                        nb_cases_avancer = self.get_dice_value_because_of_obstacle(
                            player_id, position, BOARD_SIZE
                        )
                        if nb_cases_avancer > 0:
                            valid_actions.append(
                                Action_EXACT_ASCENSION.GET_STUCK_BEHIND
                            )
                    else:
                        distance_avant = BOARD_SIZE - position
                        recule_de = dice_value - distance_avant
                        position_apres = BOARD_SIZE - recule_de
                        if position_apres > position:
                            valid_actions.append(
                                Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER
                            )

            elif state == State_EXACT.PIED_ESCALIER:
                if dice_value == 1:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_1)

            elif state == State_EXACT.ESCALIER:
                if position == N_FIRST_STEP and dice_value == 2:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_2)
                elif position == 58 and dice_value == 3:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_3)
                elif position == 59 and dice_value == 4:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_4)
                elif position == 60 and dice_value == 5:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_5)
                elif position == 61 and dice_value == 6:
                    valid_actions.append(Action_EXACT_ASCENSION.MARCHE_6)
                elif position == N_LAST_STEP and dice_value == 6:
                    valid_actions.append(Action_EXACT_ASCENSION.REACH_GOAL)

            elif state == State_EXACT.OBJECTIF:
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
            if self.get_action() == Action_EXACT_ASCENSION:
                valid_actions.append(Action_EXACT_ASCENSION.NO_ACTION)
            elif self.get_action() == Action_NO_EXACT:
                valid_actions.append(Action_NO_EXACT.NO_ACTION)
            elif self.get_action() == Action_EXACT:
                valid_actions.append(Action_EXACT.NO_ACTION)

        else:
            valid_actions.append(False)  # en indice NB_PAWNS
        return valid_actions

    def encode_action(self, pawn_id, action_type):
        if self.get_action() == Action_NO_EXACT:
            if action_type == Action_NO_EXACT.NO_ACTION:
                return 0
            elif action_type == Action_NO_EXACT.MOVE_OUT:
                return 1
            elif action_type == Action_NO_EXACT.MOVE_OUT_AND_KILL:
                return 2
            return pawn_id * (len(Action_NO_EXACT) - 3) + action_type.value

        elif self.get_action() == Action_EXACT:
            if action_type == Action_EXACT.NO_ACTION:
                return 0
            elif action_type == Action_EXACT.MOVE_OUT:
                return 1
            elif action_type == Action_EXACT.MOVE_OUT_AND_KILL:
                return 2
            return pawn_id * (len(Action_EXACT) - 3) + action_type.value

        elif self.get_action() == Action_EXACT_ASCENSION:
            if action_type == Action_EXACT_ASCENSION.NO_ACTION:
                return 0
            elif action_type == Action_EXACT_ASCENSION.MOVE_OUT:
                return 1
            elif action_type == Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL:
                return 2
            return pawn_id * (len(Action_EXACT_ASCENSION) - 3) + action_type.value

        else:
            raise ValueError("Action non valide")

    def encode_valid_actions(self, valid_actions):
        if self.get_action() == Action_NO_EXACT:
            if valid_actions[self.nb_chevaux] == Action_NO_EXACT.NO_ACTION:
                return [0]
            valid_actions = valid_actions[: self.nb_chevaux]
            encoded_actions = []
            for i, actions in enumerate(valid_actions):
                for action in actions:
                    encoded_actions.append(self.encode_action(i, action))
            return list(set(encoded_actions))

        elif self.get_action() == Action_EXACT:
            if valid_actions[self.nb_chevaux] == Action_EXACT.NO_ACTION:
                return [0]
            valid_actions = valid_actions[: self.nb_chevaux]
            encoded_actions = []
            for i, actions in enumerate(valid_actions):
                for action in actions:
                    encoded_actions.append(self.encode_action(i, action))
            return list(set(encoded_actions))

        elif self.get_action() == Action_EXACT_ASCENSION:
            if valid_actions[self.nb_chevaux] == Action_EXACT_ASCENSION.NO_ACTION:
                return [0]
            valid_actions = valid_actions[: self.nb_chevaux]
            encoded_actions = []
            for i, actions in enumerate(valid_actions):
                for action in actions:
                    encoded_actions.append(self.encode_action(i, action))
            return list(set(encoded_actions))
        else:
            raise ValueError("Action non valide")

    def decode_action(self, action):
        if self.get_action() == Action_NO_EXACT:
            if action == 0:
                return 0, Action_NO_EXACT.NO_ACTION
            elif action == 1:
                return 0, Action_NO_EXACT.MOVE_OUT
            elif action == 2:
                return 0, Action_NO_EXACT.MOVE_OUT_AND_KILL

            pawn_id = (action - 3) // (len(Action_NO_EXACT) - 3)
            if action < len(Action_NO_EXACT):
                action_type = action
            else:
                action_type = (action - 3) % (len(Action_NO_EXACT) - 3) + 3
            return pawn_id, Action_NO_EXACT(action_type)
        elif self.get_action() == Action_EXACT:
            if action == 0:
                return 0, Action_EXACT.NO_ACTION
            elif action == 1:
                return 0, Action_EXACT.MOVE_OUT
            elif action == 2:
                return 0, Action_EXACT.MOVE_OUT_AND_KILL

            pawn_id = (action - 3) // (len(Action_EXACT) - 3)
            if action < len(Action_EXACT):
                action_type = action
            else:
                action_type = (action - 3) % (len(Action_EXACT) - 3) + 3
            return pawn_id, Action_EXACT(action_type)
        elif self.get_action() == Action_EXACT_ASCENSION:
            if action == 0:
                return 0, Action_EXACT_ASCENSION.NO_ACTION
            elif action == 1:
                return 0, Action_EXACT_ASCENSION.MOVE_OUT
            elif action == 2:
                return 0, Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL

            pawn_id = (action - 3) // (len(Action_EXACT_ASCENSION) - 3)
            if action < len(Action_EXACT_ASCENSION):
                action_type = action
            else:
                action_type = (action - 3) % (len(Action_EXACT_ASCENSION) - 3) + 3
            return pawn_id, Action_EXACT_ASCENSION(action_type)
        else:
            raise ValueError("Action non valide")

    def get_reward(self, action, agent_type=None):
        # Use instance agent_type if none provided
        agent_type = agent_type if agent_type is not None else self.agent_type
        reward_table = get_reward_table(
            self.mode_pied_escalier, self.mode_ascension, agent_type
        )  
        if self.mode_protect == "activé" and (agent_type == AgentType.DEFENSIVE or agent_type == "defensive"):
            # pour defensive : reward de base de l'action
            # + 5 * nombre de pions protégés 
            nb_pawns_protect = self.get_nb_pawns_protect()
            return (
                reward_table[action] + 5 * nb_pawns_protect
            ) 
        else:
            return reward_table[action]

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

        chemin = [[] for _ in range(BOARD_SIZE)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, N_FIRST_STEP):  # Cases du plateau
                for _ in range(self.board[p][j]):
                    relative_position = self.get_relative_position(
                        p, perspective_player, j
                    )
                    relative_position_chemin = (
                        relative_position - 1
                    )  # 1 à BOARD_SIZE -> 0 à 55
                    # Calcul de l'indice selon l'ordre des joueurs et l'offset
                    chemin[relative_position_chemin].append(p)
            i = (i + 1) % self.num_players
        return chemin

    def get_chemin_pdv_2_joueurs(self, perspective_player):
        """
        Retourne un chemin relatif à la perspective d'un joueur donné (le joueur qui regarde)
        """
        assert self.num_players == 2, "Nombre de joueurs incorrect."

        chemin = [[] for _ in range(BOARD_SIZE)]

        # Déterminer l'ordre des joueurs selon la perspective
        player_order = self.get_player_order(perspective_player)

        i = 0
        for p in player_order:
            for j in range(1, N_FIRST_STEP):
                for _ in range(self.board[p][j]):
                    relative_position = self.get_relative_position(
                        p, perspective_player, j
                    )
                    relative_position_chemin = relative_position - 1
                    chemin[relative_position_chemin].append(p)
            i = (i + 1) % self.num_players

        return chemin

    def get_str_adversaires_overview_plateau(self, player_id):
        str_game_overview = ""
        for i in range(self.num_players):
            if i != player_id:
                str_game_overview += f"JOUEUR {i} : {self.get_overview_of(i)}\n"
        return str_game_overview

    def debug_action(self, encoded_valid_actions):
        for action in get_default_action_order(
            self.nb_chevaux, self.mode_pied_escalier, self.mode_ascension
        ):
            if action in encoded_valid_actions:
                return action
        assert (
            False
        ), "Erreur : Aucune action possible dans la liste d'actions par défaut" 

    def get_observation_my_ecurie(self, player_id) -> int:
        return self.board[player_id][0]

    def get_observation_my_chemin(self, player_id):
        chemin = (
            self.get_chemin_pdv(player_id)
            if self.num_players > 2
            else self.get_chemin_pdv_2_joueurs(player_id)
        )

        other_player_ids = [0, 1, 2, 3]
        other_player_ids.remove(player_id)

        result = [0 for _ in range(BOARD_SIZE)]
        for i in range(BOARD_SIZE):
            # assert len(chemin[i]) <= 1, "Erreur dans la logique du jeu"
            if player_id in chemin[i]:
                assert set(chemin[i]) == {player_id}, "Erreur dans la logique du jeu"
                result[i] = len(chemin[i])
            else:
                for other_player_id in other_player_ids:
                    if other_player_id in chemin[i]:
                        assert set(chemin[i]) == {
                            other_player_id
                        }, "Erreur dans la logique du jeu"
                        result[i] = -(len(chemin[i]))
                        break
        return result

    def get_observation_my_escalier(self, player_id):
        return self.board[player_id][N_FIRST_STEP:FINAL_POSITION]

    def get_observation_my_goal(self, player_id) -> int:
        return self.board[player_id][-1]

    def get_nb_pawns_protect(self, player_id):
        if self.mode_protect != "activé":
            raise ValueError("Mode protect non activé")
        nb = 0
        for i in self.board[player_id][1:N_FIRST_STEP]:
            if i > 2:
                nb += i
        return nb
