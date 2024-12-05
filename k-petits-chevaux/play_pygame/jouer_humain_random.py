# Ajouter la racine du projet au chemin Python
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
from reinforcement_learning.agent import RandomAgent
import pygame
import time

def handle_mouse_click(event, button_mapping):
    """
    Handle a mouse click event and return the action associated with the clicked button.
    """
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
        mouse_pos = event.pos
        for (x, y, width, height), action in button_mapping.items():
            # Check if the mouse click is within the button's rectangle
            if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                return action  # Return the associated action
    return None  # No button was clicked

env = LudoEnv(with_render=True, num_players=2, nb_chevaux=2, mode_fin_partie="tous_pions", mode_gym="jeu")
players_type = ["human", "ai"]

def play_game(env):
    obs, info = env.reset()
    done = False
    turn = 0

    env.render(env.game, players_type = players_type)

    while not done: 
        button_mapping = env.renderer.button_mapping

        if env.current_player == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break

                # Handle mouse click
                selected_action = handle_mouse_click(event, button_mapping)
                if selected_action is not None:
                    print("-" * 50)
                    print("TOUR DE L'HUMAIN")
                    # Perform the action
                    action = selected_action
                    obs, reward, done, truncated, info = env.step(action)
                    turn += 1
                    env.render(env.game, players_type = players_type)
                else:
                    # Print message that need to click on a button
                    env.renderer.show_click_button_message()
        
        elif env.current_player == 1:
            print()
            print("-" * 50)
            print("TOUR DE L'AGENT")
            time.sleep(1)

            valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
            encoded_valid_actions = env.game.encode_valid_actions(valid_actions)

            # L'agent choisit une action
            action = agent.choose_action(encoded_valid_actions)
            print("main choose action : ", action)

            # Effectue une étape dans l'environnement
            obs, reward, done, truncated, info = env.step(action)

            # Affiche des informations pour vérifier
            print(
                f"Tour {turn} - Joueur {env.current_player}: Action {action}, Récompense {reward}"
            )
            turn += 1

            env.render(env.game, players_type = players_type)

agent = RandomAgent(env.action_space)

play_game(env)
pygame.quit()