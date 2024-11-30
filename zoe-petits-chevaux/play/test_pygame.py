# pour tester à quoi ressemble l'interface graphique

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from ludo_env import LudoEnv

import random
import pygame

# Initialiser la logique du jeu
game = LudoEnv(um_players=2, nb_chevaux=2, with_render=True)

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Simuler un lancer de dé
    dice_value = random.randint(1, 6)

    # Afficher le plateau et la valeur du dé
    game.render(game.game)  # Met à jour le plateau via Pygame

    pygame.time.wait(500)  # Attendre un peu avant de redessiner le plateau

pygame.quit()
