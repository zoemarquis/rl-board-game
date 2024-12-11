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
    cd .\Labyrinth-Python\
    sudo apt install python3-pip  
    pip install -r requirements.txt

## Commandes à exécuter pour pouvoir lancer le jeu 
    chmod u+x *
    cd .\Labyrinth-Python\
    python3 play.py [option]

Vous pouvez configurer le nombre total de joueurs, le nombre de joueurs humains et IA, ainsi que le thème du jeu à l'aide d'options passées en ligne de commande.

### Option
- `-j`, `--joueurs` : Nombre total de joueurs (par défaut : 2).
- `-hu`, `--humains` : Nombre de joueurs humains (par défaut : 0).
- `-ia`, `--intelligence-artificielle` : Nombre de joueurs IA (par défaut : 0).
- `-t`, `--theme` : Choix du thème (disponibles : original, kity, par défaut : original).

! Si seul le nombre total de joueurs est precisé, on considere que la partie se passe entre les joueurs IA.

## Test de l'environnement Gymnasium
### Execution rapide
Pour tester l'environnement de jeu `gym_env_2dim.py`, il faut lancer la commande suivante :  
```console
python3 ./main_env.py
```
Cette commande lance une partie entre deux agents RL jouant des actions aléatoires dans l'environnement, et la visualisation en temps réel du jeu est assurée par le `GUI_manager`.

### Notebooks pour l'entainement des agents
Le notebook `entrainement_agents.ipynb` permet d'entraîner des agents RL sur l'environnement `gym_env_2dim.py`. Il enregistre les modèles d'agents entraînés et permet de suivre les métriques de performance avec TensorBoard.

Le notebook `notebook.ipynb` permet d'entraîner des agents sur l'ancien environnement `gym_env_labyrinthe.py`, qui est conçu pour un seul agent jouant seul. Cet environnement a été abandonné au profit de gym_env_2dim.py.


## En cours 🛠️
Pour la base de données : 

    sudo apt install postgresql postgresql-contrib
    sudo systemctl start postgresql
    sudo systemctl enable postgresql


lancer les tests
    python3 -m pytest tests_pytest


TODOCOMM : mettre à jour règles qu'on peut faire varier avec explication : 

Choix entre 2, 3 et 4 joueurs.

Règles qu'on peut faire changer : 

choisir entre 1 et 2 (exclusif, par défaut 1)
1. tous les chevaux d'un joueur doivent atteindre le centre du plateau pour gagner
2. le premier cheval au centre du plateau fait gagner son joueur 

choisir entre 2, 3, 4 (exclusif) (voire plus ?) chevaux par joueur
2. chaque joueur a 2 chevaux
3. chaque joueur a 3 chevaux
4. chaque joueur a 4 chevaux
5. chaque joueur a 5 chevaux
6. chaque joueur a 6 chevaux 

choisir entre atteindre exactement le pied de l'escalier pour pouvoir monter ou non 
0. pas beosin d'atteindre exactement le pied
1. atteindre exactement le pied de l'escalier (possible que si avec la valeur du dé il se rapproche de l'objectif : TODOREGLE gestion si y a un autre joueur à cet endroit là)

si la dernière réponse était 1:
0. monter de la valeur indiquée (si il fait plus que l'objectif, atteint quand même l'objectif)
1. monter exactement les marches 1 à 1 (faire 1 pour aller sur la case 1, 2 case 2, 3 case 3...) dans l'ordre et faire un 6 pour atteindre l'objectif 

TODOREGLE 
si la dernière réponse était 1:
0. ne rejoue pas à chaque fois qu'il monte d'une marche
1. rejoue à chaque fois qu'il monte correctement une marche (raccourcir la partie)

attention : chemin et escalier : plusieurs pions du meme joueur autorisé

TODOREGLE : gestion protect -> ne pas pouvoir kill / protect si on se mets dans la meme case
et dans espace observation reward si pions protégés, si plus pion protégé -> reward négatif ?



---

TODOTEST : ajouter des tests pour vérifier
TODODELETE ? : fichier à vérifier puis supprimer si besoin 
TODOCOMM : commentaires à ajouter 
TODOREGLE : regle à ajouter / faire varier 



TODOCOMM : pas le droit de doubler mais le droit de kill si je fais exactement la case où il y a un pion ou alors de rejoindre le pion sur la case si je fais exactement, sinon (je fais plus) je reste coincé derrière