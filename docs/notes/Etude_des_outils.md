# Etude des outils

### 1. **Frameworks d'apprentissage par renforcement (RL)**

### a) **Stable-Baselines3**

- **Description** : Stable-Baselines3 est une bibliothèque pour l'apprentissage par renforcement basée sur PyTorch. Elle inclut plusieurs algorithmes populaires comme PPO, DQN, et A2C, et est facile à utiliser pour implémenter des agents RL.
- **Avantages** :
    - Documentation claire et exemples nombreux.
    - Supporte plusieurs algorithmes bien adaptés à des environnements discrets comme les jeux de plateau.
    - Intégration avec PyTorch pour un contrôle plus précis sur l'entraînement des agents.
- **Inconvénients** :
    - Limité aux algorithmes standards, ce qui peut nécessiter des modifications si des approches plus avancées sont souhaitées.
- **Cas d'usage** : Idéal pour un projet où plusieurs algorithmes RL doivent être testés rapidement, tout en offrant une bonne flexibilité pour des ajustements spécifiques.

### b) **Ray RLlib**

- **Description** : Ray RLlib est conçu pour gérer des environnements distribués, mais peut aussi être utilisé pour des projets moins complexes. Il offre une grande variété d'algorithmes RL et s’intègre bien avec d'autres outils de calcul comme TensorFlow ou PyTorch.
- **Avantages** :
    - Prend en charge une grande variété d'algorithmes RL et est conçu pour être extensible.
    - Peut être utilisé avec PyTorch ou TensorFlow, ce qui donne plus de flexibilité dans la configuration des modèles.
- **Inconvénients** :
    - Plus complexe à mettre en œuvre que Stable-Baselines3 pour des projets de taille réduite.
- **Cas d'usage** : Utilisé lorsque des simulations plus complexes sont envisagées, ou lorsqu'un contrôle fin sur les algorithmes est nécessaire.

---

### 2. **Frameworks de deep learning : TensorFlow vs PyTorch**

### a) **PyTorch**

- **Description** : PyTorch est une bibliothèque de deep learning utilisée pour des projets variés, y compris l'apprentissage par renforcement. Elle est réputée pour sa facilité d'utilisation et son mode de calcul dynamique, ce qui facilite le développement de modèles complexes.
- **Avantages** :
    - Plus simple à utiliser pour le prototypage rapide et le débogage grâce à son calcul dynamique.
    - Très populaire dans la communauté de la recherche RL et bien documenté.
    - Meilleure intégration avec des outils comme Stable-Baselines3, qui est directement construit sur PyTorch.
- **Inconvénients** :
    - Nécessite parfois plus de configuration pour des tâches d’inférence à grande échelle.
- **Cas d'usage** : PyTorch est idéal pour les projets où la flexibilité est clé, particulièrement pour l'ajustement des modèles et des algorithmes d'apprentissage par renforcement.

### b) **TensorFlow**

- **Description** : TensorFlow est une autre bibliothèque populaire pour le deep learning, utilisée aussi bien en production qu’en recherche. Elle offre un support robuste pour les projets d’apprentissage automatique à grande échelle.
- **Avantages** :
    - Supporte des projets à grande échelle, avec une intégration solide dans des environnements de production.
    - TensorBoard pour la visualisation des résultats d'entraînement.
    - Large écosystème et compatibilité avec de nombreux autres outils.
- **Inconvénients** :
    - Plus difficile à manipuler pour le prototypage rapide, en raison de sa nature de calcul statique.
- **Cas d'usage** : TensorFlow est plus adapté aux projets d'apprentissage automatique à grande échelle et aux situations où des besoins de production sont présents.

---

### 3. **Frameworks pour l'environnement multi-agents et simulation : Gym et PettingZoo**

### a) **OpenAI Gym**

- **Description** : OpenAI Gym est l’un des cadres les plus populaires pour la création et l’utilisation d’environnements d’apprentissage par renforcement. Il propose des environnements standards pour tester des algorithmes RL et permet également de créer des environnements personnalisés.
- **Avantages** :
    - Large support d'algorithmes RL via de nombreuses bibliothèques comme Stable-Baselines3.
    - Documentation exhaustive et large communauté.
    - Intégration facile avec des environnements standards (Atari, CartPole) et possibilité de créer un environnement personnalisé, par exemple pour simuler **Blokus**.
