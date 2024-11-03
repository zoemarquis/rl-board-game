### Développement d’agents autonomes et création de nouvelles règles pour jeux de plateau via l’apprentissage par renforcement

Projet realisé dans le cadre de l'UE "Projet Master" en Master 2 Sciences des Données et Systèmes Complexes par:
- KRUZIC Charlotte
- MARQUIS Zoé
- KUDRIASHOV Daniil
- ZAITCEVA Ekaterina

## Description

Ce projet a pour objectif de créer des joueurs automatiques à l'aide de techniques d'apprentissage par renforcement (RL), capables de maîtriser des jeux de plateau simulés informatiquement. 

Ces agents seront entraînés pour optimiser leurs stratégies en fonction des règles et des interactions avec d'autres joueurs (humains ou agents). 

En plus de jouer, ces agents seront utilisés pour tester de nouvelles règles de jeu et adapter leurs stratégies à des scénarios variés. 

Chaque agent aura un comportement différent, ce qui permettra d'analyser l'impact des variantes de règles sur l'équilibre et la “jouabilité” du jeu.

## Objectifs  

- Entraîner des agents RL pour qu'ils puissent jouer efficacement à des jeux de plateau.
- Tester et optimiser les stratégies de jeu, améliorant ainsi l'équilibrage et la profondeur des jeux.
- Adapter les agents aux nouvelles règles ou variantes de jeu.
- Tester différentes mécaniques de jeu grâce à des simulations massives.
- Personnaliser les agents selon divers styles de jeu.
- Optimiser les règles grâce aux retours des simulations d'agents RL.

## Installer les packages : 

    sudo apt install python3-pip  
    pip install -r requirements

## Jouer avec 2 humains : 
    cd Labyrinth-Python
    python3 play.py -hu 2



## En cours 🛠️
Pour la base de données : 

    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
