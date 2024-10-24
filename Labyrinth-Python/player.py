from random import randint


class Player(object):
    def __init__(self, id: int, start_position):
        self.id_player = id
        self.treasures = []
        self.nb_treasures = len(self.treasures)
        self.start_position = start_position
        self.current_position = start_position

    def get_nb_treasures_remaining(self):
        return len(self.treasures)

    def add_treasure(self, treasure: int):
        self.treasures.append(treasure)
        self.nb_treasures = len(self.treasures)

    def remove_treasure(self, treasure: int):
        self.treasures.remove(treasure)
        self.nb_treasures = len(self.treasures)

    def remove_current_treasure(self):
        self.treasures.pop(0)
        self.nb_treasures = len(self.treasures)
        return self.nb_treasures

    def get_next_treasure(self):
        if len(self.treasures) > 0:
            return self.treasures[0]
        else:
            return None

    # Ajouté pour tester l'entrainement dans le notebook - à modifier
    def has_won(self):
        return (
            self.get_nb_treasures_remaining() == 0
            and self.current_position == self.start_position
        )

    # Ajouté pour tester l'entrainement dans le notebook - à modifier
    def move_to(self, new_position):
        self.current_position = new_position


class Players(object):
    """Class Players
    This class is used to create between two and four players
    and distribute treasures_per_player treasures to each player
    """

    def __init__(self, nb_players, nb_total_treasures, treasures_per_player):
        assert (
            nb_players >= 2 and nb_players <= 4
        ), "The number of players must be between 2 and 4"
        assert (
            nb_total_treasures >= nb_players * treasures_per_player
        ), "Not enough treasures for all players"

        start_positions = {
            0: (0, 0),  # haut gauche
            1: (0, 6),  # haut droit
            2: (6, 0),  # bas gauche
            3: (6, 6),  # bas droit
        }

        self.players = {
            i: Player(id=i, start_position=start_positions[i])
            for i in range(nb_players)
        }
        self.nb_players = nb_players
        self.nb_total_treasures = nb_total_treasures
        self.treasures_per_player = treasures_per_player
        self.distribute_treasures()

    def distribute_treasures(self):
        # randomly distribute the available treasures to the players
        available_treasures = [i for i in range(self.nb_total_treasures)]
        # select randomly treasures_per_player treasures
        # and distribute them to the players
        for i in range(self.nb_players):
            for _ in range(self.treasures_per_player):
                treasure = available_treasures[randint(0, len(available_treasures) - 1)]
                self.players[i].add_treasure(treasure)
                available_treasures.remove(treasure)

    def get_next_treasure(self, id_player: int):
        assert id_player >= 0 and id_player < self.nb_players, "Invalid player id"
        return self.players[id_player].get_next_treasure()

    def remove_current_treasure(self, id_player: int):
        assert id_player >= 0 and id_player < self.nb_players, "Invalid player id"
        return self.players[id_player].remove_current_treasure()

    def get_nb_treasures_remaining(self, id_player: int):
        assert id_player >= 0 and id_player < self.nb_players, "Invalid player id"
        return self.players[id_player].get_nb_treasures_remaining()

    # Ajouté pour tester l'entrainement dans le notebook - à modifier
    def tresorTrouve(self, id_player):
        assert id_player >= 0 and id_player < self.nb_players, "Invalid player id"
        self.players[id_player].remove_current_treasure()

    # Ajouté pour tester l'entrainement dans le notebook - à modifier
    def check_for_winner(self):
        """Vérifie si un des joueurs a gagné la partie."""
        for player_id, player in self.players.items():
            if player.has_won():
                return player_id
        return None
