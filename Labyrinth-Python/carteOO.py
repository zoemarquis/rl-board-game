from random import randint

# la liste des caractère semi-graphiques correspondants aux différentes cartes
# l'indice du caractère dans la liste correspond au codage des murs sur la carte
# le caractère 'Ø' indique que l'indice ne correspond pas à une carte
listeCartes=['Ø','╦','╣','╗','╩','═','╝','Ø','╠','╔','║','Ø','╚','Ø','Ø','Ø']
            # 0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15
# permet de créer une carte: True = Pas de mur nord/est/sud/ouest
# les quatre premiers paramètres sont des booléens indiquant s'il y a un mur ou non dans chaque direction
# tresor est le numéro du trésor qui se trouve sur la carte (0 s'il n'y a pas de trésor)
# pions donne la liste des pions qui seront posés sur la carte (un pion est un entier entre 1 et 4)
class Carte(object):

    def __init__(self, nord, est, sud, ouest, tresor=0, pions=[]):
        self.nord = nord
        self.est = est
        self.sud = sud
        self.ouest = ouest
        self.tresor = tresor
        self.pions = set(pions)

    # retourne un booléen indiquant si la carte est valide ou non c'est à dire qu'elle a un ou deux murs
    def estValide(self):
        cpt = 0
        if self.nord:
            cpt+=1
        if self.est:
            cpt+=1
        if self.sud:
            cpt+=1
        if self.ouest:
            cpt+=1
        return cpt == 2 or cpt ==3

    # retourne un booléen indiquant si la carte possède un mur au nord
    def murNord(self):
        return self.nord

    # retourne un booléen indiquant si la carte possède un mur au sud
    def murSud(self):
        return self.sud

    # retourne un booléen indiquant si la carte possède un mur à l'est
    def murEst(self):
        return self.est

    # retourne un booléen indiquant si la carte possède un mur à l'ouest
    def murOuest(self):
        return self.ouest

    # retourne la liste des pions se trouvant sur la carte
    def getListePions(self):
        return list(self.pions)

    # retourne le nombre de pions se trouvant sur la carte
    def getNbPions(self):
        return len(self.pions)

    # retourne un booléen indiquant si la carte possède le pion passé en paramètre
    def possedePion(self,pion):
        return pion in self.pions

    # retourne le codage de la liste des pions
    def getPions(self):
        return type(self.pions)

    # affecte les pions de la cartes en utilisant directement le codage de la liste des pions
    def setPions(self,pions):
        self.pions = self.pions.union(pions)

    # retourne la valeur du trésor qui se trouve sur la carte (0 si pas de trésor)
    def getTresor(self):
        return self.tresor

    # enlève le trésor qui se trouve sur la carte et retourne la valeur de ce trésor
    def prendreTresor(self):
        tresor = self.getTresor()
        self.tresor = 0
        return tresor

    # met le trésor passé en paramètre sur la carte et retourne la valeur de l'ancien trésor
    def mettreTresor(self,tresor):
        tresorAncien = self.getTresor()
        self.tresor = tresor
        return tresorAncien

    # enlève le pion passé en paramètre de la carte. Si le pion n'y était pas ne fait rien
    def prendrePion(self, pion):
        self.pions=self.pions.difference({pion})

    # pose le pion passé en paramètre sur la carte. Si le pion y était déjà ne fait rien
    def poserPion(self, pion):
        self.pions.add(pion)

    # fait tourner la carte dans le sens horaire
    def tournerHoraire(self):
        nord=self.nord
        self.nord=self.ouest
        self.ouest=self.sud
        self.sud=self.est
        self.est=nord

    # fait tourner la carte dans le sens anti horaire
    def tournerAntiHoraire(self):
        nord=self.nord
        self.nord=self.est
        self.est=self.sud
        self.sud=self.ouest
        self.ouest=nord

    # faire tourner la carte dans nombre de tour aléatoire
    def tourneAleatoire(self):
        for i in range(randint(0,4)):
            self.tournerHoraire()


    # code les murs sous la forme d'un entier dont le codage binaire 
    # est de la forme bNbEbSbO où bN, bE, bS et bO valent 
    #      soit 0 s'il n'y a pas de mur dans dans la direction correspondante
    #      soit 1 s'il y a un mur dans la direction correspondante
    # bN est le chiffre des unité, BE des dizaine, etc...
    # le code obtenu permet d'obtenir l'indice du caractère semi-graphique
    # correspondant à la carte dans la liste listeCartes au début de ce fichier
    def coderMurs(self):
        code = 0
        if not self.nord:
            code += 1
        if not self.est:
            code += 2
        if not self.sud:
            code += 4
        if not self.ouest:
            code += 8
        return code

    # positionne les mur d'une carte en fonction du code décrit précédemment
    def decoderMurs(self,code):
        if code >=8:
            self.nord = False
            code-=8
        else:
            self.nord = True
        if code >= 4:
            self.est = False
            code-=4
        else:
            self.est = True
        if code >=2:
            self.sud = False
            code-=2
        else:
            self.sud = True
        if code >=1:
            self.ouest = False
        else:
            self.ouest = True

    # fournit le caractère semi graphique correspondant à la carte (voir la variable listeCartes au début de ce script)
    def toChar(self):
        return listeCartes[self.coderMurs()]

    # suppose que la carte2 est placée au nord de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par le nord
    def passageNord(self,carte):
        return self.murNord() and carte.murSud()
    # suppose que la carte2 est placée au sud de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par le sud
    def passageSud(self,carte):
        return self.murSud() and carte.murNord()

    # suppose que la carte2 est placée à l'ouest de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par l'ouest
    def passageOuest(self,carte):
        return self.murOuest() and carte.murEst()

    # suppose que la carte2 est placée à l'est de la carte1 et indique
    # s'il y a un passage entre ces deux cartes en passant par l'est
    def passageEst(self,carte):
        return self.murEst() and carte.murOuest()
        
################
# Zone de Test #
################
# print('='*10+' Test sur les Cartes '+'='*10)
# carte1 = Carte(True,False,False,True)
# carte2 = Carte(True,False,False,False)
# carte3 = Carte(True,True,True,False)
# print(carte1.estValide())
# print(carte2.estValide())
# print(carte1.getPions())
# carte1.setPions({1,2,4})
# print(carte1.pions)
# carte1.poserPion(1)
# print(carte1.pions)
# carte1.poserPion(3)
# print(carte1.pions)
# carte1.prendrePion(3)
# print(carte1.pions)
# print(carte1.toChar())
# carte1.tournerHoraire()
# print(carte1.toChar())
# print(carte3.toChar())