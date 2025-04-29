<div align="right">
  <a href="README.md">English</a> |
  <b>Français</b>
</div>

# Développement d’agents autonomes et création de nouvelles règles pour jeux de plateau via l’apprentissage par renforcement
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

## Description du Projet 🎮🤖

Ce projet explore l'apprentissage par renforcement appliqué à des jeux de plateau, avec un focus sur le célèbre jeu de société Ludo (également connu sous le nom de "Petits Chevaux"). Initialement, nous avions expérimenté avec le jeu Labyrinthe, mais ce choix a été abandonné en raison de contraintes spécifiques, comme expliqué dans la documentation.

---

### Description reformulée du sujet et les objectifs du projet

Ce projet vise à développer différents agents autonomes pour des jeux de plateau en s’appuyant sur des
techniques d’apprentissage par renforcement. L’objectif principal est double : d’une part, entraîner ces
agents à adopter des stratégies optimales adaptées aux règles du jeu, et d’autre part, étudier les interactions
entre différentes règles et différents types d’agents afin d’analyser leur influence sur la jouabilité et l’équilibre
global du jeu.

1. Modélisation du jeu
    - Représenter le jeu de manière formelle, avec ses états, actions et espaces d’observation.
    - Intégrer dès le départ la possibilité d’ajouter des règles ou variantes futures, en prévoyant une
architecture flexible.

2. Apprentissage par renforcement
    - Utiliser des techniques de RL pour entraîner des agents autonomes capables de jouer effica-
cement au jeu choisi.
3. Comportements et personnalisation des agents
    - Développer différents types d’agents, chacun ayant des stratégies distinctes.
    - Étudier leurs comportements face aux variantes des règles testées.
4. Ajout de nouvelles règles et variantes
    - Analyser comment ces variantes influencent les comportements des agents.
    - Tester l’impact de différentes règles sur la jouabilité et l’équilibre du jeu.
5. Analyse statistique des parties simulées
    - Collecter des statistiques détaillées sur les parties jouées par les agents pour évaluer leurs
performances.
    - Définir des critères pour comparer les règles ou les variantes afin de déterminer ce qui améliore
le gameplay.

## Fonctionnalités principales :
🧠 Création d'agents : Plusieurs agents ont été développés, utilisant notamment l'algorithme Proximal Policy Optimization (PPO) pour optimiser leurs stratégies.  
⚙️ Entraînement des agents : Les agents ont été entraînés sur des environnements simulés, avec des règles variées pour modéliser différents scénarios de jeu.  
🎲 Simulation de parties : Nous avons simulé des affrontements entre agents pour analyser leurs performances dans différents contextes, tout en testant les impacts des variations de règles.  
📊 Analyse des performances : Une analyse approfondie des résultats a été réalisée à l'aide de techniques statistiques et des outils dédiés. 
🎮 Interface graphique interactive : L’interface graphique développée permet à l’utilisateur humain d’affronter les agents directement ou de simuler des parties entre humains.

---

## Règles du Jeu et Variations 📝🎲

### Règles de Base :

- Chaque joueur commence avec tous ses pions dans son écurie.
- Un 6 au dé est requis pour sortir un pion de l'écurie.
- Une fois sur le plateau, les pions avancent sur un chemin commun de 56 cases menant à un escalier de 6 cases, propre à chaque joueur, qui aboutit à une case objectif.
- Règles pour les déplacements dans le chemin commun :
    - Tuer un pion adverse : Un pion peut éliminer un pion adverse uniquement s’il tombe exactement sur la même case.
    - Rejoindre un pion allié : Un pion d’un joueur peut rejoindre un autre pion du même joueur uniquement si le résultat du lancer de dé correspond exactement à la distance qui les sépare.
    - Rester bloqué derrière un pion : Si la valeur du dé est supérieure au nombre de cases jusqu’au pion suivant sur le plateau (qu’il appartienne au même joueur ou à un adversaire), le pion avancera jusqu’à la case précédant l’obstacle. Les dépassements de pions sont interdits. Ces règles ne s’appliquent pas à l’escalier.
