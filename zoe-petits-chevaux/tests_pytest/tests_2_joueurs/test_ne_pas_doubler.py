import pytest
from ludo_env import LudoEnv, GameLogic,  Action

@pytest.fixture
def setup_env():
    return LudoEnv(num_players=2, nb_chevaux=2)

@pytest.fixture
def game_4chevaux():
    game = GameLogic(num_players=2, nb_chevaux=4)
    game.board[0] = [ 0, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                1, 0, 0, 0, 0, 0,
                0]
    game.board[1] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                1, 0, 0, 0, 0, 0,
                0]
    return game

def test_not_double_me_basic(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] = 0
    env.game.board[0][4] = 1
    env.game.board[0][6] = 1

    print(env.game.board)
    env.dice_roll = 5

    action = env.game.encode_action(0, Action.MOVE_FORWARD)
    env.step(action)

    print(env.game.board)
   
    assert env.game.board[0][9] == 0, "Le pion devrait être bloqué avant la case occupée."
    assert env.game.board[0][3] == 1, "Le pion devrait avoir reculé du nombre de dé restant."

def test_not_double_opponent_basic(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 1
    env.game.board[0][4] = 1
    pos = env.game.get_relative_position(1, 0, 6)
    env.game.board[1][pos] = 1

    env.dice_roll = 5

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][9] == 0, "Le pion devrait être bloqué avant la case occupée par un pion adverse."
    assert env.game.board[0][3] == 1, "Le pion devrait avoir reculé du nombre de dé restant."

def test_blocked_near_escalier_NORMAL_FAILED(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 2
    env.game.board[0][54] = 1
    env.game.board[0][56] = 1

    env.dice_roll = 3

    action = env.game.encode_action(0, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][57] == 0, "Le pion devrait être bloqué avant l'escalier."
    assert env.game.board[0][55] == 1, "Le pion devrait avoir reculé correctement."

def test_multiple_blocking_pawns(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 2
    env.game.board[0][4] = 1
    pos_1 = env.game.get_relative_position(1, 0, 6)
    pos_2 = env.game.get_relative_position(1, 0, 7)
    env.game.board[1][pos_1] = 1
    env.game.board[1][pos_2] = 1 

    env.dice_roll = 5

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][8] == 0, "Le pion devrait être bloqué par le premier pion adverse."
    assert env.game.board[0][3] == 1, "Le pion devrait avoir reculé du nombre de dé restant."


def test_jump_and_hit_second_opponent(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 2
    env.game.board[0][4] = 1
    pos_1 = env.game.get_relative_position(1, 0, 6)
    pos_2 = env.game.get_relative_position(1, 0, 7)
    env.game.board[1][pos_1] = 1
    env.game.board[1][pos_2] = 1

    env.dice_roll = 3

    print(env.game.board)

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    print(env.game.board)

    assert env.game.board[0][7] == 0, "Le pion ne devrait pas aller au-delà du premier pion adverse."
    assert env.game.board[0][5] == 1, "Le pion devrait reculer dès le premier pion adverse bloquant."

def test_recoil_stops_at_start(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 1
    env.game.board[0][2] = 1
    pos_1 = env.game.get_relative_position(1, 0, 4)
    env.game.board[1][pos_1] = 1

    env.dice_roll = 6

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][1] == 1, "Le pion doit s'arrêter à la case 1."
    assert env.game.board[0][2] == 0, "Le pion doit quitter sa position initiale."

def test_recoil_me_behind(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 2
    env.game.board[1][0] -= 1
    env.game.board[0][10] = 1
    env.game.board[0][8] = 1
    pos_1 = env.game.get_relative_position(1, 0, 12)
    env.game.board[1][pos_1] = 1

    env.dice_roll = 7

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][15] == 0, "Le pion ne doit pas doubler le joueur devant lui."
    assert env.game.board[0][7] == 0, "Le pion ne doit pas reculer plus loin que le joueur derrière lui."
    assert env.game.board[0][9] == 1, "Le joueur ne s'est pas arrêté avant le joueur."

def test_recoil_between_two_players_with_opponent_behind(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 2
    env.game.board[0][10] = 1

    pos_behind = env.game.get_relative_position(1, 0, 8)
    env.game.board[1][pos_behind] = 1

    pos_front = env.game.get_relative_position(1, 0, 12)
    env.game.board[1][pos_front] = 1

    env.dice_roll = 7

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][15] == 0, "Le pion ne doit pas doubler le joueur devant lui."
    assert env.game.board[0][7] == 0, "Le pion ne doit pas reculer plus loin que le joueur derrière lui."
    assert env.game.board[0][9] == 1, "Le joueur ne s'est pas arrêté avant le joueur."


def test_recoil_me_behind_on_me(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 2
    env.game.board[1][0] -= 1
    env.game.board[0][10] = 1
    env.game.board[0][8] = 1
    pos_1 = env.game.get_relative_position(1, 0, 12)
    env.game.board[1][pos_1] = 1

    env.dice_roll = 6

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][15] == 0, "Le pion ne doit pas doubler le joueur devant lui."
    assert env.game.board[0][7] == 0, "Le pion ne doit pas s'arrêter sur le joueur derrière lui."
    assert env.game.board[0][9] == 1, "Le joueur ne s'est pas arrêté avant le joueur."

def test_recoil_between_two_players_with_opponent_behind_on_opponent(setup_env):
    env = setup_env
    env.reset()

    env.game.board[0][0] -= 1
    env.game.board[1][0] -= 2
    env.game.board[0][10] = 1

    pos_behind = env.game.get_relative_position(1, 0, 8)
    env.game.board[1][pos_behind] = 1

    pos_front = env.game.get_relative_position(1, 0, 12)
    env.game.board[1][pos_front] = 1

    env.dice_roll =6

    action = env.game.encode_action(1, Action.MOVE_FORWARD)
    env.step(action)

    assert env.game.board[0][15] == 0, "Le pion ne doit pas doubler le joueur devant lui."
    assert env.game.board[0][7] == 0, "Le pion ne doit pas s'arrêter sur le joueur derrière lui."
    assert env.game.board[0][9] == 1, "Le joueur ne s'est pas arrêté avant le joueur."



def test_no_overtake_8(game_4chevaux):
    assert game_4chevaux.get_valid_actions(0, 1) == [[Action.MOVE_FORWARD], [Action.MOVE_FORWARD], [Action.KILL], [Action.MOVE_IN_SAFE_ZONE], False]
    assert game_4chevaux.get_valid_actions(1, 1) == [[], [Action.KILL], [Action.ENTER_SAFEZONE], [Action.MOVE_IN_SAFE_ZONE], False]
    
    # assert game_4chevaux.get_valid_actions(0, 2) == [[Action.MOVE_FORWARD], [Action.MOVE_FORWARD], [Action.KILL], [Action.MOVE FORWARD ET BACKWARD NON ?], False]
    # TODO
    
    game_4chevaux.avance_pion_path(1, 28, 2)
    assert game_4chevaux.board[1][28] == 1