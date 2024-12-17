# Fichier permettant de définir les configurations de jeu pour les parties entre agents
import os
import sys
import rules
from itertools import permutations
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning/agents"))


racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning"))
sys.path.append(racine_dir)

from config import config_param

racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/"))
sys.path.append(racine_dir)
from ludo_env.reward import AgentType

# Créer un nom de fichier à partir des paramètres de l'environnement
def generate_model_name(agent_type, num_env, num_players, nb_chevaux, total_timesteps):
    model_name = (f"{agent_type}_{num_players}j_{nb_chevaux}c_conf_{num_env}_{total_timesteps}_steps")
    model_path = os.path.join(BASE_DIR, f"{num_players}_joueurs", f"{nb_chevaux}_pions", f"conf_{num_env}", model_name)
    return model_path



# TODO :  Ajouter d'autres paramètres pouvant être utiles
def generate_game_config(num_players, nb_chevaux, my_config_param, nb_train_steps, num_conf, total_timesteps, agent_types):

    agent_paths = [
        generate_model_name(agent_type, num_conf, num_players, nb_chevaux, total_timesteps)
        for agent_type in agent_types
    ]

    my_ids_rules = rules.determine_rules(num_players, nb_chevaux, my_config_param['mode_fin_partie'], my_config_param['mode_ascension'], my_config_param['mode_pied_escalier'], my_config_param['mode_rejoue_6'], my_config_param['mode_rejoue_marche'])
    return {
        "num_players": num_players,
        "nb_chevaux": nb_chevaux,
        "mode_fin_partie": my_config_param['mode_fin_partie'],
        "mode_ascension": my_config_param['mode_ascension'],
        "mode_pied_escalier": my_config_param['mode_pied_escalier'],
        "mode_rejoue_6": my_config_param['mode_rejoue_6'],
        "mode_rejoue_marche": my_config_param['mode_rejoue_marche'],
        "agents": [{"path": agent_paths[i], "name": os.path.basename(agent_paths[i])} for i in range(num_players)],
        "rules_ids": my_ids_rules,
        "nb_train_steps": nb_train_steps,
    }



# TODO : Ajouter toutes les configurations de jeu + avoir tous les agents correspondants
# TODO : Revoir comment automatiser cela
agent_types = AgentType.get_all_agent_types()
#print(agent_types)
game_configs = {}
total_timesteps = 2000

for agent_type in agent_types:
    for num_players in [2, 3, 4]:
        for nb_chevaux in [2]:
            for num_env in range(1, 17):
                game_configs[f"{agent_type}_conf_{num_env}_{num_players}j_{nb_chevaux}c"] = generate_game_config(
                    num_players, nb_chevaux, config_param[num_env], total_timesteps, num_env, total_timesteps, agent_type
                )

# Exemple de config
# generate_model_name(16, 2, 2, 10000) : generate_game_config(2, 2, config_param[16], 10000, generate_model_name(16, 2, 2, 10000))