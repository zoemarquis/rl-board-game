# renderer.py
import pygame
from .action import Action_NO_EXACT, Action_EXACT, Action_EXACT_ASCENSION

# Configuration de base de pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 750
SQUARE_SIZE = 50  # Taille de chaque case du plateau

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

PLAYER_4_COLORS = {0: GREEN, 1: YELLOW, 2: RED, 3: BLUE}
PLAYER_2_COLORS = {0: GREEN, 1: RED}


class Renderer:
    def __init__(self, espace_action):
        self.espace_action = espace_action
        # Configuration de la fenêtre Pygame
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Petits Chevaux")

        dice_files = [f"images/dice_face{i}.png" for i in range(1, 7)]
        self.dice_images = {}

        for i, file in enumerate(dice_files, start=1):
            image = pygame.image.load(file)
            resized_image = pygame.transform.scale(
                image, (3 * SQUARE_SIZE, 3 * SQUARE_SIZE)
            )
            self.dice_images[i] = resized_image
        
        gameover_file = pygame.image.load("images/game_over.png")
        self.gameover_image = pygame.transform.scale(
            gameover_file, (3 * SQUARE_SIZE, 3 * SQUARE_SIZE)
        )


    def render(
        self, 
        game, 
        current_player, 
        dice_value, 
        valid_actions, 
        infos, 
        players_type, 
        game_over=False
    ):
        if game.num_players == 2:
            self.colors = PLAYER_2_COLORS
        else:
            self.colors = PLAYER_4_COLORS

        self.window.fill(GREY)  # Remplir l'écran avec du noir

        # Dessiner les cases du parcours
        self.draw_path(game)

        self.draw_safe_zone_player_0(game)
        self.draw_safe_zone_player_1(game)
        self.draw_safe_zone_player_2(game)
        self.draw_safe_zone_player_3(game)

        self.draw_ecurie_player_0(game)
        self.draw_ecurie_player_1(game)
        self.draw_ecurie_player_2(game)
        self.draw_ecurie_player_3(game)

        if game_over:
            self.show_winner_message(game, current_player)
        else:
            self.show_current_player(game, current_player)
            if players_type[current_player] == "humain":
                self.show_valid_actions(
                    valid_actions, current_player, infos, game.num_players
                )
            self.show_dice_value(dice_value)

        pygame.display.flip()  # Mettre à jour l'affichage

    def draw_path(self, game):
        """Dessiner les cases du parcours et les pions"""
        positions = [
            (6, 0),
            (6, 1),
            (6, 2),
            (6, 3),
            (6, 4),
            (6, 5),
            (6, 6),  # 7
            (5, 6),
            (4, 6),
            (3, 6),
            (2, 6),
            (1, 6),
            (0, 6),
            (0, 7),  # 14
            (0, 8),
            (1, 8),
            (2, 8),
            (3, 8),
            (4, 8),
            (5, 8),
            (6, 8),  # 21
            (6, 9),
            (6, 10),
            (6, 11),
            (6, 12),
            (6, 13),
            (6, 14),
            (7, 14),  # 28
            (8, 14),
            (8, 13),
            (8, 12),
            (8, 11),
            (8, 10),
            (8, 9),
            (8, 8),
            (9, 8),
            (10, 8),
            (11, 8),
            (12, 8),
            (13, 8),
            (14, 8),  # 41
            (14, 7),
            (14, 6),  # 43
            (13, 6),
            (12, 6),
            (11, 6),
            (10, 6),
            (9, 6),
            (8, 6),  # 49
            (8, 5),
            (8, 4),
            (8, 3),
            (8, 2),
            (8, 1),
            (8, 0),
            (7, 0),  # 56
        ]

        # Get path overview from game
        if game.num_players == 2:
            path_overview = game.get_chemin_pdv_2_joueurs(0)
        else:
            path_overview = game.get_chemin_pdv(0)

        for i, (x, y) in enumerate(positions):
            # Draw each square
            pygame.draw.rect(
                self.window,
                WHITE,
                pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                2,
            )

            # Count the number of pawns in this square
            pawn_count = len(path_overview[i])

            # Draw the number of pawns as a text inside the square
            if pawn_count > 0:
                pawns_id = path_overview[i]
                for id in pawns_id:
                    pawn_color = self.colors[id]
                    # Draw a circle for pawns (as many as needed per square)
                    pygame.draw.circle(
                        self.window,
                        pawn_color,
                        (
                            y * SQUARE_SIZE + SQUARE_SIZE // 2,
                            x * SQUARE_SIZE + SQUARE_SIZE // 2,
                        ),
                        SQUARE_SIZE // 3,
                    )  # Adjust size of the circle

                    # Create text to represent the pawn count
                    font = pygame.font.Font(
                        None, 24
                    )  # Use a larger font for visibility
                    text = font.render(str(pawn_count), True, BLACK)

                    # Position the text in the center of the circle
                    text_rect = text.get_rect(
                        center=(
                            y * SQUARE_SIZE + SQUARE_SIZE // 2,
                            x * SQUARE_SIZE + SQUARE_SIZE // 2,
                        )
                    )
                    self.window.blit(text, text_rect)

            # Add the number to each square as a fallback in case no pawns
            else:
                font = pygame.font.Font(None, 16)
                text = font.render(str(i + 1), True, WHITE)
                self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

    def draw_safe_zone_player_0(self, game):
        """Dessiner la zone de sécurité du joueur 0"""
        position = [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(
                self.window,
                GREEN,
                pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i + 1), True, BLACK)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

            self.draw_pawns_safezone_player_0(game)

    def draw_safe_zone_player_1(self, game):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4)"""
        position = [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(
                self.window,
                YELLOW,
                pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i + 1), True, BLACK)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

        if game.num_players > 2:
            self.draw_pawns_safezone_player_1(game)

    def draw_safe_zone_player_2(self, game):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4)"""
        position = [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(
                self.window,
                RED,
                pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i + 1), True, WHITE)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

        self.draw_pawns_safezone_player_2(game)

    def draw_safe_zone_player_3(self, game):
        """Dessiner la zone de sécurité du joueur 1 (dans jeu à 4)"""
        position = [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)]
        for i, (x, y) in enumerate(position):
            # Dessiner la zone de sécurité sans contour blanc
            pygame.draw.rect(
                self.window,
                BLUE,
                pygame.Rect(y * SQUARE_SIZE, x * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            # Ajouter un numéro à chaque case pour l'identification
            font = pygame.font.Font(None, 16)
            text = font.render(str(i + 1), True, WHITE)
            self.window.blit(text, (y * SQUARE_SIZE + 12, x * SQUARE_SIZE + 12))

        if game.num_players == 4:
            self.draw_pawns_safezone_player_3(game)

    def draw_ecurie_player_0(self, game):
        """Dessiner l'écurie du joueur 0"""
        # Dessiner l'écurie
        pygame.draw.rect(
            self.window,
            GREEN,
            pygame.Rect(
                0 * SQUARE_SIZE, 0 * SQUARE_SIZE, 6 * SQUARE_SIZE, 6 * SQUARE_SIZE
            ),
        )
        pygame.draw.rect(
            self.window,
            WHITE,
            pygame.Rect(
                1 * SQUARE_SIZE, 1 * SQUARE_SIZE, 4 * SQUARE_SIZE, 4 * SQUARE_SIZE
            ),
        )

        num_pawns = game.get_ecurie_player(0)
        font = pygame.font.Font(None, 64)
        text = font.render(str(num_pawns), True, BLACK)
        self.window.blit(text, (2.5 * SQUARE_SIZE, 2.5 * SQUARE_SIZE))

    def draw_ecurie_player_1(self, game):
        """Dessiner l'écurie du joueur 1"""
        pygame.draw.rect(
            self.window,
            YELLOW,
            pygame.Rect(
                9 * SQUARE_SIZE, 0 * SQUARE_SIZE, 6 * SQUARE_SIZE, 6 * SQUARE_SIZE
            ),
        )
        pygame.draw.rect(
            self.window,
            WHITE,
            pygame.Rect(
                10 * SQUARE_SIZE, 1 * SQUARE_SIZE, 4 * SQUARE_SIZE, 4 * SQUARE_SIZE
            ),
        )

        if game.num_players > 2:
            num_pawns = game.get_ecurie_player(1)
            font = pygame.font.Font(None, 64)
            text = font.render(str(num_pawns), True, BLACK)
            self.window.blit(text, (11.5 * SQUARE_SIZE, 2.5 * SQUARE_SIZE))

    def draw_ecurie_player_2(self, game):
        """Dessiner l'écurie du joueur 2"""
        pygame.draw.rect(
            self.window,
            RED,
            pygame.Rect(
                9 * SQUARE_SIZE, 9 * SQUARE_SIZE, 6 * SQUARE_SIZE, 6 * SQUARE_SIZE
            ),
        )
        pygame.draw.rect(
            self.window,
            WHITE,
            pygame.Rect(
                10 * SQUARE_SIZE, 10 * SQUARE_SIZE, 4 * SQUARE_SIZE, 4 * SQUARE_SIZE
            ),
        )

        if game.num_players == 2:
            num_pawns = game.get_ecurie_player(1)
        else:
            num_pawns = game.get_ecurie_player(2)
        font = pygame.font.Font(None, 64)
        text = font.render(str(num_pawns), True, BLACK)
        self.window.blit(text, (11.5 * SQUARE_SIZE, 11.5 * SQUARE_SIZE))

    def draw_ecurie_player_3(self, game):
        """Dessiner l'écurie du joueur 3"""
        pygame.draw.rect(
            self.window,
            BLUE,
            pygame.Rect(
                0 * SQUARE_SIZE, 9 * SQUARE_SIZE, 6 * SQUARE_SIZE, 6 * SQUARE_SIZE
            ),
        )
        pygame.draw.rect(
            self.window,
            WHITE,
            pygame.Rect(
                1 * SQUARE_SIZE, 10 * SQUARE_SIZE, 4 * SQUARE_SIZE, 4 * SQUARE_SIZE
            ),
        )

        if game.num_players == 4:
            num_pawns = game.get_ecurie_player(3)
            font = pygame.font.Font(None, 64)
            text = font.render(str(num_pawns), True, BLACK)
            self.window.blit(text, (2.5 * SQUARE_SIZE, 11.5 * SQUARE_SIZE))

    def get_coordinates_from_position(self, position):
        """Convertir la position du pion en coordonnées (x, y) sur le plateau"""
        x = (position % 14) * SQUARE_SIZE + SQUARE_SIZE // 2
        y = (position // 14) * SQUARE_SIZE + SQUARE_SIZE // 2
        return x, y

    def render_dice_value(self, dice_value):
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(f"Dé: {dice_value}", True, WHITE)
        self.window.blit(text, (WINDOW_WIDTH - 200, 20))

    def draw_pawns_safezone_player_0(self, game):
        position = [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6)]
        escalier = game.board[0][57:63]
        for i in escalier:
            if i != 0:
                x, y = position[i]
                pygame.draw.circle(
                    self.window,
                    WHITE,
                    (
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    SQUARE_SIZE // 3,
                )  # Adjust size of the circle

                # Create text to represent the pawn count
                font = pygame.font.Font(None, 24)  # Use a larger font for visibility
                text = font.render(str(i), True, BLACK)

                # Position the text in the center of the circle
                text_rect = text.get_rect(
                    center=(
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )
                self.window.blit(text, text_rect)

    def draw_pawns_safezone_player_1(self, game):
        # fonction pour 3+ joueurs
        position = [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
        escalier = game.board[1][57:63]
        for i in escalier:
            if i != 0:
                x, y = position[i]
                pygame.draw.circle(
                    self.window,
                    WHITE,
                    (
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    SQUARE_SIZE // 3,
                )  # Adjust size of the circle

                # Create text to represent the pawn count
                font = pygame.font.Font(None, 24)  # Use a larger font for visibility
                text = font.render(str(i), True, BLACK)

                # Position the text in the center of the circle
                text_rect = text.get_rect(
                    center=(
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )
                self.window.blit(text, text_rect)

    def draw_pawns_safezone_player_2(self, game):
        position = [(7, 13), (7, 12), (7, 11), (7, 10), (7, 9), (7, 8)]
        # si 2 joueurs, 2eme est en rouge
        if game.num_players == 2:
            escalier = game.board[1][57:63]
        else:
            escalier = game.board[2][57:63]

        for i in escalier:
            if i != 0:
                x, y = position[i]
                pygame.draw.circle(
                    self.window,
                    WHITE,
                    (
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    SQUARE_SIZE // 3,
                )  # Adjust size of the circle

                # Create text to represent the pawn count
                font = pygame.font.Font(None, 24)  # Use a larger font for visibility
                text = font.render(str(i), True, BLACK)

                # Position the text in the center of the circle
                text_rect = text.get_rect(
                    center=(
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )
                self.window.blit(text, text_rect)

    def draw_pawns_safezone_player_3(self, game):
        position = position = [(13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7)]
        escalier = game.board[3][57:63]
        for i in escalier:
            if i != 0:
                x, y = position[i]
                pygame.draw.circle(
                    self.window,
                    WHITE,
                    (
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    SQUARE_SIZE // 3,
                )  # Adjust size of the circle

                # Create text to represent the pawn count
                font = pygame.font.Font(None, 24)  # Use a larger font for visibility
                text = font.render(str(i), True, BLACK)

                # Position the text in the center of the circle
                text_rect = text.get_rect(
                    center=(
                        y * SQUARE_SIZE + SQUARE_SIZE // 2,
                        x * SQUARE_SIZE + SQUARE_SIZE // 2,
                    )
                )
                self.window.blit(text, text_rect)

    def show_current_player(self, game, current_player):
        if game.num_players == 2:
            colors = PLAYER_2_COLORS
        else:
            colors = PLAYER_4_COLORS

        font = pygame.font.SysFont(None, 30)
        text = font.render("Joueur actuel : ", True, BLACK)
        self.window.blit(text, (16 * SQUARE_SIZE, 1 * SQUARE_SIZE))

        # Render the current player's number in their corresponding color
        player_text = font.render(str(current_player + 1), True, colors[current_player])
        self.window.blit(player_text, (19 * SQUARE_SIZE, 1 * SQUARE_SIZE))

    def show_dice_value(self, dice_value):
        if dice_value not in self.dice_images:
            raise ValueError(
                f"Invalid dice_value: {dice_value}. Must be between 1 and 6."
            )

        # Get the corresponding image
        dice_image = self.dice_images[dice_value]

        # Blit the image onto the screen
        self.window.blit(dice_image, (18 * SQUARE_SIZE, 11 * SQUARE_SIZE))

    def show_winner_message(self, game, current_player):
        if game.num_players == 2:
            colors = PLAYER_2_COLORS
        else:
            colors = PLAYER_4_COLORS

        font = pygame.font.SysFont(None, 40)
        text = font.render("Joueur ", True, BLACK)
        self.window.blit(text, (16 * SQUARE_SIZE, 2 * SQUARE_SIZE))

        # Render the current player's number in their corresponding color
        player_text = font.render(str(current_player + 1), True, colors[current_player])
        self.window.blit(player_text, (18 * SQUARE_SIZE, 2 * SQUARE_SIZE))

        text = font.render(" a gagné !", True, BLACK)
        self.window.blit(text, (16 * SQUARE_SIZE, 3 * SQUARE_SIZE))

        self.window.blit(self.gameover_image, (18 * SQUARE_SIZE, 5 * SQUARE_SIZE))

            
    def get_action_text(self, action):
        action_value = action.value

        if action_value in [0,1,2,3,4]:
            match action_value:
                case 0:
                    return "Passer son tour"
                case 1:
                    return "Sortir un pion"
                case 2:
                    return "Sortir un pion et tuer pion adverse"
                case 3:
                    return "avancer"
                case 4:
                    return "rester bloqué derrière un pion"

        # else 
        if self.espace_action == "exact_ascension":
            match action_value:
                case 5: 
                    return "tuer pion adverse"
                case 6:
                    return "atteindre le pied de l'escalier"
                case 7:
                    return "avancer et reculer au pied de l'escalier"
                case 8:
                    return "monter la marche 1"
                case 9:
                    return "monter la marche 2"
                case 10:
                    return "monter la marche 3"
                case 11:
                    return "monter la marche 4"
                case 12:
                    return "monter la marche 5"
                case 13:
                    return "monter la marche 6"
                case 14:
                    return "atteindre l'objectif"
            raise ValueError("Action invalide")

        elif self.espace_action == "exact":
            match action_value:
                case 5: 
                    return "tuer pion adverse"
                case 6:
                    return "atteindre le pied de l'escalier"
                case 7:
                    return "avancer et reculer au pied de l'escalier"
                case 8:
                    return "avancer dans l'escalier"
                case 9:
                    return "atteindre l'objectif"
            raise ValueError("Action invalide")
        
        elif self.espace_action == "not_exact":
            match action_value:
                case 5:
                    return "entrer dans l'escalier"
                case 6:
                    return "avancer dans l'escalier"
                case 7:
                    return "atteindre l'objectif"
                case 8:
                    return "tuer pion adverse"
            raise ValueError("Action invalide")

        else:
            raise ValueError("Espace d'action invalide")
        

    def get_absolute_position(self, position, player_id, num_players):
        if player_id == 0:
            return position
        elif player_id == 1:
            if num_players == 2:
                return (position + 28) % 56
            else:
                return (position + 14) % 56
        elif player_id == 2:
            return (position + 28) % 56
        elif player_id == 3:
            return (position + 42) % 56

    def render_action_button(self, text, y):
        """
        Render a single action button and return its Rect.
        """
        font = pygame.font.SysFont(None, 30)
        x = 16 * SQUARE_SIZE
        y = y * SQUARE_SIZE

        text = font.render(text, True, BLACK)
        text_rect = text.get_rect()
        rect_width = text_rect.width + 20  # Add some padding
        rect_height = text_rect.height + 20

        button_rect = pygame.Rect(x, y, rect_width, rect_height)
        tuple = (x, y, rect_width, rect_height)
        pygame.draw.rect(self.window, WHITE, button_rect)

        text_rect.topleft = (x + 10, y + 10)
        self.window.blit(text, text_rect)

        return tuple

    def show_valid_actions(self, valid_actions, player_id, infos, num_players):
        y_current = 2
        button_mapping = {}

        for pawn_id, action in valid_actions:
            if action.value in [0, 1, 2]:
                action_text = self.get_action_text(action)
                button_rect = self.render_action_button(action_text, y_current)
                button_mapping[button_rect] = action.value
                y_current += 1.5
            else:
                action_text = self.get_action_text(action)
                position = self.get_absolute_position(
                    infos[pawn_id]["position"], 
                    player_id, 
                    num_players
                )
                text = f"Pion pos {position} : {action_text}"
                button_rect = self.render_action_button(text, y_current)
                button_mapping[button_rect] = action.value
                y_current += 1.5

        self.button_mapping = button_mapping

    def show_click_button_message(self):
        font = pygame.font.SysFont(None, 30)
        text = font.render("Cliquez sur un bouton d'action", True, WHITE)
        self.window.blit(text, (16 * SQUARE_SIZE, 10 * SQUARE_SIZE))
