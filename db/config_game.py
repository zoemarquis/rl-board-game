# Fichier permettant de définir les configurations de jeu pour les parties entre agents
import os 
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../zoe-petits-chevaux/reinforcement_learning"))


# TODO :  Ajouter les sets de règles
# TODO :  Ajouter d'autres paramètres pouvant être utiles
def generate_game_config(num_players, nb_chevaux, mode_fin, mode_escalier, agent_path):
    return {
        "num_players": num_players,
        "nb_chevaux": nb_chevaux,
        "mode_fin_partie": mode_fin,
        "mode_pied_escalier": mode_escalier,
        "agents": [{"path": os.path.join(BASE_DIR, agent_path), "name": f"Agent {i + 1}"} for i in range(num_players)]
        
    }

game_configs = {
    "two_players_two_pawns": generate_game_config(2, 2, "tous",  "exact", "agent_maskedppo_2joueurs_2chevaux_tous_exact"),
    "two_players_three_pawns": generate_game_config(2, 3, "un",  "exact", "agent_maskedppo_2joueurs_2chevaux_un_exact")
}
