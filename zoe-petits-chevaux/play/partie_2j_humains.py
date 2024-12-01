from interaction import get_human_action

# Ajouter la racine du projet (zoe-petits-chevaux) au chemin Python
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv

env = LudoEnv(
    num_players=2, nb_chevaux=3, mode_gym="jeu", mode_fin_partie="un_pion"
)


def play_game(env):
    obs, info = env.reset()
    done = False

    while not done:
        print("-" * 50)
        print("current_player : ", env.current_player)
        print("dé : ", obs["dice_roll"])
        print()
        print(env.game.get_str_game_overview())
        # print(env.game.get_instruction_for_player(env.current_player, obs["dice_roll"]))
        print(
            "actions valides : ",
            env.game.get_valid_actions(env.current_player, obs["dice_roll"]),
        )
        encoded_valid_actions = env.game.encode_valid_actions(
            env.game.get_valid_actions(env.current_player, obs["dice_roll"])
        )
        print("encoded valid actions : ", encoded_valid_actions)
        # TODO voir tout le plateau : home, chemin selon mon pdv, escalier et goal
        # TODO : voir les actions possibles

        action = int(get_human_action(encoded_valid_actions))
        obs, reward, done, truncated, info = env.step(action)


play_game(env)
