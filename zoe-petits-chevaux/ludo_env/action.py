from enum import Enum


class Action(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1  # Sortir de la maison
    MOVE_OUT_AND_KILL = 2  # Sortir de la maison et tuer un pion adverse

    MOVE_FORWARD = 3  # Avancer le long du chemin
    ENTER_SAFEZONE = 4  # Entrer dans la zone protégée
    MOVE_IN_SAFE_ZONE = 5  # Avancer dans la zone protégée
    REACH_GOAL = 6  # Atteindre l'objectif final
    KILL = 7  # Tuer un pion adverse

    # TODO :
    # REACH PIED ESCALIER
    # ESCALADER à la place de move in safe zone mais comment faire comprendre si 1 2 3 4 5 ou 6
