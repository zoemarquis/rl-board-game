from gymnasium.spaces import MultiBinary

# Remplacer Dict par MultiBinary
self.observation_space = MultiBinary(2 * TOTAL_SIZE + 6)  # 2 plateaux et dé (encodé en binaire)

# Dans `_get_observation`
def _get_observation(self):
    my_board = np.unpackbits(self.game.board[self.current_player], axis=0)
    adversaire_board = np.unpackbits(self.game.get_adversaire_relative_overview(self.current_player), axis=0)
    dice_roll = np.unpackbits(np.array([self.dice_roll], dtype=np.uint8))
    return np.concatenate([my_board, adversaire_board, dice_roll])












from gymnasium.spaces import MultiDiscrete

# Remplacer Dict par MultiDiscrete
self.observation_space = MultiDiscrete([NB_PAWNS] * (2 * TOTAL_SIZE) + [6])

# Dans `_get_observation`
def _get_observation(self):
    my_board = self.game.board[self.current_player]
    adversaire_board = self.game.get_adversaire_relative_overview(self.current_player)
    dice_roll = self.dice_roll
    return np.concatenate([my_board, adversaire_board, [dice_roll]])












import numpy as np
from gymnasium.spaces import Box

# Observation Space initial avec Dict
self.observation_space = Dict({
    "my_board": Box(low=0, high=NB_PAWNS, shape=(TOTAL_SIZE,), dtype=np.int8),
    "adversaire_board": Box(low=0, high=NB_PAWNS * (NUM_PLAYERS - 1), shape=(TOTAL_SIZE,), dtype=np.int8),
    "dice_roll": Discrete(6),
})

# Nouvelle définition
flat_size = TOTAL_SIZE + TOTAL_SIZE + 1  # Taille totale des observations (2 plateaux + dé)
self.observation_space = Box(low=0, high=NB_PAWNS * NUM_PLAYERS, shape=(flat_size,), dtype=np.int8)

# Dans `_get_observation`
def _get_observation(self):
    my_board = self.game.board[self.current_player]
    adversaire_board = self.game.get_adversaire_relative_overview(self.current_player)
    dice_roll = [self.dice_roll]
    return np.concatenate([my_board, adversaire_board, dice_roll])

