from game_logic import GameLogic, Action, State

# initie un game logic
game = GameLogic()
game.init_board()
game.print_board_overview()
print()
print("joueur 0 fait un 6 et sort un pion")
game.move_pawn(0, 0, 6, Action.MOVE_OUT)
game.print_board_overview()
print()
print("joueur 1 fait un 6 et sort un pion")
game.move_pawn(1, 0, 6, Action.MOVE_OUT)
game.print_board_overview()
print()
print("avance de 30 cases pion 0 pour voir où il se situe")
game.move_pawn(0, 0, 30, Action.MOVE_FORWARD)
game.print_board_overview()