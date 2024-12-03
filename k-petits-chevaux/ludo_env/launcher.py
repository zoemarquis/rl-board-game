from typing import Dict, List, Tuple
import sys
from dataclasses import dataclass
from enum import Enum

class PlayerType(Enum):
    HUMAN = "human"
    RANDOM_AI = "random"
    PPO_AI = "ppo"
    QLEARNING_AI = "qlearning"

class GameRule(Enum):
    MUST_ROLL_6 = "must_roll_6_to_exit"
    EXACT_GOAL = "exact_count_for_goal"
    KILL_PAWNS = "can_kill_pawns"
    BOUNCE_ON_OCCUPIED = "bounce_on_occupied"
    SAFE_ZONES = "safe_zones_enabled"
    MAX_THREE_SIXES = "max_three_consecutive_sixes"
    STRICT_GOAL_SEQUENCE = "strict_goal_sequence"

@dataclass
class PlayerConfig:
    player_id: int
    player_type: PlayerType

@dataclass
class GameConfig:
    num_players: int
    players: List[PlayerConfig]
    interface_enabled: bool
    active_rules: List[GameRule]

def clear_screen():
    print("\033[H\033[J", end="")

def get_valid_input(prompt: str, valid_values: List[str]) -> str:
    while True:
        value = input(prompt).strip().lower()
        if value in valid_values:
            return value
        print(f"Invalid input. Please choose from: {', '.join(valid_values)}")

def get_number_of_players() -> int:
    while True:
        try:
            num = int(input("Enter number of players (2-4): "))
            if 2 <= num <= 4:
                return num
            print("Please enter a number between 2 and 4")
        except ValueError:
            print("Please enter a valid number")

def get_player_type(player_num: int) -> PlayerType:
    print(f"\nPlayer {player_num} Configuration")
    print("Available player types:")
    print("1. Human")
    print("2. Random AI")
    print("3. PPO AI")
    print("4. Q-Learning AI")
    
    choice = get_valid_input("Choose player type (1-4): ", ["1", "2", "3", "4"])
    return {
        "1": PlayerType.HUMAN,
        "2": PlayerType.RANDOM_AI,
        "3": PlayerType.PPO_AI,
        "4": PlayerType.QLEARNING_AI
    }[choice]

def get_interface_preference() -> bool:
    choice = get_valid_input(
        "\nEnable graphical interface? (y/n): ",
        ["y", "n"]
    )
    return choice == "y"

def get_game_rules() -> List[GameRule]:
    print("\nGame Rules Configuration")
    print("Available rules:")
    for i, rule in enumerate(GameRule, 1):
        print(f"{i}. {rule.value}")
    
    selected_rules = []
    while True:
        choice = input("\nEnter rule numbers to toggle (comma-separated) or 'done' to finish: ").strip().lower()
        if choice == 'done':
            break
            
        try:
            selections = [int(x.strip()) for x in choice.split(",")]
            for sel in selections:
                if 1 <= sel <= len(GameRule):
                    rule = list(GameRule)[sel-1]
                    if rule in selected_rules:
                        selected_rules.remove(rule)
                        print(f"Disabled: {rule.value}")
                    else:
                        selected_rules.append(rule)
                        print(f"Enabled: {rule.value}")
                else:
                    print(f"Invalid rule number: {sel}")
        except ValueError:
            print("Please enter valid numbers separated by commas")
            
    return selected_rules

def configure_game() -> GameConfig:
    clear_screen()
    print("=== Ludo Game Configuration ===\n")
    
    # Get number of players
    num_players = get_number_of_players()
    
    # Configure each player
    players = []
    for i in range(num_players):
        player_type = get_player_type(i + 1)
        players.append(PlayerConfig(i, player_type))
    
    # Get interface preference
    interface_enabled = get_interface_preference()
    
    # Get game rules
    active_rules = get_game_rules()
    
    # Create and return configuration
    config = GameConfig(
        num_players=num_players,
        players=players,
        interface_enabled=interface_enabled,
        active_rules=active_rules
    )
    
    # Display final configuration
    print("\nFinal Configuration:")
    print(f"Number of players: {config.num_players}")
    print("Players:")
    for player in config.players:
        print(f"  Player {player.player_id + 1}: {player.player_type.value}")
    print(f"Interface enabled: {config.interface_enabled}")
    print("Active rules:")
    for rule in config.active_rules:
        print(f"  - {rule.value}")
    
    return config

if __name__ == "__main__":
    config = configure_game()
    input("\nPress Enter to exit...")