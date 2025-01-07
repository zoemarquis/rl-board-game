# Ce fichier permet de gérer les règles

ALL_RULES = {
    1: "Deux joueurs",
    2: "Trois joueurs",
    3: "Quatre joueurs",
    4: "Deux chevaux",
    5: "Trois chevaux",
    6: "Quatre chevaux",
    7: "Tous les chevaux doivent gagner",
    8: "Un seul cheval doit gagner",
    9: "Montée de l'escalier avec contrainte",
    10: "Montée de l'escalier sans contrainte",
    11: "Montée de l'escalier commence exacte",
    12: "Montée de l'escalier commence non exacte",
    13: "Relance avec un 6 autorisée",
    14: "Relance avec un 6 interdite",
    15: "Relance après une marche autorisée",
    16: "Relance après une marche interdite",
    17: "Protection des chevaux activée",
    18: "Protection des chevaux désactivée"
}

def generate_rule_description(rule_ids, all_rules):
    descriptions = [all_rules[rule_id] for rule_id in rule_ids if rule_id in all_rules]
    return ", ".join(descriptions)

def determine_rules(num_players, nb_chevaux, mode_fin_partie, mode_ascension, mode_pied_escalier, mode_rejoue_6, mode_rejoue_marche, mode_protect):
    rules = []

    # Règles pour le nombre de joueurs
    if num_players == 2:
        rules.append(1)
    elif num_players == 3:
        rules.append(2)
    elif num_players == 4:
        rules.append(3)
    
    # Règles pour le nombre de chevaux
    if nb_chevaux == 2:
        rules.append(4)
    elif nb_chevaux == 3:
        rules.append(5)
    elif nb_chevaux == 4:
        rules.append(6)
    
    # Règles pour la condition de fin de partie
    if mode_fin_partie == "tous":
        rules.append(7)
    elif mode_fin_partie == "un":
        rules.append(8)
    
    # Règles pour la montée de l'escalier
    if mode_ascension == "avec_contrainte":
        rules.append(9)
    elif mode_ascension == "sans_contrainte":
        rules.append(10)

    # Règles pour l'arrivée dans l'escalier
    if mode_pied_escalier == "exact":
        rules.append(11)
    elif mode_pied_escalier == "not_exact":
        rules.append(12)

    # Règles pour rejouer avec un 6
    if mode_rejoue_6 == "oui":
        rules.append(13)
    elif mode_rejoue_6 == "non":
        rules.append(14)

    # Règles pour rejouer après une marche
    if mode_rejoue_marche == "oui":
        rules.append(15)
    elif mode_rejoue_marche == "non":
        rules.append(16)
    
    # Règles pour la protection des chevaux
    if mode_protect == "activé":
        rules.append(17)
    elif mode_protect == "désactivé":
        rules.append(18)

    return rules