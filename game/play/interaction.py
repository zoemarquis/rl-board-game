def get_human_action(valid_actions):
    """
    Demande à l'utilisateur de choisir une action parmi les options valides.

    Args:
        valid_actions (list): Liste des actions valides.

    Returns:
        int: L'action choisie par l'utilisateur.
    """
    while True:
        try:
            print(f"Actions valides : {valid_actions}")
            choix = input("Choisissez une action : ").strip()

            # Vérifier si l'utilisateur n'a rien entré
            if choix == "":
                raise ValueError("Entrée vide.")

            # Convertir en entier
            choix = int(choix)

            # Vérifier si l'action est valide
            if choix in valid_actions:
                print(f"Action choisie : {choix}")
                return choix
            else:
                print("Choix invalide. Veuillez sélectionner une action valide.")
        except ValueError:
            print(
                "Entrée incorrecte. Veuillez entrer un entier correspondant à une action valide."
            )
