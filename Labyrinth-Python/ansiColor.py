fin = "\x1b[0m"
NOIR = 0
ROUGE = 1
VERT = 2
JAUNE = 3
BLEU = 4
VIOLET = 5
CYAN = 6
GRIS = 7
NORMAL = 9
AUCUN = 0
GRAS = 1
ITALIQUE = 3
SOULIGNE = 4


def clearscreen():
    print("\x1b[2J", end="")


def pcouleur(texte, couleurCar=9, couleurFond=9, style=0):
    print(
        "\x1b["
        + str(style)
        + ";"
        + str(30 + couleurCar)
        + ";"
        + str(40 + couleurFond)
        + "m"
        + texte
        + fin,
        sep="",
        end="",
    )
