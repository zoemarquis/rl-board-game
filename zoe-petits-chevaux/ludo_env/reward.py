from ludo_env.action import Action_NO_EXACT, Action_EXACT, Action_EXACT_ASCENSION


# ------------------- REWARD TABLES -------------------


REWARD_TABLE_MOVE_OUT_NO_EXACT = {
    Action_NO_EXACT.NO_ACTION: 0,
    Action_NO_EXACT.MOVE_OUT: 20,
    Action_NO_EXACT.MOVE_OUT_AND_KILL: 10,
    Action_NO_EXACT.MOVE_FORWARD: 5,
    Action_NO_EXACT.GET_STUCK_BEHIND: 0,
    Action_NO_EXACT.ENTER_SAFEZONE: 15,
    Action_NO_EXACT.MOVE_IN_SAFE_ZONE: 1,
    Action_NO_EXACT.REACH_GOAL: 10,
    Action_NO_EXACT.KILL: 30,
} 

REWARD_TABLE_MOVE_OUT_EXACT = {
    Action_EXACT.NO_ACTION: 0,
    Action_EXACT.MOVE_OUT: 20,
    Action_EXACT.MOVE_OUT_AND_KILL: 10,

    Action_EXACT.MOVE_FORWARD: 5,
    Action_EXACT.GET_STUCK_BEHIND: 0,
    Action_EXACT.KILL: 30,

    Action_EXACT.REACH_PIED_ESCALIER: 15,
    Action_EXACT.AVANCE_RECULE_PIED_ESCALIER: 1,
    Action_EXACT.MOVE_IN_SAFE_ZONE: 5,

    Action_EXACT.REACH_GOAL: 10,
}

REWARD_TABLE_MOVE_OUT_EXACT_ASCENSION = {
    Action_EXACT_ASCENSION.NO_ACTION: 0,
    Action_EXACT_ASCENSION.MOVE_OUT: 20,
    Action_EXACT_ASCENSION.MOVE_OUT_AND_KILL: 10,

    Action_EXACT_ASCENSION.MOVE_FORWARD: 5,
    Action_EXACT_ASCENSION.GET_STUCK_BEHIND: 0,
    Action_EXACT_ASCENSION.KILL: 30,

    Action_EXACT_ASCENSION.REACH_PIED_ESCALIER: 15,
    Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER: 1,

    Action_EXACT_ASCENSION.MARCHE_1: 5,
    Action_EXACT_ASCENSION.MARCHE_2: 5,
    Action_EXACT_ASCENSION.MARCHE_3: 5,
    Action_EXACT_ASCENSION.MARCHE_4: 5,
    Action_EXACT_ASCENSION.MARCHE_5: 5,
    Action_EXACT_ASCENSION.MARCHE_6: 5,

    Action_EXACT_ASCENSION.REACH_GOAL: 10,

}


class AgentType:
    BALANCED = "balanced"  # Current reward structure
    AGGRESSIVE = "aggressive"  # Prioritizes killing
    RUSHER = "rusher"  # Prioritizes advancing quickly
    DEFENSIVE = "defensive"  # Prioritizes getting pawns to safety
    SPAWNER = "spawner"  # Prioritizes getting pawns out
    SUBOPTIMAL = "suboptimal"  # Makes intentionally suboptimal choices

def create_reward_table(agent_type, action_enum):
    """Creates a reward table based on agent type and action enumeration."""
    if isinstance(action_enum, type(Action_NO_EXACT)):
        base_table = {action: 0 for action in Action_NO_EXACT}
    elif isinstance(action_enum, type(Action_EXACT)):
        base_table = {action: 0 for action in Action_EXACT}
    elif isinstance(action_enum, type(Action_EXACT_ASCENSION)):
        base_table = {action: 0 for action in Action_EXACT_ASCENSION}
    else:
        raise ValueError("Invalid action enumeration type")

    if agent_type == AgentType.AGGRESSIVE:
        # Prioritizes killing and aggressive moves
        base_table.update({
            'KILL': 50,
            'MOVE_OUT_AND_KILL': 40,
            'MOVE_FORWARD': 5,
            'MOVE_OUT': 10,
            'REACH_GOAL': 20,
        })
    
    elif agent_type == AgentType.RUSHER:
        # Prioritizes advancing quickly towards the goal
        base_table.update({
            'MOVE_FORWARD': 30,
            'REACH_GOAL': 50,
            'MOVE_OUT': 20,
            'KILL': 10,
            'MOVE_OUT_AND_KILL': 15,
        })
    
    elif agent_type == AgentType.DEFENSIVE:
        # Prioritizes safe moves and reaching safe zones
        base_table.update({
            'ENTER_SAFEZONE': 40,
            'MOVE_IN_SAFE_ZONE': 30,
            'REACH_GOAL': 50,
            'MOVE_OUT': 20,
            'MOVE_FORWARD': 10,
            'KILL': 5,
        })
    
    elif agent_type == AgentType.SPAWNER:
        # Prioritizes getting pawns out of home
        base_table.update({
            'MOVE_OUT': 50,
            'MOVE_OUT_AND_KILL': 40,
            'MOVE_FORWARD': 10,
            'KILL': 15,
            'REACH_GOAL': 20,
        })
    
    elif agent_type == AgentType.SUBOPTIMAL:
        # Makes intentionally suboptimal choices
        base_table.update({
            'MOVE_FORWARD': 5,
            'MOVE_OUT': 3,
            'KILL': 2,
            'REACH_GOAL': 10,
            'GET_STUCK_BEHIND': 15,  # Prioritizes getting stuck
        })

    return base_table

