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
    game = GameLogic(num_players=2, nb_chevaux=4)
    game.board[0] = [ 2, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game.board[1] = [ 4,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    return game



def test_get_relative_position_0(game_4chevaux):
    assert game_4chevaux.get_relative_position(0, 1, 1) == 29
    assert game_4chevaux.get_relative_position(0, 1, 14) == 42
    assert game_4chevaux.get_relative_position(0, 1, 15) == 43
    assert game_4chevaux.get_relative_position(0, 1, 28) == 56
    assert game_4chevaux.get_relative_position(0, 1, 29) == 1
    assert game_4chevaux.get_relative_position(0, 1, 42) == 14
    assert game_4chevaux.get_relative_position(0, 1, 56) == 28

    
def test_get_relative_position_1(game_4chevaux):
    assert game_4chevaux.get_relative_position(1, 0, 1) == 29
    assert game_4chevaux.get_relative_position(1, 0, 14) == 42
    assert game_4chevaux.get_relative_position(1, 0, 15) == 43
    assert game_4chevaux.get_relative_position(1, 0, 28) == 56
    assert game_4chevaux.get_relative_position(1, 0, 29) == 1
    assert game_4chevaux.get_relative_position(1, 0, 42) == 14
    assert game_4chevaux.get_relative_position(1, 0, 56) == 28


def test_is_opponent_pawn_on(game_4chevaux):
    assert game_4chevaux.is_opponent_pawn_on(0, 14) == False
    assert game_4chevaux.get_valid_actions(0, 1) == [[], [], [Action.MOVE_FORWARD], [Action.MOVE_FORWARD], False]

                              
    
