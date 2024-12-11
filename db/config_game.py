# Fichier permettant de définir les configurations de jeu pour les parties entre agents
import os
import rules
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning"))



# TODO :  Ajouter d'autres paramètres pouvant être utiles
def generate_game_config(num_players, nb_chevaux, mode_fin, mode_escalier, agent_path):
    my_ids_rules = rules.determine_rules(num_players, nb_chevaux, mode_fin, mode_escalier)
    return {
        "num_players": num_players,
        "nb_chevaux": nb_chevaux,
        "mode_fin_partie": mode_fin,
        "mode_pied_escalier": mode_escalier,
        "agents": [{"path": os.path.join(BASE_DIR, agent_path), "name": f"Agent {i + 1}"} for i in range(num_players)],
        "rules_ids": my_ids_rules
    }

# TODO : Ajouter toutes les configurations de jeu + avoir tous les agents correspondants
game_configs = {
    ## 2 PLAYERS
    # 2 players 2 pawns
    "2_players_2_pawns_tous_exact" : generate_game_config(2, 2, "tous", "exact", "agent_maskedppo_2joueurs_2chevaux_tous_exact"),
    "2_players_2_pawns_tous_not_exact" : generate_game_config(2, 2, "tous", "not_exact", "-"),
    "2_players_2_pawns_un_exact" : generate_game_config(2, 2, "un", "exact", "agent_maskedppo_2joueurs_2chevaux_un_exact"),
    "2_players_2_pawns_un_not_exact" : generate_game_config(2, 2, "un", "not_exact", "-"),

    # 2 players 3 pawns
    "2_players_3_pawns_tous_exact" : generate_game_config(2, 3, "tous", "exact", "-"),
    "2_players_3_pawns_tous_not_exact" : generate_game_config(2, 3, "tous", "not_exact", "-"),
    "2_players_3_pawns_un_exact" : generate_game_config(2, 3, "un", "exact", "-"),
    "2_players_3_pawns_un_not_exact" : generate_game_config(2, 3, "un", "not_exact", "-"),

    # 2 players 4 pawns
    "2_players_4_pawns_tous_exact" : generate_game_config(2, 4, "tous", "exact", "-"),
    "2_players_4_pawns_tous_not_exact" : generate_game_config(2, 4, "tous", "not_exact", "-"),
    "2_players_4_pawns_un_exact" : generate_game_config(2, 4, "un", "exact", "-"),
    "2_players_4_pawns_un_not_exact" : generate_game_config(2, 4, "un", "not_exact", "-"),

    ## 3 PLAYERS
    # 3 players 2 pawns
    "3_players_2_pawns_tous_exact" : generate_game_config(3, 2, "tous", "exact", "-"),
    "3_players_2_pawns_tous_not_exact" : generate_game_config(3, 2, "tous", "not_exact", "-"),
    "3_players_2_pawns_un_exact" : generate_game_config(3, 2, "un", "exact", "-"),
    "3_players_2_pawns_un_not_exact" : generate_game_config(3, 2, "un", "not_exact", "-"),

    # 3 players 3 pawns
    "3_players_3_pawns_tous_exact" : generate_game_config(3, 3, "tous", "exact", "-"),
    "3_players_3_pawns_tous_not_exact" : generate_game_config(3, 3, "tous", "not_exact", "-"),
    "3_players_3_pawns_un_exact" : generate_game_config(3, 3, "un", "exact", "-"),
    "3_players_3_pawns_un_not_exact" : generate_game_config(3, 3, "un", "not_exact", "-"),

    # 3 players 4 pawns
    "3_players_4_pawns_tous_exact" : generate_game_config(3, 4, "tous", "exact", "-"),
    "3_players_4_pawns_tous_not_exact" : generate_game_config(3, 4, "tous", "not_exact", "-"),
    "3_players_4_pawns_un_exact" : generate_game_config(3, 4, "un", "exact", "-"),
    "3_players_4_pawns_un_not_exact" : generate_game_config(3, 4, "un", "not_exact", "-"),

    ## 4 PLAYERS
    # 4 players 2 pawns
    "4_players_2_pawns_tous_exact" : generate_game_config(4, 2, "tous", "exact", "-"),
    "4_players_2_pawns_tous_not_exact" : generate_game_config(4, 2, "tous", "not_exact", "-"),
    "4_players_2_pawns_un_exact" : generate_game_config(4, 2, "un", "exact", "-"),
    "4_players_2_pawns_un_not_exact" : generate_game_config(4, 2, "un", "not_exact", "-"),

    # 4 players 3 pawns
    "4_players_3_pawns_tous_exact" : generate_game_config(4, 3, "tous", "exact", "-"),
    "4_players_3_pawns_tous_not_exact" : generate_game_config(4, 3, "tous", "not_exact", "-"),
    "4_players_3_pawns_un_exact" : generate_game_config(4, 3, "un", "exact", "-"),
    "4_players_3_pawns_un_not_exact" : generate_game_config(4, 3, "un", "not_exact", "-"),

    # 4 players 4 pawns
    "4_players_4_pawns_tous_exact" : generate_game_config(4, 4, "tous", "exact", "-"),
    "4_players_4_pawns_tous_not_exact" : generate_game_config(4, 4, "tous", "not_exact", "-"),
    "4_players_4_pawns_un_exact" : generate_game_config(4, 4, "un", "exact", "-"),
    "4_players_4_pawns_un_not_exact" : generate_game_config(4, 4, "un", "not_exact", "-"),

}
