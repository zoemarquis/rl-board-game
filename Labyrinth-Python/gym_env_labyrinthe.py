# Importation des librairies
from labyrinthe import NUM_TREASURES, NUM_TREASURES_PER_PLAYER, Labyrinthe
from gui_manager import GUI_manager

import gymnasium as gym
from gymnasium import spaces

import numpy as np


action_carte = {0: {"up", 1}, 2: {"up", 2}, 1: {"up", 3}, 3: {"up", 3}}

action_mouvement = {0: "droite", 1: "gauche", 2: "haut", 3: "bas"}


# Environnement Gym pour le jeu Labyrinthe
class LabyrinthEnv(gym.Env):
    metadata = {"render.modes": ["human"]}  # TODO : Peut-être mettre 'rgb_array'

    # Fonction permettant d'initialiser l'environnement
    def __init__(self, max_steps=-1):
        super(LabyrinthEnv, self).__init__()

        self.max_steps = max_steps
        self.current_step = 0

        # Nb actions possibles par le joueur : 12 emplacements d'insertion * 4 rotations * mouvements (49 pièces)
        # TODO : Voir si que 11 emplacements d'insertion (pas mouvement inverse)
        self.action_space = spaces.Discrete(12 * 4 * 49)

        # Espaces d'observation
        # Informations sur l'état du jeu
        # 4 couches pour les murs (N,S,E,O) - TODO : Peut-être à changer
        # 1 couche pour les joueurs
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(7 * 7 * 5,), dtype=np.float32
        )

        self.joueur_actuel = 1
        self.termine = False
        self.derniere_insertion = None

        self.reset()

    # Fonction permettant de réinitialiser l'environnement
    # Retourne l'état du jeu
    def reset(self, seed=None, options=None):

        self.current_step = 0

        # Fixer une seed aléatoire
        self.np_random, seed = gym.utils.seeding.np_random(seed)

        # Paramètres du jeu
        self.game = Labyrinthe(
            num_human_players=2, num_ia_players=0
        )

        self.termine = False
        self.derniere_insertion = None
        return self._get_observation(), {}

    # Fonction permettant à l'agent de réaliser une action
    def step(self, action):

        self.current_step += 1

        action_deplacement = action % 49
        idx_insertion = (action // 49) // 4
        idx_rotation = action_deplacement % 4

        # print ("idx_insertion : ", idx_insertion)
        # print ("idx_rotation : ", idx_rotation)

        # TODO : Voir comment gérer le cas où l'insertion est interdite
        if self._est_interdit(idx_insertion):
            recompense = -10  # Récompense : -10 si mouvement interdit
            termine = False
            tronque = False
            return self._get_observation(), recompense, termine, tronque, {}

        direction, rangee = self._get_insertion(idx_insertion)
        # print("Direction : ", direction)
        # print("Rangee : ", rangee)

        # Rotation
        self.game.rotate_tile("H" if idx_rotation == 0 else "A")

        # Insertion de la carte
        self.game.play_tile(direction, rangee)
        self.derniere_insertion = idx_insertion

        # Calcul des pièces accessibles
        mouvements_ok = self._get_mouvements_ok()
        # print("Mouvements possibles : ", mouvements_ok)
        # print("Action deplacement : ", action_deplacement)

        # Déplacement du joueur
        """ Choisi un mouvement aléatoire
        
        if action_deplacement < len(mouvements_ok):
            self._deplacer_joueur(mouvements_ok[action_deplacement %len(mouvements_ok)])

            # Vérification si le joueur a trouvé le trésor
            if self._is_tresor_trouve():
                self.game.current_player_find_treasure()
                recompense = 10  # Récompense : 10 si trésor trouvé
            else:
                recompense = -1  # Récompense : -1 si pas de trésor trouvé
        else:
            print("Mouvement invalide")
            recompense = -10  # Récompense : -10 si le mouvement est invalide"""

        # Choisi forcément un mouvement valide
        self._deplacer_joueur(mouvements_ok[action_deplacement % len(mouvements_ok)])
        if self._is_tresor_trouve():
            self.game.get_current_player_num_find_treasure()
            recompense = 10  # Récompense : 10 si trésor trouvé
        else:
            recompense = -1  # Récompense : -1 si pas de trésor trouvé

        gagnant = self.game.players.check_for_winner()
        if gagnant is not None:
            print(f"Le joueur {gagnant} a gagné la partie !")
            termine = True  # Terminer la partie
        else:
            termine = False

        if self.max_steps!=-1 and (self.current_step >= self.max_steps):
            termine = True

        #termine = self._is_termine()
        tronque = False # A définir si on veut arreter la partie avant la fin

        return self._get_observation(), recompense, termine, tronque, {}

    # Fonction permettant d'afficher le jeu
    def render(self):
        if not hasattr(self, "graphique"):
            # Crée l'interface graphique si elle n'existe pas encore
            self.graphique = GUI_manager(self.game)
        self.graphique.display_game()

    # Fonction permettant de fermer l'environnement
    # TODO : Voir ce qu'il y a à faire
    def close(self):
        if hasattr(self, "graphique"):
            self.graphique.close()
        super().close() 

    # Fonction permettant de retourner l'état actuel du jeu
    def _get_observation(self):
        infos_labyrinthe = np.zeros((7, 7, 5), dtype=np.float32)
        plateau = self.game.get_board()

        # Récupération des infos sur le plateau
        for i in range(7):
            for j in range(7):
                carte = plateau.get_value(i, j)
                # Infos murs
                infos_labyrinthe[i, j, 0] = carte.wall_north()
                infos_labyrinthe[i, j, 1] = carte.wall_south()
                infos_labyrinthe[i, j, 2] = carte.wall_east()
                infos_labyrinthe[i, j, 3] = carte.wall_west()
                # Infos joueur : 1 = joueur présent
                if carte.get_nb_pawns() > 0:
                    infos_labyrinthe[i, j, 4] = 1

        return infos_labyrinthe.flatten().astype(np.float32) 

    # Fonction permettant de vérifier si le joueur a atteint le trésor
    def _is_tresor_trouve(self):
        joueur_pos = self.game.get_coord_current_player()
        tresor_pos = self.game.get_coord_current_treasure()

        return joueur_pos == tresor_pos

    # Fonction permettant de déplacer le joueur
    def _deplacer_joueur(self, new_position):
        ligD, colD = self.game.get_coord_current_player()
        ligA, colA = new_position
        self.game.prendreJoueurCourant(ligD, colD)
        self.game.poserJoueurCourant(ligA, colA)

        joueur_courant = self.game.players.players[self.game.get_current_player()]
        joueur_courant.move_to((ligA, colA))

    # Fonction permettant de vérifier si le jeu est terminé
    # TODO : Ajouter le retour à la case de départ ?
    def _is_termine(self):
        # TODO changer : fin de partie = un joueur a gagné
        # return nb_treasures == 0  # Fin jeu : Plus de trésors
        return False

    # Fonction permettant de récupérer les mouvements valides pour le joueur
    def _get_mouvements_ok(self):
        ligD, colD = self.game.get_coord_current_player()
        mouvements_ok = []

        for ligA in range(7):
            for colA in range(7):
                if self.game.accessible(ligD, colD, ligA, colA):
                    # Ajout à la liste si accessible
                    mouvements_ok.append((ligA, colA))

        return mouvements_ok

    # Fonction permettant de vérifier si l'insertion de la carte est interdite (mouvement inverse)
    def _est_interdit(self, idx_insertion):
        # print("Derniere insertion : ", self.derniere_insertion)
        if self.derniere_insertion is None:
            return False

        if self.derniere_insertion < 3:
            idx_inverse = self.derniere_insertion + 3
        elif self.derniere_insertion < 6:
            idx_inverse = self.derniere_insertion - 3
        elif self.derniere_insertion < 9:
            idx_inverse = self.derniere_insertion + 3
        else:
            idx_inverse = self.derniere_insertion - 3

        return idx_insertion == idx_inverse

    # Fonction permettant de récupérer l'insertion au format direction et rangée
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
