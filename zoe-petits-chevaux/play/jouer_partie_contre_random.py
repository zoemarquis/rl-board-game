# ce fichier c'est pour jouer une partie contre un agent random
# à terme enfaite on aurait un fichier main, on spécifie qui joue contre qui et on lance la partie (Random Agent, PPO ...)
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import LudoEnv
from reinforcement_learning.agent import RandomAgent

env: LudoEnv = LudoEnv(num_players=2, nb_chevaux=2)


def play_game(env, agents):
    obs, info = env.reset()
    done = False
    turn = 0

    while not done:
        print(env.game.get_str_game_overview())
        current_agent = agents[env.current_player]
        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)
        print("main dé : ", env.dice_roll)
        print("main valid_actions : ", valid_actions)

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

    print(f"Partie terminée. Joueur {env.current_player} a gagné !")


agent1 = RandomAgent(env.action_space)
agent2 = RandomAgent(env.action_space)

agents = [agent1, agent2]  # Liste des agents
play_game(env, agents)
