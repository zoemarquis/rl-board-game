import pytest 
from ludo_env import GameLogic, Action_EXACT, Action_NO_EXACT, Action_EXACT_ASCENSION



@pytest.fixture
def game_2chevaux():
    return GameLogic(num_players=2, nb_chevaux=2, mode_protect="activé")


@pytest.fixture
def game_2chevaux_exact():
    return GameLogic(num_players=2, nb_chevaux=2,  mode_pied_escalier="exact", mode_protect="activé")


@pytest.fixture
def game_2chevaux_ascension():
    return GameLogic(num_players=2, nb_chevaux=2,  mode_pied_escalier="exact", mode_ascension="avec_contrainte", mode_protect="activé")



def test_basique_move_out_and_kill(game_2chevaux):
    game_2chevaux.board[0] = [ 1,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              1, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                                0, 0, 0, 0, 0 ,0,
                                0
    ]
    assert game_2chevaux.get_valid_actions(1, 6) == [
        [Action_NO_EXACT.MOVE_OUT_AND_KILL],
        [Action_NO_EXACT.MOVE_OUT_AND_KILL],
        False
    ]
    game_2chevaux.board[0][0]=0
    game_2chevaux.board[0][29]=2
    assert game_2chevaux.get_valid_actions(1, 6) == [
        [],
        [],
        Action_NO_EXACT.NO_ACTION
    ]


def test_exact_move_out_and_kill(game_2chevaux_exact):
    game_2chevaux_exact.board[0] = [ 1,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              1, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                                0, 0, 0, 0, 0 ,0,
                                0
    ]
    assert game_2chevaux_exact.get_valid_actions(1, 6) == [
        [Action_EXACT.MOVE_OUT_AND_KILL],
        [Action_EXACT.MOVE_OUT_AND_KILL],
        False
    ]
    game_2chevaux_exact.board[0][0]=0
    game_2chevaux_exact.board[0][29]=2
    assert game_2chevaux_exact.get_valid_actions(1, 6) == [
        [],
        [],
        Action_EXACT.NO_ACTION
    ]

def test_ascension_move_out_and_kill(game_2chevaux_ascension):
    game_2chevaux_ascension.board[0] = [ 1,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              1, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                              0, 0, 0, 0, 0 ,0, 0,0, 0, 0, 0, 0 ,0, 0,
                                0, 0, 0, 0, 0 ,0,
                                0
    ]
    print(game_2chevaux_ascension.get_str_game_overview())
    print(game_2chevaux_ascension.get_valid_actions(1, 6))
    assert game_2chevaux_ascension.get_valid_actions(1, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL],
        [Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL],
        False
    ]
    game_2chevaux_ascension.board[0][0]=0
    game_2chevaux_ascension.board[0][29]=2
    assert game_2chevaux_ascension.get_valid_actions(1, 6) == [
        [],
        [],
        Action_EXACT_ASCENSION.NO_ACTION
    ]