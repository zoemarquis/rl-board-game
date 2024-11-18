import argparse
from game import Game


def main():
    """Main function to start the game"""

    # Arguments parser
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Jeu avec options pour joueurs et IA"
    )
    parser.add_argument(
        "-j",
        "--joueurs",
        type=int,
        default=2,
        help="Nombre total de joueurs, si aucun autre argument n'est donné, le jeu sera joué par des IA",
    )
    parser.add_argument(
        "-ia",
        "--intelligence-artificielle",
        type=int,
        default=0,
        help="Nombre de joueurs IA",
    )
    parser.add_argument(
        "-hu", "--humains", type=int, default=0, help="Nombre de joueurs humains"
    )
    parser.add_argument(
        "-t",
        "--theme",
        type=str,
        default="original",
        help="Thème du jeu, choix entre original et kity (ocean)",
    )

    args: argparse.Namespace = parser.parse_args()

    # Access the number of players and AI from the arguments
    nb_players = args.joueurs
    nb_humans = args.humains
    nb_ia = args.intelligence_artificielle

    # Test parameters
    if nb_players < 2:
        print("Erreur: Le nombre de joueurs doit être supérieur ou égal à 2.")
        exit(1)

    if nb_humans < 0 or nb_ia < 0:
        print(
            "Erreur: Le nombre de joueurs humains et IA doit être supérieur ou égal à 0."
        )
        exit(1)

    if nb_humans + nb_ia > nb_players:
        print(
            "Erreur: Le nombre de joueurs humains et IA doit être inférieur ou égal au nombre total de joueurs."
        )
        exit(1)

    if nb_humans == 0 and nb_ia == 0:
        nb_ia = nb_players

    elif nb_humans == 0:
        nb_humans = nb_players - nb_ia

    elif nb_ia == 0:
        nb_ia = nb_players - nb_humans

    else:
        if nb_humans + nb_ia != nb_players:
            print(
                "Erreur: Le nombre de joueurs humains et IA doit être égal au nombre total de joueurs."
            )
            exit

    # Define theme-to-directory mapping
    theme_directories = {"original": "./original_images", "kity": "./kity_images"}

    # Get the directory based on the theme provided
    theme = args.theme.lower()  # Convert to lowercase to make it case-insensitive
    directory = theme_directories.get(theme)

    # Validate the directory
    if not directory:
        print(
            f"Error: Theme '{theme}' is not recognized. Available themes are: {', '.join(theme_directories.keys())}."
        )
        exit(1)

    use_rl_agent = False
    if nb_ia > 0:
        use_rl_agent = True

    jeu = Game(
        human_players=nb_humans,
        ia_number=nb_ia,
        directory=directory,
        use_rl_agent=use_rl_agent,
    )
    jeu.launch()


if __name__ == "__main__":
    main()
