# INFO :  Script à lancer depuis le répertoire db
# Permet d'enregistrer les statistiques d'une partie dans la base de données

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
from ludo_env.reward import AgentType
from config import config_param, print_all_configs

def convert_to_agent_type(agent_str):
    """Convert string agent type to AgentType enum value"""
    agent_str = agent_str.lower()
    if agent_str == "balanced":
        return AgentType.BALANCED
    elif agent_str == "aggressive":
        return AgentType.AGGRESSIVE
    elif agent_str == "rusher":
        return AgentType.RUSHER
    elif agent_str == "defensive":
        return AgentType.DEFENSIVE
    elif agent_str == "spawner":
        return AgentType.SPAWNER
    elif agent_str == "suboptimal":
        return AgentType.SUBOPTIMAL
    else:
        raise ValueError(f"Unknown agent type: {agent_str}")

# Fonction pour faire jouer des agents les uns contre les autres
def play_game(env, agents, agent_names, config):
    obs, info = env.reset()
    done = False
    turn = 0

    reward_action_agent = [0] * env.num_players
    reward_rectified = [0] * env.num_players
    moves = [0] * env.num_players
    nb_mouvements_interdits = [0] * env.num_players

    actions_stats_resquested = [defaultdict(int) for _ in range(env.num_players)]
    actions_stats_realized = [defaultdict(int) for _ in range(env.num_players)]

    while not done:
        
        current_player = env.current_player # car on a pas encore appelé env.step

        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)

        if env.current_player < len(agents):
            action, _ = agents[env.current_player].predict(obs, deterministic=True)
        else:
            raise ValueError("Nombre de joueurs non supporté")

        action_type_requested = env.game.decode_action(action)[1]
        actions_stats_resquested[env.current_player][action_type_requested] += 1

        obs, reward, done, truncated, info = env.step(action)

        current_player = info["current_player"] # on a appelé env.step donc on a changé de joueur
        
        
        moves[current_player] += 1

        if info["rectified"]:
            nb_mouvements_interdits[current_player] += 1

        action_type_realized = info["action_rectified"]
        actions_stats_realized[current_player][action_type_realized] += 1

        reward_action_agent[current_player] += info["reward_action_agent"]
        reward_rectified[current_player] += info["reward_rectified"]

        turn += 1

    winning_player_id = env.game.is_winner()
    pawns_in_goal = env.get_pawns_in_goal()
    rules = SetOfRulesToInsert(rules_ids=config["rules_ids"]) 

    assert winning_player_id != -1, "Aucun gagnant"
    
    players = [
        PlayerToInsert(
            name=agent_names[i],
            is_human=False,
            turn_order=i + 1,
            nb_moves=moves[i],
            is_winner=(i == winning_player_id),
            reward_action_agent=reward_action_agent[i],
            reward_rectified=reward_rectified[i],
            strategy=config["strategy"][i],
            player_id=None,
            nb_train_steps=config["nb_train_steps"][i],
            nb_actions_interdites=nb_mouvements_interdits[i],
            nb_pawns_in_goal=pawns_in_goal[i],
        )
        for i in range(env.num_players)
    ]

    actions_stats_by_player = {}
    for i in range(env.num_players):
        actions_stats_by_player[i] = {
            "requested": {str(k): v for k, v in actions_stats_resquested[i].items()},
            "realized": {str(k): v for k, v in actions_stats_realized[i].items()},
        }

    store_final_game_data(players=players, rules=rules, actions_stats_by_player=actions_stats_by_player, nb_pawns=config["nb_chevaux"], num_config=config["num_conf"])

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
    available_agents = sorted(list(available_agents))
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

    agent_types_enums = [convert_to_agent_type(agent.split("_")[0]) for agent in selected_agents]

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
        agent_types=agent_types_enums,
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


