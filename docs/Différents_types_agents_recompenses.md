# Différents types d’agents

## **Agent Collecteur**

Se concentre seulement sur la récupération de ses trésors, et ne prend pas en compte les actions des autres joueurs.

**Choix déplacement :** Calcul du chemin le plus court vers le trésor en cours.

- Algorithme de recherche de chemin : A* ou Djikstra

**Récompense :**

- Positive :
    - Trouve un trésor
    - Réduit la distance au trésor
    - Allonge ses chemins possible (vers le trésor)
- Négative :
    - Allonge/Ne réduis pas la distance au trésor
    - Réduit ses chemins possible (vers le trésor)

## **Agent Emmureur**

Cherche à bloquer les autres agents en réduisant leurs déplacements possibles, et en avançant vers ses propres trésors.

**Choix déplacement :** Priorise les actions qui réduisent les possibilités de mouvement des autres joueurs (placement de la pièce), et se déplace vers ses trésors.

**Récompense :**

- Positive :
    - Réduit le nombre de pièces accessibles par les autres joueurs
    - Se rapproche de son trésor
- Négative :
    - Ouvre plus de chemins pour les autres joueurs
    - Ne réduit pas le nombre de pièces accessibles
    - N’avance pas vers son trésor

## **Agent Bloqueur**

Anticipe les mouvements des autres joueurs en devinant leurs trésors et les bloque avant qu'ils ne puissent les atteindre.

**Choix déplacement :** Priorise les actions qui bloquent les chemins des autres joueurs vers leur trésor.

- Mémorise les trésors déjà trouvés et calcule la probabilité pour chaque joueur de rechercher un trésor particulier (Algorithme bayésien), puis tente de bloquer les chemins vers les trésors les plus probables

**Récompense :**

- Positive :
    - Bloque un joueur proche de son trésor
    - Réduit les grands chemins
    - Ralenti le déplacement d’un agent vers son trésor
- Négative :
    - Se trompe dans l’anticipation des trésors des joueurs (bloque un chemin inutile)
    - Ouvre le chemin à un joueur vers son trésor
    - Ne se rapproche pas de son trésor

## **Agent Saboteur**

Cherche à perturber les autres joueurs en réduisant les chemins (en rendant des trésors inaccessibles), et ne cherche pas à atteindre ses propres trésors.

**Choix déplacement :** Modifie le labyrinthe pour empêcher les autres joueurs d’avancer, surtout ceux qui ont le plus progressés.

**Récompense :**

- Positive :
    - Réduit les déplacement possibles d’un autre joueur
    - Bloque un joueur
- Négative :
    - Ne perturbe pas la progression d’un autre joueur
    - Réduit un chemin menant nul part
    - Facilite la progression d’un autre joueur

## **Agent Fixe**

Cherche à se positionner sur des pièces fixes pour éviter d'être déplacé par les actions des autres joueurs dans le but d’atteindre son trésor le plus rapidement possible.

**Choix déplacement :** Se place en priorité sur des cases fixes en réduisant sa distance avec son trésor. 

- Algorithme de recherche de chemin : A* avec poids pour les cases fixes

**Récompense :**

- Positive :
    - Est sur une case fixe
    - Se rapproche de son trésor
- Négative :
    - Est déplacé par un autre joueur
    - Ne trouve pas de case fixe proche de son trésor
    - Ne change pas de pièce pour rester sur une case fixer