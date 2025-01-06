import pytest
from ludo_env.game_logic import *


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=3, nb_chevaux=2)


@pytest.fixture
def game_3chevaux():
    return GameLogic(num_players=3, nb_chevaux=3)


@pytest.fixture
def game_4chevaux():
    return GameLogic(num_players=3, nb_chevaux=4)


def test_initial_board_2pawns(game_2chevaux):
    game_2chevaux.init_board()
    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 2", "ECURIE 0 doit avoir 2 pions."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "ECURIE 2 : 2", "ECURIE 2 doit avoir 2 pions."
    assert lines[3] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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


def test_initial_board_3pawns(game_3chevaux):
    game_3chevaux.init_board()
    str_to_check = game_3chevaux.get_str_game_overview()

    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pions."
    assert lines[1] == "ECURIE 1 : 3", "ECURIE 1 doit avoir 3 pions."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."

    assert lines[3] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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


def test_initial_board_4pawns(game_4chevaux):
    game_4chevaux.init_board()
    str_to_check = game_4chevaux.get_str_game_overview()

    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 4", "ECURIE 0 doit avoir 4 pions."
    assert lines[1] == "ECURIE 1 : 4", "ECURIE 1 doit avoir 4 pions."
    assert lines[2] == "ECURIE 2 : 4", "ECURIE 2 doit avoir 4 pions."

    assert lines[3] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[4] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
    ), "CHEMIN 0 incorrecte."
    assert (
        lines[5] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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
