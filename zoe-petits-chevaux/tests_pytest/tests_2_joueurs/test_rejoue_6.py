import pytest

from ludo_env import LudoEnv

@pytest.fixture
def env_pas_rejoue():
    return LudoEnv(num_players=2, nb_chevaux=4, mode_gym="jeu", mode_fin_partie="tous")

@pytest.fixture
def env_rejoue():
    return LudoEnv(num_players=2, nb_chevaux=4, mode_gym="jeu", mode_fin_partie="tous", mode_rejoue_6="oui")

def test_rejoue_6(env_pas_rejoue, env_rejoue):
    env_pas_rejoue.dice_roll = 2
    env_rejoue.dice_roll = 2

    assert env_pas_rejoue.current_player == 0
    assert env_rejoue.current_player == 0

    env_pas_rejoue.step(0)
    env_rejoue.step(0)

    assert env_pas_rejoue.current_player == 1
    assert env_rejoue.current_player == 1

    env_pas_rejoue.dice_roll = 6
    env_rejoue.dice_roll = 6

    env_pas_rejoue.step(1)
    env_rejoue.step(1)

    assert env_pas_rejoue.current_player == 0
    assert env_rejoue.current_player == 1




