import argparse
from game import Game


def main():
    """Main function to start the game"""

    # Arguments parser
    parser = argparse.ArgumentParser(description="Jeu avec options pour joueurs et IA")
    parser.add_argument(
        "-j", "--joueurs", type=int, default=2, help="Nombre total de joueurs"
    )
    parser.add_argument(
        "-ia",
        "--intelligence-artificielle",
        type=int,
        default=0,
        help="Nombre de joueurs IA",
    )
    parser.add_argument(
        '-hu', '--humains', type=int, default=0, help='Nombre de joueurs humains'
    )
    parser.add_argument(
        '-t', '--theme', type=str, default='original', 
        help='Theme du jeu, choix entre original et kity(ocean)'
    )

    args = parser.parse_args()

    # Access the number of players and AI from the arguments
    nb_joueurs = args.joueurs
    nb_humains = args.humains
    nb_ia = args.intelligence_artificielle

    if (nb_humains == 0 and nb_ia == 0):
            nb_ia = nb_joueurs

    # Define theme-to-directory mapping
    theme_directories = {
        "original": "./original_images",
        "kity": "./kity_images"
    }

    # Get the directory based on the theme provided
    theme = args.theme.lower()  # Convert to lowercase to make it case-insensitive
    directory = theme_directories.get(theme)

    # Validate the directory
    if not directory:
        print(f"Error: Theme '{theme}' is not recognized. Available themes are: {', '.join(theme_directories.keys())}.")
        exit(1)

    jeu = Game(human_players=nb_humains, ia_number=nb_ia, directory=directory)
    jeu.launch()


if __name__ == "__main__":
    main()
