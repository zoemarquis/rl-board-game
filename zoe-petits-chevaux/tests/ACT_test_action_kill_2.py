"""
Fichier pour tester les KILL en sortie de pion
"""

import unittest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ludo_env.game_logic import GameLogic, Action, State


class TestKillAction(unittest.TestCase):
    def setUp(self):
        self.game = GameLogic()

    def test_kill_on_exit_action(self):
        self.game.init_board()

        #
        # TEST AVEC JOUEUR SUR LA CASE DE SORTIE DE L'ADVERSAIRE
        #

        print("Plateau de jeu initial :")
        print(self.game.get_str_game_overview())

        # Placement d'un pion du joueur 0 sur la case de sortie du joueur 1
        self.game.board[1][29] = 1
        self.game.board[1][0] -= 1

        print("Plateau après placement d'un pion adverse sur la case de sortie :")
        print(self.game.get_str_game_overview())

        dice_value = 6
        valid_actions = self.game.get_valid_actions(player_id=0, dice_value=dice_value)

        # Check si KILL est possible et MOVE_OUT non
        self.assertIn(Action.KILL, valid_actions[0])
        self.assertNotIn(Action.MOVE_OUT, valid_actions[0])

        # Exécuter l'action KILL
        self.game.sortir_pion(player_id=0, dice_value=dice_value)

        print("Plateau après l'action KILL en sortie :")
        print(self.game.get_str_game_overview())

        # Check que le pion 0 est retourné à l'écurie et que le pion 1 est sur la case 1
        self.assertEqual(self.game.board[1][0], 2)
        self.assertEqual(self.game.board[1][29], 0)
        self.assertEqual(self.game.board[0][1], 1)
        self.assertEqual(self.game.board[0][0], 1)

        #
        # TEST SANS JOUEUR SUR LA CASE DE SORTIE DE L'ADVERSAIRE
        #
        self.game.init_board()

        print("Plateau réinitialisé :")
        print(self.game.get_str_game_overview())

        valid_actions = self.game.get_valid_actions(player_id=0, dice_value=dice_value)

        # Check si MOVE_OUT est possible et KILL non
        self.assertIn(Action.MOVE_OUT, valid_actions[0])
        self.assertNotIn(Action.KILL, valid_actions[0])

        # Exécuter l'action MOVE_OUT
        self.game.sortir_pion(player_id=0, dice_value=dice_value)

        print("Plateau après l'action MOVE_OUT en sortie :")
        print(self.game.get_str_game_overview())

        # Check que le pion du joueur 0 est bien sur la case 1
        self.assertEqual(self.game.board[0][1], 1)
        self.assertEqual(self.game.board[0][0], 1)


if __name__ == "__main__":
    unittest.main()