- **Disposition des écuries selon le nombre de joueurs** :
    - **2 joueurs** : Les écuries sont placées à l'opposé l'une de l'autre sur le plateau. Ainsi, la case 1 du chemin pour un joueur correspond à la case 29 pour l'autre.
    - **3 ou 4 joueurs** : Les écuries sont réparties de manière équidistante toutes les 14 cases. Une même case peut être perçue différemment selon le point de vue du joueur :
        Par exemple, la case 1 pour un joueur sera la case 15, case 29 ou case 43 pour les autres joueurs, en fonction de leur position de départ.
        
    Cela garantit une répartition équilibrée des positions de départ sur le plateau.

### Variations des Règles :
- Nombre de joueurs :
    - Le jeu peut être joué à 2, 3 ou 4 joueurs.
- Nombre de pions par joueur :
    - Chaque joueur peut avoir entre 2 et 6 petits chevaux en jeu.
- Conditions de victoire :
    - Victoire rapide : Le premier joueur à atteindre l’objectif avec un seul pion gagne.
    - Victoire complète : Tous les pions d’un joueur doivent atteindre l’objectif pour déclarer sa victoire.
- Règles pour atteindre le pied de l'escalier :
    - Exactitude nécessaire : Un pion doit atteindre exactement la case située au pied de l'escalier pour commencer à le gravir.
        - Si le lancé de dé dépasse la distance requise pour atteindre cette case, le pion peut avancer puis reculer, à condition que ce mouvement réduise la distance qui le sépare de la case au pied de l'escalier.
        - Si, en avançant puis reculant selon la valeur du dé, le pion finit par s'éloigner davantage de la case pied de l'escalier, alors il ne peut pas être déplacé.
    - Progression simplifiée : Si la valeur du dé dépasse le pied de l’escalier, le pion grimpe directement comme si l’escalier faisait partie du chemin.
- Ordre de progression sur l’escalier :
    - Ordre simplifié : Un pion avance de la distance indiquée par le dé. Cela lui permet de monter plusieurs marches de l’escalier en un seul lancer, et d’atteindre directement la case objectif si la valeur du dé le permet ou la dépasse.
    - Ordre strict (autorisé uniquement si l’exactitude est requise pour atteindre le pied de l’escalier):
        - Chaque marche de l’escalier nécessite un lancer spécifique : 1 pour la première marche, 2 pour la deuxième, ..., et 6 pour atteindre la case objectif.
        - Une règle optionnelle peut être ajoutée pour permettre ou non au pion de rejouer après chaque montée de marche.
- Rejouer en cas de lancer d’un 6 : Cette règle peut être activée ou désactivée.
- Protection des pions : Si deux pions d’un même joueur se trouvent sur la même case, ils deviennent invulnérables et ne peuvent pas être éliminés. Cette règle peut être activée ou désactivée.

## Différents agents : 

Dans notre projet, nous avons développé six types d'agents distincts, chacun avec sa propre stratégie et son système de récompenses :

- **Agent Balanced (Équilibré)** : Agent utilisant une stratégie équilibrée entre attaque et progression, servant de référence pour comparer les autres agents.

- **Agent Aggressive (Agressif)** : Agent privilégiant les actions offensives avec des récompenses maximales pour l'élimination des pions adverses.

- **Agent Rusher (Pressé)** : Agent focalisé sur la progression rapide vers l'objectif avec un système de récompenses favorisant les mouvements vers l'avant et l'atteinte du but.

- **Agent Defensive (Défensif)** : Agent priorisant la sécurité des pions avec des récompenses importantes pour l'atteinte des zones sûres et la protection mutuelle des pions.

- **Agent Spawner (Sortie rapide)** : Agent concentré sur la sortie rapide des pions de l'écurie avec des récompenses maximales pour les actions de sortie.

- **Agent Suboptimal (Sous-optimal)** : Agent simulant un joueur inexpérimenté avec des récompenses plus élevées pour les actions généralement moins efficaces.

Chaque agent dispose de sa propre table de récompenses, adaptée selon sa stratégie. Cette diversité permet d'explorer différentes approches du jeu et d'étudier leur efficacité relative dans différentes configurations de règles.

### Mindmap résumant les différentes configurations

![Mindmap des règles du jeu](/docs/mindmap_setup.png)

---

## Technologies utilisées :
🐍 Python : Langage principal pour la gestion du jeu et des agents.  
🛠️ Gymnasium : Environnements personnalisés pour l'apprentissage par renforcement.  
🤖 Stable-Baselines3 : Bibliothèque utilisée pour entraîner les agents sur les environnements Gymnasium.  
🗄️ PostgreSQL : Base de données pour stocker les résultats des simulations et les métriques des agents.  
📊 Pandas et Jupyter Notebook : Analyse et visualisation des performances des agents.  
🎨 Pygame : Interface graphique pour visualiser les parties en temps réel.  
✅ Pytest : Tests unitaires pour garantir la fiabilité du code.  

