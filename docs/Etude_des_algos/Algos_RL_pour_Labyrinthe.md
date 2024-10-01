# Algos RL pour Labyrinthe

### **Notions clés de l'apprentissage par renforcement appliquées au jeu du Labyrinthe**

### **1. Espace d'états**

**Définition générale** : L'espace d'états en apprentissage par renforcement (RL) représente l'ensemble de toutes les situations possibles dans lesquelles un agent peut se trouver. Chaque état s décrit pleinement l'environnement à un moment donné.

**Application au Labyrinthe** :

- **Composants de l'état** :
    - **Configuration du plateau** : Position de chaque tuile (fixe et mobile) sur le plateau, représentant le labyrinthe actuel.
    - **Position des joueurs** : Emplacement de chaque pion sur le plateau.
    - **Objectifs restants** : Liste des trésors ou objets que chaque joueur doit encore collecter.
    - **Tuile supplémentaire** : La tuile en main qui sera insérée lors du prochain tour.
- **Complexité de l'espace d'états** :
    - Le nombre total d'états possibles est très grand en raison des nombreuses configurations du labyrinthe et des positions des joueurs.
    - Pour gérer cette complexité, il peut être nécessaire de représenter les états de manière simplifiée ou d'utiliser des techniques d'approximation.

### **2. Espace d'actions**

**Définition générale** : L'espace d'actions est l'ensemble de toutes les actions possibles qu'un agent peut entreprendre à partir d'un état donné.

**Application au Labyrinthe** :

- **Actions possibles** :
    1. **Insertion de la tuile** :
        - Choisir un emplacement sur le bord du plateau pour insérer la tuile supplémentaire. Il y a généralement 12 positions possibles (flèches sur les bords du plateau).
    2. **Orientation de la tuile** :
        - Certaines versions permettent de tourner la tuile avant de l'insérer, ajoutant plus de possibilités.
    3. **Déplacement du pion** :
        - Après la modification du labyrinthe, décider jusqu'où déplacer le pion, en fonction des passages ouverts.
- **Total des actions** :
    - Le nombre total d'actions est le produit des positions d'insertion possibles, des orientations possibles de la tuile, et des déplacements possibles du pion.

### **3. Politique (Policy)**

**Définition générale** : Une politique π(a∣s) est une fonction qui, pour chaque état s, donne la probabilité de choisir une action a. Elle guide le comportement de l'agent.

**Application au Labyrinthe** :

- **Politique déterministe** : L'agent choisit toujours l'action qu'il considère comme la meilleure dans un état donné.
- **Politique stochastique** : L'agent choisit les actions selon une distribution de probabilités, ce qui peut encourager l'exploration.
- **Objectif de la politique** :
    - **Pour un agent compétitif** : Maximiser les chances de collecter tous ses trésors avant les autres joueurs.
    - **Pour un agent coopératif** : Aider les autres joueurs à atteindre leurs objectifs communs.
    - **Pour un agent avec une personnalité spécifique** : Par exemple, gêner les autres joueurs ou gagner avec la plus petite avance possible.

### **4. Fonction de récompense**

**Définition générale** : La fonction de récompense R(s,a,s′) attribue une valeur numérique à chaque transition d'état, indiquant la valeur immédiate de cette action.

**Application au Labyrinthe** :

- **Récompenses possibles** :
    - **Collecte d'un trésor** : Récompense positive importante lorsque l'agent atteint un trésor assigné.
    - **Déplacement vers un trésor** : Récompense positive proportionnelle à la proximité avec le prochain trésor.
    - **Gêner un adversaire** : Récompense positive si l'agent bloque le chemin d'un autre joueur (si c'est l'objectif).
    - **Temps écoulé** : Récompense négative pour chaque tour pour encourager une victoire rapide.
- **Conception de la fonction de récompense** :
    - Elle doit aligner les objectifs de l'agent avec le comportement souhaité.
    - Pour des agents avec des personnalités différentes, la fonction de récompense peut être modifiée pour refléter ces différences.

