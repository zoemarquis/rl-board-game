from enum import Enum


class Action(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1  # Sortir de la maison
    MOVE_FORWARD = 2  # Avancer le long du chemin
    ENTER_SAFEZONE = 3  # Entrer dans la zone protégée
    MOVE_IN_SAFE_ZONE = 4  # Avancer dans la zone protégée
    REACH_GOAL = 5  # Atteindre l'objectif final
    KILL = 6  # Tuer un pion adverse
    # TODO :
    # REACH PIED ESCALIER
    # ESCALADER à la place de move in safe zone mais comment faire comprendre si 1 2 3 4 5 ou 6
