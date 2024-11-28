import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from ludo_env import GameLogic, Action

# initie un game logic
game = GameLogic()
game.init_board()

game.move_pawn(0, 0, 6, Action.MOVE_OUT)
game.move_pawn(1, 0, 6, Action.MOVE_OUT)
game.move_pawn(1, 0, 6, Action.MOVE_OUT)

game.move_pawn(0, 1, 30, Action.MOVE_FORWARD)
game.move_pawn(1, 1, 30, Action.MOVE_FORWARD)

game.move_pawn(0, 31, 25, Action.MOVE_FORWARD)
game.move_pawn(1, 31, 25, Action.MOVE_FORWARD)

game.move_pawn(0, 56, 1, Action.ENTER_SAFEZONE)
game.move_pawn(1, 56, 1, Action.ENTER_SAFEZONE)

game.move_pawn(0, 57, 6, Action.REACH_GOAL)
game.move_pawn(0, 0, 6, Action.MOVE_OUT)
game.move_pawn(0, 1, 55, Action.MOVE_FORWARD)
game.move_pawn(0, 56, 6, Action.ENTER_SAFEZONE)
game.move_pawn(0, 62, 4, Action.REACH_GOAL)

print(game.get_str_game_overview())