import argparse
from game import Game


def main():
    """Main function to start the game"""

    # Arguments parser
    parser = argparse.ArgumentParser(description="Jeu avec options pour joueurs et IA")
    parser.add_argument(
        "-j", "--joueurs", type=int, default=4, help="Nombre de joueurs humains"
    )  # TODO default 2 IA
    parser.add_argument(
        "-ia",
        "--intelligence-artificielle",
        type=int,
        default=0,
        help="Nombre de joueurs IA",
    )
    # TODO : theme, nb joeurs != nb humains & nb_ia
    args = parser.parse_args()

    # Access the number of players and AI from the arguments
    nb_joueurs = args.joueurs
    nb_ia = args.intelligence_artificielle

    jeu = Game(human_players=nb_joueurs, ia_number=nb_ia)
    jeu.launch()


if __name__ == "__main__":
    main()
