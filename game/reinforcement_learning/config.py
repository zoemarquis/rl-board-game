# Fichier regroupant toutes les configurations de jeu possibles

# Toutes les combinaisons possibles de configurations de jeu
config_param = {
    1: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="désactivé"),
    2: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    3: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="désactivé"),
    4: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    5: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    6: dict(mode_fin_partie="tous", mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    7: dict(mode_fin_partie="tous", mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    8: dict(mode_fin_partie="tous", mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    9: dict(mode_fin_partie="un",   mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="désactivé"),
    10: dict(mode_fin_partie="un",  mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    11: dict(mode_fin_partie="un",  mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="désactivé"),
    12: dict(mode_fin_partie="un",  mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    13: dict(mode_fin_partie="un",  mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    14: dict(mode_fin_partie="un",  mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    15: dict(mode_fin_partie="un",  mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    16: dict(mode_fin_partie="un",  mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    17: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="activé"),
    18: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    19: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="activé"),
    20: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    21: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    22: dict(mode_fin_partie="tous",mode_pied_escalier="exact",     mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    23: dict(mode_fin_partie="tous",mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    24: dict(mode_fin_partie="tous",mode_pied_escalier="not_exact", mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    25: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="activé"),
    26: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="avec_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    27: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="activé"),
    28: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="avec_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    29: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    30: dict(mode_fin_partie="un", mode_pied_escalier="exact",      mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    31: dict(mode_fin_partie="un", mode_pied_escalier="not_exact",  mode_ascension="sans_contrainte",  mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    32: dict(mode_fin_partie="un", mode_pied_escalier="not_exact",  mode_ascension="sans_contrainte",  mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
}

# TODO ici retirer les configs pas possibles 
# ce qui est incompatible : escalier not exact et ascension avec contrainte
# seul combinaison compatible avec rejoue marche oui : exact et avec contrainte


def print_all_configs():
    print("Configurations disponibles :\n")
    for config_id, config in config_param.items():
        print(f"Configuration {config_id}:")
        for key, value in config.items():
            print(f"  - {key}: {value}")
        print()

def get_config_nb(victory_mode, stair_rule, progression_order, replay_climb, replay_six, protect_pawn):
    if victory_mode == "rapide":
        mode_fin_partie = "un"
    elif victory_mode == "complète":
        mode_fin_partie = "tous"
    else:
        raise ValueError("Mode de victoire invalide")
    
    if stair_rule == "exactitude": # atteindre pied escalier 
        mode_pied_escalier = "exact" # TODO pas l'inverse ?
    elif stair_rule == "simplifiée":
        mode_pied_escalier = "not_exact"
    else:
        raise ValueError("Règles pour l'escalier invalide")
    
    if progression_order == "strict":
        mode_ascension = "avec_contrainte"
    elif progression_order == "simplifié":
        mode_ascension = "sans_contrainte"
    else:
        raise ValueError("Ordre de progression invalide")
    
    if replay_climb == "oui":
        mode_rejoue_marche = "oui"
    elif replay_climb == "non":
        mode_rejoue_marche = "non"
    else:
        raise ValueError("Rejouer pour chaque marche invalide")
    
    if replay_six == "oui":
        mode_rejoue_6 = "oui"
    elif replay_six == "non":
        mode_rejoue_6 = "non"
    else:
        raise ValueError("Rejouer si 6 invalide")
    
    if protect_pawn == "oui":
        mode_protect = "activé"
    elif protect_pawn == "non":
        mode_protect = "désactivé"
    else:
        raise ValueError("Protéger un pion invalide")
    
    # return config_param number correspondant à dict
    # si None raise erros
    for config_id, config in config_param.items():
        if config == dict(mode_fin_partie=mode_fin_partie, mode_ascension=mode_ascension, mode_pied_escalier=mode_pied_escalier, mode_rejoue_6=mode_rejoue_6, mode_rejoue_marche=mode_rejoue_marche, mode_protect=mode_protect):
            return config_id
    raise ValueError("Configuration invalide")
        
# TODO SUPPRIME ?
# num_players_options = [2]
# nb_chevaux_options = [2]
# mode_fin_partie_options = ["tous", "un"]
# mode_ascension_options = ["avec_contrainte", "sans_contrainte"]
# mode_pied_escalier_options = ["exact", "not_exact"]
# mode_rejoue_6_options = ["oui", "non"]
# mode_rejoue_marche_options = ["oui", "non"]
# mode_gym_options = ["entrainement"]
#
# configurations = []
# config_id = 1
# for (num_players, nb_chevaux, mode_fin_partie, mode_ascension, mode_pied_escalier, mode_rejoue_6, mode_rejoue_marche, mode_gym) in product(num_players_options, nb_chevaux_options, mode_fin_partie_options, mode_ascension_options, mode_pied_escalier_options, mode_rejoue_6_options, mode_rejoue_marche_options, mode_gym_options,):
#     if mode_ascension == "avec_contrainte" and mode_pied_escalier != "exact":
#         continue
#     if mode_rejoue_marche == "oui" and mode_ascension != "avec_contrainte":
#         continue
#     if mode_ascension == "sans_contrainte" and mode_pied_escalier not in ["exact", "not_exact"]:
#         continue
#
#     configurations.append(f"""env_{config_id} = LudoEnv(num_players={num_players}, nb_chevaux={nb_chevaux}, mode_fin_partie="{mode_fin_partie}", mode_ascension="{mode_ascension}", mode_pied_escalier="{mode_pied_escalier}", mode_rejoue_6="{mode_rejoue_6}", mode_rejoue_marche="{mode_rejoue_marche}", mode_gym="{mode_gym}", with_render=False)""")
#     config_id += 1
#
# for config in configurations:
#     print(config)
