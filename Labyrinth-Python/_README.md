## Commandes à exécuter pour pouvoir lancer le jeu 
    chmod u+x *

    pip install pygame

    python3 play.py [option]

Vous pouvez configurer le nombre total de joueurs, le nombre de joueurs humains et IA, ainsi que le thème du jeu à l'aide d'options passées en ligne de commande.

### Option
- -j, --joueurs : Nombre total de joueurs (par défaut : 2).
- -hu, --humains : Nombre de joueurs humains (par défaut : 0).
- -ia, --intelligence-artificielle : Nombre de joueurs IA (par défaut : 0).
- -t, --theme : Choix du thème (disponibles : original, kity, par défaut : original).

! Si seul le nombre total de joueurs est precisé, on considere que la partie se passe entre les joueurs IA.