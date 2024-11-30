import pytest
from ludo_env.game_logic import *


@pytest.fixture
def game():
    """Fixture pour initialiser un objet Game."""
    return GameLogic(num_players=2, nb_chevaux=2)

def test_1(game):
    game.init_board()
    game.move_pawn(0, 0, 6, Action.MOVE_OUT)

    str_to_check = game.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."

    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[0], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."

    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrecte."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."

    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."

def test_2(game):
    game.init_board()
    game.move_pawn(0, 0, 6, Action.MOVE_OUT)
    game.move_pawn(1, 0, 6, Action.MOVE_OUT)

    str_to_check = game.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 1", "ECURIE 1 doit avoir 1 pion."

    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[0], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[1], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."

    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrecte."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."

    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."



def test_3(game):
    game.init_board()
    game.move_pawn(0, 0, 6, Action.MOVE_OUT)
    game.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game.move_pawn(1, 0, 6, Action.MOVE_OUT)

    str_to_check = game.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 0", "ECURIE 1 doit avoir 1 pion."

    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[0], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[1, 1], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[6] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."

    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrecte."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."

    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."


def test_interdit_1(game):
    game.init_board()
    game.move_pawn(0, 0, 5, Action.MOVE_OUT)

    str_to_check = game.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert False 
    # TODO 


def test_interdit_2(game):
    game.init_board()
    game.move_pawn(0, 0, 6, Action.MOVE_OUT)
    game.move_pawn(0, 1, 6, Action.MOVE_OUT)

    str_to_check = game.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert False 
    # TODO 
