# ZOÉ : Étude des différents agents et règles du jeu

J’écris cette documentation sans regarder ce qu’on fait les autres avant pour ne pas être influencée.

# Agents

### collecteur

- se concentre uniquement sur la récupération de ses propres trésors le plus rapidement possible
- ne regarde donc pas ce que font les autres agents : visibilité de tout le plateau mis pas de prise en compte des autres agents : ni leur position, ni le nombre de cartes déjà retournées, ni les trésors déjà trouvés etc
- il optimise ses mouvements pour raccourcir le chemin vers son trésor actuel (peut etre juste par startégie de trouver le chemin le plus court, ce qui n’est pas forcément l’idéal pour gagner à ce jeu…)

### emmureur

- emmurer les autres joueurs : leur réduire au maximum la possibilité de déplacement pour qu’au tour suivant le nombre de cases possibles où il peut aller soit le plus réduit possible, tout en progressant lentement vers ses propres objectifs
- donc si il a un coup a joué qui peut lui permettre de se rapprocher légèrement (voir pas du tout) de son objectif et surtout de bloquer un maximum d’autres agents, réduire leur périmetre : il obtient beaucoup de reward

### bloqueur

- il peut essayer de deviner quels sont les objectifs des autres en regardant les trésors déjà dévoilés ou les cartes que les autres agents auraient pu obtenir mais qu’ils n’ont pas pris (gestion d’une mémoire plus ou moins longue)
- et donc bloquer les joueurs allant vers les objectis autres

## Différents niveaux d’expertise des agents

- le temps de calcul alloué
- profondeur de recherche [de l’arbre]
- le nombre de cases que l’agent voit autour de lui

Pour la satisfaction : prendre en compte le temps d’attente entre 2 tours d’un même joueur

# Règles du jeu

- ne pas revenir au point de départ initial
- connaitre toutes les cartes trésors dès le départ pour optimiser l’ordre des déplacements
- tuiles spéciales quand le joueur passe dessus il tire une carte, ça peut etre ? positif ou ? négatif, mais ça peut aussi etre juste une tuile spéciale
    - téléportation : se déplacer à un des quatre coins du plateau : au choix
    - trou noir : piéger pendant 1 ou 2 tours
    
    (cela aura impact sur agents : apprendre à éviter ou utiliser ces tuiles stratégiquement pour progresser ou bloquer les autres joueurs)
    
- aléatoire :
    - cartes d’évènements : inverser les positions de joueurs
    - lancer de dé ? lancer de dé : déplacement entre 1 et 6 cases possibles à ce tour
    
    (les agents devront adapter leurs stratégies à des événements imprévisibles)
    
- actions supplémentaires pour les joueurs :
    - 1 fois dans la partie si il estime que la carte suivante est trop loin, il peut décider de la “retarder” et de retourner la suivante. Il peut à tout moment (quand il retourne une autre carte) décider de se remettre à jouer pour la carte retardée
- bonus / malus: rejouer tout de suite sous certaines conditions, par exemple si le dernier trésor a été trouvé il y a plus de 5 tours, à l’inverse, devoir passer son tour si on trouve en 1 coup le prochain trésor
- si un joueur rencontre ou s’arrete sur une case où il y a un autre joueur : celui qui était déjà là est expulsé et retourne à son coin de départ
- si un joueur rencontre ou s’arrete sur une case où il y a un autre joueur : il est coincé il ne peut pas passer et doit rester sur la tuile précédente

NB : On pourrait aussi essayer de faire varier le nombre de personnages et les compositions : ainsi le temps d’attente serait différent et les agents pourraient être plus ou moins satisfait de joueur contre certain type de joueur. On pourrait étudier les statistiques des différentes combinaisons ainsi créées.