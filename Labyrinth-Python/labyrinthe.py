from tile import *
from matrix import DIMENSION, Matrix
from joueurOO import *
import random
import copy

# TODO : change robjects name -> 1 to ... (7 x 7 - 3 (colonnes impair) *  7 - 3 * 4 (lignes impair sans case commune avec colonne) - 4 coins) )
# puis dans le code là où c'est complété -> complété jusqu'au bon nombre (pas 24 si le plateau ne fait pas 24)

TRESORS_FIXES = set([5, 13, 1, 7, 14, 22, 2, 8, 15, 23, 9, 16])

NUM_TREASURES = 24
NUM_TREASURES_PER_PLAYER = 6


class Labyrinthe(object):
    """Class representing the labyrinth game
    we have a board, players (humans, IA),
    we manage the current player, the current phase of the game, the forbidden move, the tile to play
    """

    def __init__(
        self,
        num_human_players: int,
        num_ia_players: int,
    ):
        # TODO : if board dimension is not 7x7, we need to change the fixed cards
        board: Matrix = self.init_board_with_default_7x7_values()

        self.players: Joueurs = Joueurs(
            num_human_players + num_ia_players, NUM_TREASURES, NUM_TREASURES_PER_PLAYER
        )
        # TODO Ajout des IAs
        self.joueursIA = range(
            num_human_players + 1, num_human_players + num_ia_players + 1
        )
        if num_ia_players > 1:
            self.joueursIADef = range(
                num_human_players + num_ia_players,
                num_human_players + num_ia_players + 1,
            )
        else:
            self.joueursIADef = []

        self.current_player = 1
        self.coordonneesJoueurCourant = (0, 0)

        self.phase = 1  # inutile ??

        self.forbidden_move: tuple = ("N", 0)

        # Placement des joueurs
        self.nbJoueurs = num_human_players + num_ia_players
        if self.nbJoueurs >= 1:
            board.get_value(0, 0).put_pawn(1)  # A
        if self.nbJoueurs >= 2:
            board.get_value(0, 6).put_pawn(2)  # B
        if self.nbJoueurs >= 3:
            board.get_value(6, 0).put_pawn(3)  # C
        if self.nbJoueurs == 4:
            board.get_value(6, 6).put_pawn(4)  # D

        # Trésors et cartes amovible
        listeCarte = creerCartesAmovibles(NUM_TREASURES)
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if (
                    i % 2 == 1 or j % 2 == 1
                ):  # Cela correspond aux emplacements non fixe
                    board.set_value(
                        i, j, listeCarte.pop(randint(0, len(listeCarte) - 1))
                    )
        self.tile_to_play: Tile = listeCarte[0]
        self.board = board

    def init_board_with_default_7x7_values(self):
        board: Matrix = Matrix()
        # fill the board with fixed cards
        board.set_value(0, 2, Tile(False, True, True, True, 5))  # grimoire
        board.set_value(0, 4, Tile(False, True, True, True, 13))  # bourse

        board.set_value(2, 0, Tile(True, True, True, False, 1))  # fiole
        board.set_value(2, 2, Tile(True, True, True, False, 7))  # couronne
        board.set_value(2, 4, Tile(False, True, True, True, 14))  # clef
        board.set_value(2, 6, Tile(True, False, True, True, 22))  # calice

        board.set_value(4, 0, Tile(True, True, True, False, 2))  # bague
        board.set_value(4, 2, Tile(True, True, False, True, 8))  # trésor
        board.set_value(4, 4, Tile(True, False, True, True, 15))  # pierre précieuse
        board.set_value(4, 6, Tile(True, False, True, True, 23))  # épée

        board.set_value(6, 2, Tile(True, True, False, True, 9))  # chandelier
        board.set_value(6, 4, Tile(True, True, False, True, 16))  # casque

        # 4 corners
        board.set_value(0, 0, Tile(False, True, True, False, base=1))  # A
        board.set_value(0, 6, Tile(False, False, True, True, base=2))  # B
        board.set_value(6, 0, Tile(True, True, False, False, base=3))  # C
        board.set_value(6, 6, Tile(True, False, False, True, base=4))  # D
        return board

    # getters

    def get_board(self) -> Matrix:
        return self.board

    def get_num_players(self) -> int:
        return self.players.nbJoueurs

    def get_current_player(self) -> int:
        return self.current_player

    def get_phase(self):  # ?
        return self.phase  # ? 1 choisir sens carte, 2 choisir rangee, 3 avancer ???

    def get_tile_to_play(self):
        return self.tile_to_play

    def get_players(self) -> Joueurs:
        return self.players

    def current_treasure(self) -> int:
        return self.players.next_treasure(self.get_current_player())

    def get_forbidden_move(self) -> tuple:
        return self.forbidden_move  # c'est quoi la représentation de la direction ??

    def get_coord_current_treasure(self) -> tuple:
        """return the coordinates of the current treasure to find for the current player"""
        treasure = self.current_treasure()
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.board.get_value(i, j).get_treasure() == treasure:
                    return (i, j)
        return None

    def get_coord_current_player(self) -> tuple:
        """return the coordinates of the current player"""
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.board.get_value(i, j).has_pawn(
                    self.get_current_player()
                ):  # TODO
                    return (i, j)
        return None

    def next_phase(self):
        """change the phase of the game"""
        # TODO modifier pour 0 1 %2 et pas 1 2 ...
        if self.get_phase() == 1:
            self.phase = 2
        else:
            self.phase = 1

    def next_player(self):
        """change the current player"""
        # TODO : modulo nb joueurs... améliorer
        # current = self.get_current_player()
        # current += 1
        # 1 à 4 ou 0 à 3 ???
        if self.get_current_player() == self.get_num_players():
            self.current_player = 1
        else:
            self.current_player += 1
        self.coordonneesJoueurCourant = self.get_coord_current_player()

    def get_current_player_num_find_treasure(self):
        """update the player structure when the current player find the treasure"""
        return self.players.tresorTrouve(self.current_player)  # TODO : améliorer code
    
    def get_current_player_remaining_treasure(self):
        """return the number of remaining treasures for the current player"""
        return self.get_remaining_treasures(self.current_player)

    def get_remaining_treasures(self, num_player):
        """return the number of remaining treasures for the player num_player"""
        return self.players.nbTresorsRestants(num_player)  # TODO : améliorer code

    def is_forbidden_move(self, direction, position):
        return self.forbidden_move == (direction, position)

    # TODO : remove this function
    # Test si le joueur courant est un IA attaquant
    def joueurCourantIsIA(self):
        return self.current_player in self.joueursIA

    # TODO : remove this function
    # Test si le joueur courant est un IA defensif
    def joueurCourantIsIADef(self):
        return self.current_player in self.joueursIADef

    def is_current_player_human(self):
        return self.current_player not in self.joueursIA

    def is_current_player_IA(self):
        return self.current_player in self.joueursIA

    # inutile ..
    ## # enlève le trésor numTresor sur la carte qui se trouve sur la case lin,col du plateau
    ## # si le trésor ne s'y trouve pas la fonction ne fait rien
    ## def prendreTresorL(self, lin, col, numTresor):
    ##     if self.board.get_value(lin, col).get_treasure() == numTresor:
    ##         self.board.get_value(lin, col).pop_treasure()

    # enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    # si le joueur ne s'y trouve pas la fonction ne fait rien
    def prendreJoueurCourant(self, lin, col):
        self.board.get_value(lin, col).remove_pawn(self.get_current_player())

    # pose le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    # si le joueur s'y trouve déjà la fonction ne fait rien
    def poserJoueurCourant(self, lin, col):
        self.board.get_value(lin, col).put_pawn(self.get_current_player())

    # fonction qui joue la carte amovible dans la direction et sur la rangée passées
    # en paramètres. Cette fonction
    #      - met à jour le plateau du labyrinthe
    #      - met à jour la carte à jouer
    #      - met à jour la nouvelle direction interdite
    def play_tile(self, direction, rangee):
        if direction == "N":
            self.tile_to_play = self.board.shift_column_down(rangee, self.tile_to_play)
            self.forbidden_move = ("S", rangee)
        if direction == "E":
            self.tile_to_play = self.board.shift_row_left(rangee, self.tile_to_play)
            self.forbidden_move = ("O", rangee)
        if direction == "S":
            self.tile_to_play = self.board.shift_column_up(rangee, self.tile_to_play)
            self.forbidden_move = ("N", rangee)
        if direction == "O":
            self.tile_to_play = self.board.shift_row_right(rangee, self.tile_to_play)
            self.forbidden_move = ("E", rangee)
        pions = self.tile_to_play.get_pawns()
        for pion in pions:
            self.tile_to_play.remove_pawn(pion)
            if pion == 1:
                self.poserPionL(6, 6, 1)
            if pion == 2:
                self.poserPionL(0, 6, 2)
            if pion == 3:
                self.poserPionL(6, 0, 3)
            if pion == 4:
                self.poserPionL(0, 0, 4)
        self.coordonneesJoueurCourant = self.get_coord_current_player()

    # Cette fonction tourne la carte à jouer dans le sens indiqué
    # en paramètre (H horaire A antihoraire)
    def rotate_tile(self, sens="H"):
        if sens == "H":
            self.tile_to_play.rotate_clockwise()
        else:
            self.tile_to_play.rotate_counter_clockwise()

    # TODO inutile ??
    # # prend le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
    # def prendrePionL(self, lin, col, numJoueur):
    #     self.board.get_value(lin, col).remove_pawn(numJoueur)

    # pose le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
    def poserPionL(self, lin, col, joueur):
        self.board.get_value(lin, col).put_pawn(joueur)

    # indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
    # Fonction marquant les case autour d'une case dont la valeur est val et qui est accessible
    def marquer(self, mat: Matrix, val, marque):
        changer = False
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if mat.get_value(i, j) == val:
                    if i > 0:
                        if self.board.get_value(i, j).can_go_north(
                            self.board.get_value(i - 1, j)
                        ):
                            if mat.get_value(i - 1, j) == 0:
                                mat.set_value(i - 1, j, marque)
                                changer = True
                    if i < DIMENSION - 1:
                        if self.board.get_value(i, j).can_go_south(
                            self.board.get_value(i + 1, j)
                        ):
                            if mat.get_value(i + 1, j) == 0:
                                mat.set_value(i + 1, j, marque)
                                changer = True
                    if j > 0:
                        if self.board.get_value(i, j).can_go_west(
                            self.board.get_value(i, j - 1)
                        ):
                            if mat.get_value(i, j - 1) == 0:
                                mat.set_value(i, j - 1, marque)
                                changer = True
                    if j < DIMENSION - 1:
                        if self.board.get_value(i, j).can_go_east(
                            self.board.get_value(i, j + 1)
                        ):
                            if mat.get_value(i, j + 1) == 0:
                                mat.set_value(i, j + 1, marque)
                                changer = True
        return changer

    def accessible(self, ligD, colD, ligA, colA):
        matTest = Matrix()
        matTest.set_value(ligD, colD, 1)
        changer = True
        while changer and matTest.get_value(ligA, colA) == 0:
            changer = self.marquer(matTest, 1, 1)
        return matTest.get_value(ligA, colA) == 1

    # indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
    # mais la valeur de retour est None s'il n'y a pas de chemin, sinon c'est un chemin possible entre ces deux cases
    def accessibleDist(self, ligD, colD, ligA, colA):
        if not self.accessible(ligD, colD, ligA, colA):
            return []
        else:
            matTest = Matrix()
            matTest.set_value(ligD, colD, 1)
            changer = True
            i = 1
            while changer and matTest.get_value(ligA, colA) == 0:
                changer = self.marquer(matTest, i, i + 1)
                i += 1
            x, y = ligA, colA
            chemin = [(x, y)]
            val = matTest.get_value(x, y)
            while x != ligD or y != colD:
                if x > 0:
                    if 0 < matTest.get_value(
                        x - 1, y
                    ) == val - 1 and self.board.get_value(x, y).can_go_north(
                        self.board.get_value(x - 1, y)
                    ):
                        x -= 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if y > 0:
                    if 0 < matTest.get_value(
                        x, y - 1
                    ) == val - 1 and self.board.get_value(x, y).can_go_west(
                        self.board.get_value(x, y - 1)
                    ):
                        y -= 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if x < DIMENSION - 1:
                    if 0 < matTest.get_value(
                        x + 1, y
                    ) == val - 1 and self.board.get_value(x, y).can_go_south(
                        self.board.get_value(x + 1, y)
                    ):
                        x += 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if y < DIMENSION - 1:
                    if 0 < matTest.get_value(
                        x, y + 1
                    ) == val - 1 and self.board.get_value(x, y).can_go_east(
                        self.board.get_value(x, y + 1)
                    ):
                        y += 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
            chemin.reverse()
            return chemin

    # verifie si le joueur courant peut accéder la case ligA,colA
    # si c'est le cas la fonction retourne une liste représentant un chemin possible
    # sinon ce n'est pas le cas, la fonction retourne None
    def accessibleDistJoueurCourant(self, ligA, colA):
        (ligD, colD) = self.get_coord_current_player()
        return self.accessibleDist(ligD, colD, ligA, colA)

    ###################
    # Gestion de l'IA #
    ###################
    # L'idée est de testé toutes les possibilité avec une copie du labyrinte

    # fonction renvoyant la position accessible a partir de posDepart où la distance entre posDepart et posCible est minimale ( recherche en "étoile" )
    def getPositionMinDistance(self, posCible, posDepart):
        listePos = {posCible}
        dist = 0
        xD, yD = posDepart
        continuer = True
        while (
            continuer
        ):  # La boucle s'arrete quand on trouve une position accessible au plus pres de la pôsition Cible
            listeNewPos = (
                set()
            )  # On utilise un ensemble afin de reduire le nombre de calculs, mais cela oblige a mettre un return dans la boucle for
            ld = []
            for pos in listePos:
                x, y = pos
                if x > 0:
                    xN = x - 1
                    yN = y
                    d = distance((xN, y), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(xN, y, xD, yD):
                            continuer = False
                            return ((xN, y), d)
                        else:
                            listeNewPos.add((xN, y))
                if DIMENSION - 1 > x:
                    xN = x + 1
                    yN = y
                    d = distance((xN, y), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(xN, y, xD, yD):
                            continuer = False
                            return ((xN, y), d)
                        else:
                            listeNewPos.add((xN, y))
                if y > 0:
                    yN = y - 1
                    xN = x
                    d = distance((x, yN), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(x, yN, xD, yD):
                            continuer = False
                            return ((x, yN), d)
                        else:
                            listeNewPos.add((x, yN))
                if DIMENSION - 1 > y:
                    yN = y + 1
                    xN = x
                    d = distance((x, yN), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(x, yN, xD, yD):
                            continuer = False
                            return ((x, yN), d)
                        else:
                            listeNewPos.add((x, yN))
            dist = min(ld)
            listePos = listeNewPos

    # Calcul la "meilleur" action celle ou le joueurCourant peut trouver son tresor si c'est possible,
    # sinon l'action choisie est celle minimisant la distance de ce joueur au tresors apres s'être déplacé,
    # revoie le chemin du joueur a effectuer
    # Change l'orientation de la carte et le coup interdit
    def getMeilleurAction(self):
        actionsPossible = []
        lDirection = ["N", "E", "S", "O"]
        lRangee = [1, 3, 5]
        nbRotation = 0
        continuer = True
        while nbRotation < 4 and continuer:
            j = 0
            while j < len(lDirection) and continuer:
                direction = lDirection[j]
                k = 0
                while k < len(lRangee) and continuer:
                    rangee = lRangee[k]
                    labyTest = copy.deepcopy(self)
                    labyTest.play_tile(direction, rangee)
                    posT = labyTest.get_coord_current_treasure()
                    xJ, yJ = labyTest.get_coord_current_player()
                    if posT != None:  # Cas ou le tresors sort du plateau
                        xT, yT = posT
                        if labyTest.accessible(xJ, yJ, xT, yT):
                            self.play_tile(direction, rangee)
                            continuer = False
                        else:
                            (xC, yC), d = labyTest.getPositionMinDistance(
                                (xT, yT), (xJ, yJ)
                            )
                            if xC != xJ or yC != yJ or actionsPossible == []:
                                actionsPossible.append(
                                    (nbRotation, direction, rangee, xC, yC, d)
                                )
                    k += 1
                j += 1
            self.rotate_tile()
            nbRotation += 1

        if continuer:

            def getDistance(elem):
                return elem[5]

            (nbRotation, direction, rangee, xC, yC, d) = min(
                actionsPossible, key=getDistance
            )
            for i in range(nbRotation):
                self.rotate_tile()
            self.play_tile(direction, rangee)
            xJ, yJ = self.get_coord_current_player()
            return self.accessibleDist(xJ, yJ, xC, yC)
        else:
            return self.accessibleDist(xJ, yJ, xT, yT)

    # Fonction cherchant le meilleur coup pour empecher le joueur suivant de trouver son tresor
    def getMeilleurActionDefensive(self):
        actionsPossible = []
        lDirection = ["N", "E", "S", "O"]
        lRangee = [1, 3, 5]
        i = 0
        continuer = True
        while i < len(lDirection) and continuer:
            direction = lDirection[i]
            j = 0
            while j < len(lRangee) and continuer:
                rangee = lRangee[j]
                nbRotation = 0
                while nbRotation < 4 and continuer:
                    # On crée une copy du labyrinthe pour ne pas altérer la structure initiale
                    labyTest = copy.deepcopy(self)
                    for i in range(nbRotation):
                        labyTest.rotate_tile()
                    labyTest.play_tile(direction, rangee)
                    labyTest.next_player()
                    cptCoupGG = 0
                    for nbRotationT in range(4):
                        labyTest.rotate_tile()
                        for directionT in "NESO":
                            for rangeeT in [1, 3, 5]:
                                if (
                                    directionT,
                                    rangeeT,
                                ) != labyTest.get_forbidden_move():
                                    # On crée une seconde copy pour tester les possibilités du joueur suivant
                                    labyTest2 = copy.deepcopy(labyTest)
                                    labyTest2.play_tile(directionT, rangeeT)
                                    posT = labyTest2.get_coord_current_treasure()
                                    xJ, yJ = labyTest2.get_coord_current_player()
                                    if posT != None:
                                        xT, yT = posT
                                        if labyTest2.accessible(xT, yT, xJ, yJ):
                                            cptCoupGG += 1
                    if cptCoupGG == 0:
                        continuer = False
                    else:
                        actionsPossible.append(
                            (nbRotation, direction, rangee, cptCoupGG)
                        )
                    nbRotation += 1
                j += 1
            i += 1
        if continuer:

            def getNbCoupGG(elem):
                return elem[3]

            (nbRotation, direction, rangee, cptCoupGG) = min(
                actionsPossible, key=getNbCoupGG
            )
        return (nbRotation, direction, rangee)

    # Renvoie le chemin de l'IA défensive, utilise la fonction getMeilleurActionDefensive pour recupérer l'action
    # et getPositionMinDistance pour buger au plus pres de son tresors ( sait on jamais )
    def getCheminDefensif(self):
        (nbRotation, direction, rangee) = self.getMeilleurActionDefensive()
        for i in range(nbRotation):
            self.rotate_tile()
        self.play_tile(direction, rangee)
        xJ, yJ = self.get_coord_current_player()
        ((xD, yD), _) = self.getPositionMinDistance(
            self.get_coord_current_treasure(), (xJ, yJ)
        )
        return self.accessibleDist(xJ, yJ, xD, yD)

    ######################
    # Gestion Cheat Code #
    ######################

    # Ajoute un caractere code dans le code du joueur courant
    def ajouterCode(self, code):
        self.players.ajouterCode(code, self.current_player)

    # supprime un caractere code dans le code du joueur courant
    def supprimerCode(self):
        self.players.effacerCode(self.current_player)

    # Efface tout le code du joueur courant
    def effacerDernierCode(self):
        self.players.effacerDernierCode(self.current_player)

    # Permet de recuperer le code du joueur courant
    def getCode(self):
        return self.players.getCode(self.current_player)

    # Permet de verifier si le code du joueur courant est bon ( on peut ainsi changer le bon code ici )
    def estBonCode(self):
        return self.getCode() == [2, 7, 1, 3]


#############################################################
# Fonction Utilitaire ne dépandant pas de l'objet labyrinte #
#############################################################
# fonction qui permet de créer les cartes amovibles du jeu en y positionnant aléatoirement nbTresor Trésors
# la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées
def creerCartesAmovibles(nbTresors):
    listeCarte = []
    for i in range(16):  # 16 carte coude
        carte = Tile(True, True, False, False)
        carte.rotate_random()
        listeCarte.append(carte)
    for i in range(12):  # 12 carte tout-droit
        carte = Tile(True, False, True, False)
        carte.rotate_random()
        listeCarte.append(carte)
    for i in range(6):  # 6 carte T
        carte = Tile(True, True, True, False)
        carte.rotate_random()
        listeCarte.append(carte)
    random.shuffle(listeCarte)
    # Placer les trésors sur les cartes (attention à ne pas mettre les trésors déjà sur cartes fixes
    for tresor in range(1, nbTresors + 1):
        if not tresor in TRESORS_FIXES:
            listeCarte[tresor].put_treasure(tresor)
    return listeCarte


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + ((pos1[1] - pos2[1]) ** 2)) ** (0.5)
