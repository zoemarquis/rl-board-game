from labyrinthe import *
from eztext import *
import pygame
import time
import os
import pythoncom

NB_MAX_PLAYER = 4  # TODO : enlever ça


class GUI_manager(object):
    """Class GUI_manager : manage the graphical interface of the game"""

    def __init__(
        self,
        labyrinthe,
        model,
        env,
        prefixeImage="./original_images",
        titre="Labyrinthe",
        size=(1500, 900),
        couleur=(209, 238, 238),
    ):

        self.rl_model = model
        self.env = env

        self.info_message = None
        self.info_img = None
        self.labyrinthe = labyrinthe
        self.fini = False
        self.text_color = couleur
        self.matrix = labyrinthe.board
        self.num_cols = DIMENSION
        self.num_rows = DIMENSION
        self.titre = titre
        self.load_images(prefixeImage)
        pygame.init()
        pygame.display.set_icon(self.logo)
        window = pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.surface.fill((0, 0, 139))
        self.update_parameters()
        self.display_game()

    # Fermeture de la fenêtre
    def close(self):
        pygame.quit()

    def load_images(self, prefixImage="./original_images"):
        self.tiles_images = []
        self.pawns_images = []
        self.pawns_images_for_text = []
        self.bases_images = []
        self.bases_images_for_text = []
        self.treasures_images = []
        self.treasures_images_for_text = []

        if os.path.isfile(os.path.join(prefixImage, "carte_dos" + ".png")):
            self.treasure_face_down = pygame.image.load(
                os.path.join(prefixImage, "carte_dos" + ".png")
            )
        else:
            self.treasure_face_down = None

        for i in range(16):
            if os.path.isfile(os.path.join(prefixImage, "Carte" + str(i) + ".png")):
                s = pygame.image.load(
                    os.path.join(prefixImage, "Carte" + str(i) + ".png")
                )
            else:
                s = None
            self.tiles_images.append(s)

        for i in range(NB_MAX_PLAYER):
            s = pygame.image.load(os.path.join(prefixImage, "pion" + str(i) + ".png"))
            self.pawns_images.append(s)
            s = pygame.image.load(
                os.path.join(prefixImage, "texte_pion" + str(i) + ".png")
            )
            self.pawns_images_for_text.append(s)
            s = pygame.image.load(os.path.join(prefixImage, "base" + str(i) + ".png"))
            self.bases_images.append(s)

            s = pygame.image.load(
                os.path.join(prefixImage, "texte_base" + str(i) + ".png")
            )
            self.bases_images_for_text.append(s)

        for i in range(NUM_TREASURES):
            s = pygame.image.load(os.path.join(prefixImage, "tresor" + str(i) + ".png"))
            self.treasures_images.append(s)
            s = pygame.image.load(
                os.path.join(prefixImage, "carte_tresor" + str(i) + ".png")
            )
            self.treasures_images_for_text.append(s)

        self.logo = pygame.image.load(os.path.join(prefixImage, "logo.png"))
        self.boussole = pygame.image.load(
            os.path.join(prefixImage, "boussole.png")
        )  # TODO inutile ?

    def update_parameters(self):
        self.surface = pygame.display.get_surface()
        self.dimension = self.surface.get_height()
        self.delta = self.dimension // (self.num_rows + 2)
        self.finh = self.delta * (self.num_rows + 2)
        self.finl = self.delta * (self.num_cols + 2)
        self.tailleFont = min(self.delta, self.delta) * 1 // 4

    def draw_tile_surface(self, tile: Tile):
        tresor = tile.get_treasure()
        base = tile.is_base()
        pions = tile.get_pawns()
        img = self.tiles_images[tile.tile_to_char()]

        if img == None:  # TODO : à enlever ?
            return None

        surfCarte = pygame.transform.smoothscale(img, (self.delta, self.delta))
        if base != -1:
            surfBase = pygame.transform.smoothscale(
                self.bases_images[base], (self.delta // 2, self.delta // 2)
            )
            base_x = (self.delta - surfBase.get_width()) // 2
            base_y = (self.delta - surfBase.get_height()) // 2
            surfCarte.blit(surfBase, (base_x, base_y))
        if tresor != -1:
            surfTresor = pygame.transform.smoothscale(
                self.treasures_images[tresor], (self.delta // 2, self.delta // 2)
            )
            base_x = (self.delta - surfTresor.get_width()) // 2
            base_y = (self.delta - surfTresor.get_height()) // 2
            surfCarte.blit(surfTresor, (base_x, base_y))

        dist = 10
        coord = [
            (dist, dist),
            (dist, self.delta - (self.delta // 4 + dist)),
            (
                self.delta - (self.delta // 4 + dist),
                self.delta - (self.delta // 4 + dist),
            ),
            (self.delta - (self.delta // 4 + dist), dist),
        ]
        for pions in pions:
            surfPion = pygame.transform.smoothscale(
                self.pawns_images[pions], (self.delta // 4, self.delta // 4)
            )
            surfCarte.blit(surfPion, coord.pop(0))
        return surfCarte

    def draw_arrow_surface(self, direction="O", color=(255, 0, 0)):
        res = pygame.Surface((self.delta, self.delta))
        pygame.draw.polygon(
            res,
            color,
            [
                (self.delta // 2, self.delta // 3),
                (self.delta - self.delta // 8, self.delta // 2),
                (self.delta // 2, self.delta * 2 // 3),
            ],
            0,
        )
        if direction == "N":
            res = pygame.transform.rotate(res, -90.0)
        elif direction == "E":
            res = pygame.transform.rotate(res, 180.0)
        elif direction == "S":
            res = pygame.transform.rotate(res, 90.0)
        return res

    def draw_pawn_surface(self, pawn):
        res = pygame.Surface((self.delta, self.delta))
        pawn_surface = pygame.transform.smoothscale(
            self.pawns_images[pawn], (self.delta // 2, self.delta // 2)
        )
        res.blit(pawn_surface, (self.delta // 4, self.delta // 4))
        return res

    def render_text_pawn_surface(self, pawn):
        res = pygame.Surface((self.delta, self.delta))
        pawn_surface = pygame.transform.smoothscale(
            self.pawns_images_for_text[pawn], (self.delta, self.delta)
        )
        res.blit(pawn_surface, (0, 0))
        return res

    def draw_treasure_surface(self, treasure):
        res = pygame.Surface((self.delta, self.delta))
        treasure_surface = pygame.transform.smoothscale(
            self.treasures_images[treasure], (self.delta // 2, self.delta // 2)
        )
        res.blit(treasure_surface, (self.delta // 4, self.delta // 4))
        return res
    
    def render_text_base(self, id_player: int):
        res = pygame.Surface((self.delta, self.delta))
        base_surface = pygame.transform.smoothscale(
            self.bases_images_for_text[id_player], (self.delta, self.delta)
        )
        res.blit(base_surface, (0, 0))
        return res

    def render_text_treasure(self, treasure):
        if treasure is None:
            # retourner une surface vide
            return pygame.Surface((self.delta, self.delta))
            # TODO : coté interface graphique, retourner la surface représentant la base
        elif treasure == -1:
            res = pygame.Surface((self.delta, self.delta))
            treasure_surface = pygame.transform.smoothscale(
                self.treasure_face_down, (self.delta, self.delta)
            )
            res.blit(treasure_surface, (0, 0))
            return res
        else:
            res = pygame.Surface((self.delta, self.delta))
            treasure_surface = pygame.transform.smoothscale(
                self.treasures_images_for_text[treasure], (self.delta, self.delta)
            )
            res.blit(treasure_surface, (0, 0))
            return res

    def display_message(self, ligne, text, images=[], color=None):
        font = pygame.font.Font(None, self.tailleFont)
        if color == None:
            color = self.text_color

        posy = self.delta * (
            ligne - 1
        )  # Garde la même hauteur pour chaque ligne de texte
        posx = (
            self.finl 
        )  # Déplace à droite du plateau en utilisant la largeur du plateau

        text_list = text.split("@img@")
        for msg in text_list:
            if msg != "":
                text = font.render(msg, 1, color)
                textpos = text.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(text, textpos)
                posx += textpos.width  # +(self.deltal//3)
            if images != []:
                surface = images.pop(0)
                beginy = posy - (self.delta // 3)
                self.surface.blit(surface, (posx, beginy))
                posx += surface.get_width()  # +(self.deltal//3)

    def display_message_second_column(self, ligne, text, images=[], color=None):
        font = pygame.font.Font(None, self.tailleFont)
        if color == None:
            color = self.text_color

        posy = self.delta * (
            ligne - 1
        )  # Garde la même hauteur pour chaque ligne de texte
        posx = (
            self.finl + self.delta * 4
        )  # Déplace à droite du plateau en utilisant la largeur du plateau

        text_list = text.split("@img@")
        for msg in text_list:
            if msg != "":
                text = font.render(msg, 1, color)
                textpos = text.get_rect()
                textpos.y = posy
                textpos.x = posx
                self.surface.blit(text, textpos)
                posx += textpos.width  # +(self.deltal//3)
            if images != []:
                surface = images.pop(0)
                beginy = posy - (self.delta // 3)
                self.surface.blit(surface, (posx, beginy))
                posx += surface.get_width()  # +(self.deltal//3)

    def display_score(self, row_index=3):
        text = "Trésors de chaque joueur : "
        self.display_message(row_index, text)
        current_row_index = row_index + 1
        for i in range(self.labyrinthe.get_num_players()):
            text_player = ""
            img = []
            img.append(self.render_text_pawn_surface(i))
            for treasure in self.labyrinthe.players.get_found_treasures(i):
                text_player += " @img@ "
                img.append(self.render_text_treasure(treasure))

            for treasure in range(self.labyrinthe.players.get_nb_treasures_remaining(i)):
                text_player += " @img@ "
                img.append(self.render_text_treasure(-1))
                
            self.display_message(current_row_index, text_player, img)
            current_row_index += 1

    def display_info_message(self, row_index=4):
        if self.info_message != None:
            self.display_message(row_index, self.info_message, self.info_img)
        self.info_message = None
        self.info_img = None

    def display_playable_tile(self, row_index):
        text_player = "Tuile à insérer :  "
        tile_surface = self.draw_tile_surface(self.labyrinthe.get_tile_to_play())
    
        self.display_message(
            row_index,      
            text_player,            
            images=[tile_surface]   
        )


    def draw_arrows(self, couleur=(255, 255, 0)):
        self.surface.fill((0, 0, 139))  # pour gérer les effets de transparence
        for i in range(1, self.num_rows, 2):
            if self.labyrinthe.forbidden_move == ("O", i):
                flecheO = self.draw_arrow_surface("O", (255, 68, 51))
            else:
                flecheO = self.draw_arrow_surface("O", couleur)
            flecheO.set_colorkey((0, 0, 0))  # Set transparency color key
            self.surface.blit(flecheO, (0, (i + 1) * self.delta))

            if self.labyrinthe.forbidden_move == ("E", i):
                flecheE = self.draw_arrow_surface("E", (255, 68, 51))
            else:
                flecheE = self.draw_arrow_surface("E", couleur)
            flecheE.set_colorkey((0, 0, 0))  # Set transparency color key
            self.surface.blit(
                flecheE, (self.delta * (self.num_cols + 1), (i + 1) * self.delta)
            )

        for i in range(1, self.num_cols, 2):
            if self.labyrinthe.forbidden_move == ("N", i):
                flecheN = self.draw_arrow_surface("N", (255, 68, 51))
            else:
                flecheN = self.draw_arrow_surface("N", couleur)
            flecheN.set_colorkey((0, 0, 0))  # Set transparency color key
            self.surface.blit(flecheN, ((i + 1) * self.delta, 0))

            if self.labyrinthe.forbidden_move == ("S", i):
                flecheS = self.draw_arrow_surface("S", (255, 68, 51))
            else:
                flecheS = self.draw_arrow_surface("S", couleur)
            flecheS.set_colorkey((0, 0, 0))  # Set transparency color key
            self.surface.blit(
                flecheS, ((i + 1) * self.delta, self.delta * (self.num_rows + 1))
            )

    def draw_board(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                try:
                    tile = self.matrix.get_value(r, c)
                    tile_surface = self.draw_tile_surface(tile)
                    if tile_surface == None:
                        self.surface.fill(
                            (0, 255, 0),
                            (
                                (c + 1) * self.delta,
                                (r + 1) * self.delta,
                                self.delta,
                                self.delta,
                            ),
                        )
                    else:
                        self.surface.blit(
                            tile_surface, ((c + 1) * self.delta, (r + 1) * self.delta)
                        )
                except:
                    pass

    def animated_path(self, chemin, pause=0.2):
        (xp, yp) = chemin.pop(0)
        for x, y in chemin:
            self.labyrinthe.remove_current_player_from_tile(
                xp, yp
            )  # pas la bonne fonction
            self.labyrinthe.put_current_player_in_tile(x, y)  # la meme
            self.display_game()
            time.sleep(pause)
            xp, yp = x, y
        return xp, yp

    def get_case(self, pos): 
        """determine the type of action to do based the position on the mouseclick"""
        if (
            self.finl + 1.35 * self.delta
            <= pos[0]
            <= self.finl + 1.35 * self.delta + self.delta
            and (self.finh - 5.5 * self.delta) // 2 
            <= pos[1] 
            <= (self.finh - 5.5 * self.delta) // 2 + self.delta
        ):
            return ("T", "T")
        if pos[0] < 0 or pos[0] > self.finl or pos[1] < 0 or pos[1] > self.finh:
            return (-1, -1)

        x = pos[1] // self.delta
        y = pos[0] // self.delta
        if x == 0 and y in [2, 4, 6]:
            return ("N", y - 1)
        if x == self.num_cols + 1 and y in [2, 4, 6]:
            return ("S", y - 1)
        if y == 0 and x in [2, 4, 6]:
            return ("O", x - 1)
        if y == self.num_rows + 1 and x in [2, 4, 6]:
            return ("E", x - 1)
        if x == 0 or x == self.num_cols + 1 or y == 0 or y == self.num_rows + 1:
            return (-1, -1)
        return (x - 1, y - 1)

    def display_game(self):
        self.draw_arrows()
        self.draw_board()
        if not self.fini:
            if self.labyrinthe.is_current_player_ai():
                self.display_message_second_column(
                    2,
                    "C'est au tour de l'IA @img@",
                    [
                        self.render_text_pawn_surface(
                            self.labyrinthe.get_current_player()
                        )
                    ],
                )
                if self.labyrinthe.get_current_player_remaining_treasure() == 0:
                    self.display_message_second_column(
                        2, 
                        "Retournez à @img@", 
                        [
                            self.render_text_base(
                                self.labyrinthe.get_current_player()
                            )
                        ]
                    )
                else:
                    self.display_message_second_column(
                        2,
                        "Trésor à trouver @img@",
                        [self.render_text_treasure(self.labyrinthe.current_treasure())],
                    )
            else:
                self.display_message(
                    2,
                    "C'est au tour du joueur @img@",
                    [
                        self.render_text_pawn_surface(
                            self.labyrinthe.get_current_player()
                        )
                    ],
                )
                if self.labyrinthe.get_current_player_remaining_treasure() == 0:
                    self.display_message_second_column(
                        2, 
                        "Retournez à @img@", 
                        [
                            self.render_text_base(
                                self.labyrinthe.get_current_player()
                            )
                        ]
                    )
                else:
                    self.display_message_second_column(
                        2,
                        "Trésor à trouver @img@",
                        [self.render_text_treasure(self.labyrinthe.current_treasure())],
                    )
        self.display_playable_tile(3)
        self.display_info_message(4)
        self.display_score(5)
        pygame.display.flip()

    def start(self):  # TODO : à revoir
        self.phase = 1
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)

        # Boucle d'événements
        while True:
            
            pythoncom.PumpWaitingMessages()

            ev = pygame.event.wait()

            if ev.type == pygame.QUIT:
                print("Fermeture de la fenêtre")
                break

            if ev.type == pygame.USEREVENT + 1:
                pygame.display.flip()

            if ev.type == pygame.VIDEORESIZE:
                self.update_parameters()
                self.display_game()

            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    break

            if self.labyrinthe.is_current_player_human():

                if ev.type == KEYDOWN:  # TODO : à revoir
                    if ev.key == K_KP0:
                        self.labyrinthe.ajouterCode(0)
                    if ev.key == K_KP1:
                        self.labyrinthe.ajouterCode(1)
                    if ev.key == K_KP2:
                        self.labyrinthe.ajouterCode(2)
                    if ev.key == K_KP3:
                        self.labyrinthe.ajouterCode(3)
                    if ev.key == K_KP4:
                        self.labyrinthe.ajouterCode(4)
                    if ev.key == K_KP5:
                        self.labyrinthe.ajouterCode(5)
                    if ev.key == K_KP6:
                        self.labyrinthe.ajouterCode(6)
                    if ev.key == K_KP7:
                        self.labyrinthe.ajouterCode(7)
                    if ev.key == K_KP8:
                        self.labyrinthe.ajouterCode(8)
                    if ev.key == K_KP9:
                        self.labyrinthe.ajouterCode(9)
                    if ev.key == K_BACKSPACE:
                        self.labyrinthe.effacerDernierCode()
                        self.display_game()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    (x, y) = self.get_case(ev.pos)
                    if self.fini:
                        continue

                    if self.phase == 1:
                        if x == "T":
                            self.labyrinthe.rotate_tile()
                        elif x in ["N", "S", "O", "E"]:
                            if self.labyrinthe.is_forbidden_move(x, y):
                                self.info_message = (
                                    "Coup interdit : mouvement opposé au dernier."
                                )
                                self.info_img = []
                            else:
                                self.labyrinthe.play_tile(x, y)
                                self.phase = 2  # TODO : revoir gestion des phases, surement autre modele pour gym (3 phases ou seulement 1)

                        elif x != -1:
                            self.info_message = (
                                "Insérez d'abord la carte avant de bouger."
                            )
                            self.info_img = []
                    else:
                        if x in ["T", "N", "S", "O", "E", -1]:
                            self.info_message = (
                                "Sélectionnez une case dans le labyrinthe."
                            )
                            self.info_img = []
                        else:
                            jc = self.labyrinthe.get_current_player()
                            xD, yD = self.labyrinthe.coords_current_player
                            chemin = self.labyrinthe.is_accessible(xD, yD, x, y)
                            if len(chemin) == 0:
                                self.info_message = (
                                    "Cette case est inaccessible pour le joueur @img@"
                                )
                                self.info_img = [self.render_text_pawn_surface(jc)]
                            else:
                                self.animated_path(chemin)
                                c = self.labyrinthe.board.get_value(x, y)
                                t = self.labyrinthe.current_treasure()
                                player_at_start = (
                                    self.labyrinthe.get_coord_player() == 
                                    self.labyrinthe.get_current_player_object().get_start_position()
                                )
                                if c.get_treasure() == t:
                                    self.labyrinthe.remove_current_treasure()
                                    if (
                                        self.labyrinthe.get_current_player_remaining_treasure()
                                        == 0  
                                    ):
                                        if player_at_start:
                                            self.info_message = "Le joueur @img@ a gagné"
                                            self.info_img = [self.render_text_pawn_surface(jc)]
                                            self.fini = True
                                        else:
                                            self.info_message = "Le joueur @img@ trouvé tous ses trésors, retournez à @img@ pour gagner"
                                            self.info_img = [self.render_text_pawn_surface(jc), self.render_text_base(jc)]
                                    else:
                                        self.info_message = (
                                            "Le joueur @img@ a trouvé le trésor @img@"
                                        )
                                        self.info_img = [
                                            self.render_text_pawn_surface(jc),
                                            self.render_text_treasure(t),
                                        ]
                                
                                if (
                                        self.labyrinthe.get_current_player_remaining_treasure()
                                        == 0  and player_at_start
                                    ):
                                        self.info_message = "Le joueur @img@ a gagné"
                                        self.info_img = [self.render_text_pawn_surface(jc)]
                                        self.fini = True

                                self.labyrinthe.next_player()
                                self.phase = 1

                    self.display_game()
            # TODO : gestion de l'IA : temporiser les coups
            # TODO : Zoé pour la DB
            elif not self.fini:
                if self.rl_model:
                    # Récupération action insertion de la tuile
                    obs = self.env._get_observation()
                    action, _ = self.rl_model.predict(obs, deterministic=True)

                    # Ajout de la tuile au labyrinthe
                    rotation_idx, insertion_idx = action

                    direction_map = {0: "N", 1: "E", 2: "S", 3: "O"}
                    direction = direction_map[rotation_idx]

                    insertion_positions = [1, 3, 5]
                    index = insertion_positions[insertion_idx % 3]

                    self.labyrinthe.play_tile(direction, index)

                    # Affichage sur labyrinthe graphique
                    self.display_game()
                    pygame.display.flip()
                    time.sleep(0.5)

                    # Récupération de l'action de déplacement
                    obs = self.env._get_observation()
                    movement_action, _ = self.rl_model.predict(obs, deterministic=True)

                    print("Action de déplacement :", movement_action)

                    mouvements_possibles = self.env._get_mouvements_possibles(joueur_id=self.env.game.get_current_player())
                    
                    #print("Mouvements possibles :", mouvements_possibles)

                    # Vérification de l'action de déplacement
                    if isinstance(movement_action[0], int) and 0 <= movement_action[0] < len(mouvements_possibles):
                        nouvelle_position = mouvements_possibles[movement_action[0]]

                        if 0 <= nouvelle_position[0] < DIMENSION and 0 <= nouvelle_position[1] < DIMENSION:
                            self.env._deplacer_joueur(nouvelle_position)    
                        else:
                            print("Déplacement hors limites. Le joueur reste à sa position.")
                    else:
                        print("Action de déplacement invalide. Le joueur reste à sa position.")

                    # Déplacement sur labyrinth
                    

                    # Afficahge
                    self.display_game()
                    pygame.display.flip()
                    time.sleep(0.5)
                else:
                    print("Modèle RL manquant pour l'agent.")

                self.labyrinthe.next_player()
                self.display_game()
            pygame.display.flip()
