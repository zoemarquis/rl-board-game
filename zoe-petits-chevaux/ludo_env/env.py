import gymnasium as gym
import numpy as np

from ludo_env.game_logic import (
    GameLogic,
    TOTAL_SIZE,
    BOARD_SIZE,
)
from ludo_env.action import Action
from ludo_env.renderer import Renderer


class LudoEnv(gym.Env):
    def __init__(
        self,
        num_players,
        nb_chevaux,
        mode_fin_partie="tous_pions",

        mode_gym="entrainement",

        with_render=False,
    ):
        assert num_players in [2, 3, 4], "Only 2, 3 or 4 players are allowed"
        assert nb_chevaux in [2, 3, 4, 5, 6], "Only 2, 3, 4, 5 or 6 pawns are allowed"
        assert mode_fin_partie in [
            "tous_pions",
            "un_pion",
        ], "Only 'tous_pions' or 'un_pion' are allowed"
        assert mode_gym in [
            "entrainement",
            "jeu",
        ], "Only 'entrainement' or 'jeu' are allowed"

        super(LudoEnv, self).__init__()
        self.metadata = {"render.modes": ["human", "rgb_array"], "render_fps": 10}
        self.with_render = with_render
        self.mode_gym = mode_gym

        self.num_players = num_players
        self.nb_chevaux = nb_chevaux
        self.mode_fin_partie = mode_fin_partie

        self.board_size = 56  # TODO delete
        self.safe_zone_size = 6  # TODO delete

        if self.with_render:
            self.renderer = Renderer()

        self.action_space = gym.spaces.Discrete(
            3 + self.nb_chevaux * (len(Action) - 3)
        )  # 1 NO_ACTION + 1 MOVE_OUT + 1 MOVE_OUT_AND_KILl 

        self.observation_space = gym.spaces.Dict(
            {
                # "my_board": gym.spaces.Box(
                #     low=0, high=self.nb_chevaux, shape=(TOTAL_SIZE,), dtype=np.int8
                # ),  # État du plateau du joueur courant
                # # "my_chemin_with_adversaires": gym.spaces.Box(
                # #     low=0,
                # #     high=self.nb_chevaux * (self.num_players - 1),
                # #     shape=(BOARD_SIZE,),
                # #     dtype=np.int8,
                # # ),  # Agrégation des autres joueurs selon quel pdv ? TODO
                # "dice_roll": gym.spaces.Discrete(7),  # Résultat du dé (1 à 6)

                "my_ecurie" : gym.spaces.Discrete(self.nb_chevaux + 1),
                # État de l'écurie du joueur courant

                "my_chemin" : gym.spaces.Box(
                    low=-1, high=1, shape=(self.board_size,), dtype=np.int8
                ), # État du chemin du joueur courant : -1 = adversaire, 0 = vide, 1 = joueur courant

                "my_escalier" : gym.spaces.Box(
                    low=0, high=self.nb_chevaux, shape=(self.safe_zone_size,) , dtype=np.int8
                ), # État de l'escalier du joueur courant

                "my_goal" : gym.spaces.Discrete(self.nb_chevaux + 1),
                # État du goal du joueur courant

                "dice_roll": gym.spaces.Discrete(7),  # Résultat du dé (1 à 6)
            }
        )

        self.reset()

    def _get_observation(self):
        obs = {
            # "my_board": self.game.board[self.current_player],
            # # "my_chemin_with_adversaires": self.game.get_opponent_positions_on_my_board(
            # #     self.current_player
            # # ),  # TODO : ici ça ne fonctionne que quand self.num_players = 2, on a pas encore testé pour plus
            # # TODO je crois qu'on retournne pas ce qu'il fait pour les plateaux des adversaires : on veut les adversaires sur NOTRE plateau
            # "dice_roll": self.dice_roll,

            "my_ecurie" : self.game.get_observation_my_ecurie(self.current_player),
            "my_chemin" : self.game.get_observation_my_chemin(self.current_player),
            "my_escalier" : self.game.get_observation_my_escalier(self.current_player),
            "my_goal" : self.game.get_observation_my_goal(self.current_player),
            "dice_roll": self.dice_roll,
        }
        return obs

    def reset(self, seed=None, options=None):
        super().reset(seed=seed, options=options)
        self.current_player = 0
        self.game: GameLogic = GameLogic(
            num_players=self.num_players,
            nb_chevaux=self.nb_chevaux,
            mode_fin_partie=self.mode_fin_partie,
        )
        self.dice_roll = self.game.dice_generator()
        return self._get_observation(), {}

    def render(self, game, mode="human", players_type=["human", "human", "human", "human"]):
        if self.with_render:
            self.renderer.render(
                self.game, 
                self.current_player, 
                self.dice_roll,
                self.game.encode_valid_actions(self.game.get_valid_actions(self.current_player, self.dice_roll)),
                self.game.get_pawns_info(self.current_player),
                players_type)

    def step(self, action):
        obs = self._get_observation()
        if self.mode_gym == "jeu":
            print()
            print("joueur : ", self.current_player)
            print("dé : ", obs["dice_roll"])
            print("my_ecurie : ", obs["my_ecurie"])
            print("my_chemin : ", obs["my_chemin"])
            print("my_escalier : ", obs["my_escalier"])
            print("my_goal : ", obs["my_goal"])
        info = {}
        pawn_id, action_type = self.game.decode_action(action)
        valid_actions = self.game.get_valid_actions(self.current_player, self.dice_roll)
        encoded_valid_actions = self.game.encode_valid_actions(valid_actions)
        if action not in encoded_valid_actions:
            if self.mode_gym == "jeu":
                print(
                        f"ACTION INTERDITE : {Action(action%len(Action))} not in valid_actions {valid_actions} : {encoded_valid_actions}"
                )
                action = self.game.debug_action(encoded_valid_actions)
                pawn_id, action_type = self.game.decode_action(action)
                print("debug : ", action, pawn_id, action_type)
            else:
                self.change_player()
                return self._get_observation(), -10, False, False, {}

        pawn_pos = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]

        self.game.move_pawn(self.current_player, pawn_pos, self.dice_roll, action_type)
        reward = self.game.get_reward(action_type)
        done = self.game.is_game_over()

        if not done:
            self.change_player()

        # TODO : 6 alors on rejoue

        self.dice_roll = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, False, {}

    def change_player(self):
        self.current_player = (self.current_player + 1) % self.num_players
        if self.current_player == 0:
            self.game.tour += 1