### **5. Fonction de valeur**

**Définition générale** : La fonction de valeur V(s) estime la valeur future attendue à partir d'un état s, en suivant une politique donnée. Elle indique la qualité d'un état en termes de récompenses futures attendues.

**Application au Labyrinthe** :

- **Estimation des bénéfices futurs** :
    - Un état où l'agent est proche de plusieurs trésors aura une valeur élevée.
    - Un état où l'agent est bloqué aura une valeur faible.
- **Utilisation** :
    - Aider l'agent à choisir des actions qui mènent à des états avec des valeurs élevées.
    - Peut être utilisée pour planifier plusieurs coups à l'avance.

### **6. Fonction de transition**

**Définition générale** : La fonction de transition T(s,a,s′) décrit la probabilité de passer de l'état s à l'état s′ en exécutant l'action a.

**Application au Labyrinthe** :

- **Déterminisme** :
    - Dans le jeu du Labyrinthe, les transitions sont généralement déterministes : une action spécifique dans un état donné conduit toujours au même état suivant.
- **Complexité** :
    - Les modifications du labyrinthe peuvent avoir des effets importants sur les états futurs, rendant la modélisation des transitions complexe.

## Utilisation des Méthodes Classiques vs Multi-Agents

### Avantages des Méthodes Classiques

1. **Simplicité de mise en œuvre**
    
    Les algorithmes d'apprentissage par renforcement classiques sont bien documentés et plus simples à implémenter, en particulier pour un premier projet. Leur simplicité en fait une option accessible aux équipes avec une expérience limitée dans ce domaine.
    
2. **Compréhension des Bases**
    
    Les méthodes classiques permettent d'acquérir une bonne compréhension des principes fondamentaux de l'apprentissage par renforcement. Cela facilite la maîtrise des concepts clés tels que l'exploration, l'exploitation, et la convergence des politiques.
    
3. **Adaptation aux Petits Espaces d'États**
    
    Ces algorithmes peuvent s'avérer efficaces si l'espace d'états est représenté de manière compacte. Ils conviennent particulièrement bien lorsque les espaces d'états et d'actions sont limités, rendant les calculs plus gérables.
    

### Considérations sur l'Utilisation du Multi-Agents

### 1. Quand le Multi-Agent est-il Nécessaire ?

- **Interactions Complexes entre Agents**
    
    Le recours aux systèmes multi-agents devient nécessaire lorsque le projet implique la modélisation et l'étude des interactions dynamiques entre plusieurs agents apprenants. Ces interactions peuvent inclure la compétition ou la coopération, où chaque agent ajuste son comportement en fonction des actions des autres.
    
- **Objectifs Spécifiques**
    
    Le multi-agent est particulièrement pertinent lorsque l'objectif est de créer des agents ayant des personnalités ou des stratégies distinctes, qui s'adaptent et apprennent en fonction des actions des autres agents. Ce contexte est souvent présent dans des environnements compétitifs ou collaboratifs.
    

### 2. Limitations des Méthodes Classiques en Environnement Multi-Agents

- **Non-Stationnarité de l'Environnement**
    
    Dans un environnement multi-agents, chaque agent perçoit un environnement en constante évolution. Cette non-stationnarité est due au fait que les autres agents apprennent et modifient continuellement leurs politiques, ce qui complique la convergence des algorithmes d'apprentissage classiques.
    
- **Difficulté d'Apprentissage**
    
    Les méthodes classiques d'apprentissage par renforcement sont souvent mal adaptées aux environnements multi-agents en raison des problèmes de convergence dans ces contextes dynamiques. Cela peut entraîner des politiques sous-optimales, rendant l'apprentissage moins efficace.
    

### 3. Approches pour Utiliser des Méthodes Classiques en Multi-Agents

