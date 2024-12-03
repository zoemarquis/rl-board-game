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



def test_get_stuck_behind(game_3chevaux):
    game_3chevaux.board[0] = [ 1, 
                1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_3chevaux.get_valid_actions(0, 1) == [[], [Action.MOVE_FORWARD], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 2) == [[], [Action.MOVE_FORWARD], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 3) == [[], [Action.MOVE_FORWARD], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 4) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 5) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 6) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    game_3chevaux.board[1] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 1,
                0]
    assert game_3chevaux.get_valid_actions(0, 1) == [[], [Action.KILL], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 2) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 3) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 4) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 5) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    assert game_3chevaux.get_valid_actions(0, 6) == [[], [Action.GET_STUCK_BEHIND], [Action.MOVE_FORWARD], False]
    
    assert game_3chevaux.get_valid_actions(1, 1) == [[], [Action.MOVE_FORWARD], [Action.REACH_GOAL], False]
    assert game_3chevaux.get_valid_actions(1, 2) == [[], [Action.MOVE_FORWARD], [Action.REACH_GOAL], False]
    assert game_3chevaux.get_valid_actions(1, 3) == [[], [Action.KILL], [Action.REACH_GOAL], False]
    assert game_3chevaux.get_valid_actions(1, 4) == [[], [Action.GET_STUCK_BEHIND], [Action.REACH_GOAL], False]
    assert game_3chevaux.get_valid_actions(1, 5) == [[], [Action.GET_STUCK_BEHIND], [Action.REACH_GOAL], False]
    assert game_3chevaux.get_valid_actions(1, 6) == [[Action.MOVE_OUT], [Action.GET_STUCK_BEHIND], [Action.REACH_GOAL], False]
    