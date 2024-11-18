class Player:

    def __init__(self):
        self.pawns = []
        self.set_all_pawns_to_home()

    def get_pawns_that_can_move(self, dice):
        movable_pawns = []
        for pawn, pawn_place in enumerate(self.pawns):
            if pawn_place == -1 and dice == 6:
                movable_pawns.append(pawn)
            elif pawn_place != -1:
                movable_pawns.append(pawn)