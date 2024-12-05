# Fichier permettant de faire jouer 2 agents avec 4 pions chacun l'un contre l'autre

import sys
from pathlib import Path
from collections import defaultdict
from stable_baselines3 import PPO

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
from ludo_env.action import Action_NO_EXACT

agent1_model = PPO.load("reinforcement_learning/checkpoints/agent_600000_steps.zip")
agent2_model = PPO.load("reinforcement_learning/checkpoints/agent_600000_steps.zip")


env = LudoEnv(num_players=2, nb_chevaux=4, mode_gym="jeu", mode_fin_partie="tous_pions")

intentional_actions = defaultdict(int)
impossible_actions = defaultdict(int)

def play_game(env, agents):
    obs, info = env.reset()
    done = False
    turn = 0

    while not done:
        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)


        if env.current_player == 0:
            print("Agent 1")
            action, _ = agents[0].predict(obs, deterministic=True)
        elif env.current_player == 1:
            print("Agent 2")
            action, _ = agents[1].predict(obs, deterministic=True)

        else:
            raise ValueError("Nombre de joueurs non supporté")
        

        _, action_type = env.game.decode_action(action)
        print()
        if action in encoded_valid_actions:
            intentional_actions[action_type] += 1
        else:
            impossible_actions[action_type] += 1

        obs, reward, done, truncated, info = env.step(action)

        turn += 1

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
    print("Pourcentage coups impossibles : ", round(pct_tour_imp*100,2), "%")

    print()

    print("Tour total : ", turn)



# Lancer la partie
play_game(env, [agent1_model, agent2_model])