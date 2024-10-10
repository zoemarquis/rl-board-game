import time
import random
from gym_env_labyrinthe import LabyrinthEnv


# Création de l'environnement et test rapide des fonctions
env = LabyrinthEnv()

num_tours = 1000
for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")

    action = env.action_space.sample() # Au hasard pour le test

    observation, recompense, termine, info = env.step(action)

    print(f"Action : {action}")
    print(f"Recompense : {recompense}")

    env.render()
    time.sleep(1)

    if termine:
        print("Game over !")
        break

env.close() # Fait rien pour l'instant
