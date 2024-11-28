version actuelle du jeu : 

2 joueurs
2 pions par joueur
actions : rien, sortir un pion de l'écurie, avancer un pion, entrer dans la safe zone, avancer dans la safe zone, atteindre l'objectif
(il manque kill surtout)

## TO DO

### écrire les règles du jeu 
- en dur l'ordre des actions à essayer pour chaque agent si il veut faire un truc interdit
(donc dupliquer env avec version entrainement et version jouer une partie (ou alors juste un booléen dans le jeu))

### jeu
- mettre en place 4 pions par joueur
- mettre en place 2, 3 ou 4 joueurs (au début ça peut etre que des humains puis créer un fichier où on choisit qui sont les agents / humains pour lancer une partie) : attention si 2 joueurs : pion en 1 / 29, mais si + de joueurs : 1/15/29/43

### agents
rien trop besoin de faire : on va juste mettre des reward différents pour chaque action en fonction de son type (si "max_chevaux", si "avance_rapide" ...)
et une table en cas d'action invalide de gestion dans l'ordre des coups à essayer

on purrait tenter un player qui se base sur l'observation -> rester grouper ?

### règles

- faire un 6 pour sortir un cheval

#### kill / combien de cheval par case
- un seul cheval par case : sauf dans écurie : donc retirer des actions possibles le fait d'etre 2 (meme pour meme joueur) dans la meme case (ça c'est une variante) -> meme oueru alors on arrete son pion juste derriere
(donc en soit on peut pas sortir de petit cheval si )
- interdiction de doubler : pour tuer il faut tomber exactement sur sa case : idem on pourrait faire une variante avec / sans cette règle
- ici pareil pour kill on peut faire des variantes
- ajouter des cases safe (on ne peut pas mourir ici) pour une variantes
- variante : si pas kill (pas nomnre case exacte) si il rencontre un autre joueur et doit le dépasser -> rebondit et recule,sauf soit meme : juste derriere

#### dé
- si le dé est un 6 alors le joueur peut rejouer
- max deux 6 d'affilés (si le joueur fait un troisième 6 alors il n'a pas le droit de faire d'action)

#### safe zone 
- un cheval doit s'arreter pile à sa case 56 (devant son escalier)
    - si le dé est trop grand il doit reculer d'autant de cases (donc si il est sur 53 et qu'il fait 5 alors il avance de 3 et recule de 2 -> case 54)
- doit faire 1 puis 2 puis 3 puis 4 puis 5 puis 6 et de nouveau un 6
- variante : assouplir regles : il suffit de faire un 6 pour gagner ?

## variantes
- raccourcir la partie : jouer avec moins de chevaux
- le premier qui place un cheval au milieu à gagner / tous chevaux au milieu 


## organisation du dossier

petits_chevaux/
│
├── ludo_env/
│   ├── env.py              # Classe de l'environnement Gymnasium
│   ├── game_logic.py       # Gestion de la logique et des règles du jeu
│   └── renderer.py         # interface graphique
├── reinforcement_learning/
│   ├── agent.py            # Définir des agents (Random par exemple), qlearnin : brouillon
│   ├── notebook_maskedppo.ipynb    # notebook avec un pseudo masked ppo
│   ├── notebook_ppo.ipynb          # notebook avec ppo
│   └── notebook_qlearning.ipynb    # notebook avec qlearning : pas fonctionnel juste un brouillon
└── tests/
│   └── TODO


TODO : prendre en compte distance entre toi et sécuriser escalier ?