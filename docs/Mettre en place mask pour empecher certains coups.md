# Mettre en place mask pour empêcher certains coups

- déterminer le coup impossible (repousser ce qui vient d'etre poussé)
- déterminer les cases qui ne sont pas accessibles
-> changer la proba de ça à zéro

- si Q learning (ou value based method) -> Q value à l'infini
- policy based method (REINFORCE / PPO) -> changer la policy -> 0 for invalid actions (multiplier par 0 l'output du réseau de policy : enfaite mettre en place une matrice avec 1 pour actions autorisées et 0 pour ooptions (/ cases) pas autorisées)
    - -> par exemple le plateau est représenté par une matrice de 7 x 7 :
    si la case 0,0 est atteignable il y a un 1, un 0 sinon
    -> pour les 12 endroits où insérer quelle est la représentation ? multiplier par une "matrice" composée de 11 un et 1 zéro