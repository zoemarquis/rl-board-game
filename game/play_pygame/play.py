from stable_baselines3 import PPO

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
from play_pygame.launcher import setup_game, get_models, get_config
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


def play_game(env, players, players_types):
    obs, info = env.reset()
    done = False
    turn = 0

    env.render(env.game, players_type=players_types)

    while not done:

        if players_types[env.current_player] == "humain":
            button_mapping = env.renderer.button_mapping

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
                    env.render(env.game, players_type=players_types)
                else:
                    # Print message that need to click on a button
                    env.renderer.show_click_button_message()
        else:
            print()
            print("-" * 50)
            print("TOUR DE L'AGENT")
            # For humain to be able to see game progress
            time.sleep(0.3)

            # L'agent choisit une action via son modèle
            action_agent = players[env.current_player].predict(obs, deterministic=True)[0]
            pawn_id, action_type = env.game.decode_action(action_agent)

            print("Action de l'agent : ", action_agent, " action_agent ", action_type)
            obs, reward, done, truncated, info = env.step(action_agent)

            env.render(env.game, players_type=players_types)
        if done:
            time.sleep(2)


set_up_config = setup_game()
trad_config = get_config(set_up_config)
models = get_models(set_up_config=set_up_config, trad_config=trad_config)

print("models", models)

env = LudoEnv(
    with_render=True,
    num_players=set_up_config["num_players"],
    nb_chevaux=set_up_config["num_pawns"],
    mode_fin_partie=trad_config["mode_fin_partie"],
    mode_ascension=trad_config["mode_ascension"],
    mode_pied_escalier=trad_config["mode_pied_escalier"],
    mode_rejoue_6=trad_config["mode_rejoue_6"],
    mode_rejoue_marche=trad_config["mode_rejoue_marche"],
    mode_protect=trad_config["mode_protect"],
    mode_gym="jeu",
)
players_types = set_up_config["players_types"]

players = []
for model in models:
    if model == "humain":
        players.append(model)
    else:
        agent = PPO.load(model)
        players.append(agent)

play_game(env, players, players_types)
pygame.quit()