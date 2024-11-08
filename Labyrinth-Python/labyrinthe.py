from tile import *
from matrix import DIMENSION, Matrix
from player import *
import copy

# TODO : change robjects name -> 1 to ... (7 x 7 - 3 (colonnes impair) *  7 - 3 * 4 (lignes impair sans case commune avec colonne) - 4 coins) )
# puis dans le code là où c'est complété -> complété jusqu'au bon nombre (pas 24 si le plateau ne fait pas 24)

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
        num_ai_players: int,
    ):
        
        self.player_types = ["human"] * num_human_players + ["ai"] * num_ai_players
        
        # TODO : if board dimension is not 7x7, we need to change the fixed cards
        board: Matrix = self.init_board_with_default_7x7_values()

        self.total_players = num_human_players + num_ai_players

        self.players: Players = Players(
            nb_players=self.total_players,
            nb_total_treasures=NUM_TREASURES,
            treasures_per_player=NUM_TREASURES_PER_PLAYER,
        )
        self.ai_players = range(num_human_players + 1, self.total_players + 1)
        if num_ai_players > 1:
            self.ia_players_def = range(
                num_human_players + num_ai_players,
                num_human_players + num_ai_players + 1,
            )
        else:
            self.ia_players_def = []

        self.current_player = 0
        self.coords_current_player = (0, 0)

        self.phase = 1  # inutile ??

        self.forbidden_move: tuple = ("N", 0)

        # Players placement
        if self.total_players >= 1:
            board.get_value(0, 0).put_pawn(0)  # A
        if self.total_players >= 2:
            board.get_value(0, 6).put_pawn(1)  # B
        if self.total_players >= 3:
            board.get_value(6, 0).put_pawn(2)  # C
        if self.total_players == 4:
            board.get_value(6, 6).put_pawn(3)  # D

        # Treasures and movable tiles
        tiles_list = create_movable_tiles(NUM_TREASURES)
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if (
                    i % 2 == 1 or j % 2 == 1
                ):  # Cela correspond aux emplacements non fixe
                    board.set_value(
                        i, j, tiles_list.pop(randint(0, len(tiles_list) - 1))
                    )
        self.tile_to_play: Tile = tiles_list[0]
        self.board = board

    def init_board_with_default_7x7_values(self):
        board: Matrix = Matrix()
        # fill the board with fixed cards
        board.set_value(0, 2, Tile(False, True, True, True, treasure=5))  # grimoire
        board.set_value(0, 4, Tile(False, True, True, True, treasure=13))  # bourse

        board.set_value(2, 0, Tile(True, True, True, False, treasure=1))  # fiole
        board.set_value(2, 2, Tile(True, True, True, False, treasure=7))  # couronne
        board.set_value(2, 4, Tile(False, True, True, True, treasure=14))  # clef
        board.set_value(2, 6, Tile(True, False, True, True, treasure=22))  # calice

        board.set_value(4, 0, Tile(True, True, True, False, treasure=2))  # bague
        board.set_value(4, 2, Tile(True, True, False, True, treasure=8))  # trésor
        board.set_value(
            4, 4, Tile(True, False, True, True, treasure=15)
        )  # pierre précieuse
        board.set_value(4, 6, Tile(True, False, True, True, treasure=23))  # épée

        board.set_value(6, 2, Tile(True, True, False, True, treasure=9))  # chandelier
        board.set_value(6, 4, Tile(True, True, False, True, treasure=16))  # casque

        # 4 corners
        board.set_value(0, 0, Tile(False, True, True, False, base=0))  # A
        board.set_value(0, 6, Tile(False, False, True, True, base=1))  # B
        board.set_value(6, 0, Tile(True, True, False, False, base=2))  # C
        board.set_value(6, 6, Tile(True, False, False, True, base=3))  # D
        return board

    # getters

    def get_board(self) -> Matrix:
        return self.board

    def get_num_players(self) -> int:
        return self.players.nb_players

    def get_current_player(self) -> int:
        return self.current_player

    def get_current_player_object(self):
        return self.players.players[self.current_player]

    def get_current_tile(self) -> Tile:
        return self.tile_to_play

    def get_phase(self):  # ?
        return self.phase  # ? 1 choisir sens carte, 2 choisir rangee, 3 avancer ???

    def get_tile_to_play(self):
        return self.tile_to_play

    def get_players(self) -> Players:
        return self.players

    def current_treasure(self) -> int:
        return self.players.get_next_treasure(self.get_current_player())

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

    def get_coord_player(self, joueur_id=None) -> tuple:
        """return the coordinates of the current player"""
        if joueur_id is None:
            joueur_id = self.get_current_player()

        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if self.board.get_value(i, j).has_pawn(joueur_id):
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
        self.current_player += 1
        self.current_player %= self.get_num_players()
        self.coords_current_player = self.get_coord_player()

    def get_current_player_num_find_treasure(self):
        """update the player structure when the current player find the treasure"""
        return self.players.tresorTrouve(self.current_player)  # TODO : améliorer code

    def get_current_player_remaining_treasure(self):
        """return the number of remaining treasures for the current player"""
        return self.get_remaining_treasures(self.current_player)

    def get_remaining_treasures(self, num_player):
        """return the number of remaining treasures for the player num_player"""
        return self.players.get_nb_treasures_remaining(
            num_player
        )  # TODO : améliorer code

    def is_forbidden_move(self, direction, position):
        return self.forbidden_move == (direction, position)

    def is_current_player_human(self):
        return self.player_types[self.current_player] == "human" # ne pas changer sinon ca marche pas

    def is_current_player_ai(self):
        return self.player_types[self.current_player] == "ai"  # ne pas changer sinon ca marche pas

    def remove_current_treasure(self):
        return self.players.remove_current_treasure(self.current_player)

    def remove_current_player_from_tile(self, row, col):
        """remove the current player from the tile at row, col"""
        self.board.get_value(row, col).remove_pawn(self.get_current_player())

    def put_current_player_in_tile(self, row, col):
        """put the current player in the tile at row, col"""
        self.board.get_value(row, col).put_pawn(self.get_current_player())

    def play_tile(self, direction, index):
        """play the tile in the direction and on the row/col index
        direction : N, E, S, O
        index : 1, 3, 5 if board is 7x7

        update the board, the tile to play and the forbidden move
        """
        if direction == "N" :
            ejected_tile = self.board.shift_column_down(index, self.tile_to_play)
            self.forbidden_move = ("S", index)
            opposite_position = (0, index)
        elif direction == "E":
            ejected_tile = self.board.shift_row_left(index, self.tile_to_play)
            self.forbidden_move = ("O", index)
            opposite_position = (index, 6)
        elif direction == "S":
            ejected_tile = self.board.shift_column_up(index, self.tile_to_play)
            self.forbidden_move = ("N", index)
            opposite_position = (6, index)
        elif direction == "O":
            ejected_tile = self.board.shift_row_right(index, self.tile_to_play)
            self.forbidden_move = ("E", index)
            opposite_position = (index, 0)
        else:
            raise ValueError(f"Direction non valide : {direction}")

        pions = ejected_tile.get_pawns()
        for pion in pions:
            ejected_tile.remove_pawn(pion)
            self.put_pawn(opposite_position[0], opposite_position[1], pion)

        self.tile_to_play = ejected_tile
        self.coords_current_player = self.get_coord_player()

    def rotate_tile(self, sens="H"):
        """rotate the tile to play
        sens : H for clockwise, A for counter clockwise
        """
        if sens == "H":
            self.tile_to_play.rotate_clockwise()
        else:
            self.tile_to_play.rotate_counter_clockwise()

    def put_pawn(self, row, col, player):
        """put the player in the tile at row, col"""
        self.board.get_value(row, col).put_pawn(player)

    # TODO : revoir les fonctions d'accessibilité des paths

    def tag_tiles(self, matrix: Matrix, value, tag):
        # TODO : remove cette fonction pour calcul plus efficace OU réutiliser ce tag pour ne pas tester tous les chemins possibles
        """mark the cells around a tile with value val and that is accessible from the current tile with tag"""
        changer = False
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if matrix.get_value(i, j) == value:
                    if i > 0:
                        if self.board.get_value(i, j).can_go_north(
                            self.board.get_value(i - 1, j)
                        ):
                            if matrix.get_value(i - 1, j) == 0:
                                matrix.set_value(i - 1, j, tag)
                                changer = True
                    if i < DIMENSION - 1:
                        if self.board.get_value(i, j).can_go_south(
                            self.board.get_value(i + 1, j)
                        ):
                            if matrix.get_value(i + 1, j) == 0:
                                matrix.set_value(i + 1, j, tag)
                                changer = True
                    if j > 0:
                        if self.board.get_value(i, j).can_go_west(
                            self.board.get_value(i, j - 1)
                        ):
                            if matrix.get_value(i, j - 1) == 0:
                                matrix.set_value(i, j - 1, tag)
                                changer = True
                    if j < DIMENSION - 1:
                        if self.board.get_value(i, j).can_go_east(
                            self.board.get_value(i, j + 1)
                        ):
                            if matrix.get_value(i, j + 1) == 0:
                                matrix.set_value(i, j + 1, tag)
                                changer = True
        return changer

    def accessible(self, rowS, colS, rowE, colE):
        """
        propagation algo to check if there is a path between the two cells (rowS, colS) and (rowE, colE)
        by tagging the cells with a value and checking if the destination cell is tagged
        """
        matTest = Matrix()
        matTest.set_value(rowS, colS, 1)
        change = True
        while change and matTest.get_value(rowE, colE) == 0:
            change = self.tag_tiles(matTest, 1, 1)
        return matTest.get_value(rowE, colE) == 1

    def is_accessible(self, rowS, colS, rowE, colE):
        """
        return None if there is no path between the two cells (rowS, colS) and (rowE, colE)
        """
        if not self.accessible(rowS, colS, rowE, colE):
            return []
        else:
            matTest = Matrix()
            matTest.set_value(rowS, colS, 1)
            changer = True
            i = 1
            while changer and matTest.get_value(rowE, colE) == 0:
                changer = self.tag_tiles(matTest, i, i + 1)
                i += 1
            x, y = rowE, colE
            chemin = [(x, y)]
            val = matTest.get_value(x, y)
            while x != rowS or y != colS:
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

    def get_accessible_current_player(self, rowE, colE):
        """return the path from the current player to the cell (rowE, colE) if it exists
        if not return None"""
        (ligD, colD) = self.get_coord_player()
        return self.is_accessible(ligD, colD, rowE, colE)

    # TODO :
    # tout ça : doit disaparaitre
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
                    xJ, yJ = labyTest.get_coord_player()
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
            xJ, yJ = self.get_coord_player()
            return self.is_accessible(xJ, yJ, xC, yC)
        else:
            return self.is_accessible(xJ, yJ, xT, yT)

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
                                    xJ, yJ = labyTest2.get_coord_player()
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
        xJ, yJ = self.get_coord_player()
        ((xD, yD), _) = self.getPositionMinDistance(
            self.get_coord_current_treasure(), (xJ, yJ)
        )
        return self.is_accessible(xJ, yJ, xD, yD)


# TODO : placer cette fonction ailleurs ?
def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + ((pos1[1] - pos2[1]) ** 2)) ** (0.5)
