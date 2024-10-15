from random import randint

# List of semi-graphic characters representing the tiles
SEMI_GRAPHIC_TILES = [
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

    def __init__(
        self,
        north: bool,
        east: bool,
        south: bool,
        west: bool,
        treasure: int = 0,
        base=0,
    ):
        # check form of the tile is correct
        assert (
            (north and south and not east and not west)
            or (not north and not south and east and west)
            or (north and east and not south and not west)
            or (not north and east and south and not west)
            or (not north and not east and south and west)
            or (north and not east and not south and west)
            or (north and not east and not south and west)
            or (north and east and south and not west)
            or (north and east and not south and west)
            or (not north and east and south and west)
            or (north and not east and south and west)
        ), "The form of the tile is incorrect"
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.treasure = treasure
        self.pawns = set()
        self.base = base

    def is_base(self) -> int:
        return self.base

    def way_north(self) -> bool:
        return self.north

    def way_east(self) -> bool:
        return self.east

    def way_south(self) -> bool:
        return self.south

    def way_west(self) -> bool:
        return self.west

    def wall_north(self) -> bool:
        return not self.north

    def wall_east(self) -> bool:
        return not self.east

    def wall_south(self) -> bool:
        return not self.south

    def wall_west(self) -> bool:
        return not self.west

    def get_pawns(self) -> list[int]:
        return list(self.pawns)

    def get_nb_pawns(self) -> int:
        return len(self.pawns)

    def has_pawn(self, pawn: int) -> bool:
        return pawn in self.pawns

    def set_pions(self, pawns: list[int]) -> None:
        self.pawns = self.pawns.union(pawns)

    def get_treasure(self) -> int:
        """Return the value of the treasure on the tile, 0 if there is no treasure"""
        return self.treasure

    def pop_treasure(self) -> int:
        """Remove the treasure from the tile and return the value of the treasure"""
        tresor = self.treasure
        self.treasure = 0
        return tresor

    def put_treasure(self, tresor: int) -> None:
        assert self.treasure == 0, "There is already a treasure on this tile"
        self.treasure = tresor

    def remove_pawn(self, pawn: int) -> None:
        self.pawns = self.pawns.difference({pawn})

    def put_pawn(self, pawn: int) -> None:
        self.pawns.add(pawn) 

    # TODO : check c'est le mauvais sens ???
    def rotate_clockwise(self) -> None:
        tmp = self.north
        self.north = self.west
        self.west = self.south
        self.south = self.east
        self.east = tmp

    # TODO : va avec le mauvais sens ???
    def rotate_counter_clockwise(self) -> None:
        tmp = self.north
        self.north = self.east
        self.east = self.south
        self.south = self.west
        self.west = tmp

    def rotate_random(self) -> None:
        for _ in range(randint(0, 3)):
            self.rotate_clockwise()

    def can_go_north(self, tile2: "Tile") -> bool:
        """Check if there is a passage between the two tiles by the north side"""
        return self.way_north() and tile2.way_south()

    def can_go_south(self, tile2: "Tile") -> bool:
        return self.way_south() and tile2.way_north()

    def can_go_west(self, tile2: "Tile") -> bool:
        return self.way_west() and tile2.way_east()

    def can_go_east(self, tile2: "Tile") -> bool:
        return self.way_east() and tile2.way_west()

    def tile_to_char(self) -> int:
        """
        Return the binary integer corresponding to the tile's walls configuration.
        The binary representation is as follows:
        - Each bit represents a wall in a specific direction: north, east, south, west.
        - A bit value of 1 indicates the presence of a wall, and 0 indicates no wall.

        Examples:
        - If there are walls on every side, the binary is 1111 -> 15.
        - If there are no walls, the binary is 0000 -> 0.
        - If there is a wall on the north side, the binary is 0001 -> 1.
        - If there are walls on the west and south sides, the binary is 1100 -> 12.
        """
        code = 0
        if self.wall_north():
            code += 1
        if self.wall_east():
            code += 2
        if self.wall_south():
            code += 4
        if self.wall_west():
            code += 8
        return code

    def char_to_tile(self, code: int) -> None:
        """
        Set the walls configuration of the tile based on the binary integer.
        The binary representation is as follows:
        - Each bit represents a wall in a specific direction: north (1), east(2), south(4), west(8).
        - A bit value of 1 indicates the presence of a wall, and 0 indicates no wall.
        """
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

    def to_char(self) -> str:
        """Return the semi-graphic character corresponding to the tile"""
        return SEMI_GRAPHIC_TILES[self.tile_to_char()]
