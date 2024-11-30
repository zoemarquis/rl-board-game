# test : humain jouer contre modele entrainer
from stable_baselines3 import PPO

model = PPO.load(
    "reinforcement_learning/masked_ppo_ludo_model"
)  # notre modele entrainé


import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv

# Ajouter la racine du projet (zoe-petits-chevaux) au chemin Python


env = LudoEnv(
    num_players=2, nb_chevaux=2, mode_jeu="debug", print_action_invalide_mode=True
)
obs = env.reset()
obs = obs[0]
done = False

# TODO : à chaque tour : afficher à l'humain la liste des actions valides

while not done:

    print(env.game.get_str_game_overview())
    print("dé : ", obs["dice_roll"])  # Afficher le dé

    if env.current_player == 0:
        # Afficher l'état actuel du jeu
        print("-" * 50)
        print("TOUR DE L'HUMAIN")
        # print(env.game.get_instruction_for_player(env.current_player))
        # TODO : afficher le plateau global (vu par ce joueur) env.game.get_my_board_4_lignes(env.current_player)

        action_humain = int(
            input("Choisissez une action : ")
        )  # get action humain au clavier

        # Appliquez l'action de l'humain
        obs, reward, done, truncated, info = env.step(action_humain)

    elif env.current_player == 1:
        print()
        print("-" * 50)
        print("TOUR DE L'AGENT")
        # L'agent choisit une action via son modèle
        action_agent = model.predict(obs, deterministic=True)[0]
        pawn_id, action_type = env.game.decode_action(action_agent)
        print("Action de l'agent : ", action_agent, " action_agent ", action_type)
        obs, reward, done, truncated, info = env.step(action_agent)
    else:
        raise ValueError("Il n'y a que 2 joueurs dans le jeu")
