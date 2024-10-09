from random import randint


# permet de créer entre deux et quatre joueurs et leur distribue de manière équitable
# les trésors compris entre 1 et nbTresor avec au plus nbMaxTresor chacun
# si nbMaxTresor vaut 0, la fonction distribue le maximum de trésors possible
class Joueurs(object):
    def __init__(self, nbJoueurs=2, nbTresors=24, nbTresorMax=0):
        joueurs = {}
        for i in range(1, nbJoueurs + 1):
            joueurs[i] = []
            joueurs["code" + str(i)] = []
        self.nbJoueurs = nbJoueurs
        self.nbTresors = nbTresors
        if nbTresorMax == 0:
            self.nbTresorMax = nbTresors // nbJoueurs
        else:
            self.nbTresorMax = nbTresorMax
        self.joueurs = joueurs
        self.initTresor()

    # attribue effectivement les trésors de manière aléatoire
    def initTresor(self):
        tresorsDispo = [i for i in range(1, self.nbTresors + 1)]
        i = 0
        while i < self.nbTresorMax and tresorsDispo != []:
            j = 1
            while j <= self.nbJoueurs and i < self.nbTresorMax and tresorsDispo != []:
                tresor = randint(0, len(tresorsDispo) - 1)
                self.joueurs[j].append(tresorsDispo.pop(tresor))
                j += 1
            i += 1

    # retourne le numéro du prochain trésor à trouver pour la joueur numJoueur
    # None s'il n'y a pas de prochain trésor
    def prochainTresor(self, numJoueur):
        if self.joueurs[numJoueur] == []:
            return None
        else:
            return self.joueurs[numJoueur][0]

    # enlève le trésor courant du joueur numJoueur et retourne le nombre de trésor
    # qu'il reste à trouver pour ce joueur
    def tresorTrouve(self, numJoueur):
        self.nbTresors -= 1
        self.joueurs[numJoueur].pop(0)
        return len(self.joueurs[numJoueur])

    # retourne le nombre de trésors qu'il reste à trouver pour le joueur numJoueur
    def nbTresorsRestants(self, numJoueur):
        return len(self.joueurs[numJoueur])

    def ajouterCode(self, code, numJoueur):
        self.joueurs["code" + str(numJoueur)].append(code)

    def effacerCode(self, numJoueur):
        self.joueurs["code" + str(numJoueur)] = []

    def effacerDernierCode(self, numJoueur):
        if self.joueurs["code" + str(numJoueur)] != []:
            self.joueurs["code" + str(numJoueur)].pop()

    def getCode(self, numJoueur):
        return self.joueurs["code" + str(numJoueur)]


################
# Zone de Test #
################
# print('='*10+' Test sur les Joueurs '+'='*10)
# joueurs=Joueurs(1,24,1)
# print(joueurs.joueurs)
# print(joueurs.prochainTresor(1))
# print(joueurs.tresorTrouve(1))
# print(joueurs.joueurs)
# print(joueurs.nbTresorsRestants(1))
