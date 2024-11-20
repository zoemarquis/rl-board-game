# test jouer contre 
from stable_baselines3 import PPO

# Charger le modèle pré-entraîné
model = PPO.load("masked_ppo_ludo_model")

# Imaginons que l'environnement `LudoEnv` permet à un humain de choisir une action via l'input
from ludo_env import LudoEnv

env = LudoEnv()  # Créez l'environnement

obs = env.reset()  # Réinitialiser l'environnement
done = False

while not done:
    # Afficher l'état actuel du jeu
    print("Observation actuelle : ", obs)
    
    # Choix de l'action de l'humain (entrée au clavier ou autre)
    action_humain = int(input("Choisissez une action (par exemple, 0 pour avancer, 1 pour changer de pion, etc.) : "))
    
    # Appliquez l'action de l'humain
    obs, reward, done, truncated, info = env.step(action_humain)
    
    # Si le jeu n'est pas terminé, faire jouer l'agent
    if not done:
        print("tour de l'agent")
        print("dé : ", obs["dice_roll"])  # Afficher le dé
        print("current_player : ", env.current_player)  # Afficher le joueur actuel
        print("my board : ", obs["my_board"])
        print("adversaire board : ", obs["adversaire_board"])  # Afficher le plateau de l'adversaire
        # L'agent choisit une action via son modèle
        action_agent = model.predict(obs, deterministic=True)[0]
        pawn_id, action_type = env.game.decode_action(action_agent)
        print("Action de l'agent : ", action_agent , " action_agent ", action_type)
        obs, reward, done, truncated, info = env.step(action_agent)