--- 

## Installation 

#### Version de Python 
Nous avons utilisé **Python 3.11** pour ce projet.
Assurez-vous que cette version est installée sur votre machine : 

##### Installation de Python 3.11
- MacOS (via Homebrew) : 
```bash
brew install python@3.11
```

- Linux (Ubuntu):
```bash
sudo apt update
sudo apt install python3.11
```

##### Vérification de l'installation : 
```bash
python3.11 --version
```

#### Création de l'environnement virtuel
Pour garantir la compatibilité et faciliter les tests, nous avons utilisé `venv`.

##### Vérifier la disponibilité de `venv``
```bash
python3.11 -m venv --help
```
- Si cette commande fonctionne, vous pouvez continuer.
- Sinon installez `venv`:
    - Sous MacOS, lorsque Python 3.11 est installé via Homebrew, le module `venv` est inclus par défaut. Si la commande précédent a généré une erreur : 
    ```bash
    brew update
    brew upgrade python
    brew reinstall python@3.11
    ```

    - Linux (Ubuntu)
    ```bash
    sudo apt update
    sudo apt install python3.11-venv
    ```


##### Étapes pour créer et configurer l'environnement virtuel 
- Créer l'environnement virtuel
Depuis la racine du projet : 
```bash
python3.11 -m venv ludo_venv
```

- Activer l'environnement virtuel 
    ```bash
    source ludo_venv/bin/activate
    ```

- Mettre à jour `pip` dans l'environnement virtuel
```bash
pip install --upgrade pip
```

- Installer les dépendances 
```bash
pip install -r requirements_venv.txt
```

##### Désactiver l'environnement virtuel
Une fois que vous avez terminé vos tests ou que vous n'avez plus besoin d'utiliser l'environnement virtuel, vous pouvez le désactiver facilement. Cela vous permettra de revenir à votre environnement Python global ou de système.

Pour désactiver l'environnement virtuel, exécutez simplement la commande suivante :
```bash
deactivate
```

Cela désactive l'environnement virtuel actif sans supprimer ses fichiers. Vous pourrez le réactiver ultérieurement si nécessaire.

### Utilisation de l'environnement virtuel dans les notebooks 

Pour les analyses, expérimentations et entraînements, nous avons utilisé des notebooks Jupyter via VSCode. Si vous souhaitez exécuter un notebook dans le cadre de ce projet, nous vous recommandons d’utiliser VSCode, car nous n'avons pas testé cette configuration avec d'autres outils ou éditeurs.

Le package `ipykernel`, nécessaire pour connecter l'environnement virtuel aux notebooks Jupyter, est déjà inclus dans les dépendances listées dans le fichier `requirements_venv.txt`.

##### Étapes pour configurer le kernel dans VSCode : 

- Ouvrez un notebook `.ipynb` dans VSCode
- Cliquez sur **Run All** ou sur l'option **Select Kernel** située en haut à droite de l'interface.
- Dans le menu qui s'affiche, cliquez sur **Select Another Kernel...**
- Dans la section **Python Envrionments**, choisissez l'environnement virtuel correspondant (`ludo_venv`)

Une fois ces étapes terminées, le notebook sera configuré pour utiliser l'environnement virtuel, et vous pourrez exécuter vos analyses en toute compatibilité avec les dépendances du projet.

### Étapes pour configurer la base de données

Veuillez vous référer au fichier suivant pour les instructions complètes sur la configuration de PostgreSQL, la création de la base de données ludo_stats, et l'initialisation de sa structure : `./db/Windows_db_configuration_and_setup.md` et `./db/Ubuntu_db_configuration_and_setup.md`

Ces instructions sont spécifiquement adaptées pour Windows et Ubuntu. Si vous utilisez un autre système d'exploitation, elles peuvent ne pas fonctionner. Dans ce cas, veuillez chercher sur internet comment installer PostgreSQL pour votre environnement.

Notez que **l'installation de PostgreSQL n'est pas obligatoire**, sauf si vous souhaitez enregistrer de nouvelles données. Les données nécessaires pour nos analyses ont déjà été exportées en fichiers CSV et se trouvent dans le dossier `db/data`.

