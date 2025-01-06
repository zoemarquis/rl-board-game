# Ajouter la racine du projet au chemin Python
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
from reinforcement_learning.agent import RandomAgent
import pygame
import time

env = LudoEnv(
    with_render=True,
    num_players=2,
    nb_chevaux=2,
    mode_fin_partie="tous",
    mode_gym="jeu",
)


def play_game(env, agents):
    obs, info = env.reset()
    done = False
    turn = 0

    env.render(env.game, players_type=["ai", "ai"])

    while not done:
        print("-" * 50)
        current_agent = agents[env.current_player]
        # For humain to be able to see game progress
        time.sleep(0.3)

        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)

        # L'agent choisit une action
        action = current_agent.choose_action(encoded_valid_actions)
        print("main choose action : ", action)

        # Effectue une étape dans l'environnement
        obs, reward, done, truncated, info = env.step(action)

        # Affiche des informations pour vérifier
        print(
            f"Tour {turn} - Joueur {env.current_player}: Action {action}, Récompense {reward}"
        )
        turn += 1

        env.render(env.game, players_type=["ai", "ai"])


agent1 = RandomAgent(env.action_space)
agent2 = RandomAgent(env.action_space)

play_game(env, [agent1, agent2])
pygame.quit()
