DIMENSION = 7

class Matrix(object):
    ''' Class representing a matrix of NB_ROWS * NB_ROWS with default value in each cell ''' 

    def __init__(self, default_value=0):
        matrix = {}
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                matrix[(i, j)] = default_value
        self.matrix = matrix

    def get_value(self, row, col):
        ''' Return the value in the matrix at the line and column passed as parameters '''
        assert row >= 0 and row < DIMENSION, "Row out of bounds"
        assert col >= 0 and col < DIMENSION, "Column out of bounds"
        return self.matrix[row, col]

    def set_value(self, row, col, value):
        ''' Set the value in the matrix at the line and column passed as parameters '''
        self.matrix[row, col] = value

    # decale la ligne numLig d'une case vers la gauche en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageLigneAGauche(self, numLig, nouvelleValeur=0):
        valeurEjecte = self.get_value(numLig, 0)
        for j in range(DIMENSION - 1):
            self.set_value(numLig, j, self.get_value(numLig, j + 1))
        self.set_value(numLig, DIMENSION - 1, nouvelleValeur)
        return valeurEjecte

    # decale la ligne numLig d'une case vers la droite en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageLigneADroite(self, numLig, nouvelleValeur=0):
        valeurEjecte = self.get_value(numLig, DIMENSION - 1)
        for j in range(DIMENSION, 0, -1):
            self.set_value(numLig, j, self.get_value(numLig, j - 1))
        self.set_value(numLig, 0, nouvelleValeur)
        return valeurEjecte

    # decale la colonne numCol d'une case vers le haut en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageColonneEnHaut(self, numCol, nouvelleValeur=0):
        valeurEjecte = self.get_value(0, numCol)
        for i in range(DIMENSION - 1):
            self.set_value(i, numCol, self.get_value(i + 1, numCol))
        self.set_value(DIMENSION - 1, numCol, nouvelleValeur)
        return valeurEjecte

    # decale la colonne numCol d'une case vers le bas en insérant la nouvelleValeur
    # dans la case ainsi libérée
    # la fonction retourne la valeur de la case "ejectée" par le décalage
    def decalageColonneEnBas(self, numCol, nouvelleValeur=0):
        valeurEjecte = self.get_value(DIMENSION - 1, numCol)
        for i in range(DIMENSION, 0, -1):
            self.set_value(i, numCol, self.get_value(i - 1, numCol))
        self.set_value(0, numCol, nouvelleValeur)
        return valeurEjecte

    # -----------------------------------------
    # entrées sorties
    # -----------------------------------------
    # sauvegarde une matrice en mode texte
    # ATTENTION NE MARCHE QUE POUR DES MATRICE CONTENANT DES TYPES SIMPLES
    def sauveMatrice(self, nomFic):
        fic = open(nomFic, "w")
        ligne = str(DIMENSION) + "," + str(DIMENSION) + "\n"
        fic.write(ligne)
        for i in range(DIMENSION):
            ligne = ""
            for j in range(DIMENSION - 1):
                val = self.get_value(i, j)
                if val == None:
                    ligne += ","
                else:
                    ligne += str(val) + ","
            val = self.get_value(i, j + 1)
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
        matrice = Matrix(int(listeLinCol[0]), int(listeLinCol[1]))
        i = 0
        for ligne in fic:
            listeVal = ligne.split(",")
            j = 0
            for elem in listeVal:
                if elem == "" or elem == "\n":
                    self.set_value(i, j, None)
                elif typeVal == "int":
                    self.set_value(i, j, int(elem))
                elif typeVal == "float":
                    self.set_value(i, j, float(elem))
                elif typeVal == "bool":
                    self.set_value(i, j, bool(elem))
                else:
                    self.set_value(i, j, elem)
                j += 1
            i += 1
        return matrice

    # fonction utilitataire
    def afficheLigneSeparatrice(self, tailleCellule=4):
        print()
        for i in range(DIMENSION + 1):
            print("-" * tailleCellule + "+", end="")
        print()

    # fonction d'affichage d'une
    def afficheMatrice(self, tailleCellule=4):
        nbColonnes = DIMENSION
        nbLignes = DIMENSION
        print(" " * tailleCellule + "|", end="")
        for i in range(nbColonnes):
            print(str(i).center(tailleCellule) + "|", end="")
        self.afficheLigneSeparatrice(tailleCellule)
        for i in range(nbLignes):
            print(str(i).rjust(tailleCellule) + "|", end="")
            for j in range(nbColonnes):
                print(str(self.get_value(i, j)).rjust(tailleCellule) + "|", end="")
            self.afficheLigneSeparatrice(tailleCellule)
        print()
