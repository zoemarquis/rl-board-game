import random
import gymnasium as gym
from game_logic import GameLogic
from ludo_env import LudoEnv

def main():
    # Créer l'environnement
    env = LudoEnv()  # Nombre de joueurs
    done = False
    total_rewards = 0
    
    while not done:
        # Choisir aléatoirement un joueur et un lancer de dé
        player_id = env.current_player
        dice_value = env.game.dice_generator()
        print(f"Joueur {player_id} lance le dé : {dice_value}")
        
        # Récupérer les actions valides pour ce joueur avec la valeur du dé
        valid_actions = env.game.get_valid_actions(player_id, dice_value)
        if valid_actions:
            action = random.choice(valid_actions)  # Choisir une action valide au hasard
            print(f"Joueur {player_id} choisit l'action : {action}")
        else:
            print(f"Aucune action valide pour le joueur {player_id}. Passer son tour.")
            action = None  # Aucun mouvement si aucune action valide

        # Effectuer l'action et obtenir l'observation, récompense, et si le jeu est terminé
        observation, reward, done, info = env.step(action) if action is not None else env.step(None)
        total_rewards += reward
        
        # Afficher l'état du jeu après chaque tour
        env.render(mode='human')
        print(f"Récompense reçue : {reward}")
        print(f"Total des récompenses : {total_rewards}")
    
    print("Jeu terminé!")

# Appel de la fonction main
if __name__ == "__main__":
    main()
