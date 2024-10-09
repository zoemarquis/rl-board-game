from eztext import *
import time
from labyrintheModeGraphiqueOO import *


class Menu(object):
    """Classe gérant le menu du jeu"""

    def __init__(self):

        self.espace = 50
        self.nombreParam = 4
        self.select = 0
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
        self.menuQ = []
        self.questions = []
        self.nb_joueur = 4
        self.nb_ia = 0
        self.nb_tresor = 24
        self.nb_tresor_par_joueur = 6
        self.parametre = []
        self.fenetreParam = []
        self.initMenu()
        self.initOption()

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

    # Fonction initialisant les éléments pour la page des options
    def initOption(self):
        self.initQuestion()
        # nombre de joueur -> on en veut 4
        parametre = Input()
        parametre.value = "4"
        parametre.color = (0, 255, 0)
        self.parametre.append(parametre)
        # nombre d'IA -> on en veut 0 (pour le moment)
        parametre1 = Input()
        parametre1.value = "0"
        parametre1.color = (0, 255, 0)
        self.parametre.append(parametre1)
        # nombre de trésors -> on en veut toujours 24
        parametre2 = Input()
        parametre2.value = "24"
        parametre2.color = (0, 255, 0)
        self.parametre.append(parametre2)
        # nombre de trésors par personnes -> on en veut toujours 6
        parametre3 = Input()
        parametre3.value = "6"
        parametre3.color = (0, 255, 0)
        self.parametre.append(parametre3)
        self.initMenuQuestion()

    # Fonction initialisant les questions s'affichant dans les options
    def initQuestion(self):
        self.questions = []
        self.questions.append(self.initTexte("Nombre de joueurs ? entre 1 et 3"))
        self.questions.append(self.initTexte("Nombre d'IA ?"))
        self.questions.append(self.initTexte("Nombre de Trésors ? entre 12 et 34"))
        self.questions.append(self.initTexte("Nombre de Trésors par joueur ? "))

    # Fonction initialisant le menu de la page option
    def initMenuQuestion(self):
        self.menuQ = []
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont * 2)
        self.menuQ.append(self.initTexte("Jouer !"))
        self.menuQ.append(self.initTexte("Précédent"))
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)

    # Fonction calculant la position des éléments de la page option
    def actualiserQuestion(self):
        hauteur = self.hauteur
        self.initQuestion()
        fenetre = []
        y = self.espace
        x = self.largeur // 3
        for i in range(len(self.questions)):
            espace = (self.espace - self.questions[i][1].height) // 2
            y += espace
            self.questions[i][1].y = y
            y += self.questions[i][1].height + espace
            taille = self.largeur // 6
            fenetre.append(
                Rect(
                    (self.largeur - taille) // 2,
                    y,
                    taille,
                    self.questions[i][1].height * 3 // 2,
                )
            )
            self.parametre[i].set_pos(
                (self.largeur - taille) // 2 + self.questions[i][1].height // 4,
                y + self.questions[i][1].height // 4,
            )
            self.parametre[i].set_font(self.font)
            y += espace + self.espace * 2
        self.fenetreParam = fenetre
        self.menuQ[0][1].y = self.hauteur - 2 * self.espace
        self.menuQ[0][1].x = self.largeur - self.espace - self.menuQ[0][1].width
        self.menuQ[1][1].y = self.hauteur - 2 * self.espace
        self.menuQ[1][1].x = self.espace

    # Fonction testant les valeur des paramètre de la page option
    def testValeur(self, i):
        assert 0 <= self.nb_joueur <= 4
        assert 0 <= self.nb_ia <= 4
        assert 2 <= self.nb_joueur + self.nb_ia <= 4
        assert self.nb_tresor == 24
        assert self.nb_tresor_par_joueur == 6

        if i == 0:
            return self.parametre[i].value in ["1", "2", "3", "4"]
        if i == 1:
            if self.parametre[i].value.isdigit():
                if self.parametre[0].value.isdigit():
                    return (
                        0
                        <= int(self.parametre[i].value)
                        < 5 - int(self.parametre[0].value)
                    )
        if i == 2:
            if self.parametre[i].value.isdigit():
                return 12 <= int(self.parametre[i].value) < 35
        if i == 3:
            if self.parametre[0].value.isdigit():
                if self.parametre[1].value.isdigit():
                    if self.parametre[2].value.isdigit():
                        if self.parametre[3].value.isdigit():
                            return (
                                0
                                < int(self.parametre[3].value)
                                <= int(self.parametre[2].value)
                                // (
                                    int(self.parametre[0].value)
                                    + int(self.parametre[1].value)
                                )
                            )
        return False

    # Fonction affichant la page Option
    def afficherQuestion(self):
        self.surface.fill((0, 0, 0))
        i = 0
        for texte, textepos in self.questions:
            self.surface.blit(texte, textepos)
            self.parametre[i].draw(self.surface)
            if self.iOpt == i:
                pygame.draw.rect(self.surface, (0, 0, 255), self.fenetreParam[i], 1)
            else:
                if self.testValeur(i):
                    pygame.draw.rect(self.surface, (0, 255, 0), self.fenetreParam[i], 1)
                else:
                    pygame.draw.rect(self.surface, (255, 0, 0), self.fenetreParam[i], 1)
            i += 1
        for texte, textepos in self.menuQ:
            self.surface.blit(texte, textepos)
        pygame.display.flip()

    # Fonction initialisant le menu principale
    def initMenu(self):

        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont * 4)
        listeMenu = []
        listeMenu.append(self.initTexte("Labyrinthe"))
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont * 2)
        listeMenu.append(self.initTexte("Jouer !"))
        listeMenu.append(self.initTexte("Options"))
        listeMenu.append(self.initTexte("Quitter"))
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)
        hauteur = self.espace
        for _, tp in listeMenu:
            hauteur += tp.height + self.espace
        delta = (self.hauteur - hauteur) // 2
        for i in range(len(listeMenu)):
            if i == 0:
                listeMenu[i][1].y = delta
            elif i == 1:
                listeMenu[i][1].y = delta + listeMenu[i - 1][1].height + self.espace * 2
            else:
                listeMenu[i][1].y = (
                    listeMenu[i - 1][1].y + listeMenu[i - 1][1].height + self.espace
                )
        self.menu = listeMenu

    # Fonction affichant le menu principale
    def afficherMenu(self):
        self.surface.fill((0, 0, 0))
        for txt, tp in self.menu:
            self.surface.blit(txt, tp)

    # Foncion changean l'affichage de la page option en fonction de la position de la souris
    def changerMenuQuestion(self):
        coord = pygame.mouse.get_pos()
        self.couleur = (0, 0, 255)
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont * 3)
        if self.menuQ[0][1].collidepoint(coord):
            self.menuQ[0] = self.initTexte("Jouer !", self.menuQ[0][1].y)
            self.menuQ[0][1].x = self.largeur - self.espace - self.menuQ[0][1].width
        elif self.menuQ[1][1].collidepoint(coord):
            self.menuQ[1] = self.initTexte("Précédent", self.menuQ[1][1].y)
            self.menuQ[1][1].x = self.espace
        else:
            self.couleur = (0, 255, 0)
            self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)
            self.initMenuQuestion()
        self.couleur = (0, 255, 0)
        self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)

    # Foncion changeant l'affichage du menu principale en fonction de la position de la souris
    def changerMenu(self):
        coord = pygame.mouse.get_pos()
        ind = None
        i = 1
        while ind == None and i < len(self.menu):
            if self.menu[i][1].collidepoint(coord):
                ind = i
            else:
                i += 1
        self.initMenu()
        if ind != None:
            self.couleur = (0, 0, 255)
            self.font = pygame.font.SysFont(self.styleFont, self.tailleFont * 3)
            if ind == 1:
                self.menu[ind] = self.initTexte("Jouer !", self.menu[ind][1].y)
            elif ind == 2:
                self.menu[ind] = self.initTexte("Options", self.menu[ind][1].y)
            else:
                self.menu[ind] = self.initTexte("Quitter", self.menu[ind][1].y)
            self.couleur = (0, 255, 0)
            self.font = pygame.font.SysFont(self.styleFont, self.tailleFont)

    # Fonction permettant de géré l'action de clické quelque soit le menu
    def changerSelect(self, pos):
        # if self.rectFont.collidepoint(pos):
        # 	self.iFont +=1
        # 	if self.iFont == len(self.allFont):
        # 		self.iFont=0
        if self.select == 0:
            i = 1
            ind = None
            while ind == None and i < len(self.menu):
                if self.menu[i][1].collidepoint(pos):
                    ind = i
                else:
                    i += 1
            if ind != None:
                self.select = ind
        elif self.select == 2:
            if self.menuQ[0][1].collidepoint(pos):
                self.select = 1
            elif self.menuQ[1][1].collidepoint(pos):
                self.select = 0
            else:
                for i in range(4):
                    if self.fenetreParam[i].collidepoint(pos):
                        self.iOpt = i

    # Fonction permettant de changer la zone de texte selectionné avec la touche TAB ou DOWN
    def changeOptionInd(self):
        self.iOpt += 1
        if self.iOpt == 4:
            self.iOpt = 0

    # Fonction permettant de changer la zone de texte selectionné avec la touche UP
    def monteOptionInd(self):
        self.iOpt -= 1
        if self.iOpt == -1:
            self.iOpt = 3

    # Fonction principale du menu gérant tous les évenements
    def demarrer(self):
        continuer = True
        while continuer:
            # self.afficherFont()
            ev = pygame.event.wait()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    continuer = False
                elif ev.key == K_TAB:
                    if self.select == 2:
                        self.changeOptionInd()
                elif ev.key == K_DOWN:
                    if self.select == 2:
                        self.changeOptionInd()

                elif ev.key == K_UP:
                    if self.select == 2:
                        self.monteOptionInd()
                else:
                    if self.select == 2:
                        # Check si Shift est appuyé
                        keys = pygame.key.get_pressed()
                        if keys[K_LSHIFT] or keys[K_RSHIFT]:
                            if K_0 <= ev.key <= K_9:
                                self.parametre[self.iOpt].value += str(ev.key - K_0)
                        else:
                            self.parametre[self.iOpt].update(ev)

            if ev.type == pygame.VIDEORESIZE:
                fenetre = pygame.display.set_mode(
                    ev.size, pygame.RESIZABLE | pygame.DOUBLEBUF
                )
                self.miseAjourParametres()
                if self.select == 0:
                    self.initMenu()
                elif self.select == 2:
                    self.afficherQuestion()

            if ev.type == pygame.QUIT:
                print("quit here")
                continuer = False

            if ev.type == pygame.MOUSEBUTTONDOWN:
                self.changerSelect(ev.pos)
                self.miseAjourParametres()

            if self.select == 0:
                self.changerMenu()
                self.afficherMenu()

            elif self.select == 1:
                ok = True
                for i in range(4):
                    ok = ok and self.testValeur(i)
                if ok:
                    g = LabyrintheGraphique(
                        Labyrinthe(
                            int(self.parametre[0].value),
                            int(self.parametre[2].value),
                            int(self.parametre[3].value),
                            int(self.parametre[1].value),
                        )
                    )
                    g.demarrer()
                    self.initMenu()
                    self.select = 0
                else:
                    self.select = 2

            elif self.select == 2:
                self.actualiserQuestion()
                self.afficherQuestion()
                self.changerMenuQuestion()

            elif self.select == 3:
                continuer = False
                print("here")

            pygame.display.flip()
        pygame.quit()


param = Menu()
param.demarrer()
