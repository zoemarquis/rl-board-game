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
def generate_game_config(num_players, nb_chevaux, my_config_param, nb_train_steps, agent_path):

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
        "rules_ids": my_ids_rules,
        "nb_train_steps": nb_train_steps,
    }



# TODO : Ajouter toutes les configurations de jeu + avoir tous les agents correspondants
# TODO : Revoir comment automatiser cela
game_configs = {

    # 2 players 2 pawns
    generate_model_name(1, 2, 2, 10000) : generate_game_config(2, 2, config_param[1], 10000, generate_model_name(1, 2, 2, 10000)),
    #generate_model_name(2, 2, 2, 10000) : generate_game_config(2, 2, config_param[2], generate_model_name(2, 2, 2, 10000)),
    #generate_model_name(3, 2, 2, 10000) : generate_game_config(2, 2, config_param[3], generate_model_name(3, 2, 2, 10000)),
    #generate_model_name(4, 2, 2, 10000) : generate_game_config(2, 2, config_param[4], generate_model_name(4, 2, 2, 10000)),
    #generate_model_name(5, 2, 2, 10000) : generate_game_config(2, 2, config_param[5], generate_model_name(5, 2, 2, 10000)),
    #generate_model_name(6, 2, 2, 10000) : generate_game_config(2, 2, config_param[6], generate_model_name(6, 2, 2, 10000)),
    #generate_model_name(7, 2, 2, 10000) : generate_game_config(2, 2, config_param[7], generate_model_name(7, 2, 2, 10000)),
    #generate_model_name(8, 2, 2, 10000) : generate_game_config(2, 2, config_param[8], generate_model_name(8, 2, 2, 10000)),
    #generate_model_name(9, 2, 2, 10000) : generate_game_config(2, 2, config_param[9], generate_model_name(9, 2, 2, 10000)),
    #generate_model_name(10, 2, 2, 10000) : generate_game_config(2, 2, config_param[10], generate_model_name(10, 2, 2, 10000)),
    #generate_model_name(11, 2, 2, 10000) : generate_game_config(2, 2, config_param[11], generate_model_name(11, 2, 2, 10000)),
    #generate_model_name(12, 2, 2, 10000) : generate_game_config(2, 2, config_param[12], generate_model_name(12, 2, 2, 10000)),
    #generate_model_name(13, 2, 2, 10000) : generate_game_config(2, 2, config_param[13], generate_model_name(13, 2, 2, 10000)),
    #generate_model_name(14, 2, 2, 10000) : generate_game_config(2, 2, config_param[14], generate_model_name(14, 2, 2, 10000)),
    #generate_model_name(15, 2, 2, 10000) : generate_game_config(2, 2, config_param[15], generate_model_name(15, 2, 2, 10000)),
    #generate_model_name(16, 2, 2, 10000) : generate_game_config(2, 2, config_param[16], generate_model_name(16, 2, 2, 10000)),

    # 3 players 2 pawns
    generate_model_name(1, 3, 2, 10000) : generate_game_config(3, 2, config_param[1], 10000, generate_model_name(1, 3, 2, 10000)),
    #generate_model_name(2, 3, 2, 10000) : generate_game_config(3, 2, config_param[2], generate_model_name(2, 3, 2, 10000)),
    #generate_model_name(3, 3, 2, 10000) : generate_game_config(3, 2, config_param[3], generate_model_name(3, 3, 2, 10000)),
    #generate_model_name(4, 3, 2, 10000) : generate_game_config(3, 2, config_param[4], generate_model_name(4, 3, 2, 10000)),
    #generate_model_name(5, 3, 2, 10000) : generate_game_config(3, 2, config_param[5], generate_model_name(5, 3, 2, 10000)),
    #generate_model_name(6, 3, 2, 10000) : generate_game_config(3, 2, config_param[6], generate_model_name(6, 3, 2, 10000)),
    #generate_model_name(7, 3, 2, 10000) : generate_game_config(3, 2, config_param[7], generate_model_name(7, 3, 2, 10000)),
    #generate_model_name(8, 3, 2, 10000) : generate_game_config(3, 2, config_param[8], generate_model_name(8, 3, 2, 10000)),
    #generate_model_name(9, 3, 2, 10000) : generate_game_config(3, 2, config_param[9], generate_model_name(9, 3, 2, 10000)),
    #generate_model_name(10, 3, 2, 10000) : generate_game_config(3, 2, config_param[10], generate_model_name(10, 3, 2, 10000)),
    #generate_model_name(11, 3, 2, 10000) : generate_game_config(3, 2, config_param[11], generate_model_name(11, 3, 2, 10000)),
    #generate_model_name(12, 3, 2, 10000) : generate_game_config(3, 2, config_param[12], generate_model_name(12, 3, 2, 10000)),
    #generate_model_name(13, 3, 2, 10000) : generate_game_config(3, 2, config_param[13], generate_model_name(13, 3, 2, 10000)),
    #generate_model_name(14, 3, 2, 10000) : generate_game_config(3, 2, config_param[14], generate_model_name(14, 3, 2, 10000)),
    #generate_model_name(15, 3, 2, 10000) : generate_game_config(3, 2, config_param[15], generate_model_name(15, 3, 2, 10000)),
    #generate_model_name(16, 3, 2, 10000) : generate_game_config(3, 2, config_param[16], generate_model_name(16, 3, 2, 10000)),    

    # 4 players 2 pawns
    generate_model_name(1, 4, 2, 10000) : generate_game_config(4, 2, config_param[1], 10000, generate_model_name(1, 4, 2, 10000)),
    #generate_model_name(2, 4, 2, 10000) : generate_game_config(4, 2, config_param[2], generate_model_name(2, 4, 2, 10000)),
    #generate_model_name(3, 4, 2, 10000) : generate_game_config(4, 2, config_param[3], generate_model_name(3, 4, 2, 10000)),
    #generate_model_name(4, 4, 2, 10000) : generate_game_config(4, 2, config_param[4], generate_model_name(4, 4, 2, 10000)),
    #generate_model_name(5, 4, 2, 10000) : generate_game_config(4, 2, config_param[5], generate_model_name(5, 4, 2, 10000)),
    #generate_model_name(6, 4, 2, 10000) : generate_game_config(4, 2, config_param[6], generate_model_name(6, 4, 2, 10000)),
    #generate_model_name(7, 4, 2, 10000) : generate_game_config(4, 2, config_param[7], generate_model_name(7, 4, 2, 10000)),
    #generate_model_name(8, 4, 2, 10000) : generate_game_config(4, 2, config_param[8], generate_model_name(8, 4, 2, 10000)),
    #generate_model_name(9, 4, 2, 10000) : generate_game_config(4, 2, config_param[9], generate_model_name(9, 4, 2, 10000)),
    #generate_model_name(10, 4, 2, 10000) : generate_game_config(4, 2, config_param[10], generate_model_name(10, 4, 2, 10000)),
    #generate_model_name(11, 4, 2, 10000) : generate_game_config(4, 2, config_param[11], generate_model_name(11, 4, 2, 10000)),
    #generate_model_name(12, 4, 2, 10000) : generate_game_config(4, 2, config_param[12], generate_model_name(12, 4, 2, 10000)),
    #generate_model_name(13, 4, 2, 10000) : generate_game_config(4, 2, config_param[13], generate_model_name(13, 4, 2, 10000)),
    #generate_model_name(14, 4, 2, 10000) : generate_game_config(4, 2, config_param[14], generate_model_name(14, 4, 2, 10000)),
    #generate_model_name(15, 4, 2, 10000) : generate_game_config(4, 2, config_param[15], generate_model_name(15, 4, 2, 10000)),
    #generate_model_name(16, 4, 2, 10000) : generate_game_config(4, 2, config_param[16], generate_model_name(16, 4, 2, 10000)),

}