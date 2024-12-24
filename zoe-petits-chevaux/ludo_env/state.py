from enum import Enum


class State_NO_EXACT(Enum):
    ECURIE = 0
    CHEMIN = 1
    ESCALIER = 2
    OBJECTIF = 3

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State_NO_EXACT.ECURIE
        elif relative_position < 57:
            return State_NO_EXACT.CHEMIN
        elif relative_position < 63:
            return State_NO_EXACT.ESCALIER
        else:
            return State_NO_EXACT.OBJECTIF


class State_EXACT(Enum):
    ECURIE = 0
    CHEMIN = 1
    PIED_ESCALIER = 2
    ESCALIER = 3
    OBJECTIF = 4

    @staticmethod
    def get_state_from_position(relative_position: int):
        assert 0 <= relative_position <= 63, "Position invalide"
        if relative_position == 0:
            return State_EXACT.ECURIE
        elif relative_position < 56:
            return State_EXACT.CHEMIN
        elif relative_position == 56:
            return State_EXACT.PIED_ESCALIER
        elif relative_position < 63:
            return State_EXACT.ESCALIER
        else:
            return State_EXACT.OBJECTIF
