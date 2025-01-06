import pytest
from game.ludo_env import GameLogic, Action_NO_EXACT


@pytest.fixture
def game_logic():
    return GameLogic(num_players=2, nb_chevaux=2)


def test_kill_on_exit_action_with_opponent(game_logic):
    # Placement d'un pion du joueur 1 sur la case de sortie du joueur 0
    game_logic.board[1][29] = 1
    game_logic.board[1][0] -= 1

    valid_actions = game_logic.get_valid_actions(player_id=0, dice_value=6)
    print(valid_actions)

    # Vérifie que KILL est possible et MOVE_OUT non
    assert valid_actions == [
        [Action_NO_EXACT.MOVE_OUT_AND_KILL],
        [Action_NO_EXACT.MOVE_OUT_AND_KILL],
        False,
    ]

    # Exécute l'action KILL
    game_logic.sortir_pion(player_id=0, dice_value=6)

    # Vérifications après l'action KILL
    assert game_logic.board[1][0] == 2  # L'adversaire retourne à l'écurie
    assert game_logic.board[1][29] == 0  # La case de sortie est libérée
    assert game_logic.board[0][1] == 1  # Le pion du joueur 0 avance sur la case 1
    assert game_logic.board[0][0] == 1  # Un pion reste dans l'écurie


def test_move_out_action_without_opponent(game_logic):
    dice_value = 6
    valid_actions = game_logic.get_valid_actions(player_id=0, dice_value=dice_value)

    # Vérifie que MOVE_OUT est possible et KILL non
    assert Action_NO_EXACT.MOVE_OUT in valid_actions[0]
    assert Action_NO_EXACT.KILL not in valid_actions[0]

    # Exécute l'action MOVE_OUT
    game_logic.sortir_pion(player_id=0, dice_value=dice_value)

    # Vérifications après l'action MOVE_OUT
    assert game_logic.board[0][1] == 1  # Le pion du joueur 0 avance sur la case 1
    assert game_logic.board[0][0] == 1  # Un pion reste dans l'écurie


def test_kill_action(game_logic):
    # Placement des pions sur le plateau
    game_logic.board[0][5 + 2 * 14] = 1
    game_logic.board[0][0] -= 1
    game_logic.board[1][10] = 1
    game_logic.board[1][0] -= 1

    dice_value = 5

    # Vérifie les positions initiales
    assert game_logic.board[0][5 + 2 * 14] == 1
    assert game_logic.board[1][10] == 1

    # Déplacement du pion du joueur 0 pour tuer celui du joueur 1
    game_logic.move_pawn(
        player_id=0,
        old_position=5 + 2 * 14,
        dice_value=dice_value,
        action=Action_NO_EXACT.KILL,
    )

    # Vérifie les positions après l'action
    expected_position = 10 + 2 * 14  # Nouvelle position du pion 0
    assert game_logic.board[0][expected_position] == 1
    assert game_logic.board[0][5 + 2 * 14] == 0
    assert game_logic.board[1][0] == 2  # Le pion 1 retourne à l'écurie
    assert game_logic.board[1][10] == 0

    # Vérifie que le pion 0 est bien à la nouvelle position
    pawns_info = game_logic.get_pawns_info(0)
    pawn_positions = [pawn["position"] for pawn in pawns_info]
    assert expected_position in pawn_positions

    # Vérifie le total des pions sur le plateau
    assert sum(game_logic.board[0]) == 2
    assert sum(game_logic.board[1]) == 2
