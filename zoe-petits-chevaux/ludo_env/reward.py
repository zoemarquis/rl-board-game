from ludo_env.action import Action

REWARD_TABLE_MOVE_OUT = {
    Action.NO_ACTION: -1,
    Action.MOVE_OUT: 20,
    Action.MOVE_FORWARD: 5,
    Action.ENTER_SAFEZONE: 15,
    Action.MOVE_IN_SAFE_ZONE: 1,
    Action.REACH_GOAL: 10,
    Action.KILL: 30,
    # Action.PROTECT: 20,
    #
    # Action.DIE: -20 # TODO -> reward pas d'action enfaite, on le subit pendant un tour
}  # faudrait que les sommes répartis soient égales

DEFAULT_ACTION_ORDER = {
    0,  # ça veut dire rien de possible
    1,  # d'abord essayer de sortir
    6,
    11,  # tuer un pion
    3,
    8,  # sauver le pion
    5,
    10,  # atteindre l'objectif
    2,
    7,  # avancer
    4,
    9,  # avancer dans la safezone
}
