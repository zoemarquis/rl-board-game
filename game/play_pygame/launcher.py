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

    # Type de joueurs (humain ou agent)
    players = []
    for i in range(1, num_players + 1):
        while True:
            player_type = input(f"Le joueur {i} est-il humain ou agent ? (h pour humain / a pour agent) : ").lower()
            if player_type in ["h", "a"]:
                players.append("humain" if player_type == "h" else "agent")
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
        if victory_mode in ["rapide", "complete"]:
            break
        else:
            print("Veuillez entrer 'rapide' ou 'complete'.")

    # Règles pour l'escalier
    while True:
        stair_rule = input("Règles pour l'escalier (exactitude ou simplifiée) : ").lower()
        if stair_rule in ["exactitude", "simplifiee"]:
            break
        else:
            print("Veuillez entrer 'exactitude' ou 'simplifiee'.")

    # Ordre de progression dans l'escalier
    if stair_rule == "exactitude":
        while True:
            progression_order = input("Ordre de progression (simplifié ou strict) : ").lower()
            if progression_order in ["simplifie", "strict"]:
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
        progression_order = "simplifie"
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
        "num_pawns": num_pawns,
        "victory_mode": victory_mode,
        "stair_rule": stair_rule,
        "progression_order": progression_order,
        "replay_climb": replay_climb,
        "replay_six": replay_six,
        "protect_pawn": protect_pawn,
    }

# Exemple d'appel
config = setup_game()