---

## Lancer une partie avec interface graphique
Pour jouer avec l'interface graphique, placer vous dans le dossier `game`

```bash
cd game
```

Puis exécuter le fichier `play.py` comme ceci:

```bash
python3 play_pygame/play.py
```

Voici un extrait d'une partie montrant un joueur humain et trois agents en action.
![Demo of the app](docs/demo_assets/demo_pc_1humain_3agents.gif)

#### Agents Non Entraînés
Après avoir configuré les règles du jeu selon vos préférences, il est possible que l'agent correspondant à cette configuration ne soit pas encore entraîné. Si un agent non entraîné est utilisé, le programme échouera.
Dans ce cas, il faut relancer le programme et choisir une configuration de règles différente.

**Message d'Erreur Attendu**

Voici un exemple de message d'erreur qui peut apparaître dans ce cas :
```bash
"Le fichier <model_file_name> n'existe pas. Veuillez entraîner l'agent avant de l'utiliser."
```
---

## Tests avec Pytest

Afin de garantir que la logique du jeu est robuste et fonctionne comme prévu, nous avons mis en place des tests unitaires avec Pytest. Ces tests couvrent différents aspects de la logique du jeu pour s'assurer que chaque fonctionnalité est correctement implémentée.

#### Lancer les tests Pytest 
Pour exécuter les tests, utilisez la commande suivante à la racine du projet :
```bash
pytest game/tests_pytest/
```

#### Résultat attendu
Si tous les tests passent avec succès, vous devriez voir une sortie similaire à celle-ci :

```bash
============================== 81 passed, 1 warning in 1.30s ==============================
```

Cela indique que 81 tests ont été validés avec succès. Le warning peut être dû à une dépendance ou une configuration et ne devrait pas affecter le fonctionnement principal du jeu.

---


## Résultats et analyses

### Base de données et simulations de parties

#### Base de données

Le projet s’appuie sur une base de données relationnelle PostgreSQL pour collecter, structurer et analyser les données générées lors des simulations de parties. Cette base de données centralise des informations pertinentes sur les joueurs, les parties, les règles et les actions effectuées.

![Schéma de la base de données](docs/schema_db.jpg)

#### Simulations de parties

Les simulations de parties sont exécutées de manière automatisée grâce au fichier `ludo_stats_play.py` depuis le dossier `./db`. Ce script est conçu pour lancer un grand nombre de parties entre agents, avec pour objectif principal d’enregistrer les données générées lors de chaque partie. Les statistiques collectées, telles que les performances des agents, leurs actions, leurs scores, et les résultats des parties, sont automatiquement sauvegardées dans la base de données. Ces informations servent ensuite à l'analyse des performances et des comportements des agents.

Les données générées lors des simulations sont enregistrées dans la base de données, puis exportées au format CSV pour faciliter leur analyse dans des notebooks Python. Ces fichiers constituent la base d’analyses détaillées, permettant de visualiser des métriques clés telles que les scores obtenus, les taux d’erreurs, ou encore la répartition des types d’actions effectuées par les agents. Ces analyses visent à démontrer l’efficacité de l’entraînement des agents, leurs performances, mais aussi à identifier les marges d’amélioration dans leurs comportements et stratégies.

### Analyse de l'entrainement des agents 

NB : L'analyse complète de l'entrainement est disponible dans le notebook `db/analyse/analyse_entrainement.ipynb`.

#### Objectif

Étudier l'entrainement des agents RL en analysant l'évolution de leurs performances en fonction du nombre de pas d'entraînement, à travers des configurations de jeu de complexité croissante.

#### Données et paramètres de l'analyse
**Données**  

Les données utilisées pour cette analyse ont été collectées à partir de simulations massives de parties entre
agents identiques, c’est-à-dire de même type et de même nombre de pas d’entraînement, lancées avec la fonction `main_lancer_parties_pour_analyse_entrainement()` du fichier `ludo_stats_play.py`.

**Métriques**  
- Répartition des types d'actions demandées
- Pourcentage moyen d'erreurs
- Score moyen des agents

**Configurations**  
- Configuration 16 : Règles de base sans contraintes
- Configuration 12 : Règles intermédiaires avec contraintes
- Configuration 17 : Règles complètes avec interactions avancées

