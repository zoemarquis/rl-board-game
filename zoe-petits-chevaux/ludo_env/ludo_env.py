import gymnasium as gym
import numpy as np
from gymnasium import spaces
from constants import *
from game_logic import GameLogic
# from renderer import Renderer
# from gym.spaces import Discrete, Dict, Box
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

        self.action_space = gym.spaces.Discrete(1 + NUM_PLAYERS * (len(Action) - 1))  # 1 pour NO_ACTION
        
        # self.observation_space = gym.spaces.Dict({
        #     "my_board": gym.spaces.Box(low=0, high=NB_PAWNS, shape=(TOTAL_SIZE,), dtype=np.int8),  # État du plateau du joueur courant
        #     "adversaire_board": gym.spaces.Box(low=0, high=NB_PAWNS * (NUM_PLAYERS - 1), shape=(TOTAL_SIZE,), dtype=np.int8),  # Agrégation des autres joueurs
        #     "dice_roll": gym.spaces.Discrete(6),  # Résultat du dé (1 à 6)
        # })
        # 
        self.observation_space = gym.spaces.Box(
            low=0,
            high=NB_PAWNS * NUM_PLAYERS,
            shape=(TOTAL_SIZE * NUM_PLAYERS + 1,),  # Taille totale + 1 pour le dé
            dtype=np.int8
        )


        self.reset()

    def _flatten_observation(self, observation):
        print(f"my_board: \t\t{observation['my_board']}")
        print(f"adversaire_board: \t{observation['adversaire_board']}")
        my_board = np.array(observation["my_board"]).flatten()
        adversaire_board = np.array(observation["adversaire_board"]).flatten()
        dice_roll = np.array([observation["dice_roll"]])
        return np.concatenate([my_board, adversaire_board, dice_roll])

    def _get_observation(self):
        print("get_observation")
        obs = {
            "my_board": self.game.board[self.current_player], 
            "adversaire_board": self.game.get_adversaire_relative_overview(self.current_player),
            "dice_roll": self.dice_roll,
        }
        return  self._flatten_observation(obs) #  obs #

    def reset(self, seed=None, options=None):
        print("reset")
        super().reset(seed=seed, options=options)
        self.board = np.full(self.board_size, -1) # TODO : revoir en fonction observation
        print("board", self.board)
        self.current_player = 0
        self.game = GameLogic()
        self.dice_roll = self.game.dice_generator()
        return self._get_observation(), {}    

    def render(self, mode='human'):
        img = self.renderer.render(self.board, self.pieces)
        return img

    

    def step(self, action):
        print("step : action", action)
        info = {}
        reward = 0 # TODO

        pawn_id, action_type = self.game.decode_action(action)
        print("action", action)
        print(f"pawn_id {pawn_id}, action_type {Action(action_type)}")

        valid_actions = self.game.get_valid_actions(self.current_player, self.dice_roll)
        encoded_valid_actions = self.game.encode_valid_actions(valid_actions)
        if action not in encoded_valid_actions:
            print(f"action {action} not in valid_actions {valid_actions}")
            return self._get_observation(), -10, False, {}

        # get_pawn position
        pawn_position = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]
        
        self.game.move_pawn(self.current_player, pawn_position, self.dice_roll, action_type)
        # reward = self.game.get_reward(self.current_player) TODO
        done = self.game.is_game_over()
        
        if not done and self.dice_roll != 6: # règle qu'on pourra faire changer
            self.current_player = (self.current_player + 1) % NUM_PLAYERS
            
        else: 
            info["replay"] = True

        self.dice_roll = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, {}   