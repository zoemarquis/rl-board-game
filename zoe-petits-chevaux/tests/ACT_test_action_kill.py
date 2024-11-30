"""
Fichier pour tester l'action et la fonction de tuer un pion adverse
"""

import unittest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ludo_env import *


class TestKillAction(unittest.TestCase):
    def setUp(self):
        self.game = GameLogic(num_players=2)

    def test_kill_action(self):
        self.game.init_board()

        print("Plateau de jeu initial :")
        print(self.game.get_str_game_overview())

        # Placement des pions sur le plateau
        self.game.board[0][5 + 2 * 14] = 1
        self.game.board[0][0] -= 1

        self.game.board[1][10] = 1
        self.game.board[1][0] -= 1

        print("Plateau après placement des pions :")
        print(self.game.get_str_game_overview())

        # Dé à 5 (comme 5 d'intervalle)
        dice_value = 5

        # Test des positions
        self.assertEqual(self.game.board[0][5 + 2 * 14], 1)
        self.assertEqual(self.game.board[1][10], 1)

        # Déplacement sur la case de l'adversaire
        self.game.move_pawn(
            player_id=0,
            old_position=5 + 2 * 14,
            dice_value=dice_value,
            action=Action.KILL,
        )

        print("Plateau après déplacement :")
        print(self.game.get_str_game_overview())

        # Test déplacement
        expected_position = 10 + 2 * 14  # New position relative to Player 0
        self.assertEqual(self.game.board[0][expected_position], 1)
        self.assertEqual(self.game.board[0][5 + 2 * 14], 0)

        # Test du retour à l'écurie
        self.assertEqual(self.game.board[1][0], 2)
        self.assertEqual(self.game.board[1][10], 0)

        # Test que le pion qui a tué l'autre est bien sur la case
        pawns_info = self.game.get_pawns_info(0)
        pawn_positions = [pawn["position"] for pawn in pawns_info]
        self.assertIn(expected_position, pawn_positions)  # Use expected_position

        # Test total des pions
        self.assertEqual(sum(self.game.board[0]), 2)
        self.assertEqual(sum(self.game.board[1]), 2)


if __name__ == "__main__":
    unittest.main()
