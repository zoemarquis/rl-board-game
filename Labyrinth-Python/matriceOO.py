import random

# -----------------------------------------
# contructeur et accesseurs
# -----------------------------------------


NB_LIGNES = 7


# crée une matrice de nbLignes lignes sur nbColonnes colonnes en mettant valeurParDefaut
# dans chacune des cases
class Matrice(object):

    def __init__(self, nbLignes, nbColonnes, valeurParDefaut=0):
        matrice = {}
        for i in range(nbLignes):
            for j in range(nbColonnes):
                matrice[(i, j)] = valeurParDefaut
        self.nbLignes = nbLignes
        self.nbColonnes = nbColonnes
        self.matrice = matrice

    # retourne le nombre de ligne de la matrice
    def getNbLignes(self):
        return self.nbLignes

    # retourne le nombre de colonnes de la matrice
    def getNbColonnes(self):
        return self.nbColonnes

    # retourne la valeur qui se trouve à la ligne et la colonne passées en paramètres
    def getVal(self, ligne, colonne):
        return self.matrice[ligne, colonne]

    # place la valeur à l'emplacement ligne colonne de la matrice
    def setVal(self, ligne, colonne, valeur):
        self.matrice[ligne, colonne] = valeur

    # decale la ligne numLig d'une case vers la gauche en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageLigneAGauche(self, numLig, nouvelleValeur=0):
        valeurEjecte = self.getVal(numLig, 0)
        for j in range(self.getNbColonnes() - 1):
            self.setVal(numLig, j, self.getVal(numLig, j + 1))
        self.setVal(numLig, self.getNbColonnes() - 1, nouvelleValeur)
        return valeurEjecte

    # decale la ligne numLig d'une case vers la droite en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageLigneADroite(self, numLig, nouvelleValeur=0):
        valeurEjecte = self.getVal(numLig, self.getNbColonnes() - 1)
        for j in range(self.getNbColonnes(), 0, -1):
            self.setVal(numLig, j, self.getVal(numLig, j - 1))
        self.setVal(numLig, 0, nouvelleValeur)
        return valeurEjecte

    # decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageColonneEnHaut(self, numCol, nouvelleValeur=0):
        valeurEjecte = self.getVal(0, numCol)
        for i in range(self.getNbLignes() - 1):
            self.setVal(i, numCol, self.getVal(i + 1, numCol))
        self.setVal(self.getNbLignes() - 1, numCol, nouvelleValeur)
        return valeurEjecte

    # decale la colonne numCol d'une case vers le bas en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageColonneEnBas(self, numCol, nouvelleValeur=0):
        valeurEjecte = self.getVal(self.getNbLignes() - 1, numCol)
        for i in range(self.getNbLignes(), 0, -1):
            self.setVal(i, numCol, self.getVal(i - 1, numCol))
        self.setVal(0, numCol, nouvelleValeur)
        return valeurEjecte

    # -----------------------------------------
    # entrées sorties
    # -----------------------------------------
    # sauvegarde une matrice en mode texte
    # ATTENTION NE MARCHE QUE POUR DES MATRICE CONTENANT DES TYPES SIMPLES
    def sauveMatrice(self, nomFic):
        fic = open(nomFic, "w")
        ligne = str(self.getNbLignes()) + "," + str(self.getNbColonnes()) + "\n"
        fic.write(ligne)
        for i in range(self.getNbLignes()):
            ligne = ""
            for j in range(self.getNbColonnes() - 1):
                val = self.getVal(i, j)
                if val == None:
                    ligne += ","
                else:
                    ligne += str(val) + ","
            val = self.getVal(i, j + 1)
            if val == None:
                ligne += "\n"
            else:
                ligne += str(val) + "\n"
            fic.write(ligne)
        fic.close()

    # construit une matrice à partir d'un fichier texte
    # ATTENTION NE MARCHE QUE POUR DES MATRICE CONTENANT DES TYPES SIMPLES
    def chargeMatrice(self, nomFic, typeVal="int"):
        fic = open(nomFic, "r")
        ligneLinCol = fic.readline()
        listeLinCol = ligneLinCol.split(",")
        matrice = Matrice(int(listeLinCol[0]), int(listeLinCol[1]))
        i = 0
        for ligne in fic:
            listeVal = ligne.split(",")
            j = 0
            for elem in listeVal:
                if elem == "" or elem == "\n":
                    self.setVal(i, j, None)
                elif typeVal == "int":
                    self.setVal(i, j, int(elem))
                elif typeVal == "float":
                    self.setVal(i, j, float(elem))
                elif typeVal == "bool":
                    self.setVal(i, j, bool(elem))
                else:
                    self.setVal(i, j, elem)
                j += 1
            i += 1
        return matrice

    # fonction utilitataire
    def afficheLigneSeparatrice(self, tailleCellule=4):
        print()
        for i in range(self.getNbColonnes() + 1):
            print("-" * tailleCellule + "+", end="")
        print()

    # fonction d'affichage d'une
    def afficheMatrice(self, tailleCellule=4):
        nbColonnes = self.getNbColonnes()
        nbLignes = self.getNbLignes()
        print(" " * tailleCellule + "|", end="")
        for i in range(nbColonnes):
            print(str(i).center(tailleCellule) + "|", end="")
        self.afficheLigneSeparatrice(tailleCellule)
        for i in range(nbLignes):
            print(str(i).rjust(tailleCellule) + "|", end="")
            for j in range(nbColonnes):
                print(str(self.getVal(i, j)).rjust(tailleCellule) + "|", end="")
            self.afficheLigneSeparatrice(tailleCellule)
        print()


################
# Zone de Test #
################
# print('='*10+' Test Matrice '+'='*10)
# mat1=Matrice(5,5)
# for i in range(5):
#     for j in range(5):
#         mat1.setVal(i,j,i+j)
# mat1.afficheMatrice()
# print(mat1.decalageLigneADroite(2))
# mat1.afficheMatrice()
# print(mat1.decalageLigneAGauche(2,6))
# mat1.afficheMatrice()
# print(mat1.decalageColonneEnBas(4))
# mat1.afficheMatrice()
# print(mat1.decalageColonneEnHaut(4,8))
# mat1.afficheMatrice()
# mat2=Matrice(4,4)
# mat2.setVal(0,0,1)
# mat2.afficheMatrice()