# Fonction permettant de lancer des parties automatiquement entre mêmes agents
def main_auto(num_conf, num_players, nb_chevaux, num_games):
    # Vérifie si des agents sont entraînés
    agent_dir = os.path.join(racine_dir, f"reinforcement_learning/agents/{num_players}_joueurs/{nb_chevaux}_pions/conf_{num_conf}")
    if not os.path.exists(agent_dir):
        print(f"Erreur : Le répertoire {agent_dir} n'existe pas. Aucun agent n'est disponible pour ces paramètres.")
        return
    
    # Chargement de tous les agents dispo
    available_agents = sorted([filename for filename in os.listdir(agent_dir) if filename.endswith(".zip")])
    if not available_agents:
        print(f"Aucun agent correspondant n'est disponible dans le répertoire {agent_dir}.")
        return

    #print("\nAgents disponibles :")
    #for idx, agent in enumerate(available_agents, start=1):
    #    print(f"{idx}. {agent}")
    
    # Chargement des paths
    agent_paths = [os.path.join(agent_dir, agent) for agent in available_agents]
    
    try:
        agents = [PPO.load(path) for path in agent_paths]
        agent_names = [os.path.basename(path) for path in agent_paths]
    except Exception as e:
        print(f"Erreur lors du chargement des agents : {e}")
        return

    # Lancement des parties
    for agent, agent_name in zip(agents, agent_names):
        print(f"\n=== Partie pour l'agent : {agent_name} ===")

        # Répéter l'agent pour chaque joueur
        agent_team = [agent] * num_players
        agent_names_team = [agent_name] * num_players

        # Configuration de l'environnement
        config_param_for_env = config_param[num_conf]
        
        nb_train_steps = [int(agent.split("_")[-2].replace("steps", "")) for agent in available_agents]
        agent_index = available_agents.index(agent_name)
        steps = nb_train_steps[agent_index]
        
        # Type d'agent identique pour tous les joueurs
        agent_type = available_agents[0].split("_")[0]
        agent_types_enums = [convert_to_agent_type(agent_type) for _ in range(num_players)] 

        config = generate_game_config(
            num_players=num_players,
            nb_chevaux=nb_chevaux,
            my_config_param=config_param_for_env,
            nb_train_steps=[steps] * num_players,
            num_conf=num_conf,
            agent_types=[agent_name.split("_")[0]] * num_players
        )

        env = LudoEnv(
            num_players=config["num_players"],
            nb_chevaux=config["nb_chevaux"],
            agent_types=agent_types_enums,
            mode_fin_partie=config["mode_fin_partie"],
            mode_ascension=config["mode_ascension"],
            mode_pied_escalier=config["mode_pied_escalier"],
            mode_rejoue_6=config["mode_rejoue_6"],
            mode_rejoue_marche=config["mode_rejoue_marche"],
            mode_protect=config["mode_protect"],
            mode_gym="stats_game",
        )

        for i in range(1, num_games + 1):
            print(f"\n=== Partie {i}/{num_games} avec l'agent {agent_name} ===")
            play_game(env, agent_team, agent_names_team, config)

def get_200k_agents(agent_dir):
    """Get all available agents with 200000 training steps."""
    available_agents = {}
    for filename in os.listdir(agent_dir):
        if filename.endswith(".zip"):
            parts = filename.split("_")
            agent_type = parts[0]  # e.g., 'balanced', 'aggressive'
            steps = int(parts[-2])
            
            # Only keep 200000-step agents
            if steps == 200000:
                available_agents[agent_type] = filename
                
    return available_agents

