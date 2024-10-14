from random import randint


# TODO : supprimer ? inutile ??
# la liste des caractère semi-graphiques correspondants aux différentes cartes
# l'indice du caractère dans la liste correspond au codage des murs sur la carte
# le caractère 'Ø' indique que l'indice ne correspond pas à une carte
listeCartes = [
    "Ø",
    "╦",
    "╣",
    "╗",
    "╩",
    "═",
    "╝",
    "Ø",
    "╠",
    "╔",
    "║",
    "Ø",
    "╚",
    "Ø",
    "Ø",
    "Ø",
]


class Tile(object):
    """Class Tile
    This class is used to create a tile with 4 walls and a treasure
    - 4 directions : north, east, south, west
        if north == True, there is no wall on the north side
        elif north == False, there is a wall on the north side
    - treasure : the value of the treasure on the tile
        0 if there is no treasure
    - pawns : list of pawns on the tile
    - is_base : 0 if it's not a base, else the number of the player who has the base
    """

    def __init__(self, north, east, south, west, treasure=0, pawns=[], base=0):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.treasure = treasure
        self.pawns = set(pawns)
        self.base = base

    def is_base(self):
        return self.base

    # TODO : inutile ?
    # # retourne un booléen indiquant si la carte est valide ou non c'est à dire qu'elle a un ou deux murs
    # def estValide(self):
    #     cpt = 0
    #     if self.nord:
    #         cpt += 1
    #     if self.est:
    #         cpt += 1
    #     if self.sud:
    #         cpt += 1
    #     if self.ouest:
    #         cpt += 1
    #     return cpt == 2 or cpt == 3

    def way_north(self):
        return self.north

    def way_east(self):
        return self.east

    def way_south(self):
        return self.south

    def way_west(self):
        return self.west

    def wall_north(self):
        return not self.north

    def wall_east(self):
        return not self.east

    def wall_south(self):
        return not self.south

    def wall_west(self):
        return not self.west

    def get_pawns(self):
        return list(self.pawns)

    def get_nb_pawns(self):
        return len(self.pawns)

    def has_pawn(self, pawn):
        return pawn in self.pawns

    def set_pions(self, pawns):
        self.pawns = self.pawns.union(pawns)

    def get_treasure(self):
        return self.treasure

    def pop_treasure(self):
        """Remove the treasure from the tile and return the value of the treasure"""
        tresor = self.treasure
        self.treasure = 0
        return tresor

    def put_treasure(self, tresor):
        assert self.treasure == 0, "There is already a treasure on this tile"
        self.treasure = tresor

    def remove_pawn(self, pawn):
        self.pawns = self.pawns.difference({pawn})

    def put_pawn(self, pawn):
        self.pawns.add(pawn)

    def rotate_clockwise(self):  # TODO : check c'est le mauvais sens ???
        tmp = self.north
        self.north = self.west
        self.west = self.south
        self.south = self.east
        self.east = tmp

    def rotate_counter_clockwise(self):  # TODO : va avec le mauvais sens ???
        tmp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = tmp

    def rotate_random(self):
        for i in range(randint(0, 3)):
            self.rotate_clockwise()

    def can_go_north(self, tile2) -> bool:
        """Check if there is a passage between the two tiles by the north side"""
        return self.way_north() and tile2.way_south()

    def can_go_south(self, tile2):
        return self.way_south() and tile2.way_north()

    def can_go_west(self, tile2):
        return self.way_west() and tile2.way_east()

    def can_go_east(self, tile2):
        return self.way_east() and tile2.way_west()

    # TODO : nettoyage
    # code les murs sous la forme d'un entier dont le codage binaire
    # est de la forme bNbEbSbO où bN, bE, bS et bO valent
    #      soit 0 s'il n'y a pas de mur dans dans la direction correspondante
    #      soit 1 s'il y a un mur dans la direction correspondante
    # bN est le chiffre des unité, BE des dizaine, etc...
    # le code obtenu permet d'obtenir l'indice du caractère semi-graphique
    # correspondant à la carte dans la liste listeCartes au début de ce fichier
    def coderMurs(self):
        code = 0
        if not self.north:
            code += 1
        if not self.east:
            code += 2
        if not self.south:
            code += 4
        if not self.west:
            code += 8
        return code

    # positionne les mur d'une carte en fonction du code décrit précédemment
    def decoderMurs(self, code):
        if code >= 8:
            self.north = False
            code -= 8
        else:
            self.north = True
        if code >= 4:
            self.east = False
            code -= 4
        else:
            self.east = True
        if code >= 2:
            self.south = False
            code -= 2
        else:
            self.south = True
        if code >= 1:
            self.west = False
        else:
            self.west = True

    # fournit le caractère semi graphique correspondant à la carte (voir la variable listeCartes au début de ce script)
    def to_char(self):
        return listeCartes[self.coderMurs()]
