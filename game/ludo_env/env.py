import gymnasium as gym
import numpy as np

from .game_logic import (
    GameLogic,
    TOTAL_SIZE,
    BOARD_SIZE,
    SAFE_ZONE_SIZE,
)
from .action import Action_NO_EXACT, Action_EXACT, Action_EXACT_ASCENSION
from .renderer import Renderer
from .reward import AgentType


class LudoEnv(gym.Env):
    def __init__(
        self,
        num_players,
        nb_chevaux,
        agent_type=AgentType.BALANCED,
        mode_fin_partie="tous",
        mode_ascension="sans_contrainte",
        mode_pied_escalier="not_exact",
        mode_rejoue_6="non",
        mode_rejoue_marche="non",
        mode_protect="désactivé",
        mode_gym="entrainement",
        with_render=False,
    ):
        assert num_players in [2, 3, 4], "Only 2, 3 or 4 players are allowed"
        assert nb_chevaux in [2, 3, 4, 5, 6], "Only 2, 3, 4, 5 or 6 pawns are allowed"
        assert mode_fin_partie in [
            "tous",
            "un",
        ], "Only 'tous' or 'un' are allowed"
        assert mode_gym in [
            "entrainement",
            "jeu",
            "stats_game",
        ], "Only 'entrainement' or 'jeu' or 'stats_game' are allowed"
        assert mode_pied_escalier in [
            "exact",
            "not_exact",
        ], "Only 'exact' or 'not_exact' are allowed"
        assert mode_ascension in [
            "avec_contrainte",
            "sans_contrainte",
        ], "Only 'avec_contrainte' or 'sans_contrainte' are allowed"
        assert mode_rejoue_6 in [
            "oui",
            "non",
        ], "Only 'oui' or 'non' are allowed"
        assert mode_rejoue_marche in [
            "oui",
            "non",
        ], "Only 'oui' or 'non' are allowed"
        assert mode_protect in [
            "activé",
            "désactivé",
        ], "Only 'activé' or 'désactivé' are allowed"

        # si escalier not exact alors ascension sans contrainte
        # si escalier exact alors 2 modes d'ascension tolérées
        # si exact + avec contrainte alors on peut rejouer marche ou pas 
        assert ((
                mode_pied_escalier == "not_exact" and mode_ascension == "sans_contrainte"
            ) or (mode_ascension == "avec_contrainte" and mode_pied_escalier == "exact")
            or (mode_ascension == "sans_contrainte" and mode_pied_escalier == "exact")
        ), "Only 'avec_contrainte' and 'exact' or 'sans_contrainte' and 'not_exact' or 'sans_contrainte' and 'exact' are allowed"
        if mode_rejoue_marche == "oui":
            assert mode_ascension == "avec_contrainte" and mode_pied_escalier == "exact", "Only 'avec_contrainte' and 'exact' are allowed"

        super(LudoEnv, self).__init__()
        self.metadata = {"render.modes": ["human", "rgb_array"], "render_fps": 10}
        self.with_render = with_render
        self.mode_gym = mode_gym

        self.agent_type = agent_type

        self.num_players = num_players
        self.nb_chevaux = nb_chevaux
        self.mode_fin_partie = mode_fin_partie
        self.mode_pied_escalier = mode_pied_escalier
        self.mode_ascension = mode_ascension
        self.mode_rejoue_6 = mode_rejoue_6
        self.mode_rejoue_marche = mode_rejoue_marche
        self.mode_protect = mode_protect

        if self.mode_ascension == "avec_contrainte":
            self.espace_action = "exact_ascension"
        elif self.mode_pied_escalier == "not_exact":
            self.espace_action = "not_exact"
        elif self.mode_pied_escalier == "exact":
            self.espace_action = "exact"
        else:
            raise ValueError("Erreur de paramètrage")
        
        if self.with_render:
            self.renderer = Renderer(espace_action=self.espace_action)

        if mode_ascension == "sans_contrainte":
            if mode_pied_escalier == "not_exact":
                self.action_space = gym.spaces.Discrete(
                    3 + self.nb_chevaux * (len(Action_NO_EXACT) - 3)
                )
            elif mode_pied_escalier == "exact":
                self.action_space = gym.spaces.Discrete(
                    3 + self.nb_chevaux * (len(Action_EXACT) - 3)
                )
        elif mode_ascension == "avec_contrainte":
            self.action_space = gym.spaces.Discrete(
                3 + self.nb_chevaux * (len(Action_EXACT_ASCENSION) - 3)
            )

        self.observation_space = gym.spaces.Dict(
            {
                "my_ecurie": gym.spaces.Discrete(self.nb_chevaux + 1),
                # État de l'écurie du joueur courant
                "my_chemin": gym.spaces.Box(
                    low=-self.nb_chevaux,
                    high=self.nb_chevaux,
                    shape=(BOARD_SIZE,),
                    dtype=np.int8,
                ),  # État du chemin du joueur courant : -1 = adversaire, 0 = vide, 1 = joueur courant
                "my_escalier": gym.spaces.Box(
                    low=0, high=self.nb_chevaux, shape=(SAFE_ZONE_SIZE,), dtype=np.int8
                ),  # État de l'escalier du joueur courant
                "my_goal": gym.spaces.Discrete(self.nb_chevaux + 1),
                # État du goal du joueur courant
                "dice_roll": gym.spaces.Discrete(7),  # Résultat du dé (1 à 6)
            }
        )

        self.reset()

    def _get_observation(self):
        obs = {
            "my_ecurie": self.game.get_observation_my_ecurie(self.current_player),
            "my_chemin": self.game.get_observation_my_chemin(self.current_player),
            "my_escalier": self.game.get_observation_my_escalier(self.current_player),
            "my_goal": self.game.get_observation_my_goal(self.current_player),
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
            mode_ascension=self.mode_ascension,
            mode_pied_escalier=self.mode_pied_escalier,
            agent_type=self.agent_type,
        )
        self.actions_par_type = {
            player: {action_type: 0 for action_type in self.game.get_action()}
            for player in range(self.num_players)
        }
        self.nb_actions_interdites = {player: 0 for player in range(self.num_players)}
        self.dice_roll = self.game.dice_generator()
        return self._get_observation(), {}

    def render(
        self, game, mode="human", players_type=["human", "human"],game_over=False, 
    ):
        if self.with_render:
            actions = []
            for action in self.game.encode_valid_actions(
                self.game.get_valid_actions(self.current_player, self.dice_roll)):
                pawn_id, action_type = self.game.decode_action(action)
                actions.append(
                    {
                        "pawn_id": pawn_id,
                        "action_type": action_type,
                        "encoded_action": action,
                    })
                
            self.renderer.render(
                game = self.game,
                current_player = self.current_player,
                dice_value = self.dice_roll,
                valid_actions = actions,
                infos = self.game.get_pawns_info(self.current_player),
                players_type = players_type,
                game_over=self.game.is_game_over()
            )


    def step(self, action):
        obs = self._get_observation()

        # affichage dans le terminal 
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
        
        # définition de l'action que l'agent essaye de jouer
        info["action_agent"] = action_type
        info["reward_action_agent"] = self.game.get_reward(action_type, self.agent_type)
        
        # définition de l'action que l'agent va réellement jouer
        info["action_rectified"] = action_type
        info["reward_rectified"] = self.game.get_reward(action_type, self.agent_type)
        # marqueur pour savoir si l'action a été modifiée ou non
        info["rectified"] = False
        
        is_auto_action = False

        valid_actions = self.game.get_valid_actions(self.current_player, self.dice_roll)
        encoded_valid_actions = self.game.encode_valid_actions(valid_actions)

        if action not in encoded_valid_actions:
            self.nb_actions_interdites[self.current_player] += 1
            is_auto_action = True

            if self.mode_gym == "stats_game":
                action = self.game.debug_action(encoded_valid_actions)
                pawn_id, action_type = self.game.decode_action(action)  
                # On reward l'action interdite de -10
                info["reward_action_agent"] = -10
                # On récupère le reward associé à l'action rectifiée
                info["action_rectified"] = action_type   
                info["reward_rectified"] = self.game.get_reward(action_type, self.agent_type)       
                info["rectified"] = True  

            elif self.mode_gym == "jeu":
                print("L'agent a joué une action interdite")
                print(f"encoded action : {action}, pawn_id : {pawn_id}, action_type : {action_type}")
                print()
                action = self.game.debug_action(encoded_valid_actions)
                pawn_id, action_type = self.game.decode_action(action)
                
            else:
                # mode entrainement, si action pas valide -> changer de joueur et reward -10
                self.change_player(action_type)
                return self._get_observation(), -10, False, False, info
            
        pawn_pos = self.game.get_pawns_info(self.current_player)[pawn_id]["position"]

        self.game.move_pawn(self.current_player, pawn_pos, self.dice_roll, action_type)

        # On ajoute seulement les actions non automatiques aux statistiques
        # Et on calcule la récompense correspondante à l'action initiale
        if not is_auto_action or self.mode_gym == "jeu":
            if action_type in self.actions_par_type[self.current_player]:
                self.actions_par_type[self.current_player][action_type] += 1
            reward = self.game.get_reward(action_type, self.agent_type)
        elif is_auto_action and self.mode_gym == "stats_game" :
            reward = -10
        # TODO CHARLOTTE T'AS OUBLIE DES CAS, à voir tout est ok pour mode entrainement, mode stat et mode jeu 

        done = self.game.is_game_over()

        if not done:
            self.change_player(action_type)

        self.dice_roll = self.game.dice_generator()
        observation = self._get_observation()
        return observation, reward, done, False, info

    def change_player(self, action_type):
        if self.mode_rejoue_6 == "oui" and self.dice_roll == 6:
            pass
        elif self.mode_rejoue_marche == "oui" and (
            action_type == Action_EXACT_ASCENSION.MARCHE_1
            or action_type == Action_EXACT_ASCENSION.MARCHE_2
            or action_type == Action_EXACT_ASCENSION.MARCHE_3
            or action_type == Action_EXACT_ASCENSION.MARCHE_4
            or action_type == Action_EXACT_ASCENSION.MARCHE_5
            or action_type == Action_EXACT_ASCENSION.MARCHE_6
        ):
            pass
        else:
            self.current_player = (self.current_player + 1) % self.num_players
            if self.current_player == 0:
                self.game.tour += 1

    # Retourne le nombre de chaque type d'actions par participants
    def export_action_stats(self):
        action_stats_by_player = {}
        for player, actions in self.actions_par_type.items():
            action_stats_by_player[player] = {
                action.name: count for action, count in actions.items()
            }
        return action_stats_by_player
    
    def get_pawns_in_goal(self):
        return [self.game.get_pawns_in_goal(player_id) for player_id in range(self.num_players)]
