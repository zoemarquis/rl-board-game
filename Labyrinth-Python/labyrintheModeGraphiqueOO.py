from labyrintheOO import *
from eztext import *
import pygame
import time
import sys
import os


AUCUNE = 0
ALPHA = 1
NUMERIQUE = 2

NB_JOUEUR = 4
NB_TRESOR = 24


class LabyrintheGraphique(object):
    """Classe simple d'affichage et d'interaction pour le labyrinthe."""

    def __init__(
        self,
        labyrinthe,
        titre="Labyrinthe",
        size=(1500, 900),
        couleur=(209, 238, 238),
        prefixeImage="./original_images",
    ):
        """Method docstring."""
        self.messageInfo = None
        self.imgInfo = None
        self.labyrinthe = labyrinthe
        self.fini = False
        self.couleurTexte = couleur
        self.laMatrice = labyrinthe.plateau
        self.nbColonne = self.laMatrice.getNbColonnes()
        self.nbLigne = self.laMatrice.getNbLignes()
        self.titre = titre
        self.cheat = False
        self.getImages(prefixeImage)
        pygame.init()
        pygame.display.set_icon(self.icone)
        fenetre = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.surface.fill((0, 0, 130))
        self.miseAjourParametres()
        self.afficheJeu()

    def getImages(self, prefixImage="./original_images"):
        self.imagesCartes = []
        for i in range(16):
            if os.path.isfile(os.path.join(prefixImage, "Carte" + str(i) + ".png")):
                s = pygame.image.load(
                    os.path.join(prefixImage, "Carte" + str(i) + ".png")
                )
            else:
                s = None
            self.imagesCartes.append(s)
        # load images
        self.imagesPions = []
        self.imagesBases = []
        for i in range(1, NB_JOUEUR + 1):
            s = pygame.image.load(os.path.join(prefixImage, "pion" + str(i) + ".png"))
            self.imagesPions.append(s)
            s = pygame.image.load(os.path.join(prefixImage, "base" + str(i) + ".png"))
            self.imagesBases.append(s)
        self.imagesTresors = []
        for i in range(1, NB_TRESOR + 1):
            s = pygame.image.load(os.path.join(prefixImage, "tresor" + str(i) + ".png"))
            self.imagesTresors.append(s)
        # no random on all images
        # random.shuffle(self.imagesTresors)
        self.icone = pygame.image.load(os.path.join(prefixImage, "logo.png"))
        self.bousole = pygame.image.load(os.path.join(prefixImage, "boussole.png"))

    def miseAjourParametres(self):
        self.surface = pygame.display.get_surface()
        self.dimension = self.surface.get_height()  # *2//3
        self.delta = self.dimension // (self.nbLigne + 2)
        self.finh = self.delta * (self.nbLigne + 2)
        self.finl = self.delta * (self.nbColonne + 2)
        self.tailleFont = min(self.delta, self.delta) * 1 // 3

    def surfaceCarte(self, carte):
        tresor = carte.getTresor()
        base = carte.isBase()
        pions = carte.getListePions()
        img = self.imagesCartes[carte.coderMurs()]
        if img == None:
            return None

        surfCarte = pygame.transform.smoothscale(img, (self.delta, self.delta))
        if base != 0:
            surfBase = pygame.transform.smoothscale(
                self.imagesBases[base - 1], (self.delta // 2, self.delta // 2)
            )
            base_x = (self.delta - surfBase.get_width()) // 2
            base_y = (self.delta - surfBase.get_height()) // 2
            surfCarte.blit(surfBase, (base_x, base_y))
        if tresor != 0:
            surfTresor = pygame.transform.smoothscale(
                self.imagesTresors[tresor - 1], (self.delta // 2, self.delta // 2)
            )
            base_x = (self.delta - surfTresor.get_width()) // 2
            base_y = (self.delta - surfTresor.get_height()) // 2
            surfCarte.blit(surfTresor, (base_x, base_y))

        dist = 10
        coord = [
            (dist, dist),
            (dist, self.delta - (self.delta // 4 + dist)),
            (
                self.delta - (self.delta // 4 + dist),
                self.delta - (self.delta // 4 + dist),
            ),
            (self.delta - (self.delta // 4 + dist), dist),
        ]
        for pions in pions:
            surfPion = pygame.transform.smoothscale(
                self.imagesPions[pions - 1], (self.delta // 4, self.delta // 4)
            )
            surfCarte.blit(surfPion, coord.pop(0))
        return surfCarte

    def surfaceFleche(self, direction="O", couleur=(209, 238, 238)):
        res = pygame.Surface((self.delta, self.delta))
        pygame.draw.polygon(
            res,
            couleur,
            [
                (self.delta // 2, self.delta // 3),
                (self.delta - self.delta // 8, self.delta // 2),
                (self.delta // 2, self.delta * 2 // 3),
            ],
            0,
        )
        if direction == "N":
            res = pygame.transform.rotate(res, -90.0)
        elif direction == "E":
            res = pygame.transform.rotate(res, 180.0)
        elif direction == "S":
            res = pygame.transform.rotate(res, 90.0)
        return res

    def surfacePion(self, pion):
        res = pygame.Surface((self.delta, self.delta))
        surfPion = pygame.transform.smoothscale(
            self.imagesPions[pion - 1], (self.delta // 2, self.delta // 2)
        )
        res.blit(surfPion, (self.delta // 4, self.delta // 4))
        return res

    def surfaceTresor(self, tresor):
        res = pygame.Surface((self.delta, self.delta))
        surfTresor = pygame.transform.smoothscale(
            self.imagesTresors[tresor - 1], (self.delta // 2, self.delta // 2)
        )
        res.blit(surfTresor, (self.delta // 4, self.delta // 4))
        return res

    def afficheMessage(self, ligne, texte, images=[], couleur=None):
        font = pygame.font.Font(None, self.tailleFont)
        if couleur == None:
            couleur = self.couleurTexte

        # posy=self.finh+self.deltah*(ligne-1)
        # posx=self.deltal//3
        posy = self.delta * (
            ligne - 1
        )  # Garde la même hauteur pour chaque ligne de texte
        posx = (
            self.finl + self.delta
        )  # Déplace à droite du plateau en utilisant la largeur du plateau

        # self.surface.fill((0,0,0),(0,posy,self.surface.get_width(),posy+self.deltah))

        listeTextes = texte.split("@img@")
        for msg in listeTextes:
            if msg != "":
                texte = font.render(msg, 1, couleur)
                textpos = texte.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(texte, textpos)
                posx += textpos.width  # +(self.deltal//3)
            if images != []:
                surface = images.pop(0)
                debuty = posy - (self.delta // 3)
                self.surface.blit(surface, (posx, debuty))
                posx += surface.get_width()  # +(self.deltal//3)

    def afficheScore(self, numLigne=3):
        texte = "Nb trésors restants:"
        img = []
        for i in range(self.labyrinthe.getNbJoueurs()):
            texte += " @img@ " + str(
                self.labyrinthe.nbTresorsRestantsJoueur(i + 1)
            )  # ERREUR ici nbTresorsRestants au lieu de nbTresorsRestantsJoueur
            img.append(self.surfacePion(i + 1))
        self.afficheMessage(numLigne, texte, img)

    def afficheMessageInfo(self, numLigne=4):
        if self.messageInfo != None:
            self.afficheMessage(numLigne, self.messageInfo, self.imgInfo)
        self.messageInfo = None
        self.imgInfo = None

    def afficheCarteAJouer(self):
        self.surface.blit(
            self.surfaceCarte(self.labyrinthe.carteAjouer),
            (self.finl + self.delta // 2, self.finh // 2),
        )  # Ici, carte == carteAjouer

    def dessineGrille(self, couleur=(255, 255, 0)):
        for i in range(1, self.nbLigne, 2):
            self.surface.blit(self.surfaceFleche("O", couleur), (0, (i + 1) * self.delta))
            self.surface.blit(self.surfaceFleche("E", couleur), (self.delta * (self.nbColonne + 1), (i + 1) * self.delta))

        for i in range(1, self.nbColonne, 2):
            self.surface.blit(self.surfaceFleche("N", couleur), ((i + 1) * self.delta, 0))
            self.surface.blit(self.surfaceFleche("S", couleur), ((i + 1) * self.delta, self.delta * (self.nbLigne + 1)))

    def afficheGrille(self):
        font = pygame.font.Font(None, self.tailleFont)
        for i in range(self.nbLigne):
            for j in range(self.nbColonne):
                try:
                    carte = self.laMatrice.getVal(i, j)
                    s = self.surfaceCarte(carte)
                    if s == None:
                        self.surface.fill(
                            (0, 0, 0),
                            (
                                (j + 1) * self.delta,
                                (i + 1) * self.delta,
                                self.delta,
                                self.delta,
                            ),
                        )
                    else:
                        self.surface.blit(
                            s, ((j + 1) * self.delta, (i + 1) * self.delta)
                        )
                except:
                    pass

    def animationChemin(self, chemin, joueur, pause=0.2):
        (xp, yp) = chemin.pop(0)
        for x, y in chemin:
            self.labyrinthe.prendreJoueurCourant(xp, yp)  # pas la bonne fonction
            self.labyrinthe.poserJoueurCourant(x, y)  # la meme
            self.afficheJeu()
            time.sleep(pause)
            xp, yp = x, y
        return xp, yp

    def parcoursChemin(self):
        chemin = self.leJeu.getChemin()
        if chemin == None or chemin == []:
            return
        pos = chemin.pop(0)
        val = self.laMatrice.getVal(pos[0], pos[1])
        for elem in chemin:
            self.laMatrice.setVal(pos[0], pos[1], 0)
            self.laMatrice.setVal(elem[0], elem[1], val)
            self.afficheGrille()
            pygame.display.flip()
            pos = elem
            time.sleep(0.1)
        self.leJeu.unsetChemin()
        return pos

    def getCase(self, pos):
        if (
            self.finl + self.delta // 2
            <= pos[0]
            <= self.finl + self.delta // 2 + self.delta
            and self.finh // 2 <= pos[1] <= self.finh // 2 + self.delta
        ):
            return ("T", "T")
        if pos[0] < 0 or pos[0] > self.finl or pos[1] < 0 or pos[1] > self.finh:
            return (-1, -1)

        x = pos[1] // self.delta
        y = pos[0] // self.delta
        if x == 0 and y in [2, 4, 6]:
            return ("N", y - 1)
        if x == self.nbColonne + 1 and y in [2, 4, 6]:
            return ("S", y - 1)
        if y == 0 and x in [2, 4, 6]:
            return ("O", x - 1)
        if y == self.nbLigne + 1 and x in [2, 4, 6]:
            return ("E", x - 1)
        if x == 0 or x == self.nbColonne + 1 or y == 0 or y == self.nbLigne + 1:
            return (-1, -1)
        return (x - 1, y - 1)

    def afficheJeu(self):
        self.dessineGrille()
        self.afficheGrille()
        if not self.fini:
            if self.labyrinthe.joueurCourantIsIA():
                self.afficheMessage(
                    2,
                    "C'est au tour de l'IA@img@",
                    [self.surfacePion(self.labyrinthe.getJoueurCourant())],
                )
                self.afficheMessage(
                    3,
                    "Trésor à trouver :@img@",
                    [self.surfaceTresor(self.labyrinthe.getTresorCourant())],
                )
            else:
                self.afficheMessage(
                    2,
                    "C'est au tour du joueur@img@",
                    [self.surfacePion(self.labyrinthe.getJoueurCourant())],
                )
                self.afficheMessage(
                    3,
                    "Trésor à trouver :@img@",
                    [self.surfaceTresor(self.labyrinthe.getTresorCourant())],
                )
        self.afficheScore(4)
        self.afficheMessageInfo(5)
        self.afficheCarteAJouer()
        pygame.display.flip()

    def demarrer(self):
        self.phase = 1
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        while True:
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.USEREVENT + 1:
                pygame.display.flip()
            if ev.type == pygame.VIDEORESIZE:
                fenetre = pygame.display.set_mode(
                    ev.size, pygame.RESIZABLE | pygame.DOUBLEBUF
                )
                self.miseAjourParametres()
                self.afficheJeu()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    break
            if not self.labyrinthe.joueurCourantIsIA():
                if ev.type == KEYDOWN:
                    if ev.key == K_KP0:
                        self.labyrinthe.ajouterCode(0)
                    if ev.key == K_KP1:
                        self.labyrinthe.ajouterCode(1)
                    if ev.key == K_KP2:
                        self.labyrinthe.ajouterCode(2)
                    if ev.key == K_KP3:
                        self.labyrinthe.ajouterCode(3)
                    if ev.key == K_KP4:
                        self.labyrinthe.ajouterCode(4)
                    if ev.key == K_KP5:
                        self.labyrinthe.ajouterCode(5)
                    if ev.key == K_KP6:
                        self.labyrinthe.ajouterCode(6)
                    if ev.key == K_KP7:
                        self.labyrinthe.ajouterCode(7)
                    if ev.key == K_KP8:
                        self.labyrinthe.ajouterCode(8)
                    if ev.key == K_KP9:
                        self.labyrinthe.ajouterCode(9)
                    if ev.key == K_BACKSPACE:
                        self.labyrinthe.effacerDernierCode()
                    if ev.key == K_RETURN:
                        if self.labyrinthe.estBonCode():
                            self.cheat = True
                            self.messageInfo = "Mode invincible activé. Profitez-en !"
                            self.imgInfo = []
                            self.labyrinthe.supprimerCode()
                        else:
                            self.cheat = False
                            self.messageInfo = "Mode invincible désactivé."
                            self.imgInfo = []
                        self.afficheJeu()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = self.getCase(ev.pos)
                    if self.fini:
                        continue

                    if self.phase == 1:
                        if x == "T":
                            self.labyrinthe.tournerCarte()
                        elif x in ["N", "S", "O", "E"]:
                            if self.labyrinthe.coupInterdit(x, y):
                                self.messageInfo = (
                                    "Coup interdit : mouvement opposé au dernier."
                                )
                                self.imgInfo = []
                            else:
                                self.labyrinthe.jouerCarte(x, y)
                                self.phase = 2
                        elif x != -1:
                            self.messageInfo = (
                                "Insérez d'abord la carte avant de bouger."
                            )
                            self.imgInfo = []
                    else:
                        if x in ["T", "N", "S", "O", "E", -1]:
                            self.messageInfo = (
                                "Sélectionnez une case dans le labyrinthe."
                            )
                            self.imgInfo = []
                        else:
                            if self.cheat:
                                self.labyrinthe.plateau.getVal(x, y).tournerHoraire()
                            else:
                                jc = self.labyrinthe.getJoueurCourant()
                                xD, yD = self.labyrinthe.coordonneesJoueurCourant
                                chemin = self.labyrinthe.accessibleDist(xD, yD, x, y)

                                if len(chemin) == 0:
                                    self.messageInfo = "Cette case est inaccessible pour le joueur @img@."
                                    self.imgInfo = [self.surfacePion(jc)]
                                else:
                                    self.animationChemin(chemin, jc)
                                    c = self.labyrinthe.plateau.getVal(x, y)
                                    t = self.labyrinthe.getTresorCourant()
                                    if c.getTresor() == t:
                                        c.prendreTresor()
                                        if (
                                            self.labyrinthe.joueurCourantTrouveTresor()
                                            == 0
                                        ):
                                            self.messageInfo = "Le joueur @img@ a gagné"
                                            self.imgInfo = [self.surfacePion(jc)]
                                            self.fini = True
                                        else:
                                            self.messageInfo = "Le joueur @img@ a trouvé le trésor @img@."
                                            self.imgInfo = [
                                                self.surfacePion(jc),
                                                self.surfaceTresor(t),
                                            ]

                                    self.labyrinthe.changerJoueurCourant()
                                    self.phase = 1

                    self.afficheJeu()
            elif not self.fini:
                if self.labyrinthe.joueurCourantIsIADef():
                    chemin = self.labyrinthe.getCheminDefensif()
                else:
                    chemin = self.labyrinthe.getMeilleurAction()
                jc = self.labyrinthe.getJoueurCourant()
                self.animationChemin(chemin, jc)
                x, y = self.labyrinthe.getCoordonneesJoueurCourant()
                c = self.labyrinthe.plateau.getVal(x, y)
                t = self.labyrinthe.getTresorCourant()
                if c.getTresor() == t:
                    c.prendreTresor()
                    if self.labyrinthe.joueurCourantTrouveTresor() == 0:
                        self.messageInfo = "L'IA @img@ a gagné !!!"
                        self.imgInfo = [self.surfacePion(jc)]
                        self.fini = True
                    else:
                        self.messageInfo = "L'IA @img@ a trouvé le trésor @img@"
                        self.imgInfo = [self.surfacePion(jc), self.surfaceTresor(t)]

                self.labyrinthe.changerJoueurCourant()
                self.afficheJeu()
            pygame.display.flip()
