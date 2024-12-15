# Fichier permettant de définir les configurations de jeu pour les parties entre agents
import os
import sys
import rules
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning/agents"))


racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning"))
sys.path.append(racine_dir)

from config import config_param


# Créer un nom de fichier à partir des paramètres de l'environnement
def generate_model_name(num_env, num_players, nb_chevaux, total_timesteps):
    model_name = (f"{num_players}j_{nb_chevaux}c_conf_{num_env}_{total_timesteps}_steps"
    )
    return model_name



# TODO :  Ajouter d'autres paramètres pouvant être utiles
def generate_game_config(num_players, nb_chevaux, my_config_param, agent_path):

    my_ids_rules = rules.determine_rules(num_players, nb_chevaux, my_config_param['mode_fin_partie'], my_config_param['mode_ascension'], my_config_param['mode_pied_escalier'], my_config_param['mode_rejoue_6'], my_config_param['mode_rejoue_marche'])
    return {
        "num_players": num_players,
        "nb_chevaux": nb_chevaux,
        "mode_fin_partie": my_config_param['mode_fin_partie'],
        "mode_ascension": my_config_param['mode_ascension'],
        "mode_pied_escalier": my_config_param['mode_pied_escalier'],
        "mode_rejoue_6": my_config_param['mode_rejoue_6'],
        "mode_rejoue_marche": my_config_param['mode_rejoue_marche'],
        "agents": [{"path": os.path.join(BASE_DIR, agent_path), "name": agent_path} for i in range(num_players)],
        "rules_ids": my_ids_rules
    }



# TODO : Ajouter toutes les configurations de jeu + avoir tous les agents correspondants
# TODO : Revoir comment automatiser cela
game_configs = {
    ## 2 PLAYERS
    # 2 players 2 pawns

    generate_model_name(1, 2, 2, 10000) : generate_game_config(2, 2, config_param[1], generate_model_name(1, 2, 2, 10000)),
    generate_model_name(2, 2, 2, 10000) : generate_game_config(2, 2, config_param[2], generate_model_name(2, 2, 2, 10000)),
    generate_model_name(3, 2, 2, 10000) : generate_game_config(2, 2, config_param[3], generate_model_name(3, 2, 2, 10000)),
    generate_model_name(4, 2, 2, 10000) : generate_game_config(2, 2, config_param[4], generate_model_name(4, 2, 2, 10000)),
    generate_model_name(5, 2, 2, 10000) : generate_game_config(2, 2, config_param[5], generate_model_name(5, 2, 2, 10000)),
    generate_model_name(6, 2, 2, 10000) : generate_game_config(2, 2, config_param[6], generate_model_name(6, 2, 2, 10000)),
    generate_model_name(7, 2, 2, 10000) : generate_game_config(2, 2, config_param[7], generate_model_name(7, 2, 2, 10000)),
    generate_model_name(8, 2, 2, 10000) : generate_game_config(2, 2, config_param[8], generate_model_name(8, 2, 2, 10000)),
    generate_model_name(9, 2, 2, 10000) : generate_game_config(2, 2, config_param[9], generate_model_name(9, 2, 2, 10000)),
    generate_model_name(10, 2, 2, 10000) : generate_game_config(2, 2, config_param[10], generate_model_name(10, 2, 2, 10000)),
    generate_model_name(11, 2, 2, 10000) : generate_game_config(2, 2, config_param[11], generate_model_name(11, 2, 2, 10000)),
    generate_model_name(12, 2, 2, 10000) : generate_game_config(2, 2, config_param[12], generate_model_name(12, 2, 2, 10000)),
    generate_model_name(13, 2, 2, 10000) : generate_game_config(2, 2, config_param[13], generate_model_name(13, 2, 2, 10000)),
    generate_model_name(14, 2, 2, 10000) : generate_game_config(2, 2, config_param[14], generate_model_name(14, 2, 2, 10000)),
    generate_model_name(15, 2, 2, 10000) : generate_game_config(2, 2, config_param[15], generate_model_name(15, 2, 2, 10000)),
    generate_model_name(16, 2, 2, 10000) : generate_game_config(2, 2, config_param[16], generate_model_name(16, 2, 2, 10000)),
}


"""
# 2 players 3 pawns
    "2_players_3_pawns_tous_exact" : generate_game_config(2, 3, "tous", "exact", "agent_maskedppo_2joueurs_3chevaux_tous_exact_ascension"),
    "2_players_3_pawns_tous_not_exact" : generate_game_config(2, 3, "tous", "not_exact", "-"),
    "2_players_3_pawns_un_exact" : generate_game_config(2, 3, "un", "exact", "agent_maskedppo_2joueurs_3chevaux_un_exact_ascension"),
    "2_players_3_pawns_un_not_exact" : generate_game_config(2, 3, "un", "not_exact", "-"),

    # 2 players 4 pawns
    "2_players_4_pawns_tous_exact" : generate_game_config(2, 4, "tous", "exact", "agent_maskedppo_2joueurs_4chevaux_tous_exact_ascension"),
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

"""