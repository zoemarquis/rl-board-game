# Fichier regroupant toutes les configurations de jeu possibles

# Toutes les combinaisons possibles de configurations de jeu
config_param = {
    1: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui"),
    2: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    3: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui"),
    4: dict(mode_fin_partie="tous", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
    5: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    6: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
    7: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    8: dict(mode_fin_partie="tous", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
    9: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="oui"),
    10: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    11: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="oui"),
    12: dict(mode_fin_partie="un", mode_ascension="avec_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
    13: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    14: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
    15: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="oui", mode_rejoue_marche="non"),
    16: dict(mode_fin_partie="un", mode_ascension="sans_contrainte", mode_pied_escalier="not_exact", mode_rejoue_6="non", mode_rejoue_marche="non"),
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
