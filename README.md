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