- **Apprentissage Indépendant**
    
    Chaque agent apprend sa propre politique en traitant les autres agents comme une partie fixe de l'environnement. Cette approche simplifie la mise en œuvre, car elle permet de traiter chaque agent de manière isolée sans modéliser explicitement les interactions entre eux.
    
    - **Avantage** : Simplicité de mise en œuvre.
    - **Inconvénient** : Cette approche peut entraîner des politiques sous-optimales, car elle ne prend pas en compte la non-stationnarité induite par l'apprentissage simultané des autres agents.
- **Approches Centralisées**
    
    Une autre approche consiste à entraîner un agent central qui contrôle tous les agents. Bien que cela simplifie l'apprentissage en coordonnant les actions de l'ensemble des agents, cette méthode n'est pas toujours réaliste dans des environnements compétitifs où chaque agent est supposé être autonome.
    
    - **Inconvénient** : Cette approche ne reflète pas fidèlement les environnements compétitifs ou décentralisés, où chaque joueur doit agir de manière autonome, ce qui est souvent le cas dans les jeux de société ou les simulations complexes.

### **Application des algorithmes d'apprentissage par renforcement au jeu du Labyrinthe**

### **1. Q-Learning**

- **Principe** : Apprendre une fonction de valeur d'action Q(s,a) qui estime la récompense future en exécutant l'action a depuis l'état s.
- **Application** :
    - **Mise à jour des valeurs Q** : Après chaque action, l'agent met à jour Q(s,a) en tenant compte de la récompense reçue et de la valeur maximale des actions possibles dans le nouvel état.
        
        Q(s,a)
        
    - **Choix de l'action** : L'agent choisit l'action avec la valeur Q la plus élevée pour l'état actuel.
- **Défis** :
    - **Taille de l'espace d'états** : Peut devenir ingérable si on considère toutes les configurations possibles du labyrinthe.
    - **Approximation** : Il peut être nécessaire d'utiliser des méthodes d'approximation, comme les réseaux de neurones (Deep Q-Networks), pour gérer de grands espaces d'états.

### **2. Deep Q-Networks (DQN)**

- **Principe** : Utiliser un réseau de neurones pour approximer la fonction Q(s,a), permettant de gérer de grands espaces d'états.
- **Application** :
    - **Entrées du réseau** : Représentation numérique de l'état actuel (configuration du labyrinthe, positions des joueurs, etc.).
    - **Sorties du réseau** : Valeurs Q estimées pour chaque action possible.
- **Avantages** :
    - **Gestion de la complexité** : Capable de traiter des espaces d'états continus ou très grands.
    - **Généralisation** : Peut généraliser à des états non rencontrés pendant l'entraînement.

### **3. Méthodes basées sur les politiques (Policy Gradient)**

- **Principe** : Apprendre directement la politique π(a∣s) en optimisant la probabilité des actions qui mènent à des récompenses élevées.
- **Application** :
    - **Réseau de politique** : Un réseau de neurones qui prend l'état en entrée et sort une distribution de probabilités sur les actions.
    - **Optimisation** : Utiliser des algorithmes comme REINFORCE pour mettre à jour les poids du réseau en fonction des récompenses reçues.
- **Avantages** :
    - **Politiques stochastiques** : Permet d'explorer plus efficacement en évitant de se fixer prématurément sur des actions déterministes.
    - **Adaptation** : Peut s'adapter rapidement à des changements dans l'environnement ou les règles.

### **4. Méthodes Actor-Critic**

- **Principe** : Combiner les approches basées sur les valeurs et les politiques. L'« acteur » propose des actions, tandis que le « critique » évalue ces actions.
- **Application** :
    - **Acteur** : Génère la politique π(a∣s).
        
        π(a∣s)\pi(a|s)
        
    - **Critique** : Estime la fonction de valeur V(s) pour évaluer la performance de l'acteur.
        
        V(s)V(s)
        
    - **Mise à jour** : Les deux composants sont entraînés simultanément pour améliorer la politique.
- **Avantages** :
    - **Efficacité** : Convergence plus rapide grâce à une meilleure estimation des valeurs.
    - **Flexibilité** : Peut gérer des environnements complexes avec des espaces d'actions et d'états larges.