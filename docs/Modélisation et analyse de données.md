# Modélisation et analyse de données

## Modification des class

- dans la class Player : ajouter des attributs comme
    - self.strategy
    - self.difficulty
    - self.history = [] # mémoire
- dans la class Game :
    - self.rules → adapter le code actuel (une fois premiere version avec agents réalisés) pour faire varier les règles
- créer une classe Match qui pour des joueurs donnés et des règles données, des résultats donnée → construit stat

## DB

- utiliser une base de données relationnelle comme SQLite ou PostgreSQL
- envisager les csv ou les json pour les exports de données
- librairies habituelles pour analyse de données et visualisation (pandas, scipy, matplotlib, searborn, plotly, …)

## Types de visualisations

- comparer les agents : barre, au cours du temps et des entrainements, déterminer quel est le meilleur match (les meilleures adversaires) pour chacun d’entre eux
- heatmaps pour visualiser l’efficacité des stratégies selon les règles appliquées ? (à voir)
- streamlit ? interactif et déjà beaucoup de choses mises en place → dashboard interactif

## Intégration

- automatiser le reporting après chaque simulation pour situer la partie avec les memes parametres etc par rapport “à d’habitude”

---

| Match |  |
| --- | --- |
| match_id | pk auto increment : numéro de la partie, identifiant unique |
| date | timestamp |
| duration | durée de la partie |
| set de règles |  |
| set de joueurs |  |
| winner |  |

| Agent |  |
| --- | --- |
| agent_id | pf auto incr |
| name |  |
| strategy |  |
| difficulty |  |
| nb parties |  |
| descr | texte pour expliquer ce qu’il apprécie ou non |
|  | ! comment gérer le cas des humains ? s’enregistrer en tappant son nom au début de la partie ? |

| Participants |  |
| --- | --- |
| participant_id | pk |
| match_id |  |
| agent_id |  |
| numéro ordre | si il a joué en premier, deu, trois ou quatre |
| nb_adversaire |  |
| score |  |
| winner |  |