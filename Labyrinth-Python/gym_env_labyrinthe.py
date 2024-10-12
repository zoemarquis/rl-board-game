# Importation des librairies
from labyrintheOO import Labyrinthe
from labyrintheModeGraphiqueOO import LabyrintheGraphique

import gym
from gym import spaces

import numpy as np


action_carte = {
    0: {'up', 1},
    2: {'up', 2},
    1: {'up', 3},
    3: {'up', 3}    

}

action_mouvement = {
    0: 'droite',
    1: 'gauche',
    2: 'haut',
    3: 'bas'}


# Environnement Gym pour le jeu Labyrinthe
class LabyrinthEnv(gym.Env):
    metadata = {'render.modes': ['human']}# TODO : Peut-être mettre 'rgb_array'

    # Fonction permettant d'initialiser l'environnement
    def __init__(self):
        super(LabyrinthEnv, self).__init__()

        # Nb actions possibles par le joueur : 12 emplacements d'insertion * 4 rotations * mouvements (49 pièces) 
        # TODO : Voir si que 11 emplacements d'insertion (pas mouvement inverse)
        self.action_space = spaces.Discrete(12*4*49)

        # Espaces d'observation
        # Informations sur l'état du jeu
        # 4 couches pour les murs (N,S,E,O) - TODO : Peut-être à changer
        # 1 couche pour les joueurs
        self.observation_space = spaces.Box(low=0, high=1, shape=(7*7*5,), dtype=np.float32)


        self.joueur_actuel = 1
        self.termine = False
        self.derniere_insertion = None

        self.reset()

    # Fonction permettant de réinitialiser l'environnement
    # Retourne l'état du jeu
    def reset(self):
        # Paramètres du jeu
        self.game = Labyrinthe(nbHumains=1, 
                               nbTresors=2, 
                               nbTresorMax=0, 
                               nbIA=0)

        self.termine = False
        self.derniere_insertion = None
        return self._get_observation()

    # Fonction permettant à l'agent de réaliser une action
    def step(self, action):
        
        action_deplacement = action % 49      
        idx_insertion = (action // 49) // 4
        idx_rotation = action_deplacement % 4

        # print ("idx_insertion : ", idx_insertion)
        # print ("idx_rotation : ", idx_rotation)

        # TODO : Voir comment gérer le cas où l'insertion est interdite
        if self._est_interdit(idx_insertion):
            recompense = -10  # Récompense : -10 si mouvement interdit
            termine = False
            return self._get_observation(), recompense, termine, {}

        direction, rangee = self._get_insertion(idx_insertion)
        # print("Direction : ", direction)
        # print("Rangee : ", rangee)

        # Rotation
        self.game.tournerCarte('H' if idx_rotation == 0 else 'A')

        # Insertion de la carte
        self.game.jouerCarte(direction, rangee)
        self.derniere_insertion = idx_insertion

        # Calcul des pièces accessibles
        mouvements_ok = self._get_mouvements_ok()
        # print("Mouvements possibles : ", mouvements_ok)
        # print("Action deplacement : ", action_deplacement)

        # Déplacement du joueur
        ''' Choisi un mouvement aléatoire
        
        if action_deplacement < len(mouvements_ok):
            self._deplacer_joueur(mouvements_ok[action_deplacement %len(mouvements_ok)])

            # Vérification si le joueur a trouvé le trésor
            if self._is_tresor_trouve():
                self.game.joueurCourantTrouveTresor()
                recompense = 10  # Récompense : 10 si trésor trouvé
            else:
                recompense = -1  # Récompense : -1 si pas de trésor trouvé
        else:
            print("Mouvement invalide")
            recompense = -10  # Récompense : -10 si le mouvement est invalide'''
        
        # Choisi forcément un mouvement valide
        self._deplacer_joueur(mouvements_ok[action_deplacement %len(mouvements_ok)])
        if self._is_tresor_trouve():
            self.game.joueurCourantTrouveTresor()
            recompense = 10  # Récompense : 10 si trésor trouvé
        else:
            recompense = -1  # Récompense : -1 si pas de trésor trouvé

        termine = self._is_termine()

        return self._get_observation(), recompense, termine, {}
    
    # Fonction permettant d'afficher le jeu
    def render(self):
        if not hasattr(self, 'graphique'):
            # Crée l'interface graphique si elle n'existe pas encore
            self.graphique = LabyrintheGraphique(self.game)
        self.graphique.afficheJeu()

    # Fonction permettant de fermer l'environnement
    # TODO : Voir ce qu'il y a à faire
    def close(self):
        pass

    # Fonction permettant de retourner l'état actuel du jeu
    def _get_observation(self):
        infos_labyrinthe = np.zeros((7, 7, 5))
        plateau = self.game.getPlateau()

        # Récupération des infos sur le plateau
        for i in range(7):
            for j in range(7):
                carte = plateau.get_value(i, j)
                # Infos murs
                infos_labyrinthe[i, j, 0] = carte.murNord()
                infos_labyrinthe[i, j, 1] = carte.murSud()
                infos_labyrinthe[i, j, 2] = carte.murEst()
                infos_labyrinthe[i, j, 3] = carte.murOuest()
                # Infos joueur : 1 = joueur présent
                if carte.getNbPions() > 0:
                    infos_labyrinthe[i, j, 4] = 1 

        return infos_labyrinthe.flatten()


    # Fonction permettant de vérifier si le joueur a atteint le trésor
    def _is_tresor_trouve(self):
        joueur_pos = self.game.getCoordonneesJoueurCourant()
        tresor_pos = self.game.getCoordonneesTresorCourant()

        return joueur_pos == tresor_pos

    # Fonction permettant de déplacer le joueur
    def _deplacer_joueur(self, new_position):
        ligD, colD = self.game.getCoordonneesJoueurCourant()
        ligA, colA = new_position
        self.game.prendreJoueurCourant(ligD, colD)
        self.game.poserJoueurCourant(ligA, colA)

    # Fonction permettant de vérifier si le jeu est terminé
    # TODO : Ajouter le retour à la case de départ ??
    def _is_termine(self):
        return self.game.getNbTresors() == 0 # Fin jeu : Plus de trésors

    # Fonction permettant de récupérer les mouvements valides pour le joueur
    def _get_mouvements_ok(self):
        ligD, colD = self.game.getCoordonneesJoueurCourant()
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
            return ('N', rangees_ok[idx_insertion])
        elif idx_insertion < 6:
            return ('S', rangees_ok[idx_insertion % 3])
        elif idx_insertion < 9:
            return ('E', rangees_ok[idx_insertion % 3])
        else:
            return ('O', rangees_ok[idx_insertion % 3]) 

