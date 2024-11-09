import time
import random
from gym_env_2dim import LabyrinthEnv
import pythoncom
import pygame

# Création de l'environnement et test rapide des fonctions
env = LabyrinthEnv()

pygame.init()

num_tours = 1000
for tour in range(num_tours):

    pythoncom.PumpWaitingMessages()

    # Gestion fermeture de la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            pygame.quit()
            exit()

    # Au hasard pour le test (phase 0 et 1)
    if env.phase == 0:
        action = env.action_space_insertion.sample()
    else:
        action = env.action_space.sample()

    observation, recompense, termine, tronque, info = env.step(action)

    if env.phase == 0:
        print(f"\n\nJoueur : {env.game.current_player}")
        print(f"Nombre trésors restants : {env.game.get_remaining_treasures(env.game.current_player)}")
        print(f"\nPhase : Insertion")
    else:
        print(f"\nPhase : Déplacement")

    print(f"Action choisie : {action}")
    print(f"Récompense : {recompense}")
    print(f"Position joueur : {env.game.get_coord_player()}")
    print(f"Terminé : {termine}")
    print(f"Tronqué : {tronque}")

    env.render()
    time.sleep(0.5)

    if termine:
        print("Game over !")
        break

env.close()
pygame.quit()