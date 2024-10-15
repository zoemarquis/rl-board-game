## brouillon : 
## fonction utilitaire pour calculer suffisamment efficacement les cases accessibles sur le plateau pour un joueur 
## dans le but d'améliorer la rapidité lors du test de "je veux me déplacer là"
## mais aussi pour qu'un agent puisse rapidement connaitre son champ des possible et n'étudie pas tout le plateau

from tile import Tile

def get_reachable_tiles(current_tile : Tile):
    ''' la stratégie c'est que plutot que de parcourir toutes les tiles du plateau
    on peut regarder les voisins et utiliser une structure de donnée (type set ou file ?) pour parcourir les voisins
    ! les voisins sont les cases accessibles uniquement, on marque les cases déjà visitées pour ne pas boucler
    '''
    neighbors_set = set(current_tile)
    visited = set()
    while neighbors_set: # not empty

        # update set of neighbors
        visited.add(current_tile)
        neighbors_set.remove(current_tile)
    
        tile_north = current_tile.get_accessible_north_neighbor() # if not accessible, return None
        tile_south = current_tile.get_accessible_south_neighbor()
        tile_east = current_tile.get_accessible_east_neighbor
        tile_west = current_tile.get_accessible_west_neighbor()
    
        if tile_north not in visited:
            neighbors_set.add(tile_north)
        if tile_south not in visited:
            neighbors_set.add(tile_south)
        if tile_east not in visited:
            neighbors_set.add(tile_east)
        if tile_west not in visited:
            neighbors_set.add(tile_west)

    return visited


