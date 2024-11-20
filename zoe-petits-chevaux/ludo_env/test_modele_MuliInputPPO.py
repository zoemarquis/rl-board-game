# test jouer contre 
from stable_baselines3 import PPO

# Charger le modèle pré-entraîné
model = PPO.load("masked_ppo_ludo_model")

# Imaginons que l'environnement `LudoEnv` permet à un humain de choisir une action via l'input
from ludo_env import LudoEnv

env = LudoEnv()  # Créez l'environnement

obs = env.reset()  # Réinitialiser l'environnement
obs = obs[0]
done = False

while not done:
    print("current_player : ", env.current_player)
    if env.current_player == 0:
        # Afficher l'état actuel du jeu
        print()
        print("TOUR DE L'HUMAIN")
        print("board humain : ", obs["my_board"])  # Afficher l'observation
        print("dé : ", obs["dice_roll"])  # Afficher le dé
        print("current_player : ", env.current_player)  # Afficher le joueur actuel
        
        # Choix de l'action de l'humain (entrée au clavier ou autre)
        action_humain = int(input("Choisissez une action : "))
        
        # Appliquez l'action de l'humain
        obs, reward, done, truncated, info = env.step(action_humain)

    elif env.current_player == 1:
        print()
        print("TOUR DE L'AGENT")
        print("board agent : ", obs["my_board"])
        print("dé : ", obs["dice_roll"])  # Afficher le dé
        print("current_player : ", env.current_player)  # Afficher le joueur actuel
        # L'agent choisit une action via son modèle
        action_agent = model.predict(obs, deterministic=True)[0]
        pawn_id, action_type = env.game.decode_action(action_agent)
        print("Action de l'agent : ", action_agent , " action_agent ", action_type)
        obs, reward, done, truncated, info = env.step(action_agent)
    else:
        raise ValueError("Il n'y a que 2 joueurs dans le jeu")