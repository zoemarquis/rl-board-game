import gymnasium as gym
import numpy as np
from gymnasium import spaces
from ludo_env.constants import BOARD_SIZE, NUM_PLAYERS, PIECES
from ludo_env.game_logic import GameLogic
from ludo_env.renderer import Renderer
from gym.spaces import Discrete, Dict, Box


class LudoEnv(gym.Env):
    def __init__(self, render_mode='rgb_array', num_players = 2):
        super(LudoEnv, self).__init__()
        self.metadata = {'render.modes': ['human', 'rgb_array'], "render_fps": 10}
        self.render_mode = render_mode

        self.num_players = num_players
        self.num_pawns = 2
        self.board_size = 56
        self.safe_zone_size = 6

        self.game_logic = GameLogic()
        self.renderer = Renderer()

        self.action_space = Dict({
            f"pawn_{i}": Discrete(len(Action)) for i in range(1, self.num_pawns + 1)
        })

        self.observation_space =  Dict({
            "token_1": Dict({
                "position": Discrete(60),
                "state": Discrete(4),
                "distance_to_goal": Box(low=0, high=60, shape=(1,), dtype=np.int32),
                "conflict": Discrete(2),
                "actions_possibles": MultiBinary(len(Action))  # MOVE_OUT, MOVE, REACH_GOAL, NO_ACTION -> à ajuster
            }),
            "token_2": Dict({
                "position": Discrete(60),
                "state": Discrete(4),
                "distance_to_goal": Box(low=0, high=60, shape=(1,), dtype=np.int32),
                "conflict": Discrete(2)
            }),
            # Répéter pour chaque pion
        })

        self.reset()

    def reset(self, seed=None, options=None):
        """
        Reset the state of the environment and return an initial observation.

        Parameters:
        - seed (int, optional): Seed for random number generator.
        - options (dict, optional): Additional options for reset.

        Returns:
        - observation (dict): Initial observation of the environment.
        - info (dict): Additional info.
        """
        super().reset(seed=seed, options=options)
        self.board = np.full(self.board_size, -1)
        self.pawns = np.zeros((self.num_players, self.num_pawns), dtype=np.int8) # pions dans HOME
        self.current_player = 0
        return self._get_observation(), {}    

    # celui là
    def step(self, action):
        player_id = self.current_player
        dice_value = roll_dice() # TODO 
        valid_actions = get_valid_actions(self.board, self.pieces, player_id, dice_value)

        # ACTION + PION_ID * 10
        if action not in valid_actions:
            # décoder l'action : par pion et par action    # token_id, token_action = action // len(Action), action % len(Action)

            reward = -10 # euf faut qu'on fasse en sorte que on est action pour chaque pion
            print(f"Invalid action: {action} for player {player_id} with dice value {dice_value}")
        else: 
            self.board = updfate_board(self.board, self.pieces, player_id, action, dice_value)
            reward = calculate_reward(self.board, self.pieces, player_id, action, strategy_agent)

        done = is_game_over(self.board, self.pieces)

        # si le dé n'est pas un 6 -> joueur suivant
        if dice_value != 6:
            self.current_player = (self.current_player + 1) % NUM_PLAYERS

        observation = self._get_observation()
        return observation, reward, done, {}   

    def render(self, mode='human'):
        img = self.renderer.render(self.board, self.pieces)
        return img

    #def generate_observation(self):
    #    observation = {}
    #    for token_id, token in enumerate(self.tokens):  # Parcours de chaque pion
    #        possible_actions = self.get_possible_actions(token)  # Obtenir les actions valides
    #        observation[f"token_{token_id + 1}"] = {
    #            "position": token.position,
    #            "state": token.state,
    #            "distance_to_goal": np.array([self.goal_position - token.position], dtype=np.int32),
    #            "conflict": int(self.check_conflict(token)),
    #            "actions_possibles": self.encode_possible_actions(possible_actions)
    #        }
    #    return observation

    # def get_observation(self):
    # """
    # Generate the observation for the current player.
    #  
    # Returns:
    # - dict: Observation containing current state and valid actions.
    # """
    # player_id = self.current_player
    # dice_roll = self.current_dice_roll
    # player_positions = self.board[player_id]  # Positions of current player's pawns
    # opponent_positions = {pid: self.board[pid] for pid in range(self.num_players) if pid != player_id}
    # valid_actions = get_valid_actions(player_id, self.board, dice_roll)
    # 
    # return {
    #     "player_positions": player_positions,
    #     "opponent_positions": opponent_positions,
    #     "dice_roll": dice_roll,
    #     "valid_actions": valid_actions,
    # }


    # def _update_state_and_position(token, action, dice_roll):
    #     if action == Action.MOVE_OUT:
    #         token["state"] = State.PATH
    #         token["position"] = 1  # Sortie de HOME vers la première case
    #     elif action == Action.MOVE_FORWARD:
    #         token["position"] += dice_roll
    #         if token["position"] >= 50:  # Exemple : zone de sécurité après la case 50
    #             token["state"] = State.SAFEZONE
    #     elif action == Action.ENTER_SAFEZONE:
    #         token["state"] = State.SAFE
    #     elif action == Action.REACH_GOAL:
    #         token["state"] = State.SAFE
    #         token["position"] = "Goal"    
            
