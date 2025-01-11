from reinforcement_learning.config import get_config_nb, get_trad_config

def setup_game():
    print("Bienvenue dans le jeu ! Configurons votre partie.")

    # Nombre de joueurs
    while True:
        try:
            num_players = int(input("Entrez le nombre de joueurs (entre 2 et 4) : "))
            if 2 <= num_players <= 4:
                break
            else:
                print("Veuillez entrer un nombre entre 2 et 4.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Types d'agents disponibles
    agent_types = [
        "balanced",  # Structure de récompense équilibrée
        "aggressive",  # Priorité : attaquer les autres
        "rusher",  # Priorité : avancer rapidement
        "defensive",  # Priorité : sécuriser ses pions
        "spawner",  # Priorité : sortir les pions
        "suboptimal"  # Choix intentionnellement sous-optimaux
    ]

    # Type de joueurs (humain ou agent) et type d'agent
    players = []
    players_types= []
    for i in range(1, num_players + 1):
        while True:
            player_type = input(f"Le joueur {i} est-il humain ou agent ? (h pour humain / a pour agent) : ").lower()
            if player_type in ["h", "a"]:
                if player_type == "h":
                    players.append("humain")
                    players_types.append("humain")
                else:
                    while True:
                        print(f"Types d'agents disponibles : {', '.join(agent_types)}")
                        agent_type = input(f"Choisissez un type pour l'agent {i} : ").lower()
                        if agent_type in agent_types:
                            players.append(f"agent ({agent_type})")
                            players_types.append("agent")
                            break
                        else:
                            print("Veuillez entrer un type d'agent valide.")
                break
            else:
                print("Veuillez entrer 'h' pour humain ou 'a' pour agent.")

    # Nombre de pions par joueur
    while True:
        try:
            num_pawns = int(input("Entrez le nombre de pions par joueur (entre 2 et 6) : "))
            if 2 <= num_pawns <= 6:
                break
            else:
                print("Veuillez entrer un nombre entre 2 et 6.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

    # Mode de victoire
    while True:
        victory_mode = input("Choisissez le mode de victoire (rapide ou complète) : ").lower()
        if victory_mode in ["rapide", "complète"]:
            break
        else:
            print("Veuillez entrer 'rapide' ou 'complète'.")

    # Règles pour l'escalier
    while True:
        stair_rule = input("Règles pour l'escalier (exactitude ou simplifiée) : ").lower()
        if stair_rule in ["exactitude", "simplifiée"]:
            break
        else:
            print("Veuillez entrer 'exactitude' ou 'simplifiée'.")

    # Ordre de progression dans l'escalier
    if stair_rule == "exactitude":
        while True:
            progression_order = input("Ordre de progression (simplifié ou strict) : ").lower()
            if progression_order in ["simplifié", "strict"]:
                break
            else:
                print("Veuillez entrer 'simplifié' ou 'strict'.")

        # Rejouer pour chaque marche ?
        if progression_order == "strict":
            while True:
                replay_climb = input("Rejouer pour la montée de chaque marche ? (oui ou non) : ").lower()
                if replay_climb in ["oui", "non"]:
                    break
                else:
                    print("Veuillez entrer 'oui' ou 'non'.")
    else:
        progression_order = "simplifié"
        replay_climb = "non"

    # Rejouer si 6
    while True:
        replay_six = input("Rejouer si un joueur fait un 6 ? (oui ou non) : ").lower()
        if replay_six in ["oui", "non"]:
            break
        else:
            print("Veuillez entrer 'oui' ou 'non'.")

    # Protéger un pion
    while True:
        protect_pawn = input("Protéger un pion si deux sont sur la même case ? (oui ou non) : ").lower()
        if protect_pawn in ["oui", "non"]:
            break
        else:
            print("Veuillez entrer 'oui' ou 'non'.")

    # Résumé des paramètres
    print("\nConfiguration de la partie terminée :")
    print(f"- Nombre de joueurs : {num_players}")
    print(f"- Ordre des joueurs : {', '.join(players)}")
    print(f"- Nombre de pions par joueur : {num_pawns}")
    print(f"- Mode de victoire : {victory_mode}")
    print(f"- Règles pour l'escalier : {stair_rule}")
    print(f"- Ordre de progression : {progression_order}")
    if progression_order == "strict":
        print(f"- Rejouer pour chaque marche : {replay_climb}")
    print(f"- Rejouer si 6 : {replay_six}")
    print(f"- Protection des pions : {protect_pawn}")

    # Retour des paramètres
    return {
        "num_players": num_players,
        "players": players,
        "players_types": players_types,
        "num_pawns": num_pawns,
        "victory_mode": victory_mode,
        "stair_rule": stair_rule,
        "progression_order": progression_order,
        "replay_climb": replay_climb,
        "replay_six": replay_six,
        "protect_pawn": protect_pawn,
    }

def get_config(set_up_config):
    return get_trad_config(set_up_config["victory_mode"], set_up_config["stair_rule"], set_up_config["progression_order"], set_up_config["replay_climb"], set_up_config["replay_six"], set_up_config["protect_pawn"])

def get_models(set_up_config, trad_config):
    models = []
    for player in set_up_config["players"]:
        url = "reinforcement_learning/agents/"
        filename = ""
        if player.startswith("agent"):
            agent_type = player.split(" (")[1][:-1]
            filename += agent_type + "_"

            if set_up_config["num_players"] == 2:
                url += "2_joueurs/"
                filename += "2j_"
            elif set_up_config["num_players"] == 3:
                url += "3_joueurs/"
                filename += "3j_"
            elif set_up_config["num_players"] == 4:
                url += "4_joueurs/"
                filename.append("4j_")
            else: 
                raise ValueError("Nombre de joueurs invalide.")
            
            
            nb_pawns = set_up_config["num_pawns"]
            url += f"{nb_pawns}_pions/"
            filename += f"{nb_pawns}c_"
            
            num_config = get_config_nb(
                trad_config
            )
            url += f"conf_{num_config}/"
            filename += f"conf_{num_config}_"

            filename += "200000_steps"

            models.append(url + filename)
        else: 
            models.append("humain")
           
    print(models)

    # TODO raise error si le file n'existe pas, ça veut dire config pas valide (on a pas entrainé tous les agents)

    return models
