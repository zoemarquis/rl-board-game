'''
Fichier pour tester la fonction get_relative_position de la classe GameLogic
'''

import unittest
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ludo_env.game_logic import GameLogic, Action


class TestGameLogic(unittest.TestCase):

    def setUp(self):
        # Attention :  Actuellement, il faut changer NUM_PLAYERS manuellement dans game_logic.py pour tester avec 3 ou 4 joueurs
        self.game_players = GameLogic()
        self.game_3_players = GameLogic()
        self.game_4_players = GameLogic()
        
        self.game_players.init_board()
        self.game_3_players.init_board()
        self.game_4_players.init_board()

    def test_get_relative_position(self):
        # 2 joueurs
        self.assertEqual(self.game_2_players.get_relative_position(0, 1, 1), 29)
        self.assertEqual(self.game_2_players.get_relative_position(1, 0, 1), 29)

        # 3 joueurs
        self.assertEqual(self.game_3_players.get_relative_position(0, 2, 1), 29)
        self.assertEqual(self.game_3_players.get_relative_position(2, 0, 1), 29)
        self.assertEqual(self.game_3_players.get_relative_position(1, 2, 1), 15)

        # 4 joueurs
        self.assertEqual(self.game_4_players.get_relative_position(0, 1, 1), 15)
        self.assertEqual(self.game_4_players.get_relative_position(1, 2, 15), 29)
        self.assertEqual(self.game_4_players.get_relative_position(2, 3, 29), 43)
        self.assertEqual(self.game_4_players.get_relative_position(3, 0, 43), 1)

if __name__ == "__main__":
    unittest.main()