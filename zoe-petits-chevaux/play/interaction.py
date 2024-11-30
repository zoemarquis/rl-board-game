def get_human_action(valid_actions):
    """
    Demande à l'utilisateur de choisir une action parmi les options valides.

    Args:
        valid_actions (list): Liste des actions valides.

    Returns:
        str: L'action choisie par l'utilisateur.
    """
    while True:
        print(f"Actions valides : {valid_actions}")
        choix = int(input("Choisissez une action : ").strip())
        if choix in valid_actions:
            print(f"Action choisie : {choix}")
            return choix
        else:
            print("Choix invalide. Veuillez réessayer.")