- **Inconvénients** :
    - Nécessite la création d'un environnement personnalisé pour les jeux complexes comme **Blokus**, car les environnements disponibles par défaut sont limités.
- **Cas d'usage** : Approprié pour modéliser un environnement simple ou standard, avec des algorithmes RL bien établis. Peut être utilisé pour créer un environnement personnalisé pour **Blokus**, mais demande du développement spécifique.

### b) **PettingZoo (pour environnements multi-agents)**

- **Description** : PettingZoo est une bibliothèque conçue pour simuler des environnements d'apprentissage par renforcement multi-agents. Elle permet d'entraîner des agents qui interagissent entre eux, ce qui est particulièrement utile pour des jeux de plateau comme **Blokus**.
- **Avantages** :
    - Prise en charge native des environnements multi-agents.
    - Permet d’entraîner plusieurs agents en compétition ou en coopération.
    - Intégration avec des algorithmes via d'autres bibliothèques comme Stable-Baselines3.
- **Inconvénients** :
    - Moins de documentation et de maturité que Gym, ce qui peut nécessiter plus d'efforts de configuration.
    - Nécessite la création d'un environnement personnalisé pour **Blokus**, car il n'est pas disponible par défaut.
- **Cas d'usage** : Idéal pour des projets multi-agents comme **Blokus**, où plusieurs agents doivent interagir, que ce soit en compétition ou en coopération.

### c) **Alternatives :**

- **MADRaS (Multi-Agent Reinforcement Learning Simulator)** : Une autre option pour les environnements multi-agents. Elle se concentre principalement sur les interactions entre agents dans un cadre discret et permet de simuler différents scénarios de jeu.
    - **Avantages** : Bonne pour les environnements complexes nécessitant de nombreuses interactions entre agents.
    - **Inconvénients** : Moins documentée et plus complexe à configurer par rapport à Gym et PettingZoo.
- **MultiAgentGym** : Basé sur OpenAI Gym, mais spécialisé dans les environnements multi-agents. Il peut être une alternative à PettingZoo pour simuler des jeux multi-agents de façon plus directe.
    - **Avantages** : Proche de Gym, donc facile à prendre en main si Gym est déjà utilisé.
    - **Inconvénients** : Moins flexible pour des environnements très personnalisés, mais bien adapté pour des agents qui interagissent dans des jeux de plateau classiques.

---

### 4. **Propositions pour l'affichage du jeu**

### a) **Pygame**

- **Description** : Pygame est une bibliothèque Python qui permet de créer des jeux 2D. Elle est idéale pour simuler des environnements de jeux de plateau comme Blokus, en fournissant des outils simples pour dessiner le plateau, les pièces et gérer les interactions.
- **Avantages** :
    - Simple à utiliser pour créer des interfaces graphiques de base et des simulations de jeux de plateau.
    - Permet de visualiser facilement les actions des agents RL en temps réel.
- **Inconvénients** :
    - Moins adapté pour des visualisations complexes, mais suffisant pour des jeux de plateau 2D.
- **Cas d'usage** : Pygame est approprié pour créer une interface graphique simple où les agents peuvent jouer à **Blokus** tout en permettant aux humains de suivre la progression des parties.

### b) **Matplotlib (pour visualisation simple)**

- **Description** : Matplotlib est une bibliothèque Python pour créer des visualisations de données. Elle peut être utilisée pour dessiner le plateau de jeu et les pièces, bien que ce soit une solution moins interactive.
- **Avantages** :
    - Très simple à configurer pour des visualisations statiques du plateau et des mouvements des pièces.
    - Utile pour visualiser les résultats des parties après simulation, sous forme d'images.
- **Inconvénients** :
    - Moins adaptée pour des interactions en temps réel ou pour un suivi en direct de la progression du jeu.
- **Cas d'usage** : Matplotlib convient pour des visualisations basiques des états du jeu après simulation, ou pour créer des images du plateau pour l'analyse des stratégies des agents.