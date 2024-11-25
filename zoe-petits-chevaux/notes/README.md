# Stratégie à chaque tour : étapes générales

## État initial du tour :

Résultat du dé (dice_roll).
Position de tous les pions du joueur (HOME, SAFE ZONE, parcours principal, ou GOAL).
Positions des adversaires et opportunités de capture.

## Générer toutes les actions valides :

Pour chaque pion, calculer ses mouvements possibles en fonction du résultat du dé.
Les actions peuvent inclure :
Sortir de HOME (si le dé est 6).
Avancer d’un nombre de cases correspondant au dé.
Capturer un adversaire (déplacement vers une case occupée par un autre joueur).
Entrer dans la SAFE ZONE ou GOAL.

## Attribuer des récompenses à chaque action :

Définir des priorités en fonction de la stratégie souhaitée pour l’agent :
Sortir un pion de HOME peut recevoir une forte récompense pour les agents qui privilégient une présence maximale sur le plateau.
Capturer un adversaire peut être valorisé pour des agents agressifs.
Avancer un pion proche du GOAL peut être priorisé pour un agent qui cherche à terminer rapidement.

## Choisir l’action selon une politique :

Entraîner l’agent à maximiser les récompenses selon les priorités définies.
Par exemple, utiliser une méthode comme Q-learning ou une autre approche d’apprentissage par renforcement.

# Différents types d'agents
Voici quelques exemples de stratégies possibles et les récompenses associées :

## 1. Agent "Maximiser le nombre de pions en jeu"
Priorité : Sortir autant de pions que possible.
Récompenses :
+10 pour sortir un pion de HOME.
+1 pour chaque case avancée.
-5 pour toute action où un pion reste bloqué inutilement.

## 2. Agent "Concentré sur un pion"
Priorité : Avancer un pion le plus rapidement possible jusqu’à GOAL.
Récompenses :
+10 pour chaque case avancée par le pion le plus avancé.
+20 pour entrer dans la SAFE ZONE.
+50 pour atteindre le GOAL.
-10 si le pion le plus avancé aurait pu avancer mais ne l’a pas fait.

## 3. Agent "Agressif"
Priorité : Capturer des adversaires.
Récompenses :
+15 pour capturer un pion adverse.
+5 pour avancer sur une case stratégique (proche des pions adverses).
-10 pour rester dans une position vulnérable (c'est à dire à la portée d'un pion)



Représentation du plateau
Avec votre choix de représentation, le plateau sera une liste ou matrice 1D, où chaque case contient une liste des numéros des pions présents. Par exemple :

Une case vide est représentée par [].
Une case avec un pion du joueur 1 est représentée par [1].
Une case avec deux pions (joueur 1 et joueur 2) est représentée par [1, 2].