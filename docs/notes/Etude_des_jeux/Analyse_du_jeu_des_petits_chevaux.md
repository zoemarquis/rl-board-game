# Analyse du jeu des petits chevaux

# Objectif

L'objectif du jeu des petits chevaux est d'être le premier joueur à emmener ses quatre chevaux au centre du plateau de jeu. Pour cela, chaque joueur doit faire un tour complet du plateau en avançant ses chevaux en fonction des résultats des dés tout en évitant de se faire capturer par les chevaux adverses, ce qui les renverrait à leur écurie.

# Règles du jeu original

Nombre de joueurs : 1 à 4

## Début de partie

Chaque joueur commence avec ses chevaux dans son écurie.

Les joueurs lancent le dé pour déterminer qui commence.
Une fois le premier joueur déterminé, le jeu se déroule dans le sens des aiguilles d’une montre.

## Déroulement de la partie

### Sortie des pions

Un joueur doit faire 6 pour sortir un cheval de son écurie.

### Déplacements

- Un cheval se déplace d’un nombre de cases égal au résultat du dé
- Il peut y avoir seulement 1 cheval par case
- Il n’est pas possible de doubler un cheval
- Si un cheval arrive sur la case d’un cheval adverse, alors celui-ci retourne dans son écurie
- Si aucun cheval du joueur ne peut être déplacé, alors il passe son tour

### Particularité du 6

Si un joueur fait un 6, il rejoue et choisit soit de sortir un nouveau cheval, soit d'avancer de 6 cases avec un cheval en jeu.

### Arrivée au centre

Une fois qu’un cheval a terminé un tour, celui-ci doit monter son escalier afin d’atteindre le centre du plateau de jeu.

- Le cheval doit s’arrêter exactement sur la case devant son escalier. Si le résultat du dé est trop grand, le cheval recule du surplus.
- Chaque chiffre de l’escalier doit être obtenu (1, 2,3,4, 5, 6), ainsi que 6 une fois en haut pour que le cheval atteigne le centre.

## Fin de partie (Victoire)

Pour terminer la partie, il faut qu’une des joueurs ait ses 4 chevaux au centre du plateau de jeu.

# Types d’agents pour le jeu de base

## Agents jeu de base

### Agent équilibré

Joueur qui optimise ses déplacements afin de gagner tout en bloquant les autres joueurs.

### Agent défensif

Joueur qui privilégie les déplacements qui réduisent les chances de capture par ses adversaires.

### Agent agressif

Joueur qui cherche à capturer les autres chevaux en priorité, tout en avançant pour gagner.

### Agent gênant

Joueur qui se concentre sur la gêne des autres joueurs, tout en avançant pour gagner.

### Agent saboteur

Joueur qui se concentre sur la gêne et la capture des autres joueurs sans chercher spécialement à gagner.

### Agent adaptable

Joueur qui adapte sa stratégie en temps réel en fonction du déroulement du jeu et des actions des autres joueurs.

### Agent rapide

Joueur qui cherche à avancer ses chevaux avant de vouloir sortir de nouveaux chevaux.

### Agent harde

Joueur qui cherche à sortir tous ses chevaux avant de vouloir avancer

### Agent grimpeur

Joueur qui cherche à faire monter ses chevaux en haut de l’escalier avant d’y amener les autres

### Agent sécurisé

Joueur qui cherche à avoir tous ses chevaux dans l’escalier avant de vouloir qu’ils atteignent le centre

## Agents jeu modifié

### Agent collaboratif

Joueur qui cherche à aider les autres personnes de son équipe, tout en avançant pour gagner.

# Critères d'Évaluation des Agents (Score)

### Position finale

- **Classement final :** Prise en compte de la position finale.
- **Nombre de chevaux ayant atteint le centre avant la fin de la partie**
- **Position des chevaux à la fin de la partie**

### Déplacements

- **Avancement moyen par tour**
- **Nombre de tours bloqués :** Nombre de tour où le joueur n’a pas pu jouer (pas de cheval disponible, chevaux bloqués…)
- **Ratio entre tours joués et tours passés**
- **Pourcentage de déplacements optimaux :** Pourcentage de déplacements qui contribuent directement à l’objectif final (progresser, éviter une capture, bloquer un adversaire) selon le type d’agent.
- **Nombre de fois où la relance a été possible** (Peut-être trop aléatoire)
- **Nombre moyen de coups total pour terminer la partie**

### Blocages

- **Nombre de retour à l’écurie**
- **Nombre de tour avant de sortir un cheval** (peut-être pas adapté à tous les types d’agents)
- **Ratio entre capture et capturé**

### Réflexion

- **Adaptabilité aux changements liés au déplacement des autres joueurs** (Voir comment calculer ça)
- **Nombre de tour dans une position critique :** Tour où un cheval du joueur est sur une case où il peut être capturé par un autre joueur (devant l’escalier ou devant un adversaire)

# Modifications possibles du jeu

### Modification de l’environnement

- Ajustement du plateau pour accueillir plus ou moins de joueurs
- Augmenter / Diminuer le nombre de chevaux par joueur
- Augmenter / Diminuer le nombre de cases sur le plateau
- Jouer en équipe : 2 contre 2 par exemple
- Modification des conditions de victoire : Devoir manger N pions, avoir tous ses chevaux en dehors de l’écurie …

### Ajout de cases spéciales

Actions :

- Multiplication du résultat du dé
- Division du résultat du dé
- Avancer de X cases
- Reculer de X cases
- Bloquer un joueur au prochain tour
- Relancer le dé
- Protection pendant X tours contre les captures
- Echanger la place d’un pion avec un autre joueur

Soit directement sur la case, soit sur des cartes à piocher lors d’un passage sur une carte spéciale.

### Modification des règles

- Autoriser la sortie des chevaux sans forcément faire un 6
- Commencer avec 1 cheval sortie
- Ne pas rejouer lors d’un 6
- Ne pas pouvoir capturer un adversaire
- Pouvoir doubler d’autres chevaux
- Déplacement des joueurs dans un sens différent

# Sources

Règles du jeu :

- [https://www.agoralude.com/blog/la-regle-des-petits-chevaux-comment-jouer-a-ce-jeu-traditionnel--n42](https://www.agoralude.com/blog/la-regle-des-petits-chevaux-comment-jouer-a-ce-jeu-traditionnel--n42)

Jeux de petits chevaux en ligne :

- [https://www.logicieleducatif.fr/jeu/les-petits-chevaux](https://www.logicieleducatif.fr/jeu/les-petits-chevaux)

Projets existants :

- Projet RL Ludo vidéo : [https://www.youtube.com/watch?v=piTnn3dJ9QE](https://www.youtube.com/watch?v=piTnn3dJ9QE)
    - GitHub Ludo utilisé : [https://github.com/SimonLBSoerensen/LUDOpy](https://github.com/SimonLBSoerensen/LUDOpy)
- PDF RL Ludo:
    - [https://www.linkedin.com/posts/rajtilak-pal-5a78b7192_ludo-ai-reinforcementlearning-activity-7135310013371199488-0my-/?trk=public_profile_like_view](https://www.linkedin.com/posts/rajtilak-pal-5a78b7192_ludo-ai-reinforcementlearning-activity-7135310013371199488-0my-/?trk=public_profile_like_view)
    - [https://drive.google.com/file/d/18o-sI9pu9MPxhHi0sPPbZCnAaGCIQawJ/view](https://drive.google.com/file/d/18o-sI9pu9MPxhHi0sPPbZCnAaGCIQawJ/view)