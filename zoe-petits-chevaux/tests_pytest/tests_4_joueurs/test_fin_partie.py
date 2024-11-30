import pytest
from ludo_env import GameLogic, Action


@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=3, nb_chevaux=2)

@pytest.fixture
def game_3chevaux():
    return GameLogic(num_players=3, nb_chevaux=3)

@pytest.fixture
def game_4chevaux():
    return GameLogic(num_players=3, nb_chevaux=4)



# TODO : comme pour 2 et 3 joueurs

def test_fin_de_partie_un_cheval_gagne_2chevaux(game_2chevaux):
    game_2chevaux.init_board()
    game_2chevaux.move_pawn(0,0,6,Action.MOVE_OUT)
    game_2chevaux.move_pawn(0,1,55,Action.MOVE_FORWARD)
    game_2chevaux.move_pawn(0,56,1,Action.ENTER_SAFEZONE)
    game_2chevaux.move_pawn(0,57,5,Action.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.is_game_over() == False
    game_2chevaux.move_pawn(0,62,1,Action.REACH_GOAL)
    assert game_2chevaux.is_game_over() == False

def test_fin_de_partie_un_cheval_gagne_3chevaux(game_3chevaux):
    game_3chevaux.init_board()
    game_3chevaux.move_pawn(0,0,6,Action.MOVE_OUT)
    game_3chevaux.move_pawn(0,1,55,Action.MOVE_FORWARD)
    game_3chevaux.move_pawn(0,56,1,Action.ENTER_SAFEZONE)
    game_3chevaux.move_pawn(0,57,5,Action.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.is_game_over() == False
    game_3chevaux.move_pawn(0,62,1,Action.REACH_GOAL)
    assert game_3chevaux.is_game_over() == False

def test_fin_de_partie_un_cheval_gagne_4chevaux(game_4chevaux):
    game_4chevaux.init_board()
    game_4chevaux.move_pawn(0,0,6,Action.MOVE_OUT)
    game_4chevaux.move_pawn(0,1,55,Action.MOVE_FORWARD)
    game_4chevaux.move_pawn(0,56,1,Action.ENTER_SAFEZONE)
    game_4chevaux.move_pawn(0,57,5,Action.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.is_game_over() == False
    game_4chevaux.move_pawn(0,62,1,Action.REACH_GOAL)
    assert game_4chevaux.is_game_over() == False
