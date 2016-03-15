import pygame
import time
import sys
import os
import random
from pygame import KEYDOWN,K_RIGHT,K_LEFT,K_ESCAPE

class Serpent(object):

	def __init__(self,color,taille,surface,espace):
		self.taille = taille
		self.color = color
		self.surface = surface
		corps = []
		for i in range(8):
			corps.append(pygame.Rect((7-i)*taille+taille*espace,taille*espace,taille,taille))
		self.corps = corps
		

	def afficherSerpent(self):
		for case in self.corps:
			pygame.draw.rect(self.surface,self.color,case,0)
		pygame.display.flip()

	def mangeFood(self,pos):
		tete = pygame.Rect(pos[0]*self.taille,pos[1]*self.taille,self.taille,self.taille)
		pygame.draw.rect(self.surface,self.color,tete,0)
		self.corps.append(tete)

	def deplacerSerpent(self,pos):
		queue = self.corps.pop(0)
		tete = pygame.Rect(pos[0]*self.taille,pos[1]*self.taille,self.taille,self.taille)
		pygame.draw.rect(self.surface,self.color,tete,0)
		pygame.draw.rect(self.surface,(0,0,0),queue,0)
		self.corps.append(tete)
		pygame.display.flip()

class JeuSnake(object):

	def __init__(self):
		self.largeur = 800
		self.hauteur = 800
		self.espace = 52
		pygame.init()
		self.fenetre = pygame.display.set_mode((self.largeur,self.hauteur),pygame.RESIZABLE)
		pygame.display.set_caption("Snake caché")
		pygame.display.set_icon( pygame.image.load(os.path.join("./images",'logo.jpeg')))
		self.surface = pygame.display.get_surface()
		self.serpent = Serpent((245,245,245),self.largeur//100,self.surface,self.espace)
		# niveau:(vitesse, nombre Nouriture, nbr Mur)
		self.niveaux = {1:(0.08,10,0),2:(0.08,15,5),3:(0.07,20,5),4:(0.065,20,10),5:(0.06,20,15),6:(0.055,15,20),7:(0.05,15,30),8:(0.04,30,40)}
		self.niveau = 1
		self.nbNiveau = 8
		self.font = pygame.font.SysFont("texgyrechorus", 30)
		self.murs = []

	def initNiveau(self,direction,posSerpent):
		food = []
		# Initialisation des murs
		if self.niveau > 1:
			for i in range(self.niveaux[self.niveau][2]):
				pasValable = True
				
				while pasValable:
					x = random.randint(-45,40)
					y = random.randint(-45,40)
					j = 0
					xS,yS = posSerpent
					xD,yD = direction
					if xS*xD != x and yS*yD != y: # Test si la postion x,y est dans la direction du serpent
						pasValable = False	
						
						while j < len(self.serpent.corps) and not pasValable:
							if self.serpent.corps[j].collidepoint((x*self.serpent.taille,y*self.serpent.taille)):
								pasValable = True
							else:
								j+=1

				self.murs.append((self.espace+x,self.espace+y))

		# Initialisation de la nourriture
		for i in range(self.niveaux[self.niveau][1]):
			pasValable = True
			
			while pasValable:
				x = random.randint(-45,40)
				y = random.randint(-45,40)
				j = 0
				pasValable = False
				# Test si la nourriture n'est pas dans le serpent
				while j < len(self.serpent.corps) and not pasValable:
					if self.serpent.corps[j].collidepoint((x*self.serpent.taille,y*self.serpent.taille)):
						pasValable = True
					else:
						j+=1
				j = 0
				# test si la nourriture n'est pas dans un mur
				while j < len(self.murs) and not pasValable:
					if (x,y) == self.murs:
						pasValable = True
					else:
						j+=1

			food.append((self.espace+x,self.espace+y))
		self.food = food
		# affiche le tout !
		self.afficherFood()
		self.afficherMur()
		pygame.display.flip()


	def afficherFood(self):
		for (x,y) in self.food:
			pygame.draw.rect(self.surface,(0,255,0),pygame.Rect(x*self.serpent.taille, y*self.serpent.taille,self.serpent.taille,self.serpent.taille),0)

	def afficherMur(self):
		for (x,y) in self.murs:
			pygame.draw.rect(self.surface,(255,0,0),pygame.Rect(x*self.serpent.taille, y*self.serpent.taille,self.serpent.taille,self.serpent.taille),0)

	def testFood(self,x,y):
		i = 0
		trouver = False
		while i < len(self.food) and not trouver:
			if (x,y)==self.food[i]:
				trouver = True
				self.food.pop(i)
			else:
				i+=1
		return trouver

	def testMur(self,x,y):
		i = 0
		trouver = False
		while i < len(self.murs) and not trouver:
			if (x,y)==self.murs[i]:
				trouver = True
			else:
				i+=1
		return trouver


	def testSeMordre(self,x,y):
		j = 0
		trouver = False
		while j < len(self.serpent.corps) and not trouver:
			if self.serpent.corps[j].collidepoint((x*self.serpent.taille,y*self.serpent.taille)):
				trouver = True
			else:
				j+=1
		return trouver

	def afficherCadre(self):
		self.cadre = pygame.Rect(self.espace+2,self.espace+2,self.largeur-self.espace*2-3,self.hauteur-self.espace*2-3)
		pygame.draw.rect(self.surface,(255,255,255),self.cadre,1)
		pygame.display.flip()

	def afficherMessage(self,message):
		bas = pygame.draw.rect(self.surface,(0,0,0),pygame.Rect(0,self.hauteur-self.espace+2,self.largeur,self.espace-3),0)
		texte = self.font.render(message,1,(0,255,0))
		textpos = texte.get_rect()
		textpos.x = (self.largeur - textpos.width)//2
		textpos.y = self.hauteur - (self.espace + textpos.height)//2
		self.surface.blit(texte,textpos)
		pygame.display.flip()

	def afficherNiveau(self):
		bas = pygame.draw.rect(self.surface,(0,0,0),pygame.Rect(0,0,self.largeur,self.espace-3),0)
		texte = self.font.render("Niveau n°"+str(self.niveau)+" | Nourriture restante "+str(len(self.food)),1,(0,255,0))
		textpos = texte.get_rect()
		textpos.x = (self.largeur - textpos.width)//2
		textpos.y = (self.espace - textpos.height)//2
		self.surface.blit(texte,textpos)
		pygame.display.flip()

	def demarrer(self):
		continuer = True
		(xS,yS) = (self.espace,self.espace)
		direction = [(1,0),(0,1),(-1,0),(0,-1)]
		i = 2
		self.surface.fill((0,0,0))
		self.afficherCadre()
		self.afficherMessage("Bienvenue dans le jeu snake ! droite/gauche pour tourner le serpent")
		time.sleep(2)
		gg = True
		while self.niveau <= self.nbNiveau and gg:
			self.initNiveau(direction[i],(xS,yS))
			self.serpent.afficherSerpent()
			self.afficherNiveau()
			continuer = True
			while continuer:
				temps = time.time()

				while temps + self.niveaux[self.niveau][0] > time.time():
					for event in pygame.event.get():
						if event.type == KEYDOWN:
							if event.key == K_LEFT:
								i-=1
								if i == -1:
									i = 3
							elif event.key == K_RIGHT:
								i+=1
								if i == 4:
									i = 0
							elif event.key == K_ESCAPE:
								continuer = False
								gg = False
				(xD,yD) = direction[i]

				xS+=xD
				yS+=yD
				if self.espace-46 < xS < self.espace+41 and self.espace-46 < yS < self.espace+41:
					if self.testSeMordre(xS,yS):
						self.afficherMessage("Perdu vous vous êtes mordu la queue !")
						continuer = False
						gg = False
					else:
						if self.testMur(xS,yS):
							self.afficherMessage("Perdu vous vous êtes mangé un mur !")
							continuer = False
							gg = False
						else:
							if self.testFood(xS,yS):
								self.serpent.mangeFood((xS,yS))
								self.afficherNiveau()
								if len(self.food) == 0:
									continuer = False
									self.afficherMessage("Bien jouer niveau "+str(self.niveau)+" finie !")
									time.sleep(1)
									if self.niveau == self.nbNiveau:
										gg == True
									self.niveau+=1
							else:
								self.serpent.deplacerSerpent((xS,yS))
				else:
					continuer = False
					gg = False
					self.afficherMessage("Perdu vous avez mangé le bord !")

			if gg:
				if self.niveau == 2:
					self.afficherMessage("Attention les points rouges sont des murs !")
					time.sleep(1)
				else:
					self.afficherMessage("Attention la vitesse augmente !")
				time.sleep(1)

		time.sleep(2)
		if not gg:
			self.afficherMessage("Domage votre serpent était de taille "+str(len(self.serpent.corps)))
		else:
			self.afficherMessage("Bien jouer vous avez terminer le jeu caché !")
		time.sleep(2)