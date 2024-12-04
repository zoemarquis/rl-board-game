from enum import Enum


class State(Enum):
    ECURIE = 0
    CHEMIN = 1
    # TODO ZOE : PIED_ESCALIER = 2
    ESCALIER = 2
    OBJECTIF = 3

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State.ECURIE
        elif relative_position < 57:
            return State.CHEMIN
        # TODO ZOE : elif relative_position == 57:
        #     return State.PIED_ESCALIER
        elif relative_position < 63:
            return State.ESCALIER
        else:
            return State.OBJECTIF
