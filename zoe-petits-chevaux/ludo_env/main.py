from ludo_env import LudoEnv, Action
import numpy as np
from constants import NB_PAWNS

class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, valid_actions_encoded):
        if 0 in valid_actions_encoded:
            return 0
        # sinon random
        return np.random.choice(valid_actions_encoded)

env = LudoEnv()

def play_game(env, agents):
    obs, info = env.reset()
    done = False
    turn = 0

    while not done:
        env.game.print_board_overview()
        current_agent = agents[env.current_player]
        valid_actions = env.game.get_valid_actions(env.current_player, env.dice_roll)
        encoded_valid_actions = env.game.encode_valid_actions(valid_actions)
        print("main dé : ", env.dice_roll)
        print("main valid_actions : ", valid_actions)
        
        # L'agent choisit une action
        action = current_agent.choose_action(encoded_valid_actions)
        print("main choose action : ", action)
        
        # Effectue une étape dans l'environnement
        obs, reward, done, info = env.step(action)

        # Affiche des informations pour vérifier
        print(f"Tour {turn} - Joueur {env.current_player}: Action {action}, Récompense {reward}")
        turn += 1

    print(f"Partie terminée. Joueur {env.current_player} a gagné !")

agent1 = RandomAgent(env.action_space)
agent2 = RandomAgent(env.action_space)

agents = [agent1, agent2]  # Liste des agents
play_game(env, agents)