**Nombre et types d'agents**  
Tous les types agents ont été étudiés (Balanced, Aggressive, Rusher, Defensive, Spawner, et Suboptimal) dans des parties avec : 2 joueurs et 2 pions, 2 joueurs et 4 pions, et 4 joueurs et 4 pions. Nous avons entrainé, fait jouer, et analysé les performances de ces agents avec les nombres pas d'entrainement suivants : 50 000, 100 000, 200 000, et 400 000.

#### Résultats

Les résultats ont montrés que d'une manière générale, l'entraînement des agents permet l'apprentissage progressif de nouvelles actions, confirmant que le processus d'entraînement fonctionne. Les agents apprennent à s'adapter à leur environnement et à maîtriser les règles associées.

Pour la **configuration 16**, la plus simple, les agents montrent des performances claires et stables. Le pourcentage moyen d'erreurs diminue, et les scores augmentent au cours de l'entrainement, indiquant une bonne capacité d'adaptation à l'environnement. En revanche, l'augmentation du nombre de joueurs et de pions provoque un ralentissement de l'entrainement. 

Exemple pour l'agent aggressive :
![16-2-2-aggressive](/docs/graphiques_analyse_entrainement/16-2-2-aggressive.png)
![16-2-4-aggressive](/docs/graphiques_analyse_entrainement/16-2-4-aggressive.png)
![16-4-4-aggressive](/docs/graphiques_analyse_entrainement/16-4-4-aggressive.png)

Avec l'introduction de règles supplémentaires, les performances des agents deviennent moins stables. Bien que certains agents continuent de progresser, d'autres montrent des fluctuations dans leurs taux d'erreurs et leurs scores. 

Pour la **configuration 12**, l'entraînement reste efficace, mais il est moins concluant que pour la configuration 16. Les agents apprennent certaines actions adaptées aux nouvelles règles, mais leur capacité d'adaptation est moins marquée, et les performances globales restent limitées.

Exemple de l'agent aggressive :
![12-2-2-aggressive](/docs/graphiques_analyse_entrainement/12-2-2-aggressive.png)

- Actions 50000 pas : NO_ACTION
- Nouvelles actions 100000 : MOVE_FORWARD, MARCHE_2
- Nouvelles actions 200000 : KILL
- Nouvelles actions 400000 : AVANCE_RECULE_PIED_ESCALIER

Exemple de différence entre les agents aggressive et balanced :
![12-4-4-aggressive](/docs/graphiques_analyse_entrainement/12-4-4-aggressive.png)
![12-4-4-balanced](/docs/graphiques_analyse_entrainement/12-4-4-balanced.png)

Enfin, dans la **configuration 17**, la plus complexe, les agents rencontrent les plus grandes difficultés. Le pourcentage moyen d'erreurs reste élevé, et les scores moyens restent très faibles, montrant une incapacité des agents à apprendre les règles du jeu. De plus, l'apprentissage de nouvelles actions est plus lent.

Exemple de l'agent aggressive :
![17-2-2-aggressive](/docs/graphiques_analyse_entrainement/17-2-2-aggressive.png)

- Actions 50000 pas : NO_ACTION
- Nouvelles actions 100000 : MOVE_FORWARD
- Nouvelles actions 200000 : MARCHE_6
- Nouvelles actions 400000 : MOVE_OUT


Ces résultats montrent que les agents s'entrainent bien pour des configurations de règles simples, mais mettent cependant en évidence les limites des agents RL à s'adapter à des environnements de plus en plus complexes.

### Analyse des performances des agents

L'analyse complète des performances des agents est disponible dans le notebook `db/analyse/analyse_agents.ipynb`. Nous présentons ici une synthèse des résultats principaux.

L'étude des performances des agents dans notre jeu représente un défi analytique important en raison du nombre considérable de configurations possibles : 32 configurations de règles différentes, parties à 2 ou 4 joueurs, 6 types d'agents, et possibilités de 2 ou 4 pions par joueur. Nous nous sommes donc concentrés sur les configurations les plus représentatives pour illustrer nos analyses.

#### Performance des agents au sein d'une configuration fixe

Pour la configuration 8, qui offre un équilibre intéressant entre les différentes stratégies, nous avons analysé les performances relatives des agents.

![Matrice des taux de victoire entre agents](/docs/graphiques_analyse_agents/taux_victoire_conf8.png)