def get_reward_table(mode_pied_escalier, mode_ascension = "sans_contrainte", agent_type=AgentType.BALANCED):
    if agent_type == AgentType.BALANCED:
        # Use existing reward tables for balanced agents
        if mode_ascension == "avec_contrainte":
            return REWARD_TABLE_MOVE_OUT_EXACT_ASCENSION
        elif mode_pied_escalier == "not_exact":
            return REWARD_TABLE_MOVE_OUT_NO_EXACT
        elif mode_pied_escalier == "exact":
            return REWARD_TABLE_MOVE_OUT_EXACT
    else:
        # Create custom reward table based on agent type
        if mode_ascension == "avec_contrainte":
            return create_reward_table(agent_type, Action_EXACT_ASCENSION)
        elif mode_pied_escalier == "not_exact":
            return create_reward_table(agent_type, Action_NO_EXACT)
        elif mode_pied_escalier == "exact":
            return create_reward_table(agent_type, Action_EXACT)
    raise ValueError(f"mode_pied_escalier should be 'not_exact' or 'exact', not {mode_pied_escalier}")

# ------------------- DEFAULT ACTION ORDER TABLES -------------------

def get_default_action_order(nb_chevaux, mode_pied_escalier, mode_ascension = "sans_contrainte"):
    # TODO : scénario c'est toujours le premier cheval qui bouge...

    result = [0] # commun aux 2 Action 
    # favoriser move out 
    result.append(1)  # commun aux 2 Action 
    result.append(2)  # commun aux 2 Action

    if mode_ascension == "avec_contrainte":
        len_ajout = len(Action_EXACT_ASCENSION) - 3
        # puis tuer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.KILL.value + i*len_ajout)
        # puis atteindre objectif
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.REACH_GOAL.value + i*len_ajout)
        # mettre pion en sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.REACH_PIED_ESCALIER.value + i*len_ajout)
        # avancer pres du pied
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.AVANCE_RECULE_PIED_ESCALIER.value + i*len_ajout)
        # ensuite avancer dans sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.MARCHE_1.value + i*len_ajout)
            result.append(Action_EXACT_ASCENSION.MARCHE_2.value + i*len_ajout)
            result.append(Action_EXACT_ASCENSION.MARCHE_3.value + i*len_ajout)
            result.append(Action_EXACT_ASCENSION.MARCHE_4.value + i*len_ajout)
            result.append(Action_EXACT_ASCENSION.MARCHE_5.value + i*len_ajout)
            result.append(Action_EXACT_ASCENSION.MARCHE_6.value + i*len_ajout)
        # enfin juste simplement avancer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.MOVE_FORWARD.value + i*len_ajout)
        # puis get stuck
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT_ASCENSION.GET_STUCK_BEHIND.value + i*len_ajout)


    elif mode_pied_escalier == "not_exact":
        len_ajout = len(Action_NO_EXACT) - 3
        # puis tuer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.KILL.value + i*len_ajout)
        # puis atteindre objectif
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.REACH_GOAL.value + i*len_ajout)
        # mettre pion en sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.ENTER_SAFEZONE.value + i*len_ajout)
        # ensuite avancer dans sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.MOVE_IN_SAFE_ZONE.value + i*len_ajout)
        # enfin juste simplement avancer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.MOVE_FORWARD.value + i*len_ajout)
        # puis get stuck 
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_NO_EXACT.GET_STUCK_BEHIND.value + i*len_ajout)


    elif mode_pied_escalier == "exact":
        len_ajout = len(Action_EXACT) - 3
        # puis tuer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.KILL.value + i*len_ajout)
        # puis atteindre objectif
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.REACH_GOAL.value + i*len_ajout)
        # mettre pion en sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.REACH_PIED_ESCALIER.value + i*len_ajout)
        # avancer pres du pied
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.AVANCE_RECULE_PIED_ESCALIER.value + i*len_ajout)
        # ensuite avancer dans sécurité
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.MOVE_IN_SAFE_ZONE.value + i*len_ajout)
        # enfin juste simplement avancer
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.MOVE_FORWARD.value + i*len_ajout)
        # puis get stuck
        for i in range(nb_chevaux -1, -1, -1):
            result.append(Action_EXACT.GET_STUCK_BEHIND.value + i*len_ajout)
    else:
        raise ValueError(f"mode_pied_escalier should be 'not_exact' or 'exact', not {mode_pied_escalier}")
    return result 
