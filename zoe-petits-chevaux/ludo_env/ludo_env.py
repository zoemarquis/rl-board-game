import gymnasium as gym
import numpy as np
from gymnasium import spaces
from constants import *
from game_logic import GameLogic
# from renderer import Renderer
from gym.spaces import Discrete, Dict, Box
from game_logic import Action


class LudoEnv(gym.Env):
    def __init__(self, render_mode='rgb_array'): # pas num_players et NUM_PLAYERS
        super(LudoEnv, self).__init__()
        self.metadata = {'render.modes': ['human', 'rgb_array'], "render_fps": 10}
        self.render_mode = render_mode

        self.num_players = NUM_PLAYERS
        self.num_pawns = 2
        self.board_size = 56
        self.safe_zone_size = 6

        # self.renderer = Renderer()

        self.action_space = Discrete(self.num_pawns * len(Action))
        self.observation_space = Dict({
            "my_board": Box(low=0, high=NB_PAWNS, shape=(TOTAL_SIZE,), dtype=np.int8),  # État du plateau du joueur courant
            "adversaire_board": Box(low=0, high=NB_PAWNS * (NUM_PLAYERS - 1), shape=(TOTAL_SIZE,), dtype=np.int8),  # Agrégation des autres joueurs
            "dice_roll": Discrete(6),  # Résultat du dé (1 à 6)
        })

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.board = np.full(self.board_size, -1) # TODO : revoir en fonction observation
        self.pawns = np.zeros((self.num_players, self.num_pawns), dtype=np.int8) # # TODO revoir en fonction observation
        self.current_player = 0
        self.dice_roll = None  # Aucun jet au début
        self.game = GameLogic()
        return self._get_observation(), {}    

    def render(self, mode='human'):
        img = self.renderer.render(self.board, self.pieces)
        return img

    def _get_observation(self):
        return {
            "my_board": self.game.board[self.current_player], # TODO : mettre un getter
            "adversaire_board": self.game.get_adversaire_relative_overview(self.current_player),
            "dice_roll": self.dice_roll,
        }


    def step(self, action):
        token_id, action_type = divmod(action, len(Action))

        # TODO urgent is valid action
        # if not self.i__valid_action reward -10
        # ou alors dire que c'est NO ACTION ? comment faire ça ?
        # else move + calulate reward
        # valid_actions = self.game.get_valid_actions(player_id, dice_value)

        done = self.game.is_game_over()

        # si le dé n'est pas un 6 -> joueur suivant
        if dice_value != 6:
            self.current_player = (self.current_player + 1) % NUM_PLAYERS


        dice_value = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, {}   