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
    9: "Montée de l'escalier commence exacte",
    10: "Montée de l'escalier commence non exacte",
}

def generate_rule_description(rule_ids, all_rules):
    descriptions = [all_rules[rule_id] for rule_id in rule_ids if rule_id in all_rules]
    return ", ".join(descriptions)


def determine_rules(num_players, nb_chevaux, mode_fin, mode_escalier):
    rules = []

    if num_players == 2:
        rules.append(1)
    elif num_players == 3:
        rules.append(2)
    elif num_players == 4:
        rules.append(3)
    
    if nb_chevaux == 2:
        rules.append(4)
    elif nb_chevaux == 3:
        rules.append(5)
    elif nb_chevaux == 4:
        rules.append(6)
    
    if mode_fin == "tous":
        rules.append(7)
    elif mode_fin == "un":
        rules.append(8)
    
    if mode_escalier == "exact":
        rules.append(9)
    else:
        rules.append(10)
    
    return rules
