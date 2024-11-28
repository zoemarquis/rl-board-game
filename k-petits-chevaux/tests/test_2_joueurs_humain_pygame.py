# Ajouter la racine du projet (zoe-petits-chevaux) au chemin Python
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
import pygame

env = LudoEnv(print_action_invalide_mode=True, with_render=True, mode_jeu="debug")

def play_game(env):
    obs, info = env.reset()
    done = False

    while not done: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break
        
        env.render(env.game)

        print("-"*50)
        print("current_player : ", env.current_player)
        print("dé : ", obs["dice_roll"])
        print()
        print(env.game.get_str_game_overview())
        print(env.game.get_instruction_for_player(env.current_player))
        print("actions valides : ", env.game.get_valid_actions(env.current_player, obs["dice_roll"]))
        print("encoded valid actions : ", env.game.encode_valid_actions(env.game.get_valid_actions(env.current_player, obs["dice_roll"])))
        # TODO voir tout le plateau : home, chemin selon mon pdv, escalier et goal
        # TODO : voir les actions possibles

        action = int(input("Choisissez une action : "))
        obs, reward, done, truncated, info = env.step(action)
        env.render(env.game)


play_game(env)
pygame.quit()