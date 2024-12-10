# INFO :  Script à lancer depuis le répertoire db
# Permet d'enregistrer les statistiques d'une partie dans la base de données
# EN COURS DE DEVELOPPEMENT

import sys
import os

from collections import defaultdict
from stable_baselines3 import PPO
from config_game import game_configs
from insert import store_final_game_data, PlayerToInsert, SetOfRulesToInsert

racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux"))
sys.path.append(racine_dir)

from ludo_env import LudoEnv
from ludo_env.action import Action_NO_EXACT, Action_EXACT


# TODO : Modifier cela pour utiliser plusieurs configs
# TODO : Gérer les règles

config_name = "two_players_two_pawns"
config = game_configs[config_name]

agents = [PPO.load(agent_config["path"]) for agent_config in config["agents"]]
agent_names = [agent_config["name"] for agent_config in config["agents"]]

env = LudoEnv(
    num_players=config["num_players"],
    nb_chevaux=config["nb_chevaux"],
    mode_gym="jeu",
    mode_fin_partie=config["mode_fin_partie"],
    mode_pied_escalier=config["mode_pied_escalier"],
)

def play_game(env, agents, agent_names):
    obs, info = env.reset()
    done = False
    turn = 0

    # TODO : Ajouter d'autres info et voir comment ajouter dans la BD
    scores = [0] * env.num_players
    moves = [0] * env.num_players
    intentional_actions = defaultdict(int)
    impossible_actions = defaultdict(int)

    while not done:
        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)

        if env.current_player < len(agents):
            action, _ = agents[env.current_player].predict(obs, deterministic=True)
        else:
            raise ValueError("Nombre de joueurs non supporté")

        _, action_type = env.game.decode_action(action)
        if action in encoded_valid_actions:
            intentional_actions[action_type] += 1
        else:
            impossible_actions[action_type] += 1

        obs, reward, done, truncated, info = env.step(action)
        scores[env.current_player] += reward
        moves[env.current_player] += 1

        turn += 1

    # TODO : A définir + A créer manuellement pour le moment
    # TODO : Créer un fichier de règles (faire aussi pour les autres paramètres)
    rules = SetOfRulesToInsert(rules_ids=config["rules_ids"]) 
    """
    INSERT INTO game_rule (game_rule_id, name, description)
    VALUES (0, 'Test Rule', 'Règle pour tester.');
    """
    
    players = [
        PlayerToInsert(
            name=agent_names[i],
            is_human=False, # TODO : Changer cela en fonction du type (normalement toujours False je crois)
            player_id= 1, # TODO : Changer cela pour avoir un id unique par joueur
            turn_order=i + 1,
            nb_moves=moves[i],
            is_winner=(scores[i] == max(scores)),
            score=scores[i],
            # TODO : Ajouter d'autres paramètres
        )
        for i in range(env.num_players)
    ]
    store_final_game_data(players=players, rules=rules)


    print("Partie terminée")
    print("Résumé des actions intentionnelles:")
    for action_type, count in intentional_actions.items():
        print(f"- Action {action_type.name}: {count} fois")

    print()
    print("Résumé des actions impossibles:")
    for action_type, count in impossible_actions.items():
        print(f"- Action {action_type.name}: {count} fois")

    print()
    pct_tour_imp = sum(impossible_actions.values()) / (sum(intentional_actions.values()) + sum(impossible_actions.values()))
    print("Pourcentage coups impossibles : ", round(pct_tour_imp * 100, 2), "%")
    print()
    print("Scores :", scores)
    print("Nombre de coups :", moves)
    print("Nombre de tours :", turn)

# TODO : Lancer plusieurs parties et enregistrer les statistiques
play_game(env, agents, agent_names)