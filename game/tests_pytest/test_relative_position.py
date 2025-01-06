import pytest
from game.ludo_env import GameLogic


@pytest.fixture
def jeu_2_joueurs():
    return GameLogic(num_players=2, nb_chevaux=2)


@pytest.fixture
def jeu_3_joueurs():
    return GameLogic(num_players=3, nb_chevaux=2)


@pytest.fixture
def jeu_4_joueurs():
    return GameLogic(num_players=4, nb_chevaux=2)


def test_get_relative_position_2_players(jeu_2_joueurs):
    assert jeu_2_joueurs.get_relative_position(0, 1, 1) == 29
    assert jeu_2_joueurs.get_relative_position(1, 0, 1) == 29


def test_get_relative_position_3_players(jeu_3_joueurs):
    assert jeu_3_joueurs.get_relative_position(0, 1, 1) == 43
    assert jeu_3_joueurs.get_relative_position(1, 0, 1) == 15

    assert jeu_3_joueurs.get_relative_position(0, 2, 1) == 29
    assert jeu_3_joueurs.get_relative_position(2, 0, 1) == 29

    assert jeu_3_joueurs.get_relative_position(1, 2, 1) == 43
    assert jeu_3_joueurs.get_relative_position(2, 1, 1) == 15


def test_get_relative_position_4_players(jeu_4_joueurs):
    assert jeu_4_joueurs.get_relative_position(0, 1, 1) == 43
    assert jeu_4_joueurs.get_relative_position(1, 0, 1) == 15

    assert jeu_4_joueurs.get_relative_position(0, 2, 1) == 29
    assert jeu_4_joueurs.get_relative_position(2, 0, 1) == 29

    assert jeu_4_joueurs.get_relative_position(0, 3, 1) == 15
    assert jeu_4_joueurs.get_relative_position(3, 0, 1) == 43

    assert jeu_4_joueurs.get_relative_position(1, 2, 1) == 43
    assert jeu_4_joueurs.get_relative_position(2, 1, 1) == 15

    assert jeu_4_joueurs.get_relative_position(1, 3, 1) == 29
    assert jeu_4_joueurs.get_relative_position(3, 1, 1) == 29

    assert jeu_4_joueurs.get_relative_position(2, 3, 1) == 43
    assert jeu_4_joueurs.get_relative_position(3, 2, 1) == 15
