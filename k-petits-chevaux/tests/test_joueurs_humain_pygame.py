# Ajouter la racine du projet (zoe-petits-chevaux) au chemin Python
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
import pygame

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


env = LudoEnv(with_render=True, num_players=2, nb_chevaux=3, mode_fin_partie="tous_pions", mode_gym="jeu")

def play_game(env):
    obs, info = env.reset()
    done = False

    env.render(env.game)

    while not done: 
        button_mapping = env.renderer.button_mapping

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

            # Handle mouse click
            selected_action = handle_mouse_click(event, button_mapping)
            if selected_action is not None:
                # Perform the action (e.g., update the game state)
                print("-"*50)
                print("current_player : ", env.current_player)
                print("dé : ", obs["dice_roll"])
                print()
                print(env.game.get_str_game_overview())
                # print(env.game.get_instruction_for_player(env.current_player, obs["dice_roll"]))
                print("actions valides : ", env.game.get_valid_actions(env.current_player, obs["dice_roll"]))
                # print("encoded valid actions : ", env.game.encode_valid_actions(env.game.get_valid_actions(env.current_player, obs["dice_roll"])))
                # TODO voir tout le plateau : home, chemin selon mon pdv, escalier et goal
                # TODO : voir les actions possibles

                # action = int(input("Choisissez une action : "))
                action = selected_action
                obs, reward, done, truncated, info = env.step(action)
                env.render(env.game)
            else:
                # Print message that need to click on a button
                env.renderer.show_click_button_message()

play_game(env)
pygame.quit()