import pytest
from ludo_env import GameLogic, Action_EXACT


@pytest.fixture
def game_2chevaux_exact():
    return  GameLogic(num_players=2, nb_chevaux=2, mode_pied_escalier="exact")


def test_valid_actions_exact(game_2chevaux_exact):
    game_2chevaux_exact.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact.get_valid_actions(0, 1) == [ [], [Action_EXACT.REACH_PIED_ESCALIER] ,False] 
    assert game_2chevaux_exact.get_valid_actions(0, 2) == [ [], [] ,Action_EXACT.NO_ACTION]  
    assert game_2chevaux_exact.get_valid_actions(0, 3) == [ [], [] , Action_EXACT.NO_ACTION]  
    assert game_2chevaux_exact.get_valid_actions(0, 4) == [ [], [] , Action_EXACT.NO_ACTION] 
    assert game_2chevaux_exact.get_valid_actions(0, 5) == [ [], [] , Action_EXACT.NO_ACTION]  
    assert game_2chevaux_exact.get_valid_actions(0, 6) == [ [Action_EXACT.MOVE_OUT], [] ,False]  

    game_2chevaux_exact.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact.get_valid_actions(0, 1) == [ [], [Action_EXACT.MOVE_FORWARD] ,False]  
    assert game_2chevaux_exact.get_valid_actions(0, 2) == [ [], [Action_EXACT.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact.get_valid_actions(0, 3) == [ [], [Action_EXACT.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact.get_valid_actions(0, 4) == [ [], [Action_EXACT.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact.get_valid_actions(0, 5) == [ [], [Action_EXACT.MOVE_FORWARD] ,False]   
    assert game_2chevaux_exact.get_valid_actions(0, 6) ==  [ [Action_EXACT.MOVE_OUT], [Action_EXACT.REACH_PIED_ESCALIER] ,False]   

    # bloquer un pion adverse sur case 56
    game_2chevaux_exact.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact.board[1] = [ 1, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact.get_valid_actions(0, 1) ==   [ [], [Action_EXACT.KILL ] ,False]  
    assert game_2chevaux_exact.get_valid_actions(0, 2) == [ [], [], Action_EXACT.NO_ACTION]    
    assert game_2chevaux_exact.get_valid_actions(0, 3) == [ [], [], Action_EXACT.NO_ACTION]     
    assert game_2chevaux_exact.get_valid_actions(0, 4) == [ [], [], Action_EXACT.NO_ACTION]     
    assert game_2chevaux_exact.get_valid_actions(0, 5) == [ [], [], Action_EXACT.NO_ACTION]     
    assert game_2chevaux_exact.get_valid_actions(0, 6) == [ [Action_EXACT.MOVE_OUT], [], False]     

    # bloquer un pion adverse sur case avant 56 
    game_2chevaux_exact.board[0] = [ 1, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact.board[1] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact.get_valid_actions(0, 1) == [ [], [Action_EXACT.MOVE_FORWARD], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 2) == [ [], [Action_EXACT.KILL], False]  
    assert game_2chevaux_exact.get_valid_actions(0, 3) == [ [], [Action_EXACT.GET_STUCK_BEHIND], False]    
    assert game_2chevaux_exact.get_valid_actions(0, 4) == [ [], [Action_EXACT.GET_STUCK_BEHIND], False]  
    assert game_2chevaux_exact.get_valid_actions(0, 5) == [ [], [Action_EXACT.GET_STUCK_BEHIND], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 6) == [ [Action_EXACT.MOVE_OUT_AND_KILL], [Action_EXACT.GET_STUCK_BEHIND], False]   

    # se bloquer un pion avant case 56 
    game_2chevaux_exact.board[0] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    game_2chevaux_exact.board[1] = [ 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                0, 0, 0, 0, 0, 0,
                0]
    assert game_2chevaux_exact.get_valid_actions(0, 1) == [ [Action_EXACT.MOVE_FORWARD], [Action_EXACT.MOVE_FORWARD], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 2) == [ [Action_EXACT.MOVE_FORWARD], [Action_EXACT.REACH_PIED_ESCALIER], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 3) == [ [Action_EXACT.GET_STUCK_BEHIND], [Action_EXACT.AVANCE_RECULE_PIED_ESCALIER], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 4) == [ [Action_EXACT.GET_STUCK_BEHIND], [], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 5) == [ [Action_EXACT.GET_STUCK_BEHIND], [], False]   
    assert game_2chevaux_exact.get_valid_actions(0, 6) == [ [Action_EXACT.GET_STUCK_BEHIND], [],False]   

def test_exact_escalier(game_2chevaux_exact):
    pass 
    # TODOTEST


@pytest.fixture
def game_3chevaux_exact():
    return GameLogic(num_players=2, nb_chevaux=3, mode_pied_escalier="exact")


@pytest.fixture
def game_4chevaux_exact():
    return GameLogic(num_players=2, nb_chevaux=4, mode_pied_escalier="exact")




# def test_get_valid_actions(game_4chevaux_exact):
#     game_4chevaux_exact.board[0] = [ 0,
#                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#                 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 
#                 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 
#                 0, 0, 0, 0, 0, 0,
#                 0]
#     print(game_4chevaux_exact.get_valid_actions(0, 1))
#     assert game_4chevaux_exact.get_valid_actions(0, 1) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact.get_valid_actions(0, 2) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact.get_valid_actions(0, 3) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact.get_valid_actions(0, 4) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact.get_valid_actions(0, 5) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
#     assert game_4chevaux_exact.get_valid_actions(0, 6) == [[Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_FORWARD], 
#                                                      [Action_EXACT_REQUIRED.MOVE_IN_SAFE_ZONE], 
#                                                      False]
    
    
