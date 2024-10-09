# Présentation de la version bêta de l’environnement pour le jeu du Labyrinthe

Dans le cadre de notre projet, nous avons besoin d'un environnement spécifique pour entraîner nos agents RL sur le jeu du Labyrinthe. Comme aucun environnement n’existe pour ce jeu, nous l’avons créer nous-mêmes.

## Comparaison des frameworks Gym et Petting Zoo

L'analyse des frameworks Gym et PettingZoo a déjà été réalisée dans le document `Kity\docs\Étude_des_outils.md`. 

Nous présentons ici un résumé des principales différences entre ces deux outils et expliquons pourquoi nous avons choisi d'utiliser Gym pour notre projet.

**Gym** est principalement conçu pour les environnements d'apprentissage par renforcement à agent unique, contrairement à **PettingZoo** qui est spécifiquement conçu pour gérer les environnements multi-agents.

**Gym** est une API simple et bien définie avec des méthodes standard telles que `reset()`, `step()`, `render()`, et `close()`. **PettingZoo** s'appuie sur cette API tout en l'étendant pour gérer les environnements multi-agents (tours de jeu, interactions entre plusieurs agents…).

Étant donné que nous souhaitons travailler avec des agents simples, nous avons choisi d’utiliser **Gym**. Ce framework est largement documenté et constitue une option plus simple pour débuter n’étant pas certains de passer à une approche multi-agents. 
Si nous décidons de migrer vers une configuration multi-agents à l'avenir, il sera relativement facile de passer à PettingZoo, car celui-ci est basé sur Gym et partage de nombreuses fonctions et une API similaire.

## Description de l’environnement créé

### Fonctions et espaces

L'environnement que nous avons développé pour le jeu Labyrinthe respecte les conventions standard de la bibliothèque Gym en définissant les **fonctions principales** suivantes :

`__init__()` : Initialise l'environnement en configurant les paramètres de base du jeu (espace d'action, espace d'observation, et autres éléments), et en créant l'instance du Labyrinthe.

`reset()` : Réinitialise l'environnement à son état de départ, et retourne l’état du plateau.

`step(action)` : Permet à l'agent de réaliser une action dans l'environnement. Nous le définissons plus en détail dans la suite du document.

`render()` : Affiche l'état actuel du jeu, et met à jour l'interface graphique du Labyrinthe.

`close()` : Nettoie l'environnement lorsque le jeu est terminé et quitté.

 

Et les **espaces** d’actions et d’observations :

`action_space = spaces.Discrete(12*4*49)`  **:** Combinaison des 12 emplacements possibles pour l'insertion de pièces, des 4 orientations possibles, et des 49 mouvements potentiels sur le plateau. 

`observation_space` :Boîte de dimensions `(7*7*5,)`, utilisant des valeurs entre 0 et 1 pour représenter les différents aspects du plateau de jeu :

- Couches 1, 2, 3, 4 : Présence ou absence de murs sur les côtés la pièce.
- Couche 5 : Présence ou absence des joueurs sur la pièce.

### Mécanismes de la fonction `step()`

Cette fonction est le cœur de l'environnement Gym, car elle permet à l'agent d'interagir avec le jeu et d'apprendre à travers ses actions. Voici un aperçu détaillé de son fonctionnement :

#### **Récupération de l’action de l'agent**

La fonction prend une action en paramètre. Cette action est un nombre entier qui représente une combinaison d'une rotation, d'une insertion de carte, et d'un mouvement sur le plateau.

#### **Vérification de la validité de l'insertion**

La fonction vérifie si l'insertion de la carte est valide. Si l'insertion est interdite ( = si c’est l’inverse du tour précédant), une pénalité de récompense de -10 est appliquée, et le tour est terminé sans autres actions.

#### **Rotation et insertion de la pièce**

Si l'insertion est valide, la carte est d'abord tournée selon l'index de rotation spécifié. Puis, la carte est insérée à la position indiquée sur le plateau de jeu.

#### **Calcul des mouvements possibles**

Après l'insertion, la fonction identifie toutes les positions sur le plateau accessibles au joueur à partir de sa position actuelle. Ces mouvements valides sont ensuite utilisés pour déterminer où le joueur peut se déplacer.

#### **Déplacement du joueur**

L'agent choisit un mouvement parmi les positions accessibles identifiées précédemment, toujours selon l’action (= l’entier) passé en paramètre.

Si le joueur se déplace sur une case contenant un trésor, une récompense positive de +10 est accordée. Si le joueur ne trouve pas de trésor sur sa nouvelle position, une petite pénalité de -1 est appliquée pour encourager la recherche des trésors.

#### **Vérification de la fin du jeu**

La fonction vérifie si la partie est terminée (= si tous les trésors ont été trouvés). 

Si le jeu est terminé, l'environnement signale à l'agent que la session d'apprentissage est terminée.

#### **Retour de l'état du jeu**

La fonction retourne un tuple contenant quatre éléments : l**’**observation de l'état actuel du jeu, la valeur de la récompense obtenue par l'agent pour son action, le flag de terminaison (True si la partie est terminée) et un dictionnaire d’informations supplémentaires (non utilisé pour le moment).

### Calcul des récompenses (à modifier)

La logique des récompenses actuelle est la suivante :

- **-10** : insertion interdite ou mouvement invalide.
- **-1** : ne trouve pas de trésor pendant le tour.
- **+10** : trouve un trésor pendant le tour

## Limitations, améliorations et réflexion

- **Définition de l’espace d’actions**
    - **Gestion des mouvements interdits :**
        - Doit-on obliger l'agent à rejouer si la pièce n'est pas accessible ou lui infliger une pénalité ?
        - Faut-il autoriser les mouvements uniquement sur des pièces accessibles ?
    - **Insertion de la pièce :** Doit-elle toujours éviter la direction inverse précédente ? Comment gérer ces cas ?
    - **Actions multiples dans `step()`:** Est-il possible de séparer le positionnement de la carte et le déplacement du joueur ?
    - **Réduction des actions :** Comment identifier et éliminer les actions peu probables ou impossibles pour simplifier l'espace d'actions ?
- **Définition de l’espace d’observations**
    - **Ajout ou suppression de détails :** Les couches actuelles (murs et positions des joueurs) sont-elles suffisantes ? Faut-il ajouter d'autres informations utiles ou en simplifier certaines ?
    - **Affiner la représentation :** Peut-on optimiser la structure pour rendre l'apprentissage plus efficace ?
- **Vérification et tests de l’environnement :** Mise en place de tests ?
- **Amélioration de la visualisation** pour rendre l'état du jeu plus clair et plus intuitif pour l'analyse ?
- **Système de récompenses :** Actuellement basique. Comment le structurer pour mieux guider l'agent ? Faut-il en créer différents en fonction des types d’agent ?
- **Définition de la fonction `close()` :** Gestion de la fermeture de l’environnement
- **Règles du jeu et fin de la partie :** Définition des conditions de fin, clarification des règles du jeu pour pouvoir créer un environnement adapté.