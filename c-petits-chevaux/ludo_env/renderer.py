# renderer.py
import pygame
from constants import *

# Configuration de base de pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 750
WINDOW_HEIGHT = 750
SQUARE_SIZE = 50  # Taille de chaque case du plateau

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Renderer:
    def __init__(self):
        # Configuration de la fenêtre Pygame
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Jeu des Petits Chevaux")

    def render(self, game):
        self.window.fill((0, 0, 0))  # Remplir l'écran avec du noir

        # Dessiner les cases du parcours
        self.draw_path(game)

        self.draw_safe_zone_player_0()
        self.draw_safe_zone_player_1()
        self.draw_safe_zone_player_2()
        self.draw_safe_zone_player_3()

        pygame.display.flip()  # Mettre à jour l'affichage

    def draw_path(self, game):
        """Dessiner les cases du parcours"""
        # Coordonnées des cases 1 à 8
        positions = [(0, 7), (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8),
                        # 8
                        (6,9), (6, 10), (6, 11), (6, 12), (6, 13), (6, 14),
                        # 15 
                        (7, 14), (8, 14), (8, 13), (8, 12), (8, 11), (8, 10), (8, 9), (8, 8),
                        # 23
                        (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8),
                        # 29
                        (14, 7), (14, 6), (13, 6), (12, 6), (11, 6), (10, 6), (9, 6), (8, 6),
                        # 37
                        (8, 5), (8, 4), (8, 3), (8, 2), (8, 1), (8, 0),
                        # 43
                        (7, 0), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
                        # 51
                        (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 6),
                      ]
        
        # Dessiner les cases du parcours
        for i, (x, y) in enumerate(positions):
            # Vérifier si la case fait partie de la zone de sécurité du joueur 0
            if (x, y) not in [(1,7), (2,7), (3,7), (4,7), (5,7), (6,7)]:
                # Dessiner une case avec contour blanc
                # pygame.draw.rect(self.window, GREEN, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(self.window, WHITE, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
            
            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i+1), True, WHITE)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

    def draw_safe_zone_player_0(self):
        """Dessiner la zone de sécurité du joueur 0"""
        position = [(1,7), (2,7), (3,7), (4,7), (5,7), (6,7)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(self.window, GREEN, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i+1), True, BLACK)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

    def draw_safe_zone_player_1(self):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4) """
        position = [(7,13), (7,12), (7,11), (7,10), (7,9), (7,8)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(self.window, YELLOW, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i+1), True, BLACK)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

    def draw_safe_zone_player_2(self):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4) """
        position = [(13,7), (12,7), (11,7), (10,7), (9,7), (8,7)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(self.window, RED, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i+1), True, WHITE)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

    def draw_safe_zone_player_3(self):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4) """
        position = [(7,1), (7,2), (7,3), (7,4), (7,5), (7,6)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(self.window, BLUE, pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i+1), True, WHITE)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))
    

    def get_coordinates_from_position(self, position):
        """Convertir la position du pion en coordonnées (x, y) sur le plateau"""
        x = (position % 14) * SQUARE_SIZE + SQUARE_SIZE // 2
        y = (position // 14) * SQUARE_SIZE + SQUARE_SIZE // 2
        return x, y

    def render_dice_value(self, dice_value):
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Dé: {dice_value}", True, WHITE)
        self.window.blit(text, (WINDOW_WIDTH - 200, 20))
