from enum import Enum


class Action_NO_EXACT(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1  # Sortir de la maison
    MOVE_OUT_AND_KILL = 2  # Sortir de la maison et tuer un pion adverse

    MOVE_FORWARD = 3  # Avancer le long du chemin
    GET_STUCK_BEHIND = 4
    ENTER_SAFEZONE = 5  # Entrer dans la zone protégée
    MOVE_IN_SAFE_ZONE = 6  # Avancer dans la zone protégée
    REACH_GOAL = 7  # Atteindre l'objectif final
    KILL = 8  # Tuer un pion adverse
