from labyrinthe import Labyrinthe
from gui_manager import GUI_manager
import gymnasium as gym
import numpy as np
import random


# Environnement Gym pour le jeu Labyrinthe
class LabyrinthEnv(gym.Env):
    def __init__(
        self,
        num_human_players=0,
        num_ai_players=2,
        max_steps=-1,
        render_mode="human",
        epsilon=1.0,
        epsilon_decay=0.995,
        min_epsilon=0.1,
    ):
        super(LabyrinthEnv, self).__init__()

        self.epsilon = epsilon  # taux d'exploration initial
        self.epsilon_decay = epsilon_decay  # taux de décroissance de l'exploration
        self.min_epsilon = min_epsilon
        self.historique_insertions = []

        self.max_steps = max_steps
        self.current_step = 0

        # Phase du jeu : 0 pour insertion, 1 pour déplacement
        self.phase = 0

        # Espace des actions pour chaque phase
        # Phase d'insertion : [rotation (4), position d'insertion (12)]
        self.action_space_insertion = gym.spaces.MultiDiscrete([4, 12])

        # Initialiser l'action_space avec l'espace d'actions de la phase d'insertion
        self.action_space = self.action_space_insertion

        # Espace d'observation
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(7 * 7 * 5,), dtype=np.float32
        )

        self.joueur_actuel = 1
        self.termine = False
        self.derniere_insertion = None

        self.render_mode = render_mode

        self.num_human_players = num_human_players
        self.num_ai_players = num_ai_players

        self.reset(self.num_human_players, self.num_ai_players)

    def reset(self, num_human_players=0, num_ai_players=2, seed=None, options=None):
        self.current_step = 0
        self.phase = 0  # Commence par la phase d'insertion

        # Réinitialiser l'action_space pour la phase d'insertion
        self.action_space = self.action_space_insertion

        # Fixer une seed aléatoire
        self.np_random, seed = gym.utils.seeding.np_random(seed)

        # Initialisation du jeu
        self.game = Labyrinthe(
            num_human_players=num_human_players, num_ai_players=num_ai_players
        )

        self.termine = False
        self.derniere_insertion = None

        return self._get_observation(), {}

    def step(self, action):
        # selection d'une action aléatoire pour explorer
        if random.uniform(0, 1) < self.epsilon:
            action = self.action_space.sample()
        else:
            # sinon action donné
            action = action

        # reduction de epsilon après chaque action pour encourager l'exploitation au fil du temps
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)

        self.current_step += 1

        # Phase d'insertion
        if self.phase == 0:
            # print("phase 0")

            rotation_idx, insertion_idx = action

            # Rotation et insertion
            self._appliquer_rotation(rotation_idx)

            # eviter de toujours insérer au meme endroit
            if insertion_idx not in self.historique_insertions:
                recompense = 5  # insertion unique
            else:
                recompense = 0

            if self._est_insertion_interdite(insertion_idx):
                recompense = -10  # pénalité pour insertion interdite
            elif (
                insertion_idx in self.historique_insertions[-5:]
            ):  # Pénalité si l'insertion est répétitive
                recompense = -5  # pénalité légère pour répétition
            else:
                recompense = 0

            self.historique_insertions.append(
                insertion_idx
            )  # enregistrement de l'insertion

            if len(self.historique_insertions) > 20:  # garder 20 mouvements
                self.historique_insertions.pop(0)

            # Vérifier si l'insertion est valide
            """if self._est_insertion_interdite(insertion_idx):
                recompense = -10  # Pénalité pour insertion interdite
                termine = False
                tronque = False
                return self._get_observation(), recompense, termine, tronque, {}"""

            # Appliquer l'insertion
            direction, rangee = self._get_insertion(insertion_idx)
            self.game.play_tile(direction, rangee)
            self.derniere_insertion = insertion_idx

            # Passer à la phase de déplacement
            self.phase = 1

            # Définir l'espace des actions pour le déplacement
            mouvements_possibles = self._get_mouvements_possibles()
            self.mouvements_possibles = (
                mouvements_possibles  # Sauvegarder pour utilisation ultérieure
            )
            self.action_space = gym.spaces.Discrete(len(mouvements_possibles))

            # Pas de récompense à cette étape
            recompense = 0
            termine = False
            tronque = False
            return self._get_observation(), recompense, termine, tronque, {}

        # Phase de déplacement
        elif self.phase == 1:

            # print("phase 1")

            mouvement_idx = action[0] if isinstance(action, np.ndarray) else action

            # Vérifier si le mouvement est valide
            if (mouvement_idx < 0).any() or (
                mouvement_idx >= len(self.mouvements_possibles)
            ).any():
                recompense = -10  # Pénalité pour mouvement invalide
                termine = False
                tronque = False
                return self._get_observation(), recompense, termine, tronque, {}

            # Déplacer le joueur
            nouvelle_position = self.mouvements_possibles[mouvement_idx]
            self._deplacer_joueur(nouvelle_position)

            # Vérifier si le trésor est trouvé
            if self._is_tresor_trouve():
                self.game.get_current_player_num_find_treasure()
                recompense = 10  # Récompense pour avoir trouvé le trésor
            else:
                recompense = -1  # Pénalité légère pour chaque mouvement

            # Vérifier si la partie est terminée
            gagnant = self.game.players.check_for_winner()
            if gagnant is not None:
                print(f"Le joueur {gagnant} a gagné la partie !")
                termine = True
            else:
                termine = False

            if self.max_steps != -1 and (self.current_step >= self.max_steps):
                termine = True

            # Réinitialiser pour le prochain tour
            self.phase = 0
            self.action_space = self.action_space_insertion

            # Passer au joueur suivant
            self.game.next_player()

            tronque = False
            return self._get_observation(), recompense, termine, tronque, {}

    def render(self):
        if self.render_mode == "human":
            if not hasattr(self, "graphique"):
                self.graphique = GUI_manager(
                    self.game, model="./modeles/best_model.zip", env=self
                )
            self.graphique.display_game()

    def close(self):
        if hasattr(self, "graphique"):
            self.graphique.close()
        # pygame.quit()  # ferme pygame
        super().close()

    def _get_observation(self):
        infos_labyrinthe = np.zeros((7, 7, 5), dtype=np.float32)
        plateau = self.game.get_board()

        # Récupération des infos sur le plateau
        for i in range(7):
            for j in range(7):
                carte = plateau.get_value(i, j)
                # Infos murs
                infos_labyrinthe[i, j, 0] = 1 if carte.wall_north() else 0
                infos_labyrinthe[i, j, 1] = 1 if carte.wall_south() else 0
                infos_labyrinthe[i, j, 2] = 1 if carte.wall_east() else 0
                infos_labyrinthe[i, j, 3] = 1 if carte.wall_west() else 0
                # Infos joueur : 1 si le joueur courant est présent
                if carte.has_pawn(self.game.get_current_player()):
                    infos_labyrinthe[i, j, 4] = 1

        return infos_labyrinthe.flatten().astype(np.float32)

    def _is_tresor_trouve(self):
        joueur_pos = self.game.get_coord_player()
        tresor_pos = self.game.get_coord_current_treasure()
        return joueur_pos == tresor_pos

    def _deplacer_joueur(self, new_position):
        ligD, colD = self.game.get_coord_player()
        ligA, colA = new_position
        self.game.remove_current_player_from_tile(ligD, colD)
        self.game.put_current_player_in_tile(ligA, colA)

        joueur_courant = self.game.players.players[self.game.get_current_player()]
        joueur_courant.move_to((ligA, colA))

    def _get_mouvements_possibles(self, joueur_id=None):
        if joueur_id is None:
            joueur_id = self.game.get_current_player()

        ligD, colD = self.game.get_coord_player(joueur_id)
        mouvements_possibles = []

        # Utiliser une recherche en largeur pour trouver toutes les positions accessibles
        visited = [[False for _ in range(7)] for _ in range(7)]
        queue = [(ligD, colD)]
        visited[ligD][colD] = True

        while queue:
            x, y = queue.pop(0)
            mouvements_possibles.append((x, y))

            voisins = self._get_voisins_accessibles(x, y)
            for vx, vy in voisins:
                if not visited[vx][vy]:
                    visited[vx][vy] = True
                    queue.append((vx, vy))

        return mouvements_possibles

    def _get_voisins_accessibles(self, x, y):
        voisins = []
        tile = self.game.board.get_value(x, y)

        # Nord
        if x > 0 and tile.can_go_north(self.game.board.get_value(x - 1, y)):
            voisins.append((x - 1, y))
        # Sud
        if x < 6 and tile.can_go_south(self.game.board.get_value(x + 1, y)):
            voisins.append((x + 1, y))
        # Est
        if y < 6 and tile.can_go_east(self.game.board.get_value(x, y + 1)):
            voisins.append((x, y + 1))
        # Ouest
        if y > 0 and tile.can_go_west(self.game.board.get_value(x, y - 1)):
            voisins.append((x, y - 1))

        return voisins

    def _est_insertion_interdite(self, idx_insertion):
        if self.derniere_insertion is None:
            return False

        # Les positions interdites sont celles qui inversent le dernier mouvement d'insertion
        if idx_insertion == (self.derniere_insertion + 6) % 12:
            return True
        return False

    def _get_insertion(self, idx_insertion):
        rangees_ok = [1, 3, 5]

        if idx_insertion < 3:
            return ("N", rangees_ok[idx_insertion])
        elif idx_insertion < 6:
            return ("S", rangees_ok[idx_insertion % 3])
        elif idx_insertion < 9:
            return ("E", rangees_ok[idx_insertion % 3])
        else:
            return ("O", rangees_ok[idx_insertion % 3])

    def _appliquer_rotation(self, rotation_idx):
        # 0: 0°, 1: 90°, 2: 180°, 3: 270°
        for _ in range(rotation_idx):
            self.game.rotate_tile("H")
