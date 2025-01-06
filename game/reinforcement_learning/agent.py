import numpy as np


class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, valid_actions_encoded):
        if 0 in valid_actions_encoded:
            return 0
        # sinon random
        return np.random.choice(valid_actions_encoded)


class QLearningAgent:
    def __init__(
        self, action_space, state_space, learning_rate=0.1, gamma=0.99, epsilon=0.1
    ):
        self.action_space = action_space
        self.state_space = state_space
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros(
            (state_space, action_space)
        )  # Initialisation de la Q-table

    def choose_action(self, state, valid_actions_encoded):
        """
        Choisir une action parmi les actions valides en fonction de la politique epsilon-greedy
        :param state: l'état actuel
        :param valid_actions_encoded: liste des actions valides à cet état
        :return: une action choisie parmi les actions valides
        """
        # Exploration vs exploitation
        if np.random.rand() < self.epsilon:
            # Exploration: Choisir une action aléatoire parmi les actions valides
            return np.random.choice(valid_actions_encoded)
        else:
            # Exploitation: Choisir l'action avec la meilleure valeur Q parmi les actions valides
            valid_q_values = self.q_table[state, valid_actions_encoded]
            best_action = valid_actions_encoded[np.argmax(valid_q_values)]
            return best_action

    def update(self, state, action, reward, next_state, done):
        # Mise à jour de la Q-table en fonction de la récompense et de l'état suivant
        best_next_action = np.argmax(
            self.q_table[next_state]
        )  # Action avec la meilleure valeur pour l'état suivant
        td_target = (
            reward
            + (1 - done) * self.gamma * self.q_table[next_state, best_next_action]
        )
        self.q_table[state, action] += self.learning_rate * (
            td_target - self.q_table[state, action]
        )
