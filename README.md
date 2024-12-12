## Développement d’agents autonomes et création de nouvelles règles pour jeux de plateau via l’apprentissage par renforcement

Projet realisé dans le cadre de l'UE "Projet Master" en Master 2 Sciences des Données et Systèmes Complexes par:
- KRUZIC Charlotte
- MARQUIS Zoé
- KUDRIASHOV Daniil
- ZAITCEVA Ekaterina

## Description du Projet 🎮🤖

Ce projet explore l'apprentissage par renforcement appliqué à des jeux de plateau, avec un focus sur le célèbre jeu de société Ludo (également connu sous le nom de "Petits Chevaux"). Initialement, nous avions expérimenté avec le jeu Labyrinthe, mais ce choix a été abandonné en raison de contraintes spécifiques, comme expliqué dans la documentation.

Nous avons conçu plusieurs agents et défini différentes variations de règles, afin d'étudier leurs interactions et performances dans divers contextes de jeu.

## Fonctionnalités principales :
🧠 Création d'agents : Plusieurs agents ont été développés, utilisant notamment l'algorithme Proximal Policy Optimization (PPO) pour optimiser leurs stratégies.  
⚙️ Entraînement des agents : Les agents ont été entraînés sur des environnements simulés, avec des règles variées pour modéliser différents scénarios de jeu.  
🎲 Simulation de parties : Nous avons simulé des affrontements entre agents pour analyser leurs performances dans différents contextes, tout en testant les impacts des variations de règles.  
📊 Analyse des performances : Une analyse approfondie des résultats a été réalisée à l'aide de techniques statistiques et des outils dédiés.  

## Règles du Jeu et Variations 📝🎲

### Règles de Base :

- Chaque joueur commence avec tous ses pions dans une écurie.
- Un 6 au dé est requis pour sortir un pion de l'écurie.
- Une fois sur le plateau, les pions doivent avancer sur un chemin commun de 56 cases, où :
    - Les pions peuvent se croiser ou se faire tuer en arrivant exactement sur une case occupée par un pion adverse.
    - Règles pour les déplacements :
        - Un pion peut tuer un pion adverse uniquement en tombant exactement sur sa case.
        - Bloquage derrière un pion : Si la valeur du dé est strictement supérieure au nombre de cases jusqu’au pion suivant, le joueur est bloqué.
            - Si le pion bloquant appartient au même joueur, on peut :
                - Rejoindre ce pion si la valeur du dé est égale à la distance.
                - S'arrêter sur la case du pion si la valeur du dé est supérieure. : TODO vérifier
- Chaque joueur possède un escalier unique de 6 cases menant à une case objectif.

### Variations des Règles :
- Nombre de joueurs :
    - Le jeu peut être joué à 2, 3 ou 4 joueurs.
- Nombre de pions par joueur :
    - Chaque joueur peut avoir entre 2 et 6 petits chevaux en jeu.
- Conditions de victoire :
    - Victoire rapide : Le premier joueur à atteindre l’objectif avec un seul pion gagne.
    - Victoire complète : Tous les pions d’un joueur doivent atteindre l’objectif pour déclarer sa victoire.
- Règles pour l'escalier :
    - Exactitude nécessaire : Un pion doit atteindre exactement le pied de l'escalier pour pouvoir commencer à le gravir.
    - Progression simplifiée : Si la valeur du dé dépasse le pied de l’escalier, le pion grimpe directement comme si l’escalier faisait partie du chemin.
- Ordre de progression sur l'escalier :
    - Ordre simplifié : Un pion peut monter plusieurs marches de l'escalier en un seul lancé de dé, il suffit qu'il arrive ou dépasse l'objectif pour l'atteindre.
    - Dans le cas de l'exactitude nécessaire pour le pied de l'excalier, on peut utiliser l'ordre simplifié ou alors l'ordre strict : 
        - Chaque marche de l'escalier nécessite un jet spécifique : 1 pour la première marche, 2 pour la deuxième, ... ainsi que 6 pour atteindre l’objectif.

- Rejouer si dé = 6 (oui ou non)

TODOREGLE : 
si la dernière réponse était 1:
0. ne rejoue pas à chaque fois qu'il monte d'une marche
1. rejoue à chaque fois qu'il monte correctement une marche (raccourcir la partie)

TODOREGLE : gestion protect -> ne pas pouvoir kill / protect si on se mets dans la meme case
et dans espace observation reward si pions protégés, si plus pion protégé -> reward négatif ?



## Technologies utilisées :
🐍 Python : Langage principal pour la gestion du jeu et des agents.  
🛠️ Gymnasium : Environnements personnalisés pour l'apprentissage par renforcement.  
🤖 Stable-Baselines3 : Bibliothèque utilisée pour entraîner les agents sur les environnements Gymnasium.  
🗄️ PostgreSQL : Base de données pour stocker les résultats des simulations et les métriques des agents.  
📊 Pandas et Jupyter Notebook : Analyse et visualisation des performances des agents.  
🎨 Pygame : Interface graphique pour visualiser les parties en temps réel.  
✅ Pytest : Tests unitaires pour garantir la fiabilité du code.  

# packages, excéuter le jeu ... TODOCOMM 


---

notice des TODO :

TODOTEST : ajouter des tests pour vérifier
TODODELETE ? : fichier à vérifier puis supprimer si besoin 
TODOCOMM : commentaires à ajouter 
TODOREGLE : regle à ajouter / faire varier 
il reste des TODO tout court 