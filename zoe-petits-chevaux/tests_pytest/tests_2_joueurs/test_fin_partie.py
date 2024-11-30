import pytest
from ludo_env import GameLogic, Action


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=2, nb_chevaux=2)

@pytest.fixture
def game_3chevaux():
    return GameLogic(num_players=2, nb_chevaux=3)

@pytest.fixture
def game_4chevaux():
    return GameLogic(num_players=2, nb_chevaux=4)

def test_fin_de_partie_tous_chevaux_2chevaux(game_2chevaux):
    game_2chevaux.init_board()
    game_2chevaux.move_pawn(0,0,6,Action.MOVE_OUT)
    game_2chevaux.move_pawn(0,1,55,Action.MOVE_FORWARD)
    game_2chevaux.move_pawn(0,56,1,Action.ENTER_SAFEZONE)
    game_2chevaux.move_pawn(0,57,5,Action.MOVE_IN_SAFE_ZONE)

    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 1]", "ESCALIER 0 incorrecte."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."
    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."

    game_2chevaux.move_pawn(0,62,1,Action.REACH_GOAL)

    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 1", "ECURIE 0 doit avoir 1 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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
    assert lines[9] == "OBJECTIF 0 : 1", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert game_2chevaux.is_game_over() == False

    game_2chevaux.move_pawn(0,0,6,Action.MOVE_OUT)
    game_2chevaux.move_pawn(0,1,55,Action.MOVE_FORWARD)
    game_2chevaux.move_pawn(0,56,1,Action.ENTER_SAFEZONE)
    game_2chevaux.move_pawn(0,57,5,Action.MOVE_IN_SAFE_ZONE)

    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 0", "ECURIE 0 doit avoir 0 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 1]", "ESCALIER 0 incorrecte."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrecte."
    assert lines[9] == "OBJECTIF 0 : 1", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."

    game_2chevaux.move_pawn(0,62,1,Action.REACH_GOAL)

    str_to_check = game_2chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 0", "ECURIE 0 doit avoir 0 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "chemin vu par joueur 0 : ", "ligne 2 incorrecte."
    assert (
        lines[3] == "[[], [], [], [], [], [], [], [], [], [], [], [], [], []]"
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
    assert lines[9] == "OBJECTIF 0 : 2", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."

    assert game_2chevaux.is_game_over() == True


def test_fin_de_partie_tous_chevaux_3chevaux(game_3chevaux):
    game_3chevaux.init_board()

    game_3chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrect."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 1]", "ESCALIER 1 incorrect."
    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 62, 1, Action.REACH_GOAL)
    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)
    game_3chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)

    assert game_3chevaux.is_game_over() == False

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 0", "ECURIE 1 doit avoir 0 pion."
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrect."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 2]", "ESCALIER 1 incorrect."
    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 1", "OBJECTIF 1 doit être à 0."

    game_3chevaux.move_pawn(1, 62, 3, Action.REACH_GOAL)
    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 62, 6, Action.REACH_GOAL)
    assert game_3chevaux.is_game_over() == True


def test_fin_de_partie_tous_chevaux_4chevaux(game_4chevaux):
    game_4chevaux.init_board()

    game_4chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_4chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_4chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)

    str_to_check = game_4chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 4", "ECURIE 0 doit avoir 4 pion."
    assert lines[1] == "ECURIE 1 : 3", "ECURIE 1 doit avoir 3 pions."
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrect."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 1]", "ESCALIER 1 incorrect."
    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert game_4chevaux.is_game_over() == False

    game_4chevaux.move_pawn(1, 62, 1, Action.REACH_GOAL)
    assert game_4chevaux.is_game_over() == False

    game_4chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_4chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_4chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)
    game_4chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_4chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_4chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)

    assert game_4chevaux.is_game_over() == False

    str_to_check = game_4chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 4", "ECURIE 0 doit avoir 4 pion."
    assert lines[1] == "ECURIE 1 : 1", "ECURIE 1 doit avoir 1 pion."
    assert lines[7] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrect."
    assert lines[8] == "ESCALIER 1 : [0, 0, 0, 0, 0, 2]", "ESCALIER 1 incorrect."
    assert lines[9] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[10] == "OBJECTIF 1 : 1", "OBJECTIF 1 doit être à 0."

    game_4chevaux.move_pawn(1, 62, 3, Action.REACH_GOAL)
    assert game_4chevaux.is_game_over() == False
    game_4chevaux.move_pawn(1, 62, 6, Action.REACH_GOAL)
    assert game_4chevaux.is_game_over() == False

    game_4chevaux.move_pawn(1, 0, 6, Action.MOVE_OUT)
    game_4chevaux.move_pawn(1, 1, 55, Action.MOVE_FORWARD)
    game_4chevaux.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(1, 57, 5, Action.MOVE_IN_SAFE_ZONE)
    game_4chevaux.move_pawn(1, 62, 6, Action.REACH_GOAL)
    assert game_4chevaux.is_game_over() == True


## TODO faire la meme chose pour un seul cheval gagne (2 , 3 , 4)

