from ludo_env.action import Action_NO_EXACT, Action_EXACT


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
    Action_EXACT.REACH_PIED_ESCALIER: 15,
    Action_EXACT.AVANCE_RECULE_PIED_ESCALIER: 1,
    Action_EXACT.MOVE_IN_SAFE_ZONE: 5,

    Action_EXACT.REACH_GOAL: 10,
    Action_EXACT.KILL: 30,
}


def get_reward_table(mode_pied_escalier):
    if mode_pied_escalier == "not_exact":
        return REWARD_TABLE_MOVE_OUT_NO_EXACT
    elif mode_pied_escalier == "exact":
        return REWARD_TABLE_MOVE_OUT_EXACT
    else:
        raise ValueError(f"mode_pied_escalier should be 'not_exact' or 'exact', not {mode_pied_escalier}")

# ------------------- DEFAULT ACTION ORDER TABLES -------------------

def get_default_action_order(nb_chevaux, mode_pied_escalier):
    # TODO : scénario c'est toujours le premier cheval qui bouge...

    result = [0] # commun aux 2 Action 
    # favoriser move out 
    result.append(1)  # commun aux 2 Action 
    result.append(2)  # commun aux 2 Action

    if mode_pied_escalier == "not_exact":
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
