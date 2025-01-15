import pytest

from game.ludo_env import LudoEnv, Action_EXACT_ASCENSION, Action_NO_EXACT


@pytest.fixture
def env_pas_rejoue():
    return LudoEnv(num_players=2, nb_chevaux=4, mode_gym="jeu", mode_fin_partie="un",
                    mode_rejoue_6="non", mode_rejoue_marche="non")


@pytest.fixture
def env_rejoue():
    return LudoEnv(
        num_players=2,
        nb_chevaux=4,
        mode_gym="jeu",
        mode_fin_partie="un",
        mode_rejoue_6="non",
        mode_rejoue_marche="oui",
        mode_ascension="avec_contrainte",
        mode_pied_escalier="exact"
    )

@pytest.fixture
def env_rejoue_6():
    return LudoEnv(
        num_players=2,
        nb_chevaux=4,
        mode_gym="jeu",
        mode_fin_partie="un",
        mode_rejoue_6="oui",
        mode_rejoue_marche="oui",
        mode_ascension="avec_contrainte",
        mode_pied_escalier="exact"
    )


def test_rejoue(env_pas_rejoue, env_rejoue, env_rejoue_6):
    env_pas_rejoue.dice_roll = 2
    env_rejoue.dice_roll = 2
    env_rejoue_6.dice_roll = 2

    assert env_pas_rejoue.current_player == 0
    assert env_rejoue.current_player == 0
    assert env_rejoue_6.current_player == 0

    env_pas_rejoue.step(0)
    env_rejoue.step(0)
    env_rejoue_6.step(0)

    assert env_pas_rejoue.current_player == 1
    assert env_rejoue.current_player == 1
    assert env_rejoue_6.current_player == 1

    env_pas_rejoue.dice_roll = 6
    env_rejoue.dice_roll = 6
    env_rejoue_6.dice_roll = 6

    env_pas_rejoue.step(1)
    env_rejoue.step(1)
    env_rejoue_6.step(1)

    assert env_pas_rejoue.current_player == 0
    assert env_rejoue.current_player == 0
    assert env_rejoue_6.current_player == 1

    env_pas_rejoue.game.board[0][0] = 3
    env_rejoue.game.board[0][0] = 3
    env_rejoue_6.game.board[0][0] = 3

    env_pas_rejoue.game.board[0][56] = 1
    env_rejoue.game.board[0][56] = 1
    env_rejoue_6.game.board[0][56] = 1

    env_pas_rejoue.current_player = 0
    env_rejoue.current_player = 0
    env_rejoue_6.current_player = 0

    assert env_rejoue.game.get_valid_actions(0, 6) == [[Action_EXACT_ASCENSION.MOVE_OUT], [Action_EXACT_ASCENSION.MOVE_OUT], [Action_EXACT_ASCENSION.MOVE_OUT], [], False]
    assert env_rejoue_6.game.get_valid_actions(0, 6) == [[Action_EXACT_ASCENSION.MOVE_OUT], [Action_EXACT_ASCENSION.MOVE_OUT], [Action_EXACT_ASCENSION.MOVE_OUT], [], False]

    assert env_rejoue.game.get_valid_actions(0, 1) == [[], [], [], [Action_EXACT_ASCENSION.MARCHE_1], False]
    assert env_rejoue_6.game.get_valid_actions(0, 1) == [[], [], [], [Action_EXACT_ASCENSION.MARCHE_1], False]

    env_rejoue.dice_roll = 1
    env_rejoue_6.dice_roll = 1

    env_rejoue.step(44)
    env_rejoue_6.step(44)

    assert env_rejoue.current_player == 0
    assert env_rejoue_6.current_player == 0