*Figure 1: Matrice des taux de victoire entre agents (configuration 8)*

Cette matrice révèle des différences significatives dans l'efficacité des stratégies. Par exemple, l'agent aggressive montre une forte domination contre l'agent defensive (62% de victoires) mais peine davantage face à l'agent rusher (49% de victoires).

Dans les parties à quatre joueurs, la dynamique change significativement :

![Distribution des positions finales](/docs/graphiques_analyse_agents/distribution_places_conf8.png)

*Figure 2: Distribution des positions finales par type d'agent en parties à 4 joueurs*

Face à des adversaires multiples, les écarts de performance se réduisent. L'agent defensive atteint la première place aussi souvent que l'agent aggressive, mais montre des performances moindres pour les deuxièmes places.

#### Satisfaction des agents selon les règles

La satisfaction des agents a été évaluée selon des métriques spécifiques à chaque stratégie. Pour l'agent aggressive par exemple :

![Satisfaction de l'agent aggressive](/docs/graphiques_analyse_agents/satisfaction_aggressive.png)

*Figure 3: Nombre moyen d'éliminations par partie selon les configurations*

Les configurations 11 et 12, avec leurs contraintes plus strictes sur la progression vers l'objectif, permettent plus d'éliminations et donc une meilleure satisfaction pour l'agent aggressive. Cependant, ce taux de satisfaction élevé ne correspond pas toujours à un meilleur taux de victoire.

#### Équilibre et jouabilité

L'analyse de la configuration 7 révèle des aspects intéressants sur l'équilibre du jeu :

![Longueur des parties](/docs/graphiques_analyse_agents/longueur_parties_conf7.png)

*Figure 4: Distribution des longueurs de parties selon les types d'agents*

La durée des parties reste remarquablement stable quelle que soit la combinaison d'agents, suggérant un bon équilibre général.

Cependant, l'analyse des parties 2v2 montre une autre réalité :

![Distribution des pions en 2v2](/docs/graphiques_analyse_agents/pions_objectif_2v2.png)

*Figure 5: Distribution du nombre de pions à l'objectif par équipe*

La dispersion des points révèle que certaines combinaisons d'agents sont nettement plus efficaces que d'autres pour atteindre l'objectif, indiquant des déséquilibres dans cette configuration.


---

## Arborescence du projet

### À la racine 

Voici la structure des principaux dossiers et fichiers de ce projet, avec une description de leur contenu et rôle.

```bash
.
├── README.md
├── README.fr.md
├── docs/
├── db/
├── game/
├── resources/
└── requirements_venv.txt
```

#### Description des dossiers et fichiers

- `README.md` : Contient la documentation principale du projet, y compris les objectifs, instructions d'installation et exemples d'utilisation en anglais.
- `README.fr.md`: Contient la documentation principale du projet, y compris les objectifs, instructions d'installation et exemples d'utilisation en français.
- `docs/` : Utilisé tout au long du semestre pour centraliser les recherches, notes, explications, choix d'équipe et toute trace écrite utile à communiquer.
Contient également les fichiers de documentation complémentaires, tels que :
    - Des explications techniques sur le projet.
    - Des captures d'écran ou diagrammes pour illustrer les concepts clés.
- `db/` : Ce dossier stocke les fichiers nécessaires à la gestion et à l’exploitation des données du projet. Il contient :
    - Les scripts pour initialiser la base de données, insérer des données, et les exporter au format CSV.
    - Les données exportées utilisées pour les analyses.
    - Des notebooks pour analyser les performances et l’entraînement des agents.
    - Les fichiers de configuration de la base PostgreSQL.
    - Des scripts pour gérer les règles du jeu et les configurations des parties simulées.
- `game/`: Ce dossier constitue le cœur du projet et contient :
    - La logique interne du jeu, ainsi que l'environnement Gym attaché pour les simulations et l'apprentissage par renforcement.
    - Les fichiers nécessaires pour lancer le jeu avec une interface graphique.
    - Des notebooks dédiés à l'apprentissage automatique, permettant d'entraîner et d'évaluer des agents.
    - Des tests en pytest pour garantir que la logique du jeu respecte les règles définies.
- `resources/` : Contient les documents liés au projet :
    - `project-presentation-slideshow-fr.pdf`: Diaporama de présentation du projet en français.
    - `project-report-fr.pdf`: Rapport complet du projet rédigé en français.
    - `project-assignment-fr.pdf`: Énoncé initial du projet en français.

- `requirements_venv.txt` : Une version spécifique des dépendances utilisée avec l’environnement virtuel.

### `game/`

```bash
game/
├── __init__.py                  
├── images/                        
├── ludo_env/                    
├── play_pygame/    
├── reinforcement_learning/        
└── tests_pytest/                  
```

- `__init__.py` : Fichier d'initialisation pour le module Python.
- `images/` : Contient les images utilisées pour l'interface graphique.
-  `ludo_env/`: Ce répertoire contient l’implémentation complète de l’environnement Gym pour le jeu Ludo, incluant :
    - La logique du jeu.
    - La gestion des états et actions.
    - L'intégration avec Gym pour permettre l’entraînement d’agents RL.
- `play_pygame/`: Dossier contenant le code pour jouer au jeu avec une interface graphique développée avec Pygame.
- `reinforcement_learning/` : Inclut les notebooks et scripts relatifs à l'apprentissage par renforcement.
- `tests_pytest/`: Contient les tests unitaires écrits avec pytest pour s'assurer que :
    - Les règles du jeu sont correctement implémentées.
    - Les actions de l’environnement respectent les contraintes définies.
    - Les résultats sont conformes aux attentes pour différents scénarios.

### `game/ludo_env`

```bash
game/                     
└── ludo_env/                    
    ├── __init__.py              
    ├── action.py                
    ├── env.py                   
    ├── game_logic.py            
    ├── renderer.py             
    ├── reward.py                
    └── state.py                 
```

- `__init__.py` : Ce fichier fait de ludo_env un module Python. Il permet d'importer facilement les fichiers du répertoire dans d'autres parties du projet.
- `action.py` : Définit les actions disponibles pour les agents dans le jeu.
- `env.py` : L’environnement Gym au cœur du projet
    -  Le fichier env.py est une composante centrale de notre implémentation. Il constitue une interface standardisée pour :
        - Jouer au jeu Ludo entre humains via une interface graphique ou textuelle.
        - Effectuer des entraînements en apprentissage par renforcement (RL).
        - Simuler des milliers de parties afin de collecter des données statistiques ou évaluer les performances des agents.

    - Fonctions principales de env.py 
        - `reset()`: Initialise une nouvelle partie et met l’environnement dans son état de départ.
    Retourne l’état initial du plateau sous une forme exploitable par l’agent RL ou par des simulations.
        - `step(action)`: Reçoit une action (proposée par un agent ou un humain).
    Exécute cette action, calcule les conséquences (récompense, état suivant, fin de partie, etc.) et retourne :
            - Le nouvel état.
            - Une récompense associée à l’action.
            - Un indicateur booléen précisant si la partie est terminée.
            - Des informations supplémentaires utiles pour le débogage ou l’analyse.
        - `render()`: Affiche l’état actuel du plateau.

    - Modes et fonctionnalités spécifiques
        - Mode Entrainement 
            - Utilisé pour entraîner des agents en apprentissage par renforcement (RL) avec des algorithmes tels que PPO (Proximal Policy Optimization).
            - Interaction continue avec Stable-Baselines3, où env.py agit comme un pont entre l’algorithme et le jeu.

        - Mode Interface
            - Permet de jouer directement via une interface, que ce soit entre humains ou contre des agents.
            - Gestion des actions non autorisées : Si un agent propose une action invalide (par exemple, déplacer un pion qui ne peut pas bouger), une fonction de `reward.py` corrige cette action en la remplaçant par une action autorisée.
            - La correction suit un ordre par défaut, basé sur le type d'agent.

        - Mode Statistiques
            - Conçu pour analyser les performances des agents en simulant des parties complètes.
            - Deux informations clés sont enregistrées pour chaque action :
                - Si l’action initialement proposée est valide.
                - L’action réellement exécutée (après correction, si nécessaire).
            - Cela permet d’évaluer non seulement les performances des agents, mais aussi leur capacité à proposer des actions conformes aux règles.

- `game_logic.py`: Contient l'implémentation des règles du jeu, la logique du jeu. Gère les actions ainsi que leurs conséquences, vérifie quelles actions sont autorisées à un moment donné... Gère les validations des mouvements (déplacement autorisé ou non), les captures de pions, et la détection des conditions de victoire.
- `renderer.py`: Responsable de l'affichage du jeu.
- `reward.py`: Implémente les fonctions de récompense pour guider l’apprentissage des agents.
Les récompenses peuvent être basées sur :
La progression des pions sur le plateau.
La capture d’un pion adverse.
L’atteinte de la zone d’arrivée.
- `state.py`: Définit les états dans lesquels peuvent se trouver les pions.

### `db/`

Le dossier `db/` regroupe tous les éléments nécessaires pour gérer la base de données associée au projet, les scripts pour collecter, transformer et analyser les données, ainsi que les données utilisées pour nos analyses.

```bash
db/
├── analyse/
│   ├── analyse_agents.ipynb
│   └── analyse_entraînement.ipynb
├── data/
│   ├── action_stats.csv
│   ├── game.csv
│   ├── game_rule.csv
│   ├── is_rule_of.csv
│   ├── participant.csv
│   ├── player.csv
│   └── set_of_rules.csv
├── secret/                     # Dossier à créer en local
│   └── config.py
├── config_game.py
├── export.py
├── insert.py
├── ludo_stats_play.py
├── notes_db.md
├── rules.py
├── schema.py
├── Ubuntu_db_configuration_and_setup.md
└── Windows_db_configuration_and_setup.md
```
- `analyse/` : Dossier contenant les notebooks d'analyse des agents
    - `analyse_agents.ipynb` : Notebook d'analyse de performance des agents entraînés en fonction des configurations de jeu.
    - `analyse_entraînement.ipynb` : Notebook d'analyse de l'entrainement des agents
- `data/` : Dossier contenant les fichiers csv de données exportées depuis la base de données  et utilisés pour les analyses.
- `secret/config.py` : Fichier de configuration contenant l'URL de connexion à la base de données PostgreSQL. Ce dossier est à créer localement.
- `config_game.py` : Fichier contenant les fonctions nécessaires pour générer les configurations de jeu des parties entre agents.
- `export.py`: Script permettant d'exporter les données de la base de données au format CSV.
- `insert.py` : Fichier contenant les classes permettant d'insérer les données dans la base de données.
- `ludo_stats_play.py` : Scripts utilisés pour simuler les parties entre agents et enregistrer les données liées dans la base de données.  
Ce fichier contient plusieurs fonctions mains que nous avons utilisées selon nos besoins :
    - `main()` : Permet de lancer une ou plusieurs parties en définissant depuis le terminal : le nombre de joueurs, le nombre de pions, la configuration de règles, les agents a utiliser et le nombre de parties à lancer.
    - `main_auto()` : Permet de lancer automatiquement plusieurs parties entre des agents identiques (même type et même nombre de pas d'entrainement).  
    Il faut préciser la configuration de règles, le nombre de joueurs, le nombre de chevaux et le nombre de parties à lancer.  
    Lance toutes les parties pour tous les agents définis correspondant au nombre de joueurs, de pions et à la configuration spécifiée. 
    - `main_lancer_parties_pour_analyse_entrainement()` : Permet d'exécuter les parties générant les données nécessaires à l'analyse de l'entrainement des agents.
    - `main_lancer_auto_mathcups()`: Permet d'exécuter les parties générant les données nécessaires à l'analyse de des agents entraînés en fonction des configurations de jeu.
- `Ubuntu_db_configuration_and_setup.md` et `Windows_db_configuration_and_setup.md` : Fichiers fournissant les informations pour configurer et utiliser la base de données *ludo_stats*.
- `rules.py` : Fichier permettant de gérer les règles (définition, description et détermination dynamique).
- `schema.py` : Script permettant d'initialiser la base de données en créant les tables nécessaires.


---

Toutes les installations et fonctionnalités ont été testées sur Windows et Ubuntu. Sur macOS, tout a été vérifié, à l'exception de l'installation de PostgreSQL, qui n'est pas requise pour exécuter le jeu et effectuer les analyses.

## 📑 Documentation complète
Pour une vue d’ensemble complète de la méthodologie, des objectifs pédagogiques et techniques, des choix d’implémentation, de l’analyse des résultats et des discussions détaillées, veuillez consulter le [rapport complet du projet (en français)](./resources/project-report-fr.pdf) disponible dans ce dépôt.

## 👷 Contributeurs
- MARQUIS Zoé
- KRUZIC Charlotte
- KUDRIASHOV Daniil
- ZAITCEVA Ekaterina
