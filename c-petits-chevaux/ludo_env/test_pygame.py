# main.py
import pygame
from ludo_env import LudoEnv
import random

# Initialiser la logique du jeu
game = LudoEnv()

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
