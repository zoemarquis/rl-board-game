import pytest
from game.ludo_env import GameLogic, Action_NO_EXACT


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=3, nb_chevaux=2)


@pytest.fixture
def game_3chevaux():
    return GameLogic(num_players=3, nb_chevaux=3)


@pytest.fixture
def game_4chevaux():
    return GameLogic(num_players=3, nb_chevaux=4)


def test_fin_de_partie_tous_chevaux_3chevaux(game_3chevaux):
    game_3chevaux.init_board()

    game_3chevaux.move_pawn(1, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")

    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."
    assert lines[8] == "ESCALIER 0 : [0, 0, 0, 0, 0, 0]", "ESCALIER 0 incorrect."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 1]", "ESCALIER 1 incorrect."
    assert lines[10] == "ESCALIER 2 : [0, 0, 0, 0, 0, 0]", "ESCALIER 2 incorrect."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 0."
    assert lines[12] == "OBJECTIF 1 : 0", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."
    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 62, 1, Action_NO_EXACT.REACH_GOAL)

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 2", "ECURIE 1 doit avoir 2 pions."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."
    assert lines[12] == "OBJECTIF 1 : 1", "OBJECTIF 0 doit être à 1."

    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 1", "ECURIE 1 doit avoir 1 pion."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 1]", "ESCALIER 1 incorrect."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 1."
    assert lines[12] == "OBJECTIF 1 : 1", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."

    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 62, 1, Action_NO_EXACT.REACH_GOAL)

    game_3chevaux.move_pawn(1, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_3chevaux.move_pawn(1, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_3chevaux.move_pawn(1, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(1, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)

    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 0", "ECURIE 1 doit avoir 0 pion."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 1]", "ESCALIER 1 incorrect."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 1."
    assert lines[12] == "OBJECTIF 1 : 2", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."

    assert game_3chevaux.is_game_over() == False

    game_3chevaux.move_pawn(1, 62, 1, Action_NO_EXACT.REACH_GOAL)
    str_to_check = game_3chevaux.get_str_game_overview()
    lines = str_to_check.split("\n")
    assert lines[0] == "ECURIE 0 : 3", "ECURIE 0 doit avoir 3 pion."
    assert lines[1] == "ECURIE 1 : 0", "ECURIE 1 doit avoir 0 pion."
    assert lines[2] == "ECURIE 2 : 3", "ECURIE 2 doit avoir 3 pions."
    assert lines[9] == "ESCALIER 1 : [0, 0, 0, 0, 0, 0]", "ESCALIER 1 incorrect."
    assert lines[11] == "OBJECTIF 0 : 0", "OBJECTIF 0 doit être à 1."
    assert lines[12] == "OBJECTIF 1 : 3", "OBJECTIF 1 doit être à 0."
    assert lines[13] == "OBJECTIF 2 : 0", "OBJECTIF 2 doit être à 0."

    assert game_3chevaux.is_game_over() == True


def test_fin_de_partie_un_cheval_gagne_2chevaux(game_2chevaux):
    game_2chevaux.init_board()
    game_2chevaux.move_pawn(0, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_2chevaux.move_pawn(0, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_2chevaux.move_pawn(0, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_2chevaux.move_pawn(0, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.is_game_over() == False
    game_2chevaux.move_pawn(0, 62, 1, Action_NO_EXACT.REACH_GOAL)
    assert game_2chevaux.is_game_over() == False


def test_fin_de_partie_un_cheval_gagne_3chevaux(game_3chevaux):
    game_3chevaux.init_board()
    game_3chevaux.move_pawn(0, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_3chevaux.move_pawn(0, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_3chevaux.move_pawn(0, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(0, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.is_game_over() == False
    game_3chevaux.move_pawn(0, 62, 1, Action_NO_EXACT.REACH_GOAL)
    assert game_3chevaux.is_game_over() == False


def test_fin_de_partie_un_cheval_gagne_4chevaux(game_4chevaux):
    game_4chevaux.init_board()
    game_4chevaux.move_pawn(0, 0, 6, Action_NO_EXACT.MOVE_OUT)
    game_4chevaux.move_pawn(0, 1, 55, Action_NO_EXACT.MOVE_FORWARD)
    game_4chevaux.move_pawn(0, 56, 1, Action_NO_EXACT.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(0, 57, 5, Action_NO_EXACT.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.is_game_over() == False
    game_4chevaux.move_pawn(0, 62, 1, Action_NO_EXACT.REACH_GOAL)
    assert game_4chevaux.is_game_over() == False
