class RandomAgent:
    def __init__(self, action_space):
        self.action_space = action_space

    def choose_action(self, valid_actions_encoded):
        if 0 in valid_actions_encoded:
            return 0
        # sinon random
        return np.random.choice(valid_actions_encoded)
