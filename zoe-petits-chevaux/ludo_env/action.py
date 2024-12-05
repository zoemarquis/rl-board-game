from enum import Enum


# version du jeu où il ne faut pas atteindre exactement la case 56
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


# version du jeu où il faut atteindre exactement la case 56
class Action_EXACT(Enum):
    NO_ACTION = 0
    MOVE_OUT = 1 
    MOVE_OUT_AND_KILL = 2  

    MOVE_FORWARD = 3  
    GET_STUCK_BEHIND = 4

    REACH_PIED_ESCALIER = 5
    AVANCE_RECULE_PIED_ESCALIER = 6 # se rapprocher de 56, si il s'éloigne plus : coup interdit 

    MOVE_IN_SAFE_ZONE = 7
    REACH_GOAL = 8

    KILL = 9
