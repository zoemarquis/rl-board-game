# Etude du jeu Labyrinthe

# Règles du jeu

**Contenu** : 

- 1 plateau de jeu avec 16 plaques Couloir fixes
- 34 plaques Couloir
- 24 cartes Trésor
- 4 pions

**Nombre de joueurs :**  2 à 4

**Durée d’une partie :**  moins de 30 minutes

<aside>
💡

### But du jeu

Le but est de retrouver un maximum de trésors dans le labyrinthe enchanté, où les murs et les couloirs se déplacent à chaque tour. 

</aside>

<aside>
💡

### Mise en place

1. Mélanger les **plaques Couloir** face cachée, puis les placer sur les emplacements libres du plateau pour **créer un labyrinthe aléatoire**. La plaque supplémentaire servira à faire coulisser les couloirs du labyrinthe.
2. **Mélanger** à leur tour les **24 cartes Trésor** face cachée.
3. En **distribuer** le même nombre à chaque joueur. Chacun les empile devant lui sans les regarder.
4. Chaque joueur choisit ensuite **un pion** qu’il place sur sa **case Départ** au coin du plateau de la couleur correspondante.
</aside>

## **Déroulement de la partie :**

Chaque joueur commence par regarder secrètement la première carte de sa pile pour identifier le premier trésor qu'il doit chercher. 

Le tour d’un joueur se compose en deux étapes:

1. Modifier les couloirs
2. Déplacer son pion

A tour de rôle, chacun modifie le labyrinthe en insérant et en faisant coulisser la plaque supplémentaire vers l'intérieur, dans une des rangées du plateau, afin de créer le chemin qui le mènera jusqu'au trésor. Le joueur peut ensuite déplacer son pion. (mais il peut aussi rester sur place s’il le veut)

<aside>
❗

Un joueur n’a pas le droit d’annuler l’action du jouer précédent ⇒ une plaque ne peut jamais être réintroduite a l’endroit même d’ou elle vient d’être expulsée par le joueur précédent.

</aside>

<aside>
❗

Si un pion est expulsé hors du plateau lors d’un mouvement d’une colonne ou d’une rangée il est replacé à l’opposé de celle-ci. Cependant, ceci ne constitue pas un mouvement du pion.

</aside>

Quand un joueur parvient à attraper son premier trésor, il retourne sa deuxième carte pour connaître son prochain objectif. 

## Fin de la partie

<aside>
🏆

Le vainqueur est le premier joueur à avoir retourné toutes ces cartes et à ramener son pion a son point de départ.

</aside>

---

## Agents / comportements possibles

### **Agent saboteur**

Cherche à bloquer les autres joueurs en détruisant les chemins.

### **Agent explorateur**

Cherche à révéler un maximum de chemins non explorés.

### Agent opportuniste

Réagit aux changements du labyrinthe et s'adapte aux opportunités immédiates.

### Agent flemmard

Ne bouge pas son pion tant qu’il n’a pas au moins X cases de son chemin prêtes.

### Agent collaborateur

Crée des alliances temporaires avec d'autres joueurs pour maximiser les bénéfices mutuels.

### Agent indécis

Si il ne peut pas attendre son objectif toute suite, copie le mouvent de joueur précédent. 

---

## Modifications du jeu

- Certaines cartes Trésor peuvent être en double.
- Objet spécial qui permet de décaler les flèches et donc pouvoir déplacer les rangées normalement fixes.
- Chaque joueur reçoit une ou deux cartes "pouvoirs spéciaux" qu'il peut utiliser une seule fois par partie. Exemples :
    - **Double déplacement** : Permet de jouer deux fois de suite.
    - **Blocage** : Empêche un joueur de déplacer un segment du labyrinthe pendant un tour.
    - **Échange** : Permet d’échanger sa position avec un autre joueur.
- Certaines portions du labyrinthe peuvent être fermées par des portes verrouillées. Pour les ouvrir, les joueurs doivent d'abord trouver une clé cachée dans le labyrinthe avant de pouvoir traverser.
- Cartes de choix entre deux trésors différents.