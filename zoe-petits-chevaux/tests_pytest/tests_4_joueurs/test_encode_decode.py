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



def test_decode_2chevaux(game_2chevaux):
    assert game_2chevaux.decode_action(0) == (0, Action.NO_ACTION)
    assert game_2chevaux.decode_action(1) == (0, Action.MOVE_OUT)
    assert game_2chevaux.decode_action(2) == (0, Action.MOVE_FORWARD)
    assert game_2chevaux.decode_action(3) == (0, Action.ENTER_SAFEZONE)
    assert game_2chevaux.decode_action(4) == (0, Action.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.decode_action(5) == (0, Action.REACH_GOAL)
    assert game_2chevaux.decode_action(6) == (0, Action.KILL)
    assert game_2chevaux.decode_action(7) == (1, Action.MOVE_FORWARD)
    assert game_2chevaux.decode_action(8) == (1, Action.ENTER_SAFEZONE)
    assert game_2chevaux.decode_action(9) == (1, Action.MOVE_IN_SAFE_ZONE)
    assert game_2chevaux.decode_action(10) == (1, Action.REACH_GOAL)
    assert game_2chevaux.decode_action(11) == (1, Action.KILL)


def test_decode_3chevaux(game_3chevaux):
    assert game_3chevaux.decode_action(0) == (0, Action.NO_ACTION)
    assert game_3chevaux.decode_action(1) == (0, Action.MOVE_OUT)
    assert game_3chevaux.decode_action(2) == (0, Action.MOVE_FORWARD)
    assert game_3chevaux.decode_action(3) == (0, Action.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(4) == (0, Action.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(5) == (0, Action.REACH_GOAL)
    assert game_3chevaux.decode_action(6) == (0, Action.KILL)
    assert game_3chevaux.decode_action(7) == (1, Action.MOVE_FORWARD)
    assert game_3chevaux.decode_action(8) == (1, Action.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(9) == (1, Action.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(10) == (1, Action.REACH_GOAL)
    assert game_3chevaux.decode_action(11) == (1, Action.KILL)
    assert game_3chevaux.decode_action(12) == (2, Action.MOVE_FORWARD)
    assert game_3chevaux.decode_action(13) == (2, Action.ENTER_SAFEZONE)
    assert game_3chevaux.decode_action(14) == (2, Action.MOVE_IN_SAFE_ZONE)
    assert game_3chevaux.decode_action(15) == (2, Action.REACH_GOAL)
    assert game_3chevaux.decode_action(16) == (2, Action.KILL)

def test_decode_4chevaux(game_4chevaux):
    assert game_4chevaux.decode_action(0) == (0, Action.NO_ACTION)
    assert game_4chevaux.decode_action(1) == (0, Action.MOVE_OUT)
    assert game_4chevaux.decode_action(2) == (0, Action.MOVE_FORWARD)
    assert game_4chevaux.decode_action(3) == (0, Action.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(4) == (0, Action.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(5) == (0, Action.REACH_GOAL)
    assert game_4chevaux.decode_action(6) == (0, Action.KILL)
    assert game_4chevaux.decode_action(7) == (1, Action.MOVE_FORWARD)
    assert game_4chevaux.decode_action(8) == (1, Action.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(9) == (1, Action.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(10) == (1, Action.REACH_GOAL)
    assert game_4chevaux.decode_action(11) == (1, Action.KILL)
    assert game_4chevaux.decode_action(12) == (2, Action.MOVE_FORWARD)
    assert game_4chevaux.decode_action(13) == (2, Action.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(14) == (2, Action.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(15) == (2, Action.REACH_GOAL)
    assert game_4chevaux.decode_action(16) == (2, Action.KILL)
    assert game_4chevaux.decode_action(17) == (3, Action.MOVE_FORWARD)
    assert game_4chevaux.decode_action(18) == (3, Action.ENTER_SAFEZONE)
    assert game_4chevaux.decode_action(19) == (3, Action.MOVE_IN_SAFE_ZONE)
    assert game_4chevaux.decode_action(20) == (3, Action.REACH_GOAL)


def test_encode_2chevaux(game_2chevaux):
    assert 0 == game_2chevaux.encode_action(0, Action.NO_ACTION)
    assert 1 == game_2chevaux.encode_action(0, Action.MOVE_OUT)
    assert 2 == game_2chevaux.encode_action(0, Action.MOVE_FORWARD)
    assert 3 == game_2chevaux.encode_action(0, Action.ENTER_SAFEZONE)
    assert 4 == game_2chevaux.encode_action(0, Action.MOVE_IN_SAFE_ZONE)
    assert 5 == game_2chevaux.encode_action(0, Action.REACH_GOAL)
    assert 6 == game_2chevaux.encode_action(0, Action.KILL)
    assert 7 == game_2chevaux.encode_action(1, Action.MOVE_FORWARD)
    assert 8 == game_2chevaux.encode_action(1, Action.ENTER_SAFEZONE)
    assert 9 == game_2chevaux.encode_action(1, Action.MOVE_IN_SAFE_ZONE)
    assert 10 == game_2chevaux.encode_action(1, Action.REACH_GOAL)
    assert 11 == game_2chevaux.encode_action(1, Action.KILL)

def test_encode_3chevaux(game_3chevaux):
    assert 0 == game_3chevaux.encode_action(0, Action.NO_ACTION)
    assert 1 == game_3chevaux.encode_action(0, Action.MOVE_OUT)
    assert 2 == game_3chevaux.encode_action(0, Action.MOVE_FORWARD)
    assert 3 == game_3chevaux.encode_action(0, Action.ENTER_SAFEZONE)
    assert 4 == game_3chevaux.encode_action(0, Action.MOVE_IN_SAFE_ZONE)
    assert 5 == game_3chevaux.encode_action(0, Action.REACH_GOAL)
    assert 6 == game_3chevaux.encode_action(0, Action.KILL)
    assert 7 == game_3chevaux.encode_action(1, Action.MOVE_FORWARD)
    assert 8 == game_3chevaux.encode_action(1, Action.ENTER_SAFEZONE)
    assert 9 == game_3chevaux.encode_action(1, Action.MOVE_IN_SAFE_ZONE)
    assert 10 == game_3chevaux.encode_action(1, Action.REACH_GOAL)
    assert 11 == game_3chevaux.encode_action(1, Action.KILL)
    assert 12 == game_3chevaux.encode_action(2, Action.MOVE_FORWARD)
    assert 13 == game_3chevaux.encode_action(2, Action.ENTER_SAFEZONE)
    assert 14 == game_3chevaux.encode_action(2, Action.MOVE_IN_SAFE_ZONE)
    assert 15 == game_3chevaux.encode_action(2, Action.REACH_GOAL)
    assert 16 == game_3chevaux.encode_action(2, Action.KILL)

def test_encode_4chevaux(game_4chevaux):
    assert 0 == game_4chevaux.encode_action(0, Action.NO_ACTION)
    assert 1 == game_4chevaux.encode_action(0, Action.MOVE_OUT)
    assert 2 == game_4chevaux.encode_action(0, Action.MOVE_FORWARD)
    assert 3 == game_4chevaux.encode_action(0, Action.ENTER_SAFEZONE)
    assert 4 == game_4chevaux.encode_action(0, Action.MOVE_IN_SAFE_ZONE)
    assert 5 == game_4chevaux.encode_action(0, Action.REACH_GOAL)
    assert 6 == game_4chevaux.encode_action(0, Action.KILL)
    assert 7 == game_4chevaux.encode_action(1, Action.MOVE_FORWARD)
    assert 8 == game_4chevaux.encode_action(1, Action.ENTER_SAFEZONE)
    assert 9 == game_4chevaux.encode_action(1, Action.MOVE_IN_SAFE_ZONE)
    assert 10 == game_4chevaux.encode_action(1, Action.REACH_GOAL)
    assert 11 == game_4chevaux.encode_action(1, Action.KILL)
    assert 12 == game_4chevaux.encode_action(2, Action.MOVE_FORWARD)
    assert 13 == game_4chevaux.encode_action(2, Action.ENTER_SAFEZONE)
    assert 14 == game_4chevaux.encode_action(2, Action.MOVE_IN_SAFE_ZONE)
    assert 15 == game_4chevaux.encode_action(2, Action.REACH_GOAL)
    assert 16 == game_4chevaux.encode_action(2, Action.KILL)
    assert 17 == game_4chevaux.encode_action(3, Action.MOVE_FORWARD)
    assert 18 == game_4chevaux.encode_action(3, Action.ENTER_SAFEZONE)
    assert 19 == game_4chevaux.encode_action(3, Action.MOVE_IN_SAFE_ZONE)
    assert 20 == game_4chevaux.encode_action(3, Action.REACH_GOAL)
    assert 21 == game_4chevaux.encode_action(3, Action.KILL)