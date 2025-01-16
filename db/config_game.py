# Fichier permettant de définir les configurations de jeu pour les parties entre agents

import os
import sys
import rules
from itertools import permutations
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game/reinforcement_learning/agents"))
racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game/reinforcement_learning"))
sys.path.append(racine_dir)
from config import config_param
racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game/"))
sys.path.append(racine_dir)
from ludo_env.reward import AgentType

# Créer le nom de fichier du l'agent à partir des paramètres de l'environnement
def generate_model_name(agent_type, num_env, num_players, nb_chevaux, total_timesteps):
    model_name = f"{agent_type}_{num_players}j_{nb_chevaux}c_conf_{num_env}_{total_timesteps}_steps"
    model_path = os.path.join(BASE_DIR, f"{num_players}_joueurs", f"{nb_chevaux}_pions", f"conf_{num_env}", model_name)
    return model_path

# Générer les configurations de jeu
def generate_game_config(num_players, nb_chevaux, my_config_param, nb_train_steps, num_conf, agent_types):

    agent_paths = [
        generate_model_name(agent_types[i], num_conf, num_players, nb_chevaux, nb_train_steps[i])
        for i in range(num_players)
    ]

    my_ids_rules = rules.determine_rules(
        my_config_param['mode_fin_partie'],
        my_config_param['mode_ascension'],
        my_config_param['mode_pied_escalier'],
        my_config_param['mode_rejoue_6'],
        my_config_param['mode_rejoue_marche'],
        my_config_param['mode_protect'],
    )
    return {
        "num_players": num_players,
        "nb_chevaux": nb_chevaux,
        "mode_fin_partie": my_config_param['mode_fin_partie'],
        "mode_ascension": my_config_param['mode_ascension'],
        "mode_pied_escalier": my_config_param['mode_pied_escalier'],
        "mode_rejoue_6": my_config_param['mode_rejoue_6'],
        "mode_rejoue_marche": my_config_param['mode_rejoue_marche'],
        "mode_protect": my_config_param['mode_protect'],
        "agents": [{"path": agent_paths[i], "name": os.path.basename(agent_paths[i])} for i in range(num_players)],
        "rules_ids": my_ids_rules,
        "nb_train_steps": nb_train_steps,
        "strategy": agent_types,
        "num_conf": num_conf
    }