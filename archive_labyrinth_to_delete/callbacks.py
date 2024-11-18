from stable_baselines3.common.callbacks import BaseCallback

# Classe permettant de sauvegarder le modèle à chaque n steps
class SaveModelCallback(BaseCallback):
    def __init__(self, save_freq: int, save_path: str, verbose=0):
        super(SaveModelCallback, self).__init__(verbose)
        self.save_freq = save_freq
        self.save_path = save_path

    def _on_step(self) -> bool:
        if self.n_calls % self.save_freq == 0:
            model_path = f"{self.save_path}/modele_{self.n_calls}_steps"
            self.model.save(model_path)
            if self.verbose > 0:
                print(f"Sauvegarde du modele au step {self.n_calls} dans {model_path}")
        return True


# Classe permettant de d'enregistrer le nombre de rewards positifs et négatifs
class ExplorationExploitationCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(ExplorationExploitationCallback, self).__init__(verbose)
        self.positive_rewards = 0
        self.negative_rewards = 0

    def _on_step(self) -> bool:
        reward = self.locals["rewards"][0]
        if reward > 0:
            self.positive_rewards += 1
        elif reward < 0:
            self.negative_rewards += 1

        if self.n_calls % 1000 == 0:
            self.logger.record(
                "exploration_exploitation/positive_rewards", self.positive_rewards
            )
            self.logger.record(
                "exploration_exploitation/negative_rewards", self.negative_rewards
            )
        return True
