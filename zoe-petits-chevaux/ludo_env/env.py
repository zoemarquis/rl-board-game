import gymnasium as gym

import numpy as np

from ludo_env.game_logic import GameLogic, NB_CHEVAUX, NUM_PLAYERS, TOTAL_SIZE, Action, BOARD_SIZE
from ludo_env.renderer import Renderer


class LudoEnv(gym.Env):
    def __init__(self, with_render=False, print_action_invalide_mode=True, mode_jeu="normal"):
        super(LudoEnv, self).__init__()
        self.metadata = {"render.modes": ["human", "rgb_array"], "render_fps": 10}
        self.with_render = with_render
        self.print_action_invalide_mode = print_action_invalide_mode
        self.mode_jeu = mode_jeu

        self.num_players = NUM_PLAYERS
        self.num_pawns = 2
        self.board_size = 56
        self.safe_zone_size = 6

        if self.with_render:
            self.renderer = Renderer()

        self.action_space = gym.spaces.Discrete(
            2 + NUM_PLAYERS * (len(Action) - 2)
        )  # 1 pour NO_ACTION + 1 pour sortir un pion
        # TODO : à modifier quand on ajoute des actions, pour l'instant on a donc 10 actions possibles

        self.observation_space = gym.spaces.Dict(
            {
                # TODO : est ce qu'on garde my board ou alors on fait my home, my chemin, my escalier, my goal ?
                "my_board": gym.spaces.Box(
                    low=0, high=NB_CHEVAUX, shape=(TOTAL_SIZE,), dtype=np.int8
                ),  # État du plateau du joueur courant
                # "my_chemin_with_adversaires": gym.spaces.Box(
                #     low=0,
                #     high=NB_CHEVAUX * (NUM_PLAYERS - 1),
                #     shape=(BOARD_SIZE,),
                #     dtype=np.int8,
                # ),  # Agrégation des autres joueurs selon quel pdv ? TODO
                "dice_roll": gym.spaces.Discrete(7),  # Résultat du dé (1 à 6)
                # TODO : ajouter ici vu global distances ?
                # TODO : observer aussi les state des pions ?
            }
        )

        self.reset()

    def _get_observation(self):
        obs = {
            "my_board": self.game.board[self.current_player],
            # "my_chemin_with_adversaires": self.game.get_board_pour_voir_ou_sont_adversaires_sur_mon_plateau(
            #     self.current_player
            # ),  # TODO : ici ça ne fonctionne que quand NUM_PLAYERS = 2, on a pas encore testé pour plus
            # TODO je crois qu'on retournne pas ce qu'il fait pour les plateaux des adversaires : on veut les adversaires sur NOTRE plateau
            "dice_roll": self.dice_roll,
        }
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.current_player = 0
        self.game : GameLogic = GameLogic()
        self.dice_roll = self.game.dice_generator()
        return self._get_observation(), {}

    def render(self, game, mode="human"):
        if self.with_render:
            self.renderer.render(self.game)

    def step(self, action):
        obs = self._get_observation()
        if self.mode_jeu == "debug":
            print("dé : ", obs["dice_roll"])
            print("my board : ", obs["my_board"])
        info = {}
        pawn_id, action_type = self.game.decode_action(action)
        valid_actions = self.game.get_valid_actions(self.current_player, self.dice_roll)
        encoded_valid_actions = self.game.encode_valid_actions(valid_actions)
        if action not in encoded_valid_actions:
            if self.print_action_invalide_mode:
                print(f"ACTION INTERDITE : {Action(action%len(Action))} not in valid_actions {valid_actions} : {encoded_valid_actions}")
            if self.mode_jeu == "debug":
                # random action dans les actions valides
                action = np.random.choice(encoded_valid_actions)
                pawn_id, action_type = self.game.decode_action(action)
                print("random action : ", action)
            else : 
                return self._get_observation(), -10, False, False, {}

        pawn_pos = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]

        self.game.move_pawn(self.current_player, pawn_pos, self.dice_roll, action_type)
        reward = self.game.get_reward(action_type)
        done = self.game.is_game_over()

        if not done:
            self.current_player = (self.current_player + 1) % NUM_PLAYERS
            if self.current_player == 0:
                self.game.tour += 1

        # TODO : 6 alors on rejoue

        self.dice_roll = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, False, {}
