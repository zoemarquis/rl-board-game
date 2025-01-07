# Fichier regroupant toutes les configurations de jeu possibles

# Toutes les combinaisons possibles de configurations de jeu
config_param = {
    1: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="désactivé"),
    2: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    3: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="désactivé"),
    4: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    5: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    6: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    7: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    8: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    9: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="désactivé"),
    10: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    11: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="désactivé"),
    12: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    13: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    14: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    15: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="désactivé"),
    16: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="désactivé"),
    17: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="activé"),
    18: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    19: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="activé"),
    20: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    21: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    22: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    23: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    24: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    25: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui", mode_protect="activé"),
    26: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    27: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui", mode_protect="activé"),
    28: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    29: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    30: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
    31: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non", mode_protect="activé"),
    32: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non", mode_protect="activé"),
}


def print_all_configs():
    print("Configurations disponibles :\n")
    for config_id, config in config_param.items():
        print(f"Configuration {config_id}:")
        for key, value in config.items():
            print(f"  - {key}: {value}")
        print()


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
