# import pytest
# from ludo_env import GameLogic, Action
# ## TODOTEST


# @pytest.fixture
# def game_2chevaux():
#     return GameLogic(num_players=3, nb_chevaux=2)


# @pytest.fixture
# def game_3chevaux():
#     return GameLogic(num_players=3, nb_chevaux=3)


# @pytest.fixture
# def game_4chevaux():
#     game = GameLogic(num_players=3, nb_chevaux=4)
#     game.board[0] = [ 2,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0,
#                 0]
#     game.board[1] = [ 4,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0,
#                 0]
#     game.board[2] = [ 3,
#                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 0,
#                 0]
#     return game


# def test_get_relative_position_0(game_4chevaux):
#     assert game_4chevaux.get_relative_position(0, 1, 15) == 1
#     assert game_4chevaux.get_relative_position(0, 1, 28) == 14
#     assert game_4chevaux.get_relative_position(0, 1, 42) == 28
#     assert game_4chevaux.get_relative_position(0, 1, 56) == 42
#     assert game_4chevaux.get_relative_position(0, 1, 14) == 56

#     assert game_4chevaux.get_relative_position(0, 2, 1) == 29
#     assert game_4chevaux.get_relative_position(0, 2, 28) == 56
#     assert game_4chevaux.get_relative_position(0, 2, 29) == 1
#     assert game_4chevaux.get_relative_position(0, 2, 42) == 14
#     assert game_4chevaux.get_relative_position(0, 2, 56) == 28

#     # assert game_4chevaux.get_relative_position(0, 3, 1) == 15
#     # assert game_4chevaux.get_relative_position(0, 3, 15) == 29
#     # assert game_4chevaux.get_relative_position(0, 3, 28) == 42
#     # assert game_4chevaux.get_relative_position(0, 3, 29) == 43
#     # assert game_4chevaux.get_relative_position(0, 3, 42) == 56
#     # assert game_4chevaux.get_relative_position(0, 3, 56) == 14

# def test_get_relative_position_1(game_4chevaux):
#     assert game_4chevaux.get_relative_position(1, 0, 1) == 15
#     assert game_4chevaux.get_relative_position(1, 0, 14) == 28
#     assert game_4chevaux.get_relative_position(1, 0, 15) == 29
#     assert game_4chevaux.get_relative_position(1, 0, 56) == 14

#     assert game_4chevaux.get_relative_position(1, 2, 1) == 43
#     assert game_4chevaux.get_relative_position(1, 2, 14) == 56
#     assert game_4chevaux.get_relative_position(1, 2, 15) == 1
#     assert game_4chevaux.get_relative_position(1, 2, 56) == 42

# def test_get_relative_position_2(game_4chevaux):
#     assert game_4chevaux.get_relative_position(2, 0, 1) == 29
#     assert game_4chevaux.get_relative_position(2, 0, 14) == 42
#     assert game_4chevaux.get_relative_position(2, 0, 15) == 43
#     assert game_4chevaux.get_relative_position(2, 0, 56) == 28

#     assert game_4chevaux.get_relative_position(2, 1, 1) == 15
#     assert game_4chevaux.get_relative_position(2, 1, 14) == 28
#     assert game_4chevaux.get_relative_position(2, 1, 15) == 29
#     assert game_4chevaux.get_relative_position(2, 1, 56) == 14


# def test_is_opponent_pawn_on(game_4chevaux):
#     assert game_4chevaux.is_opponent_pawn_on(0, 14) == False
#     assert game_4chevaux.get_valid_actions(0, 1) == [[], [], [Action.MOVE_FORWARD], [Action.MOVE_FORWARD], False]