def main_auto_matchups(num_conf, num_players, nb_chevaux, games_per_matchup=100):
    """Run games between different agent types, all with 200000 training steps."""
    agent_dir = os.path.join(racine_dir, 
        f"reinforcement_learning/agents/{num_players}_joueurs/{nb_chevaux}_pions/conf_{num_conf}")
    
    if not os.path.exists(agent_dir):
        print(f"Error: Directory {agent_dir} doesn't exist.")
        return

    # Get 200k-step agents
    available_agents = get_200k_agents(agent_dir)
    if not available_agents:
        print("No 200000-step agents found.")
        return
        
    agent_types = list(available_agents.keys())
    print(f"Found agent types: {agent_types}")

    # For 2 player games
    if num_players == 2:
        # Generate all possible pairs of agent types (including same-type matchups)
        type_matchups = list(itertools.combinations_with_replacement(agent_types, 2))
        
        for type1, type2 in type_matchups:
            print(f"\n=== Running matches: {type1} vs {type2} ===")
            
            try:
                agent1_path = os.path.join(agent_dir, available_agents[type1])
                agent2_path = os.path.join(agent_dir, available_agents[type2])
                
                agent1 = PPO.load(agent1_path)
                agent2 = PPO.load(agent2_path)
                agents = [agent1, agent2]
                agent_names = [
                    os.path.basename(agent1_path),
                    os.path.basename(agent2_path)
                ]

                agent_types_enums = [convert_to_agent_type(type1), convert_to_agent_type(type2)]
                
                # Configure environment
                config = generate_game_config(
                    num_players=num_players,
                    nb_chevaux=nb_chevaux,
                    my_config_param=config_param[num_conf],
                    nb_train_steps=[200000, 200000],
                    num_conf=num_conf,
                    agent_types=[type1, type2]
                )
                
                env = LudoEnv(
                    num_players=config["num_players"],
                    nb_chevaux=config["nb_chevaux"],
                    agent_types=agent_types_enums,
                    mode_fin_partie=config["mode_fin_partie"],
                    mode_ascension=config["mode_ascension"],
                    mode_pied_escalier=config["mode_pied_escalier"],
                    mode_rejoue_6=config["mode_rejoue_6"],
                    mode_rejoue_marche=config["mode_rejoue_marche"],
                    mode_protect=config["mode_protect"],
                    mode_gym="stats_game",
                )
                
                # Run multiple games for this matchup
                for i in range(1, games_per_matchup + 1):
                    print(f"Game {i}/{games_per_matchup}")
                    play_game(env, agents, agent_names, config)
                    
            except Exception as e:
                print(f"Error running matchup: {e}")
                continue
    
    # For 4 player games
    elif num_players == 4:
        # Generate interesting 4-player combinations
        type_matchups = []
        
        # Add 1v1v1v1 matchups (all different types)
        type_matchups.extend(list(itertools.combinations(agent_types, 4)))
        
        # Add 2v2 matchups
        for type1 in agent_types:
            for type2 in agent_types:
                if type1 <= type2:  # Avoid duplicates
                    type_matchups.append((type1, type1, type2, type2))
        
        for matchup in type_matchups:
            print(f"\n=== Running 4-player match: {' vs '.join(matchup)} ===")
            
            try:
                # Load all agents for this matchup
                agent_paths = [os.path.join(agent_dir, available_agents[agent_type]) 
                             for agent_type in matchup]
                agents = [PPO.load(path) for path in agent_paths]
                agent_names = [os.path.basename(path) for path in agent_paths]

                agent_types_enums = [convert_to_agent_type(agent_type) for agent_type in matchup]
                
                # Configure environment
                config = generate_game_config(
                    num_players=num_players,
                    nb_chevaux=nb_chevaux,
                    my_config_param=config_param[num_conf],
                    nb_train_steps=[200000] * 4,
                    num_conf=num_conf,
                    agent_types=list(matchup)
                )
                
                env = LudoEnv(
                    num_players=config["num_players"],
                    nb_chevaux=config["nb_chevaux"],
                    agent_types=agent_types_enums,
                    mode_fin_partie=config["mode_fin_partie"],
                    mode_ascension=config["mode_ascension"],
                    mode_pied_escalier=config["mode_pied_escalier"],
                    mode_rejoue_6=config["mode_rejoue_6"],
                    mode_rejoue_marche=config["mode_rejoue_marche"],
                    mode_protect=config["mode_protect"],
                    mode_gym="stats_game",
                )
                
                for i in range(1, games_per_matchup + 1):
                    print(f"Game {i}/{games_per_matchup}")
                    play_game(env, agents, agent_names, config)
                    
            except Exception as e:
                print(f"Error running matchup: {e}")
                continue

def main_lancer_parties_pour_analyse_entrainement() :
    main_auto(num_conf=16, num_players=2, nb_chevaux=2, num_games=100)
    main_auto(num_conf=17, num_players=2, nb_chevaux=2, num_games=100)
    main_auto(num_conf=12, num_players=2, nb_chevaux=2, num_games=100)
    
    main_auto(num_conf=16, num_players=2, nb_chevaux=4, num_games=100)
    main_auto(num_conf=17, num_players=2, nb_chevaux=4, num_games=100)
    main_auto(num_conf=12, num_players=2, nb_chevaux=4, num_games=100)

    main_auto(num_conf=16, num_players=4, nb_chevaux=4, num_games=100)
    main_auto(num_conf=17, num_players=4, nb_chevaux=4, num_games=100)
    main_auto(num_conf=12, num_players=4, nb_chevaux=4, num_games=100)

if __name__ == "__main__":
    main()
    # main_lancer_parties_pour_analyse_entrainement()


    # Run matchups with different configurations
    """configs_to_test = [16, 7, 1]
    player_counts = [4]
    pawn_counts = [2]
    
    for conf in configs_to_test:
        for players in player_counts:
            for pawns in pawn_counts:
                print(f"\n=== Testing config {conf}, {players} players, {pawns} pawns ===")
                main_auto_matchups(
                    num_conf=conf,
                    num_players=players,
                    nb_chevaux=pawns,
                    games_per_matchup=100
                )"""