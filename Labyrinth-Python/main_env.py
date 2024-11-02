import time
import random
from gym_env_2dim import LabyrinthEnv


# Création de l'environnement et test rapide des fonctions
env = LabyrinthEnv()

num_tours = 1000
for tour in range(num_tours):
    print(f"Tour {tour + 1}/{num_tours}")

    # Au hasard pour le test (phase 0 et 1)
    if env.phase == 0:
        action = env.action_space_insertion.sample()
    else:
        action = env.action_space.sample()

    observation, recompense, termine, tronque, info = env.step(action)

    print(f"\n\nPhase : {'Insertion' if env.phase == 0 else 'Déplacement'}")
    print(f"Action choisie : {action}")
    print(f"Récompense : {recompense}")
    print(f"Position joueur : {env.game.get_coord_current_player()}")
    print(f"Terminé : {termine}")
    print(f"Tronqué : {tronque}")


    env.render()
    # time.sleep(1)

    if termine:
        print("Game over !")
        break

env.close()
