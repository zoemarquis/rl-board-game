import pytest
from ludo_env import *


def test_reward():
    assert get_default_action_order(2, "not_exact") == [0, 
                                                        1, 2,
                                                        14, 8, 
                                                        13, 7,
                                                        11, 5,
                                                        12, 6,
                                                        9, 3,
                                                        10, 4,] # GET STUCK
    assert get_default_action_order(3, "not_exact") == [0, 
                                                        1, 2, # MOVE OUT 
                                                        20, 14, 8, # REACH GOAL
                                                        19, 13, 7 , # MOVE IN SAFE ZONE
                                                        17, 11, 5, # REACH PIED
                                                        18, 12, 6, # AVANCE RECULE PIED
                                                        15, 9, 3,# MOVE FORWARD 
                                                        16, 10, 4, ]# GET STUCK 
    assert get_default_action_order(4, "not_exact") == [0, 
                                                        1, 2,
                                                        26, 20, 14, 8,
                                                        25, 19, 13, 7,
                                                        23, 17, 11, 5,
                                                        24, 18, 12, 6,
                                                        21, 15, 9, 3,
                                                        22, 16, 10, 4]

    assert get_default_action_order(2, "exact") == [0, 
                                                        1, 2,
                                                        16, 9, 
                                                        15, 8, 
                                                        12, 5, 
                                                        13, 6,
                                                        14, 7,
                                                        10, 3, 
                                                        11, 4]
    assert get_default_action_order(3, "exact") == [0, 
                                                        1, 2,
                                                        23, 16, 9, 
                                                        22, 15, 8, 
                                                        19, 12, 5, 
                                                        20, 13, 6,
                                                        21, 14, 7,
                                                       17,  10, 3, 
                                                       18, 11, 4]
    assert get_default_action_order(4, "exact") == [0, 
                                                        1, 2,
                                                        30, 23, 16, 9, 
                                                        29,22, 15, 8, 
                                                        26, 19, 12, 5, 
                                                        27,20, 13, 6,
                                                        28,21, 14, 7,
                                                       24, 17,  10, 3,
                                                       25, 18, 11, 4]                                                

