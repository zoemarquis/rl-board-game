import pytest
from ludo_env.game_logic import *


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=3, nb_chevaux=2)


def test_kill_move_out_2chevaux(game_2chevaux):
    game_2chevaux.init_board()
    game_2chevaux.move_pawn(0, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_2chevaux.move_pawn(0, 1, 14, Action_NO_EXACT.MOVE_FORWARD)
    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "ECURIE 2 : 2", "ECURIE 2 doit avoir 2 pions."
    assert lines[3] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[0], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[7] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert lines[8] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrecte."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."
    assert lines[10] == "ESCALIER 2 : [0, 0, 0, 0, 0, 0]", "ESCALIER 2 incorrecte."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[12] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."

    assert game_2chevaux.get_valid_actions(0, 6) == [[Action_NO_EXACT.MOVE_OUT], [Action_NO_EXACT.MOVE_FORWARD], False]
    assert game_2chevaux.get_valid_actions(1, 6) == [[Action_NO_EXACT.MOVE_OUT_AND_KILL], [Action_NO_EXACT.MOVE_OUT_AND_KILL], False]


def test_kill_2chevaux(game_2chevaux):
    game_2chevaux.init_board()
    game_2chevaux.move_pawn(0, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_2chevaux.move_pawn(1, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_2chevaux.move_pawn(0, 1, 13, Action_NO_EXACT.MOVE_FORWARD)
    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 1", "ECURIE 1 doit avoir 1 pion."
    assert lines[2] == "ECURIE 2 : 2", "ECURIE 2 doit avoir 2 pions."
    assert lines[3] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], [0]]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[1], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[7] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert lines[8] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrecte."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."
    assert lines[10] == "ESCALIER 2 : [0, 0, 0, 0, 0, 0]", "ESCALIER 2 incorrecte."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[12] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."
    
    assert game_2chevaux.get_valid_actions(0, 1) == [[], [Action_NO_EXACT.KILL], False]

    game_2chevaux.move_pawn(2, 0, 6, Action_NO_EXACT.MOVE_OUT)
    assert game_2chevaux.get_valid_actions(2, 6) == [[], [Action_NO_EXACT.MOVE_FORWARD], False]

    game_2chevaux.move_pawn(2, 1, 35, Action_NO_EXACT.MOVE_FORWARD)
    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [2], [], [], [], [], [], [0]]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[1], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[7] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte." 

    assert game_2chevaux.get_valid_actions(2, 6) == [[Action_NO_EXACT.MOVE_OUT], [Action_NO_EXACT.KILL], False]

