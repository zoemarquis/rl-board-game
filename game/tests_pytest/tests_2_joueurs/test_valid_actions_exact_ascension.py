import pytest
from game.ludo_env import GameLogic, Action_EXACT_ASCENSION


@pytest.fixture
def game_2chevaux():
    return GameLogic(
        num_players=2,
        nb_chevaux=2,
        mode_ascension="avec_contrainte",
        mode_pied_escalier="exact",
    )


@pytest.fixture
def game_3chevaux():
    return GameLogic(
        num_players=2,
        nb_chevaux=3,
        mode_ascension="avec_contrainte",
        mode_pied_escalier="exact",
    )


@pytest.fixture
def game_4chevaux():
    return GameLogic(
        num_players=2,
        nb_chevaux=4,
        mode_ascension="avec_contrainte",
        mode_pied_escalier="exact",
    )


def test_valid_actions(game_3chevaux):
    game_3chevaux.board[0] = [
        1,  # ecurie
        1,  # 1
        0,
        0,
        0,
        1,  # 5
        0,
        0,
        0,
        0,
        0,  # 10
        0,
        0,
        0,
        0,
        0,  # 15
        0,
        0,
        0,
        0,
        0,  # 20
        0,
        0,
        0,
        0,
        0,  # 25
        0,
        0,
        0,
        0,
        0,  # 30
        0,
        0,
        0,
        0,
        0,  # 35
        0,
        0,
        0,
        0,
        0,  # 40
        0,
        0,
        0,
        0,
        0,  # 45
        0,
        0,
        0,
        0,
        0,  # 50
        0,
        0,
        0,
        0,
        0,  # 55
        0,  # pied escalier
        0,  # marche 1
        0,  # marche 2
        0,  # marche 3
        0,  # marche 4
        0,  # marche 5
        0,  # marche 6
        0,  # goal
    ]
    assert game_3chevaux.get_valid_actions(0, 1) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 2) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 3) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 4) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 5) == [
        [],
        [Action_EXACT_ASCENSION.GET_STUCK_BEHIND],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [Action_EXACT_ASCENSION.GET_STUCK_BEHIND],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    game_3chevaux.board[1] = [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
    ]
    assert game_3chevaux.get_valid_actions(0, 1) == [
        [],
        [Action_EXACT_ASCENSION.KILL],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 2) == [
        [],
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 3) == [
        [],
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 4) == [
        [],
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 5) == [
        [],
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(0, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 1) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],  # 6 pour atteintdre goal
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 2) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 3) == [
        [],
        [Action_EXACT_ASCENSION.KILL],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 4) == [
        [],
        [Action_EXACT_ASCENSION.GET_STUCK_BEHIND],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 5) == [
        [],
        [Action_EXACT_ASCENSION.GET_STUCK_BEHIND],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [Action_EXACT_ASCENSION.GET_STUCK_BEHIND],
        [Action_EXACT_ASCENSION.REACH_GOAL],
        False,
    ]

    game_3chevaux.board[0] = [
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    game_3chevaux.move_pawn(0, 1, 4, Action_EXACT_ASCENSION.GET_STUCK_BEHIND)
    assert game_3chevaux.board[0] == [
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    game_3chevaux.board[1] = [
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
    ]
    game_3chevaux.move_pawn(1, 30, 6, Action_EXACT_ASCENSION.GET_STUCK_BEHIND)
    game_3chevaux.board[0] = [
        1,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    game_3chevaux.board[1] = [
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert game_3chevaux.get_valid_actions(0, 4) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]

    game_3chevaux.board[0] = [
        2,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    game_3chevaux.board[1] = [
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]
    assert game_3chevaux.get_valid_actions(1, 1) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 2) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.REACH_PIED_ESCALIER],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 3) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 4) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 5) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],
        False,
    ]

    game_3chevaux.board[1] = [
        1,  # ecurie
        0,  # 1
        0,
        0,
        0,
        0,  # 5
        0,
        0,
        0,
        0,
        0,  # 10
        0,
        0,
        0,
        0,
        0,  # 15
        0,
        0,
        0,
        0,
        0,  # 20
        0,
        0,
        0,
        0,
        0,  # 25
        0,
        0,
        0,  # 28
        0,
        0,  # 30
        0,
        0,
        0,
        0,
        0,  # 35
        0,
        0,
        0,
        0,
        0,  # 40
        0,
        0,  # 42
        0,
        0,
        0,  # 45
        0,
        0,
        0,
        0,
        0,  # 50
        0,
        0,
        0,
        1,
        0,  # 55
        1,  # pied ecalier
        0,  # marche 1
        0,  # marche 2
        0,  # marche 3
        0,  # marche 4
        0,  # marche 5
        0,  # marche 6
        0,  # goal
    ]
    assert game_3chevaux.get_valid_actions(1, 1) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [Action_EXACT_ASCENSION.MARCHE_1],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 2) == [
        [],
        [Action_EXACT_ASCENSION.REACH_PIED_ESCALIER],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 3) == [
        [],
        [Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER],  # ou GET STUCK BEHIND ?
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 4) == [
        [],
        [],
        [],
        Action_EXACT_ASCENSION.NO_ACTION,
    ]
    assert game_3chevaux.get_valid_actions(1, 5) == [
        [],
        [],
        [],
        Action_EXACT_ASCENSION.NO_ACTION,
    ]
    assert game_3chevaux.get_valid_actions(1, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [],
        [],
        False,
    ]

    # TODOTEST tuer sur pied escalier
    game_3chevaux.board[1][56] = 0
    game_3chevaux.board[1][57] = 1
    game_3chevaux.board[0] = [
        0,  # ecurie
        0,  # 1
        0,
        0,
        0,
        0,  # 5
        0,
        0,
        0,
        0,
        0,  # 10
        0,
        0,
        0,
        0,
        0,  # 15
        0,
        0,
        0,
        0,
        0,  # 20
        0,
        0,
        0,
        0,
        0,  # 25
        0,
        0,
        1,  # 28
        0,
        0,  # 30
        0,
        0,
        0,
        0,
        0,  # 35
        0,
        0,
        0,
        0,
        0,  # 40
        0,
        0,  # 42
        0,
        0,
        0,  # 45
        0,
        0,
        0,
        0,
        0,  # 50
        0,
        0,
        0,
        1,
        0,  # 55
        1,  # pied ecalier
        0,  # marche 1
        0,  # marche 2
        0,  # marche 3
        0,  # marche 4
        0,  # marche 5
        0,  # marche 6
        0,  # goal
    ]
    assert game_3chevaux.get_valid_actions(1, 1) == [
        [],
        [Action_EXACT_ASCENSION.MOVE_FORWARD],
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 2) == [
        [],
        [Action_EXACT_ASCENSION.KILL],  # ou REACH_PIED_ESCALIER ?
        [Action_EXACT_ASCENSION.MARCHE_2],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 3) == [
        [],
        [Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER],  # ou GET STUCK BEHIND ?
        [],
        False,
    ]
    assert game_3chevaux.get_valid_actions(1, 4) == [
        [],
        [],
        [],
        Action_EXACT_ASCENSION.NO_ACTION,
    ]
    assert game_3chevaux.get_valid_actions(1, 5) == [
        [],
        [],
        [],
        Action_EXACT_ASCENSION.NO_ACTION,
    ]
    assert game_3chevaux.get_valid_actions(1, 6) == [
        [Action_EXACT_ASCENSION.MOVE_OUT],
        [],
        [],
        False,
    ]
