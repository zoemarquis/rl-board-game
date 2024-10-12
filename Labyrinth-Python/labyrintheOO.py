from carteOO import *
from matriceOO import DIMENSION, Matrix
from joueurOO import *
import random
import os
import copy

TRESORS_FIXES = set([5, 13, 1, 7, 14, 22, 2, 8, 15, 23, 9, 16])


# permet de créer un labyrinthe avec nbJoueurs joueurs, nbTresors trésors
# chacun des joueurs aura au plus nbTresorMax à trouver
# si ce dernier paramètre est à 0, on distribuera le maximum de trésors possible
# à chaque joueur en restant équitable
# un joueur courant est choisi et la phase est initialisée
class Labyrinthe(object):
    def __init__(self, nbHumains=2, nbTresors=24, nbTresorMax=0, nbIA=0):
        self.joueurs = Joueurs(nbHumains + nbIA, nbTresors, nbTresorMax)
        self.joueurCourant = 1
        self.phase = 1
        self.nbTresors = nbTresors
        self.coupInter = ("N", 0)
        self.coordonneesJoueurCourant = (0, 0)
        # Ajout des IAs
        self.joueursIA = range(nbHumains + 1, nbHumains + nbIA + 1)
        if nbIA > 1:
            self.joueursIADef = range(nbHumains + nbIA, nbHumains + nbIA + 1)
        else:
            self.joueursIADef = []
        # Initialisation du plateau
        plateau = Matrix()
        # Cartes fixe
        plateau.set_value(0, 2, Carte(False, True, True, True, 5))  # grimoire
        plateau.set_value(0, 4, Carte(False, True, True, True, 13))  # bourse

        plateau.set_value(2, 0, Carte(True, True, True, False, 1))  # fiole
        plateau.set_value(2, 2, Carte(True, True, True, False, 7))  # couronne
        plateau.set_value(2, 4, Carte(False, True, True, True, 14))  # clef
        plateau.set_value(2, 6, Carte(True, False, True, True, 22))  # calice

        plateau.set_value(4, 0, Carte(True, True, True, False, 2))  # bague
        plateau.set_value(4, 2, Carte(True, True, False, True, 8))  # trésor
        plateau.set_value(4, 4, Carte(True, False, True, True, 15))  # pierre précieuse
        plateau.set_value(4, 6, Carte(True, False, True, True, 23))  # épée

        plateau.set_value(6, 2, Carte(True, True, False, True, 9))  # chandelier
        plateau.set_value(6, 4, Carte(True, True, False, True, 16))  # casque

        # Carte des joueurs fixe : les 4 coins
        plateau.set_value(0, 0, Carte(False, True, True, False, is_base=1))  # A
        plateau.set_value(0, 6, Carte(False, False, True, True, is_base=2))  # B
        plateau.set_value(6, 0, Carte(True, True, False, False, is_base=3))  # C
        plateau.set_value(6, 6, Carte(True, False, False, True, is_base=4))  # D

        # Placement des joueurs
        self.nbJoueurs = nbHumains + nbIA
        if self.nbJoueurs >= 1:
            plateau.get_value(0, 0).poserPion(1)  # A
        if self.nbJoueurs >= 2:
            plateau.get_value(0, 6).poserPion(2)  # B
        if self.nbJoueurs >= 3:
            plateau.get_value(6, 0).poserPion(3)  # C
        if self.nbJoueurs == 4:
            plateau.get_value(6, 6).poserPion(4)  # D

        # Trésors et cartes amovible
        listeCarte = creerCartesAmovibles(nbTresors)
        for i in range(7):
            for j in range(7):
                if (
                    i % 2 == 1 or j % 2 == 1
                ):  # Cela correspond aux emplacements non fixe
                    plateau.set_value(
                        i, j, listeCarte.pop(randint(0, len(listeCarte) - 1))
                    )
        self.carteAjouer = listeCarte[0]
        self.plateau = plateau

    ################
    # Les "getter" #
    ################

    def getPlateau(self):
        return self.plateau

    def getNbJoueurs(self):
        return self.joueurs.nbJoueurs

    def getJoueurCourant(self):
        return self.joueurCourant

    def getPhase(self):
        return self.phase

    def getCarteAJouer(self):
        return self.carteAjouer

    def getNbTresors(self):
        return self.nbTresors

    def getLesJoueurs(self):
        return self.joueurs

    def getTresorCourant(self):
        return self.joueurs.prochainTresor(self.getJoueurCourant())

    def getCoupInterdit(self):
        return self.coupInter

    # retourne sous la forme d'un couple (lin,col) la position du trésor à trouver
    # pour le joueur courant sur le plateau
    def getCoordonneesTresorCourant(self):
        coord = None
        tresor = self.getTresorCourant()
        finL = DIMENSION
        finC = DIMENSION
        i = 0
        while i < finL and coord == None:
            j = 0
            while j < finC and coord == None:
                if self.plateau.get_value(i, j).getTresor() == tresor:
                    coord = (i, j)
                else:
                    j += 1
            i += 1
        return coord

    # retourne sous la forme d'un couple (lin,col) la position du joueur courant sur le plateau
    def getCoordonneesJoueurCourant(self):
        coord = None
        finL = DIMENSION
        finC = DIMENSION
        i = 0
        while i < finL and coord == None:
            j = 0
            while j < finC and coord == None:
                if self.plateau.get_value(i, j).possedePion(self.getJoueurCourant()):
                    coord = (i, j)
                else:
                    j += 1
            i += 1
        return coord

    # change la phase de jeu
    def changerPhase(self):
        if self.getPhase() == 1:
            self.phase = 2
        else:
            self.phase = 1

    # diminue le nombre de trésors de 1
    def decTresor(self):
        self.nbTresors -= 1

    # Test si le joueur courant est un IA attaquant
    def joueurCourantIsIA(self):
        return self.joueurCourant in self.joueursIA

    # Test si le joueur courant est un IA defensif
    def joueurCourantIsIADef(self):
        return self.joueurCourant in self.joueursIADef

    # change de joueur courant
    def changerJoueurCourant(self):
        if self.getJoueurCourant() == self.getNbJoueurs():
            self.joueurCourant = 1
        else:
            self.joueurCourant += 1
        self.coordonneesJoueurCourant = self.getCoordonneesJoueurCourant()

    # met à jour la structure qui gère les joueurs en enlevant le trésor que le joueur
    # courant vient de trouver
    def joueurCourantTrouveTresor(self):
        return self.joueurs.tresorTrouve(self.joueurCourant)

    # retourne le nombre de trésors restant à trouver pour le joueur numJoueur
    def nbTresorsRestantsJoueur(self, numJoueur):
        return self.joueurs.nbTresorsRestants(numJoueur)

    # enlève le trésor numTresor sur la carte qui se trouve sur la case lin,col du plateau
    # si le trésor ne s'y trouve pas la fonction ne fait rien
    def prendreTresorL(self, lin, col, numTresor):
        if self.plateau.get_value(lin, col).getTresor() == numTresor:
            self.plateau.get_value(lin, col).prendreTresor()

    # enlève le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    # si le joueur ne s'y trouve pas la fonction ne fait rien
    def prendreJoueurCourant(self, lin, col):
        self.plateau.get_value(lin, col).prendrePion(self.getJoueurCourant())

    # pose le joueur courant de la carte qui se trouve sur la case lin,col du plateau
    # si le joueur s'y trouve déjà la fonction ne fait rien
    def poserJoueurCourant(self, lin, col):
        self.plateau.get_value(lin, col).poserPion(self.getJoueurCourant())

    # fonction qui retourne True si le coup proposé correspond au coup interdit
    # elle retourne False sinon
    def coupInterdit(self, direction, rangee):
        d, r = self.getCoupInterdit()
        return d == direction and r == rangee

    # fonction qui joue la carte amovible dans la direction et sur la rangée passées
    # en paramètres. Cette fonction
    #      - met à jour le plateau du labyrinthe
    #      - met à jour la carte à jouer
    #      - met à jour la nouvelle direction interdite
    def jouerCarte(self, direction, rangee):
        if direction == "N":
            self.carteAjouer = self.plateau.shift_column_down(rangee, self.carteAjouer)
            self.coupInter = ("S", rangee)
        if direction == "E":
            self.carteAjouer = self.plateau.shift_row_left(rangee, self.carteAjouer)
            self.coupInter = ("O", rangee)
        if direction == "S":
            self.carteAjouer = self.plateau.shift_column_up(rangee, self.carteAjouer)
            self.coupInter = ("N", rangee)
        if direction == "O":
            self.carteAjouer = self.plateau.shift_row_right(rangee, self.carteAjouer)
            self.coupInter = ("E", rangee)
        pions = self.carteAjouer.getListePions()
        for pion in pions:
            self.carteAjouer.prendrePion(pion)
            if pion == 1:
                self.poserPionL(6, 6, 1)
            if pion == 2:
                self.poserPionL(0, 6, 2)
            if pion == 3:
                self.poserPionL(6, 0, 3)
            if pion == 4:
                self.poserPionL(0, 0, 4)
        self.coordonneesJoueurCourant = self.getCoordonneesJoueurCourant()

    # Cette fonction tourne la carte à jouer dans le sens indiqué
    # en paramètre (H horaire A antihoraire)
    def tournerCarte(self, sens="H"):
        if sens == "H":
            self.carteAjouer.tournerHoraire()
        else:
            self.carteAjouer.tournerAntiHoraire()

    # prend le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
    def prendrePionL(self, lin, col, numJoueur):
        self.plateau.get_value(lin, col).prendrePion(numJoueur)

    # pose le pion numJoueur sur sur la carte se trouvant en position lin,col du plateau
    def poserPionL(self, lin, col, joueur):
        self.plateau.get_value(lin, col).poserPion(joueur)

    # indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
    # Fonction marquant les case autour d'une case dont la valeur est val et qui est accessible
    def marquer(self, mat, val, marque):
        changer = False
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if mat.get_value(i, j) == val:
                    if i > 0:
                        if self.plateau.get_value(i, j).passageNord(
                            self.plateau.get_value(i - 1, j)
                        ):
                            if mat.get_value(i - 1, j) == 0:
                                mat.set_value(i - 1, j, marque)
                                changer = True
                    if i < DIMENSION - 1:
                        if self.plateau.get_value(i, j).passageSud(
                            self.plateau.get_value(i + 1, j)
                        ):
                            if mat.get_value(i + 1, j) == 0:
                                mat.set_value(i + 1, j, marque)
                                changer = True
                    if j > 0:
                        if self.plateau.get_value(i, j).passageOuest(
                            self.plateau.get_value(i, j - 1)
                        ):
                            if mat.get_value(i, j - 1) == 0:
                                mat.set_value(i, j - 1, marque)
                                changer = True
                    if j < DIMENSION - 1:
                        if self.plateau.get_value(i, j).passageEst(
                            self.plateau.get_value(i, j + 1)
                        ):
                            if mat.get_value(i, j + 1) == 0:
                                mat.set_value(i, j + 1, marque)
                                changer = True
        return changer

    def accessible(self, ligD, colD, ligA, colA):
        matTest = Matrix()
        matTest.set_value(ligD, colD, 1)
        changer = True
        while changer and matTest.get_value(ligA, colA) == 0:
            changer = self.marquer(matTest, 1, 1)
        return matTest.get_value(ligA, colA) == 1

    # indique si il y a un chemin entre la case ligD,colD et la case ligA,colA du labyrinthe
    # mais la valeur de retour est None s'il n'y a pas de chemin, sinon c'est un chemin possible entre ces deux cases
    def accessibleDist(self, ligD, colD, ligA, colA):
        if not self.accessible(ligD, colD, ligA, colA):
            return []
        else:
            matTest = Matrix()
            matTest.set_value(ligD, colD, 1)
            changer = True
            i = 1
            while changer and matTest.get_value(ligA, colA) == 0:
                changer = self.marquer(matTest, i, i + 1)
                i += 1
            x, y = ligA, colA
            chemin = [(x, y)]
            val = matTest.get_value(x, y)
            while x != ligD or y != colD:
                if x > 0:
                    if 0 < matTest.get_value(
                        x - 1, y
                    ) == val - 1 and self.plateau.get_value(x, y).passageNord(
                        self.plateau.get_value(x - 1, y)
                    ):
                        x -= 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if y > 0:
                    if 0 < matTest.get_value(
                        x, y - 1
                    ) == val - 1 and self.plateau.get_value(x, y).passageOuest(
                        self.plateau.get_value(x, y - 1)
                    ):
                        y -= 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if x < DIMENSION - 1:
                    if 0 < matTest.get_value(
                        x + 1, y
                    ) == val - 1 and self.plateau.get_value(x, y).passageSud(
                        self.plateau.get_value(x + 1, y)
                    ):
                        x += 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
                if y < DIMENSION - 1:
                    if 0 < matTest.get_value(
                        x, y + 1
                    ) == val - 1 and self.plateau.get_value(x, y).passageEst(
                        self.plateau.get_value(x, y + 1)
                    ):
                        y += 1
                        chemin.append((x, y))
                        val = matTest.get_value(x, y)
            chemin.reverse()
            return chemin

    # verifie si le joueur courant peut accéder la case ligA,colA
    # si c'est le cas la fonction retourne une liste représentant un chemin possible
    # sinon ce n'est pas le cas, la fonction retourne None
    def accessibleDistJoueurCourant(self, ligA, colA):
        (ligD, colD) = self.getCoordonneesJoueurCourant()
        return self.accessibleDist(ligD, colD, ligA, colA)

    ###################
    # Gestion de l'IA #
    ###################
    # L'idée est de testé toutes les possibilité avec une copie du labyrinte

    # fonction renvoyant la position accessible a partir de posDepart où la distance entre posDepart et posCible est minimale ( recherche en "étoile" )
    def getPositionMinDistance(self, posCible, posDepart):
        listePos = {posCible}
        dist = 0
        xD, yD = posDepart
        continuer = True
        while (
            continuer
        ):  # La boucle s'arrete quand on trouve une position accessible au plus pres de la pôsition Cible
            listeNewPos = (
                set()
            )  # On utilise un ensemble afin de reduire le nombre de calculs, mais cela oblige a mettre un return dans la boucle for
            ld = []
            for pos in listePos:
                x, y = pos
                if x > 0:
                    xN = x - 1
                    yN = y
                    d = distance((xN, y), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(xN, y, xD, yD):
                            continuer = False
                            return ((xN, y), d)
                        else:
                            listeNewPos.add((xN, y))
                if DIMENSION - 1 > x:
                    xN = x + 1
                    yN = y
                    d = distance((xN, y), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(xN, y, xD, yD):
                            continuer = False
                            return ((xN, y), d)
                        else:
                            listeNewPos.add((xN, y))
                if y > 0:
                    yN = y - 1
                    xN = x
                    d = distance((x, yN), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(x, yN, xD, yD):
                            continuer = False
                            return ((x, yN), d)
                        else:
                            listeNewPos.add((x, yN))
                if DIMENSION - 1 > y:
                    yN = y + 1
                    xN = x
                    d = distance((x, yN), posCible)
                    if d > dist:
                        ld.append(d)
                        if self.accessible(x, yN, xD, yD):
                            continuer = False
                            return ((x, yN), d)
                        else:
                            listeNewPos.add((x, yN))
            dist = min(ld)
            listePos = listeNewPos

    # Calcul la "meilleur" action celle ou le joueurCourant peut trouver son tresor si c'est possible,
    # sinon l'action choisie est celle minimisant la distance de ce joueur au tresors apres s'être déplacé,
    # revoie le chemin du joueur a effectuer
    # Change l'orientation de la carte et le coup interdit
    def getMeilleurAction(self):
        actionsPossible = []
        lDirection = ["N", "E", "S", "O"]
        lRangee = [1, 3, 5]
        nbRotation = 0
        continuer = True
        while nbRotation < 4 and continuer:
            j = 0
            while j < len(lDirection) and continuer:
                direction = lDirection[j]
                k = 0
                while k < len(lRangee) and continuer:
                    rangee = lRangee[k]
                    labyTest = copy.deepcopy(self)
                    labyTest.jouerCarte(direction, rangee)
                    posT = labyTest.getCoordonneesTresorCourant()
                    xJ, yJ = labyTest.getCoordonneesJoueurCourant()
                    if posT != None:  # Cas ou le tresors sort du plateau
                        xT, yT = posT
                        if labyTest.accessible(xJ, yJ, xT, yT):
                            self.jouerCarte(direction, rangee)
                            continuer = False
                        else:
                            (xC, yC), d = labyTest.getPositionMinDistance(
                                (xT, yT), (xJ, yJ)
                            )
                            if xC != xJ or yC != yJ or actionsPossible == []:
                                actionsPossible.append(
                                    (nbRotation, direction, rangee, xC, yC, d)
                                )
                    k += 1
                j += 1
            self.tournerCarte()
            nbRotation += 1

        if continuer:

            def getDistance(elem):
                return elem[5]

            (nbRotation, direction, rangee, xC, yC, d) = min(
                actionsPossible, key=getDistance
            )
            for i in range(nbRotation):
                self.tournerCarte()
            self.jouerCarte(direction, rangee)
            xJ, yJ = self.getCoordonneesJoueurCourant()
            return self.accessibleDist(xJ, yJ, xC, yC)
        else:
            return self.accessibleDist(xJ, yJ, xT, yT)

    # Fonction cherchant le meilleur coup pour empecher le joueur suivant de trouver son tresor
    def getMeilleurActionDefensive(self):
        actionsPossible = []
        lDirection = ["N", "E", "S", "O"]
        lRangee = [1, 3, 5]
        i = 0
        continuer = True
        while i < len(lDirection) and continuer:
            direction = lDirection[i]
            j = 0
            while j < len(lRangee) and continuer:
                rangee = lRangee[j]
                nbRotation = 0
                while nbRotation < 4 and continuer:
                    # On crée une copy du labyrinthe pour ne pas altérer la structure initiale
                    labyTest = copy.deepcopy(self)
                    for i in range(nbRotation):
                        labyTest.tournerCarte()
                    labyTest.jouerCarte(direction, rangee)
                    labyTest.changerJoueurCourant()
                    cptCoupGG = 0
                    for nbRotationT in range(4):
                        labyTest.tournerCarte()
                        for directionT in "NESO":
                            for rangeeT in [1, 3, 5]:
                                if (directionT, rangeeT) != labyTest.getCoupInterdit():
                                    # On crée une seconde copy pour tester les possibilités du joueur suivant
                                    labyTest2 = copy.deepcopy(labyTest)
                                    labyTest2.jouerCarte(directionT, rangeeT)
                                    posT = labyTest2.getCoordonneesTresorCourant()
                                    xJ, yJ = labyTest2.getCoordonneesJoueurCourant()
                                    if posT != None:
                                        xT, yT = posT
                                        if labyTest2.accessible(xT, yT, xJ, yJ):
                                            cptCoupGG += 1
                    if cptCoupGG == 0:
                        continuer = False
                    else:
                        actionsPossible.append(
                            (nbRotation, direction, rangee, cptCoupGG)
                        )
                    nbRotation += 1
                j += 1
            i += 1
        if continuer:

            def getNbCoupGG(elem):
                return elem[3]

            (nbRotation, direction, rangee, cptCoupGG) = min(
                actionsPossible, key=getNbCoupGG
            )
        return (nbRotation, direction, rangee)

    # Renvoie le chemin de l'IA défensive, utilise la fonction getMeilleurActionDefensive pour recupérer l'action
    # et getPositionMinDistance pour buger au plus pres de son tresors ( sait on jamais )
    def getCheminDefensif(self):
        (nbRotation, direction, rangee) = self.getMeilleurActionDefensive()
        for i in range(nbRotation):
            self.tournerCarte()
        self.jouerCarte(direction, rangee)
        xJ, yJ = self.getCoordonneesJoueurCourant()
        ((xD, yD), _) = self.getPositionMinDistance(
            self.getCoordonneesTresorCourant(), (xJ, yJ)
        )
        return self.accessibleDist(xJ, yJ, xD, yD)

    ######################
    # Gestion Cheat Code #
    ######################

    # Ajoute un caractere code dans le code du joueur courant
    def ajouterCode(self, code):
        self.joueurs.ajouterCode(code, self.joueurCourant)

    # supprime un caractere code dans le code du joueur courant
    def supprimerCode(self):
        self.joueurs.effacerCode(self.joueurCourant)

    # Efface tout le code du joueur courant
    def effacerDernierCode(self):
        self.joueurs.effacerDernierCode(self.joueurCourant)

    # Permet de recuperer le code du joueur courant
    def getCode(self):
        return self.joueurs.getCode(self.joueurCourant)

    # Permet de verifier si le code du joueur courant est bon ( on peut ainsi changer le bon code ici )
    def estBonCode(self):
        return self.getCode() == [2, 7, 1, 3]


#############################################################
# Fonction Utilitaire ne dépandant pas de l'objet labyrinte #
#############################################################
# fonction qui permet de créer les cartes amovibles du jeu en y positionnant aléatoirement nbTresor Trésors
# la fonction retourne la liste, mélangée aléatoirement, des cartes ainsi créées
def creerCartesAmovibles(nbTresors):
    listeCarte = []
    for i in range(16):  # 16 carte coude
        carte = Carte(True, True, False, False)
        carte.tourneAleatoire()
        listeCarte.append(carte)
    for i in range(12):  # 12 carte tout-droit
        carte = Carte(True, False, True, False)
        carte.tourneAleatoire()
        listeCarte.append(carte)
    for i in range(6):  # 6 carte T
        carte = Carte(True, True, True, False)
        carte.tourneAleatoire()
        listeCarte.append(carte)
    random.shuffle(listeCarte)
    # Placer les trésors sur les cartes (attention à ne pas mettre les trésors déjà sur cartes fixes
    for tresor in range(1, nbTresors + 1):
        if not tresor in TRESORS_FIXES:
            listeCarte[tresor].mettreTresor(tresor)
    return listeCarte


def distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + ((pos1[1] - pos2[1]) ** 2)) ** (0.5)


################
# Zone de Test #
################
# print('='*10+' Test sur le labyrinthe '+'='*10)
# laby=Labyrinthe()
# matC=Matrice(7,7)
# matT=Matrice(7,7)
# matP=Matrice(7,7)
# for i in range(7):
#     for j in range(7):
#          matC.set_value(i,j,laby.plateau.get_value(i,j).toChar())
#          matT.set_value(i,j,laby.plateau.get_value(i,j).getTresor())
#          matP.set_value(i,j,laby.plateau.get_value(i,j).getListePions())
# print('Matrice des cartes :\n')
# matC.afficheMatrice()
# print('matrice des tresors :')
# matT.afficheMatrice()
# print('matrice des pions :')
# matP.afficheMatrice()
# print('Nb joueurs:',laby.getNbJoueurs())
# print('Joueur courant:',laby.getJoueurCourant())
# laby.changerJoueurCourant()
# print('Nouveau joueur courant:',laby.getJoueurCourant())
# print('Phase de Jeu:',laby.getPhase())
# laby.changerPhase()
# print('Nouvelle phase de jeu:',laby.getPhase())
# print('tresors restants dans le laby :',laby.getNbTresors())
# laby.decTresor()
# print('Tresors restants dans le laby :',laby.getNbTresors())
# print('structure des joueurs:',laby.getLesJoueurs())
# print('Nombre de tresors restant du j2:',laby.nbTresorsRestantsJoueur(2))
# laby.joueurCourantTrouveTresor()
# print('Nombre de tresors restant du j2:',laby.nbTresorsRestantsJoueur(2))
# print(laby.accessibleDist(0,0,1,1))

# print('Test fonction getPositionMinDistance :',laby.getPositionMinDistance((5,5),(0,0)))
# print('Test fonction getMeilleurAction',laby.getMeilleurAction())
# for i in range(7):
#     for j in range(7):
#          matC.set_value(i,j,laby.plateau.get_value(i,j).toChar())

# print('Matrice des cartes :\n')
# matC.afficheMatrice()
