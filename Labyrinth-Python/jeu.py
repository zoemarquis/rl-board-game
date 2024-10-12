from eztext import *
import time
from labyrintheModeGraphiqueOO import *
import argparse

# Create the argument parser
parser = argparse.ArgumentParser(description="Jeu avec options pour joueurs et IA")
parser.add_argument("-j", "--joueurs", type=int, default=4, help="Nombre de joueurs")
parser.add_argument(
    "-ia",
    "--intelligence-artificielle",
    type=int,
    default=0,
    help="Nombre de joueurs IA",
)

# Parse the arguments
args = parser.parse_args()

# Access the number of players and AI from the arguments
nb_joueurs = args.joueurs
nb_ia = args.intelligence_artificielle


class Jeu(object):
    def __init__(self):

        self.espace = 50
        # self.nombreParam = 4
        # self.select = 0
        self.iOpt = 0
        self.largeur = 1500
        self.hauteur = 900
        self.couleur = (0, 255, 0)
        self.tailleFont = 25
        self.iFont = 1
        self.allFont = pygame.font.get_fonts()
        self.styleFont = "texgyrechorus"
        pygame.init()
        self.fenetre = pygame.display.set_mode(
            (self.largeur, self.hauteur), pygame.RESIZABLE
        )
        pygame.display.set_caption("Labyrinthe")
        pygame.display.set_icon(
            pygame.image.load(os.path.join("./original_images", "logo.png"))
        )
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)
        self.surface = pygame.display.get_surface()
        self.nb_joueur = nb_joueurs
        self.nb_ia = nb_ia
        self.nb_tresor = 24
        self.nb_tresor_par_joueur = 6
        self.parametre = [
            self.nb_joueur,
            self.nb_ia,
            self.nb_tresor,
            self.nb_tresor_par_joueur,
        ]
        # self.fenetreParam = []

    # Fonction pour choisir la police d'écriture
    def afficherFont(self):
        texte = self.font.render(self.styleFont, 1, (255, 255, 255))
        textepos = texte.get_rect()
        textepos.x = self.espace
        textepos.y = self.espace
        self.rectFont = textepos
        self.surface.blit(texte, textepos)
        pygame.display.flip()

    # Fonction mettant a jour divers parametres de la fenetre, notamment pour le redimmensionnement
    def miseAjourParametres(self):
        self.surface = pygame.display.get_surface()
        self.hauteur = self.surface.get_height()
        self.largeur = self.surface.get_width()
        self.espace = self.hauteur // 16
        self.tailleFont = self.espace // 2
        # self.styleFont = self.allFont[self.iFont]
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)

    # Foncion creant des zone de texte affichable
    def initTexte(self, texte, hauteur=0):
        texte = self.font.render(texte, 1, self.couleur)
        textpos = texte.get_rect()
        textpos.x = (self.largeur - textpos.width) // 2
        textpos.y = hauteur
        return (texte, textpos)

    # Fonction testant les valeur des paramètres
    def testValeur(self):
        # assert 0 <= self.nb_joueur <= 4
        # assert 0 <= self.nb_ia <= 4
        # assert 2 <= self.nb_joueur + self.nb_ia <= 4
        # assert self.nb_tresor == 24
        # assert self.nb_tresor_par_joueur == 6
        if not (0 <= self.nb_joueur <= 4):
            return False

        if not (0 <= self.nb_ia <= 4):
            return False

        if not (2 <= self.nb_joueur + self.nb_ia <= 4):
            return False

        return True

    # Fonction principale du menu gérant tous les évenements
    def demarrer(self):
        if self.testValeur():
            g = LabyrintheGraphique(
                Labyrinthe(
                    int(self.parametre[0]),
                    int(self.parametre[2]),
                    int(self.parametre[3]),
                    int(self.parametre[1]),
                )
            )
            g.demarrer()
        else:
            print(
                "Nombre de joueurs doit être entre 1 et 4, vous avez choisi ",
                self.nb_joueur,
            )
            print("Nombre de IA doit être entre 0 et 4, vous avez choisi ", self.nb_ia)
            print("La somme de joueurs et IA doit être entre 2 et 4")
            continuer = False

        pygame.display.flip()
        pygame.quit()


jeu = Jeu()
jeu.demarrer()
