# Description de la base de données

Ce document présente les tables, leurs attributs, les clés primaires (PK), les clés étrangères (FK) et les relations entre les tables de la base de données.


## Schéma

![Texte alternatif](schema_db.jpg)


## Présentation des tables

### Player

- `player_id` (**PK**) : Identifiant unique du joueur
- `name` : Nom du joueur
- `is_human` : Indique si le joueur est humain
- `description` : Description du joueur
- `strategy` : Type de l'agent (balanced, aggressive, rusher, defensive, spawner, suboptimal)
- `difficulty` : Difficulté associée à l'agent
- `registration_date` : Date de création
- `nb_train_steps` : Nombre de pas d'entraînement

Les attributs `strategy`, `difficulty` et `nb_train_steps` sont spécifiques aux agents.

### GameRule

- `game_rule_id` (**PK**) : Identifiant unique de la règle de jeu
- `name` : Nom de la règle
- `description` : Description de la règle

### SetOfRules

- `set_of_rules_id` (**PK**) : Identifiant unique de l'ensemble de règles
- `name` : Nom de l'ensemble de règles
- `description` : Description de l'ensemble de règles
- `num_config` : Numéro de la configuration associée

### IsRuleOf

- `set_of_rules_id` (**PK**, FK SetOfRules) : Identifiant de l'ensemble de règles
- `game_rule_id` (**PK**, FK GameRule) : Identifiant de la règle de jeu

Cette table permet de faire le lien entre les tables SetOfRules et GameRule.

### Game

- `game_id` (**PK**) : Identifiant unique de la partie
- `set_of_rules_id` (FK SetOfRules) : Ensemble de règles associé à la partie
- `played_at` : Date et heure de la partie.
- `nb_participants` : Nombre de participants
- `nb_pawns` : Nombre de pions par joueur

### Participant

- `participant_id` (**PK**) : Identifiant unique du participant
- `game_id` (FK Game) : Partie associée
- `player_id` (FK Player) : Joueur associé
- `num_player_game` : Numéro du joueur dans la partie
- `action_stats` (FK ActionStats) : Lien vers les statistiques des actions associées
- `turn_order` : Ordre de jeu
- `reward_action_agent` : Récompense pour les actions que l'agent a voulu faire.  
Prend en compte les récompenses négative en cas de mouvement impossible.
- `reward_rectified` : Récompense pour les actions que l'agent a effectué.  
Prend en compte les récompenses des actions automatiques en cas de mouvement impossible.
- `nb_moves` : Nombre de coups effectués
- `is_winner` : Indique si le joueur est le gagnant
- `nb_actions_interdites` : Nombre d'actions interdites effectuées
- `nb_pawns_in_goal` : Nombre de pions ayant atteint l'objectif

### ActionStats

- `stat_id` (**PK**) : Identifiant unique des statistiques d'actions
- Nombre de chaque type d'actions demandées par l'agent :
  - `nb_no_action_d`
  - `nb_move_out_d`
  - `nb_move_out_and_kill_d`
  - `nb_move_forward_d`
  - `nb_get_stuck_behind_d`
  - `nb_enter_safezone_d`
  - `nb_move_in_safe_zone_d`
  - `nb_reach_goal_d`
  - `nb_kill_d`
  - `nb_reach_pied_escalier_d`
  - `nb_avance_recule_pied_escalier_d`
  - `nb_marche_1_d`
  - `nb_marche_2_d`
  - `nb_marche_3_d`
  - `nb_marche_4_d`
  - `nb_marche_5_d`
  - `nb_marche_6_d`
- Nombre de chaque type d'actions effectuées par l'agent :
  - `nb_no_action_e`
  - `nb_move_out_e`
  - `nb_move_out_and_kill_e`
  - `nb_move_forward_e`
  - `nb_get_stuck_behind_e`
  - `nb_enter_safezone_e`
  - `nb_move_in_safe_zone_e`
  - `nb_reach_goal_e`
  - `nb_kill_e`
  - `nb_reach_pied_escalier_e`
  - `nb_avance_recule_pied_escalier_e`
  - `nb_marche_1_e`
  - `nb_marche_2_e`
  - `nb_marche_3_e`
  - `nb_marche_4_e`
  - `nb_marche_5_e`
  - `nb_marche_6_e`