# INFO :  Script à lancer depuis le répertoire db
# Permet d'enregistrer les statistiques d'une partie dans la base de données

# TODO : Ajouter la possibilité de faire jouer des joueurs avec des timesteps différents

import sys
import os
import itertools

from collections import defaultdict
from stable_baselines3 import PPO
from config_game import config_param, generate_game_config
from insert import store_final_game_data, PlayerToInsert, SetOfRulesToInsert

racine_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../game"))
sys.path.append(racine_dir)

from ludo_env import LudoEnv
from ludo_env.action import Action_NO_EXACT, Action_EXACT
from ludo_env.reward import AgentType
from config import config_param, print_all_configs

# Fonction pour faire jouer des agents les uns contre les autres
def play_game(env, agents, agent_names, config):
    obs, info = env.reset()
    done = False
    turn = 0

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
            # TODO CHARLOTTE ZOE REWARD ASSOCIEE BONNE ACTION action = ... # prendre une action valide 

        obs, reward, done, truncated, info = env.step(action)
        scores[env.current_player] += reward
        moves[env.current_player] += 1

        turn += 1

    rules = SetOfRulesToInsert(rules_ids=config["rules_ids"]) 
    nb_actions_interdites = [env.nb_actions_interdites[player] for player in range(env.num_players)]
    
    players = [
        PlayerToInsert(
            name=agent_names[i],
            is_human=False, # TODO : Gérer le cas quand c'est un humain
            turn_order=i + 1,
            nb_moves=moves[i],
            is_winner=(scores[i] == max(scores)),
            score=scores[i],
            strategy=config["strategy"][i],
            player_id=None,
            nb_train_steps=config["nb_train_steps"][i],
            nb_actions_interdites=nb_actions_interdites[i],
            # TODO : Ajouter d'autres paramètres
        )
        for i in range(env.num_players)
    ]

    actions_stats_by_player = env.export_action_stats()
    store_final_game_data(players=players, rules=rules, actions_stats_by_player=actions_stats_by_player)

# Main pour lancer une partie en choisissant les paramètres voulu depuis le terminal
def main():
    
    # Choix config
    print_all_configs()
    num_conf = int(input("Entrez le numéro de configuration : "))

    # Choix nombre de joueurs et de chevaux
    num_players = int(input("Entrez le nombre de joueurs : "))
    nb_chevaux = int(input("Entrez le nombre de chevaux : "))

    # Vérifie si des agents sont entrainés
    agent_dir = os.path.join(racine_dir, f"reinforcement_learning/agents/{num_players}_joueurs/{nb_chevaux}_pions/conf_{num_conf}")
    if not os.path.exists(agent_dir):
        print(f"Erreur : Le répertoire {agent_dir} n'existe pas. Aucun agent n'est disponible pour ces paramètres.")
        return
    
    # Agents disponibles par timesteps
    agents_by_timesteps = {}
    
    for filename in os.listdir(agent_dir):
        if filename.endswith(".zip"):
            parts = filename.split("_")
            try:
                timesteps = int(parts[-2])
                agent_type = parts[0]
            except (IndexError, ValueError):
                print(f"Fichier ignoré : {filename}")
                continue
        
            if timesteps not in agents_by_timesteps:
                agents_by_timesteps[timesteps] = []
            agents_by_timesteps[timesteps].append(agent_type)
    
    if agents_by_timesteps:
        print("Agents disponibles par total_timesteps :")
        for timesteps, agents in sorted(agents_by_timesteps.items()):
            print(f"{timesteps} steps : {', '.join(sorted(agents))}")
    else:
        print("Aucun agent entraîné trouvé dans ce répertoire.")
        return

    available_agents = set()
    for filename in os.listdir(agent_dir):
        available_agents.add(filename)
    
    if not available_agents:
        print(f"Aucun agent correspondant n'est disponible dans le répertoire {agent_dir}.")
        return

    # Affichage des agents disponibles
    available_agents = list(available_agents)
    print("\nTypes d'agents disponibles :")
    for idx, agent in enumerate(available_agents, start=1):
        print(f"{idx}. {agent}")

    # Choix types d'agents dans la partie
    agent_indices = input(f"Entrez les numéros des agents dans l'ordre (séparés par des espaces, {num_players} à choisir) : ")
    agent_indices = list(map(int, agent_indices.split()))
    if len(agent_indices) != num_players:
        print("Le nombre de types d'agents ne correspond pas au nombre de joueurs.")
        return

    selected_agents = [available_agents[idx - 1] for idx in agent_indices]

    agent_paths = []
    found = False
    for filename in selected_agents:
        agent_paths.append(os.path.join(agent_dir, filename))
        found = True
    if not found:
        print(f"Erreur : Aucun fichier d'agent correspondant à '{agent_type}' dans {agent_dir}.")
        return

    try:
        agents = [PPO.load(path) for path in agent_paths]
        agent_names = [os.path.basename(path) for path in agent_paths]
    except Exception as e:
        print(f"Erreur lors du chargement des agents : {e}")
        return

    # Configuration de l'env
    config_param_for_env = config_param[num_conf]
    config = generate_game_config(
        num_players=num_players,
        nb_chevaux=nb_chevaux,
        my_config_param=config_param_for_env,
        nb_train_steps=[int(agent.split("_")[5]) for agent in selected_agents],  # Extraire les timesteps depuis les noms d'agents
        num_conf=num_conf,
        agent_types=[agent.split("_")[0] for agent in selected_agents]  # Extraire les types d'agents
    )
             
    env = LudoEnv(
        num_players=config["num_players"],
        nb_chevaux=config["nb_chevaux"],
        mode_fin_partie=config["mode_fin_partie"],
        mode_ascension=config["mode_ascension"],
        mode_pied_escalier=config["mode_pied_escalier"],
        mode_rejoue_6=config["mode_rejoue_6"],
        mode_rejoue_marche=config["mode_rejoue_marche"],
        mode_protect=config["mode_protect"],
        mode_gym="stats_game",
    )

    # Choix nombre parties
    num_games = int(input("\nEntrez le nombre de parties à jouer : "))

    # Lancer les parties
    for i in range(1, num_games + 1):
        print(f"\n=== Partie {i}/{num_games} ===")
        play_game(env, agents, agent_names, config)

if __name__ == "__main__":
    main()
