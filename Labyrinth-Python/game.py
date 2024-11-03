from eztext import *
from gui_manager import *
from stable_baselines3 import PPO

from gym_env_2dim import LabyrinthEnv


class Game(object):
    """Main class of the game, managing the game parameters and the events of the menu window"""

    def __init__(self, human_players, ia_number, directory, use_rl_agent=True):
        """Initialization of the Game class"""
        
        self.space = 50  # inutile ?
        self.iOpt = 0  # inutile ?

        pygame.init()

        self.window_width = 1500
        self.window_height = 900
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height), pygame.RESIZABLE
        )
        self.directory = directory
        pygame.display.set_caption("Labyrinthe")
        pygame.display.set_icon(
            pygame.image.load(os.path.join(self.directory, "logo.png"))
        )
        self.surface = pygame.display.get_surface()

        self.background_color = (0, 255, 0)

        self.fontsize = 25
        self.iFont = 1  # inutile ?
        self.allFont = pygame.font.get_fonts()  # inutile ?
        self.styleFont = "texgyrechorus"
        self.font = pygame.font.SysFont(self.styleFont, self.fontsize)

        self.human_players = human_players
        self.ia_number = ia_number
        self.use_rl_agent = use_rl_agent

        self.env = LabyrinthEnv(num_human_players=human_players, num_ai_players=ia_number, render_mode="human")

        self.model = None
        if self.use_rl_agent:
            self.model = PPO.load("./modeles/best_model.zip")
  

    def display_font(self):
        """Display the font on the screen"""
        text = self.font.render(self.styleFont, 1, (255, 255, 255))
        text_position = text.get_rect()
        text_position.x = self.space
        text_position.y = self.space
        self.rectFont = text_position
        self.surface.blit(text, text_position)
        pygame.display.flip()

    def update_window(self):
        """Update the window"""
        self.surface = pygame.display.get_surface()
        self.window_height = self.surface.get_height()
        self.window_width = self.surface.get_width()
        self.space = self.window_height // 16
        self.fontsize = self.space // 2
        self.font = pygame.font.SysFont(self.styleFont, self.fontsize)

    def text_initialization(self, text, hauteur=0):
        """Initialize text zones"""
        text = self.font.render(text, 1, self.background_color)
        text_position = text.get_rect()
        text_position.x = (self.window_width - text_position.width) // 2
        text_position.y = hauteur
        return (text, text_position)

    def launch(self):
        """Launch the game"""

        assert (
            0 <= self.human_players <= 4
        ), "Nombre de joueurs humains doit être entre 0 et 4"
        assert 0 <= self.ia_number <= 4, "Nombre de IA doit être entre 0 et 4"
        assert (
            2 <= self.human_players + self.ia_number <= 4
        ), "La somme de joueurs humains et IA doit être entre 2 et 4"

        
        g = GUI_manager(self.env.game, self.model, self.env, prefixeImage=self.directory)

        g.start()

        pygame.display.flip()
        pygame.quit()
