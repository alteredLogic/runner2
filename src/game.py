"""
Game Class
"""
from gametile import *
from star import *
from background import *
from player import *
from bullet import *
from particle import *


class Game:
    """
    Creates a game object
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.finish = False
        self.dropping_down = False
        self.falling_up = False
        self.on_floor_sound_guard = True

        self.mega_grid = self.load_level_from_disk()
        # TODO try/except block for empty grid

        if self.mega_grid is not None:
            self.scroll_direction = self.mega_grid[0][0].scroll_direction
        else:
            self.scroll_direction = 'None'

        if self.scroll_direction == 'Down':
            self.level_pixels_remaining = self.screen_height
            self.draw_distance = self.screen_height
            self.curr_level = self.mega_grid[1][0]
        elif self.scroll_direction == 'Right':
            self.level_pixels_remaining = self.screen_width
            self.draw_distance = self.screen_width
            self.curr_level = self.mega_grid[0][1]
        elif self.scroll_direction == 'None':
            pass
        else:
            pygame.quit()
            exit('No scrolling direction set.')

        self.number_of_matrix_rows = self.mega_grid[0][0].number_of_matrix_rows
        self.number_of_matrix_columns = self.mega_grid[0][0].number_of_matrix_columns
        self.tile_width = int(round(self.screen_width / self.number_of_matrix_columns))
        self.tile_height = int(round(self.screen_height / self.number_of_matrix_rows))

        self.death_calls = BLOWUP_COUNT
        self.scroll_direction_backup = None

        self.curr_level_row = 0
        self.curr_level_column = 0
        self.player_on_floor = False
        self.speed = STARTING_SPEED
        self.speed_backup = STARTING_SPEED

        self.player = Player(self.tile_width, self.tile_height, PLAYER_STARTING_X, PLAYER_STARTING_Y)

        self.floor_tiles = pygame.sprite.Group()
        self.ceiling_tiles = pygame.sprite.Group()
        self.lava_tiles = pygame.sprite.Group()
        self.shootable_0_tiles = pygame.sprite.Group()
        self.shootable_1_tiles = pygame.sprite.Group()
        self.drop_down_tiles = pygame.sprite.Group()
        self.fall_up_tiles = pygame.sprite.Group()
        self.finish_tiles = pygame.sprite.Group()
        self.gravity_up_tiles = pygame.sprite.Group()
        self.gravity_down_tiles = pygame.sprite.Group()
        self.level_tiles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        self.full_bg = pygame.Surface((self.screen_width, self.screen_height))
        self.full_bg.fill(BACKGROUND_COLOR)
        if self.scroll_direction != 'None':
            self.initial_render()

    def resize(self, matrix_rows, matrix_columns):
        """
        Resize the game
        :param matrix_rows: New number of matrix rows
        :param matrix_columns: New number of matrix columns
        """
        self.screen_width = 800
        self.screen_height = 600
        self.number_of_matrix_rows = matrix_rows
        self.number_of_matrix_columns = matrix_columns
        self.tile_width = int(round(self.screen_width / self.number_of_matrix_columns))
        self.tile_height = int(round(self.screen_height / self.number_of_matrix_rows))

        # self.full_bg = pygame.transform.scale(self.full_bg, (self.screen_width, self.screen_height))
        self.player.image = pygame.transform.scale(self.player.image, (self.tile_width, self.tile_height))
        top_left_position = self.player.rect.topleft
        self.player.rect = self.player.image.get_rect(topleft=top_left_position)

    def create_tile(self, kind, top_left_x, top_left_y):
        """
        Creates a level tile
        :param kind: Type of game tile to create
        :param top_left_x: Starting x position
        :param top_left_y: Starting y position
        """
        next_tile = None

        if kind == KIND_FLOOR:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, FLOOR_COLOR, 'Floor')
            self.floor_tiles.add(next_tile)

        elif kind == KIND_SHOOTABLE_0:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, SHOOTABLE_0_COLOR, 'Shootable 0')
            self.shootable_0_tiles.add(next_tile)

        elif kind == KIND_SHOOTABLE_1:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, SHOOTABLE_1_COLOR, 'Shootable 1')
            self.shootable_1_tiles.add(next_tile)

        elif kind == KIND_LAVA:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, LAVA_COLOR, 'Lava')
            self.lava_tiles.add(next_tile)

        elif kind == KIND_CEILING:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, CEILING_COLOR, 'Ceiling')
            self.ceiling_tiles.add(next_tile)

        elif kind == KIND_FINISH:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, FINISH_COLOR_1, 'Finish')
            self.finish_tiles.add(next_tile)

        elif kind == KIND_DROP_DOWN:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, DROP_DOWN_COLOR, 'Drop Down')
            self.drop_down_tiles.add(next_tile)

        elif kind == KIND_FALL_UP:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, FALL_UP_COLOR, 'Fall Up')
            self.fall_up_tiles.add(next_tile)

        elif kind == KIND_GRAVITY_UP:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, GRAVITY_UP_COLOR, 'Gravity Up')
            self.gravity_up_tiles.add(next_tile)

        elif kind == KIND_GRAVITY_DOWN:
            next_tile = GameTile(self.tile_width, self.tile_height,
                                 top_left_x, top_left_y, GRAVITY_DOWN_COLOR, 'Gravity Down')
            self.gravity_down_tiles.add(next_tile)

        if next_tile is not None:
            self.level_tiles.add(next_tile)

    def initial_render(self):
        """
        Draws initial screen
        """
        starting_level = self.mega_grid[0][0].grid
        for r in range(self.number_of_matrix_rows):
            for c in range(self.number_of_matrix_columns):
                curr_tile_kind = starting_level[r][c]

                top_left_x = c * self.tile_width
                top_left_y = r * self.tile_height

                self.create_tile(curr_tile_kind, top_left_x, top_left_y)

        self.spawn_initial_stars()
        self.spawn_initial_background()

    def scroll_master_control(self):
        """
        Master scroll controlling function
        """
        if self.scroll_direction == 'Left':

            self.adjust_left_x()

            if self.level_pixels_remaining > self.speed:
                self.scroll_screen_left(self.speed)
                self.draw_left_column()
            else:
                self.scroll_screen_left(self.level_pixels_remaining)
                self.draw_left_column()
                self.update_curr_level()

        elif self.scroll_direction == 'Right':

            self.adjust_right_x()

            if self.level_pixels_remaining > self.speed:
                self.scroll_screen_right(self.speed)
                self.draw_right_column()
            else:
                self.scroll_screen_right(self.level_pixels_remaining)
                self.draw_right_column()
                self.update_curr_level()

        elif self.scroll_direction == 'Up':

            self.adjust_up_y()

            if self.level_pixels_remaining > self.speed:
                self.scroll_screen_up(self.speed)
                self.draw_up_row()
            else:
                self.scroll_screen_up(self.level_pixels_remaining)
                self.draw_up_row()
                self.update_curr_level()

        elif self.scroll_direction == 'Down':

            self.adjust_down_y()

            if self.level_pixels_remaining > self.speed:
                self.scroll_screen_down(self.speed)
                self.draw_down_row()
            else:
                self.scroll_screen_down(self.level_pixels_remaining)
                self.draw_down_row()
                self.update_curr_level()

    def draw_right_column(self):
        """
        Draw in columns when scrolling right
        """
        if self.scroll_direction != 'Right' or self.falling_up or self.dropping_down:
            return

        while self.draw_distance < self.screen_width:
            for r in range(self.number_of_matrix_rows):
                curr_tile_kind = self.curr_level.grid[r][self.curr_level_column]
                top_left_x = self.draw_distance
                top_left_y = r * self.tile_height

                self.create_tile(curr_tile_kind, top_left_x, top_left_y)

            self.draw_distance += self.tile_width
            self.curr_level_column += 1

    def draw_left_column(self):
        """
        Draw in columns when scrolling left
        """
        if self.scroll_direction != 'Left' or self.falling_up or self.dropping_down:
            return

        while self.draw_distance > 0:
            self.draw_distance -= self.tile_width
            for r in range(self.number_of_matrix_rows):
                curr_tile_kind = self.curr_level.grid[r][self.curr_level_column]
                top_left_x = self.draw_distance
                top_left_y = r * self.tile_height

                self.create_tile(curr_tile_kind, top_left_x, top_left_y)

            self.curr_level_column -= 1

    def draw_up_row(self):
        """
        Draw in rows when scrolling up
        """
        if self.scroll_direction != 'Up' or self.falling_up or self.dropping_down:
            return

        while self.draw_distance > 0:
            self.draw_distance -= self.tile_height
            for c in range(self.number_of_matrix_columns):
                curr_tile_kind = self.curr_level.grid[self.curr_level_row][c]
                top_left_x = c * self.tile_width
                top_left_y = self.draw_distance

                self.create_tile(curr_tile_kind, top_left_x, top_left_y)

            self.curr_level_row -= 1

    def draw_down_row(self):
        """
        Draw in rows when scrolling down
        """
        if self.scroll_direction != 'Down' or self.falling_up or self.dropping_down:
            return

        while self.draw_distance < self.screen_height:
            for c in range(self.number_of_matrix_columns):
                curr_tile_kind = self.curr_level.grid[self.curr_level_row][c]
                top_left_x = c * self.tile_width
                top_left_y = self.draw_distance

                self.create_tile(curr_tile_kind, top_left_x, top_left_y)

            self.draw_distance += self.tile_height
            self.curr_level_row += 1

    def scroll_screen_left(self, number_of_pixels):
        """
        Moves the screen left
        :param number_of_pixels: Number of pixels to scroll left
        """
        for level_tile in self.level_tiles:
            level_tile.rect.move_ip(number_of_pixels, 0)
            if level_tile.rect.left >= self.screen_width:
                level_tile.kill()
                del level_tile

        self.level_pixels_remaining -= number_of_pixels
        self.draw_distance += number_of_pixels

    def scroll_screen_right(self, number_of_pixels):
        """
        Moves the screen right
        :param number_of_pixels: Number of pixels to scroll right
        """
        for level_tile in self.level_tiles:
            level_tile.rect.move_ip(-number_of_pixels, 0)
            if level_tile.rect.right <= 0:
                level_tile.kill()
                del level_tile

        self.level_pixels_remaining -= number_of_pixels
        self.draw_distance -= number_of_pixels

    def scroll_screen_up(self, number_of_pixels):
        """
        Moves the screen up
        :param number_of_pixels: Number of pixels to scroll up
        """
        for level_tile in self.level_tiles:
            level_tile.rect.move_ip(0, number_of_pixels)
            if level_tile.rect.top >= self.screen_height:
                level_tile.kill()
                del level_tile

        self.level_pixels_remaining -= number_of_pixels
        self.draw_distance += number_of_pixels

    def scroll_screen_down(self, number_of_pixels):
        """
        Moves the screen down
        :param number_of_pixels: Number of pixels to scroll down
        """
        for level_tile in self.level_tiles:
            level_tile.rect.move_ip(0, -number_of_pixels)
            if level_tile.rect.bottom <= 0:
                level_tile.kill()
                del level_tile

        self.level_pixels_remaining -= number_of_pixels
        self.draw_distance -= number_of_pixels

    def adjust_right_x(self):
        """
        Adjusts the player's x position while right scrolling
        """
        if self.player.rect.left > PROPER_RIGHT_SCROLL_X_POS:
            distance_from_proper_x_position = abs(self.player.rect.left - PROPER_RIGHT_SCROLL_X_POS)
            if self.speed <= distance_from_proper_x_position:
                self.player.rect.move_ip(-self.speed, 0)
            else:
                self.player.rect.move_ip(-distance_from_proper_x_position, 0)
        elif self.player.rect.left < PROPER_RIGHT_SCROLL_X_POS:
            self.player.rect.move_ip(self.speed, 0)

    def adjust_left_x(self):
        """
        Adjusts the player's x position while left scrolling
        """
        if self.player.rect.right > PROPER_LEFT_SCROLL_X_POS:
            distance_from_proper_x_position = abs(self.player.rect.right - PROPER_LEFT_SCROLL_X_POS)
            if self.speed <= distance_from_proper_x_position:
                self.player.rect.move_ip(-self.speed, 0)
            else:
                self.player.rect.move_ip(-distance_from_proper_x_position, 0)
        elif self.player.rect.right < PROPER_LEFT_SCROLL_X_POS:
            self.player.rect.move_ip(self.speed, 0)

    def adjust_up_y(self):
        """
        Adjusts the player's y position while up scrolling
        """
        if self.player.rect.bottom > PROPER_UP_SCROLL_Y_POS:
            distance_from_proper_y_position = abs(self.player.rect.bottom - PROPER_UP_SCROLL_Y_POS)
            if self.speed <= distance_from_proper_y_position:
                self.player.rect.move_ip(0, -self.speed)
            else:
                self.player.rect.move_ip(0, -distance_from_proper_y_position)
        elif self.player.rect.bottom < PROPER_UP_SCROLL_Y_POS:
            self.player.rect.move_ip(0, self.speed)

    def adjust_down_y(self):
        """
        Adjusts the player's y position while down scrolling
        """
        if self.player.rect.top > PROPER_DOWN_SCROLL_Y_POS:
            distance_from_proper_y_position = abs(self.player.rect.top - PROPER_DOWN_SCROLL_Y_POS)
            if self.speed <= distance_from_proper_y_position:
                self.player.rect.move_ip(0, -self.speed)
            else:
                self.player.rect.move_ip(0, -distance_from_proper_y_position)
        elif self.player.rect.top < PROPER_DOWN_SCROLL_Y_POS:
            self.player.rect.move_ip(0, self.speed)

    def update_curr_level(self):
        """
        Switches the direction of scrolling between between grids
        """
        mega_row = self.curr_level.mega_row
        mega_column = self.curr_level.mega_column

        next_direction = self.curr_level.scroll_direction

        if next_direction == 'Up':
            self.level_pixels_remaining = self.screen_height
            self.draw_distance = 0
            self.curr_level_row = self.number_of_matrix_rows - 1
            self.curr_level = self.mega_grid[mega_row - 1][mega_column]

            # Remove fall tiles
            if len(self.fall_up_tiles) > 0:
                self.scroll_direction_backup = next_direction
                self.speed_backup = self.speed
                self.speed = 0
                self.falling_up = True
            else:
                self.scroll_direction = next_direction

        elif next_direction == 'Down':
            self.level_pixels_remaining = self.screen_height
            self.draw_distance = self.screen_height
            self.curr_level_row = 0
            self.curr_level = self.mega_grid[mega_row + 1][mega_column]

            # Remove drop tiles
            if len(self.drop_down_tiles) > 0:
                self.scroll_direction_backup = next_direction
                self.speed_backup = self.speed
                self.speed = 0
                self.dropping_down = True
            else:
                self.scroll_direction = next_direction

        elif next_direction == 'Left':
            self.scroll_direction = next_direction
            self.level_pixels_remaining = self.screen_width
            self.draw_distance = 0
            self.curr_level_column = self.number_of_matrix_columns - 1
            self.curr_level = self.mega_grid[mega_row][mega_column - 1]

        elif next_direction == 'Right':
            self.scroll_direction = next_direction
            self.level_pixels_remaining = self.screen_width
            self.draw_distance = self.screen_width
            self.curr_level_column = 0
            self.curr_level = self.mega_grid[mega_row][mega_column + 1]

        else:
            assert False

        self.resize(self.curr_level.number_of_matrix_rows, self.curr_level.number_of_matrix_columns)
        self.vertical_collision_check()

    def render_screen(self):
        """
        Renders the screen
        """
        screen = pygame.display.get_surface()
        screen.blit(self.full_bg, (0, 0))
        self.stars.draw(screen)
        self.backgrounds.draw(screen)
        self.level_tiles.draw(screen)
        self.bullets.draw(screen)
        self.particles.draw(screen)
        screen.blit(self.player.image, self.player.rect)

    def vertical_collision_check(self):
        """
        Collision checking for jumping
        """
        in_floor = pygame.sprite.spritecollide(self.player, self.floor_tiles, False)
        in_ceiling = pygame.sprite.spritecollide(self.player, self.ceiling_tiles, False)
        in_shootable_0 = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
        in_shootable_1 = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
        in_drop = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
        in_fall = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
        in_finish = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

        if self.player.gravity_direction == 'Up':

            if in_floor or in_ceiling or in_shootable_0 or in_shootable_1 or in_drop or in_fall or in_finish:

                while pygame.sprite.spritecollideany(self.player, in_floor):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_ceiling):
                    self.player.rect.move_ip(0, 1)
                while pygame.sprite.spritecollideany(self.player, in_shootable_0):
                    self.player.rect.move_ip(0, 1)
                while pygame.sprite.spritecollideany(self.player, in_shootable_1):
                    self.player.rect.move_ip(0, 1)
                while pygame.sprite.spritecollideany(self.player, in_drop):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_fall):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_finish):
                    self.player.rect.move_ip(0, -1)

        elif self.player.gravity_direction == 'Down':

            if in_floor or in_ceiling or in_shootable_0 or in_shootable_1 or in_drop or in_fall or in_finish:

                while pygame.sprite.spritecollideany(self.player, in_floor):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_ceiling):
                    self.player.rect.move_ip(0, 1)
                while pygame.sprite.spritecollideany(self.player, in_shootable_0):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_shootable_1):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_drop):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_fall):
                    self.player.rect.move_ip(0, -1)
                while pygame.sprite.spritecollideany(self.player, in_finish):
                    self.player.rect.move_ip(0, -1)
        else:
            assert False

        if pygame.sprite.spritecollide(self.player, self.lava_tiles, False) and self.player.alive:
            self.die()

        if pygame.sprite.spritecollide(self.player, self.gravity_up_tiles, False):
            self.player.change_gravity_direction('Up')

        elif pygame.sprite.spritecollide(self.player, self.gravity_down_tiles, False):
            self.player.change_gravity_direction('Down')

    def horizontal_collision_check(self):
        """
        Collision detection for scrolling
        """
        floor = pygame.sprite.spritecollide(self.player, self.floor_tiles, False)
        ceiling = pygame.sprite.spritecollide(self.player, self.ceiling_tiles, False)
        shootable_0 = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
        shootable_1 = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
        lava = pygame.sprite.spritecollide(self.player, self.lava_tiles, False)
        drop = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
        fall = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
        finish = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

        if (floor or ceiling or shootable_0 or shootable_1 or lava or drop or fall or finish) and self.player.alive:
            self.die()

    def is_on_floor(self):
        """
        Calculates if player is on the ground and able to jump
        """
        if self.player.gravity_direction == 'Up':

            if self.player.rect.top <= 0:
                self.player_on_floor = True
                return

            group1_curr = pygame.sprite.spritecollide(self.player, self.ceiling_tiles, False)
            group2_curr = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
            group3_curr = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
            group4_curr = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
            group5_curr = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
            group6_curr = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

            self.player.rect.move_ip(0, -1)

            group1_check = pygame.sprite.spritecollide(self.player, self.ceiling_tiles, False)
            group2_check = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
            group3_check = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
            group4_check = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
            group5_check = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
            group6_check = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

            self.player.rect.move_ip(0, 1)

        elif self.player.gravity_direction == 'Down':

            if self.player.rect.bottom >= self.screen_height:
                self.player_on_floor = True
                return

            group1_curr = pygame.sprite.spritecollide(self.player, self.floor_tiles, False)
            group2_curr = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
            group3_curr = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
            group4_curr = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
            group5_curr = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
            group6_curr = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

            self.player.rect.move_ip(0, 1)

            group1_check = pygame.sprite.spritecollide(self.player, self.floor_tiles, False)
            group2_check = pygame.sprite.spritecollide(self.player, self.shootable_0_tiles, False)
            group3_check = pygame.sprite.spritecollide(self.player, self.shootable_1_tiles, False)
            group4_check = pygame.sprite.spritecollide(self.player, self.drop_down_tiles, False)
            group5_check = pygame.sprite.spritecollide(self.player, self.fall_up_tiles, False)
            group6_check = pygame.sprite.spritecollide(self.player, self.finish_tiles, False)

            self.player.rect.move_ip(0, -1)

        else:
            assert False

        bool1 = (group1_curr == [] and group1_check != [])
        bool2 = (group2_curr == [] and group2_check != [])
        bool3 = (group3_curr == [] and group3_check != [])
        bool4 = (group4_curr == [] and group4_check != [])
        bool5 = (group5_curr == [] and group5_check != [])
        bool6 = (group6_curr == [] and group6_check != [])

        if bool1 or bool2 or bool3 or bool4 or bool5:
            self.player_on_floor = True
        elif bool6:
            self.player_on_floor = True
            if not self.finish:
                self.speed = 0
                self.finish = True
                pygame.mixer.music.stop()
                pygame.mixer.Sound.play(WIN_SOUND)
        else:
            self.player_on_floor = False

    def gravity_check(self):
        """
        Gravity control function
        """
        # TODO finish gravity NEEDS ELIFS? MAYBE NOT
        if not self.player_on_floor and not self.player.in_jump:
            self.player.gravity_update()
        elif self.player_on_floor and not self.player.in_jump:
            pass
        elif not self.player_on_floor and self.player.in_jump:
            pass
        else:
            self.player.gravity_reset()

        self.player_bounds_check()

    def reset(self):
        """
        Reset the game to default variables and positions
        """
        pygame.time.set_timer(BLOWUP, 0)
        self.resize(self.mega_grid[0][0].number_of_matrix_rows, self.mega_grid[0][0].number_of_matrix_columns)
        self.scroll_direction = self.mega_grid[0][0].scroll_direction

        if self.scroll_direction == 'Down':
            self.level_pixels_remaining = self.screen_height
            self.draw_distance = self.screen_height
            self.curr_level = self.mega_grid[1][0]
        elif self.scroll_direction == 'Right':
            self.level_pixels_remaining = self.screen_width
            self.draw_distance = self.screen_width
            self.curr_level = self.mega_grid[0][1]
        else:
            assert False

        self.dropping_down = False
        self.falling_up = False
        self.curr_level_column = 0
        self.curr_level_row = 0
        self.player_on_floor = False
        self.speed = STARTING_SPEED
        self.death_calls = BLOWUP_COUNT

        for flr in self.floor_tiles:
            flr.kill()
            del flr

        for ceil in self.ceiling_tiles:
            ceil.kill()
            del ceil

        for lava in self.lava_tiles:
            lava.kill()
            del lava

        for shoot0 in self.shootable_0_tiles:
            shoot0.kill()
            del shoot0

        for shoot1 in self.shootable_1_tiles:
            shoot1.kill()
            del shoot1

        for drop in self.drop_down_tiles:
            drop.kill()
            del drop

        for fall in self.fall_up_tiles:
            fall.kill()
            del fall

        for fin in self.finish_tiles:
            fin.kill()
            del fin

        for drop in self.gravity_up_tiles:
            drop.kill()
            del drop

        for drop in self.gravity_down_tiles:
            drop.kill()
            del drop

        for lev in self.level_tiles:
            lev.kill()
            del lev

        for bul in self.bullets:
            bul.kill()
            del bul

        for bg in self.backgrounds:
            bg.kill()
            del bg

        for star in self.stars:
            star.kill()
            del star

        for part in self.particles:
            part.kill()
            del part

        self.initial_render()
        self.player.player_reset()

    def shoot_bullet(self):
        """
        Creates a bullet to shoot
        """
        if self.player.alive and not self.player.morphing:
            pygame.mixer.Sound.play(SHOOT_SOUND)
            new_bullet = Bullet(self.player.rect.center, self.scroll_direction,
                                self.screen_width, self.screen_height,
                                int(round(self.tile_width / 5)), int(round(self.tile_width / 5)),
                                self.player.bullet_power)
            self.bullets.add(new_bullet)

    def bullet_collision(self):
        """
        Checks for bullets colliding with shootable tiles
        """
        for bullet in self.bullets:

            if bullet.power == 0:
                coll = pygame.sprite.spritecollideany(bullet, self.shootable_0_tiles)

                if coll is not None:
                    bullet.kill()
                    del bullet
                    if not coll.morphing_color:
                        self.blow_up_tile(coll, SHOOTABLE_0_COLOR)
                    continue

                coll = pygame.sprite.spritecollideany(bullet, self.shootable_1_tiles)

                if coll is not None:
                    bullet.kill()
                    del bullet
                    if not coll.morphing_color:
                        pygame.mixer.Sound.play(ABSORB_BULLET_SOUND)
                        coll.morphing_color = True
                        colors = rgb_blender(SHOOTABLE_1_COLOR, ENEMY_BULLET_COLOR, COLOR_BLEND_STEPS)
                        ev = pygame.event.Event(BLEND, {'tile': coll, 'colors': colors})
                        pygame.event.post(ev)

            elif bullet.power == 1:

                coll = pygame.sprite.spritecollideany(bullet, self.shootable_1_tiles)

                if coll is not None:

                    bullet.kill()
                    del bullet
                    if not coll.morphing_color:
                        self.blow_up_tile(coll, SHOOTABLE_1_COLOR)
                    continue

                coll = pygame.sprite.spritecollideany(bullet, self.shootable_0_tiles)

                if coll is not None:
                    bullet.kill()
                    del bullet
                    if not coll.morphing_color:
                        pygame.mixer.Sound.play(ABSORB_BULLET_SOUND)
                        coll.morphing_color = True
                        colors = rgb_blender(SHOOTABLE_0_COLOR, ENEMY_BULLET_COLOR, COLOR_BLEND_STEPS)
                        ev = pygame.event.Event(BLEND, {'tile': coll, 'colors': colors})
                        pygame.event.post(ev)

            elif bullet.power == 2:
                if pygame.sprite.collide_rect(bullet, self.player):
                    self.die()

            else:
                assert False

    def player_bounds_check(self):
        """
        Enforces screen bounds on the player
        """
        if self.player.rect.left < 0:
            self.player.rect.left = 0
        if self.player.rect.right > self.screen_width:
            self.player.rect.right = self.screen_width
        if self.player.rect.top < 0:
            self.player.rect.top = 0
        if self.player.rect.bottom > self.screen_height:
            self.player.rect.bottom = self.screen_height

    def blow_up_tile(self, parent, parent_color):
        """
        Blow up a tile object
        :param parent: (sprite) Parent object which will explode
        :param parent_color: (RGBA) Color of parent object
        """
        pygame.mixer.Sound.play(DESTROY_BLOCK)
        new_tile_width = int(round(parent.tile_width / 2))
        new_tile_height = int(round(parent.tile_height / 2))

        topleft_x = parent.rect.left
        topleft_y = parent.rect.top
        center_x = parent.rect.center[0]
        center_y = parent.rect.center[1]

        parent.kill()
        del parent

        particle1 = Particle(self.screen_width, self.screen_height,
                             new_tile_width, new_tile_height, topleft_x, topleft_y, 'Top Left', parent_color)
        particle2 = Particle(self.screen_width, self.screen_height,
                             new_tile_width, new_tile_height, topleft_x, center_y, 'Bottom Left', parent_color)
        particle3 = Particle(self.screen_width, self.screen_height,
                             new_tile_width, new_tile_height, center_x, topleft_y, 'Top Right', parent_color)
        particle4 = Particle(self.screen_width, self.screen_height,
                             new_tile_width, new_tile_height, center_x, center_y, 'Bottom Right', parent_color)

        self.particles.add(particle1)
        self.particles.add(particle2)
        self.particles.add(particle3)
        self.particles.add(particle4)

    def start_jump(self):
        """
        Start of the jump process
        """
        if self.player_on_floor and self.player.alive:
            pygame.mixer.Sound.play(JUMP_SOUND)
            self.player.in_jump = True

    def jump_continue(self):
        """
        Continuation of the jump process
        """
        if self.player.in_jump:
            self.player.jump_update()

    def end_jump(self):
        """
        End of the jump process
        """
        if self.player.in_jump:
            self.player.jump_reset()

    def die(self):
        """
        Player death function
        """
        pygame.mixer.Sound.play(DEATH_SOUND)
        self.speed = 0
        self.player.kill_player()
        self.blow_up_tile(self.player, self.player.curr_color)
        pygame.time.set_timer(BLOWUP, BLOWUP_TIMER)

    def death(self):
        """
        Death function call to continue blowing up the player
        """
        if self.death_calls > 0:
            for part in self.particles:
                self.blow_up_tile(part, self.player.curr_color)
            self.death_calls -= 1
        else:
            pygame.time.set_timer(BLOWUP, 0)
            pygame.event.post(RESET_EVENT)

    def load_level_from_disk(self):
        """
        Looks on disk for a level and attempts to load it
        :return: Returns a mega grid level object
        """
        filename = generate_filename()
        try:
            return np.load(filename)
        except FileNotFoundError:
            print('No Level')
            # pygame.quit()
            # exit()

    def destroy_down_bridge(self):
        """
        Destroys the down bridge
        """
        for drop in self.drop_down_tiles:

            drop.rect.move_ip(0, BRIDGE_BREAK_RATE)
            if drop.rect.top >= self.screen_height:
                drop.kill()
                del drop
            break

        if len(self.drop_down_tiles) == 0:
            self.dropping_down = False
            self.speed = self.speed_backup
            self.scroll_direction = self.scroll_direction_backup

    def destroy_up_bridge(self):
        """
        Destroys the up bridge
        """
        for fall in self.fall_up_tiles:

            fall.rect.move_ip(0, -BRIDGE_BREAK_RATE)
            if fall.rect.bottom <= 0:
                fall.kill()
                del fall
            break

        if len(self.fall_up_tiles) == 0:
            self.falling_up = False
            self.speed = self.speed_backup
            self.scroll_direction = self.scroll_direction_backup

    def flash_objects(self):
        """
        Flashes the level tiles
        """
        for tile_up in self.gravity_up_tiles:
            tile_up.flash_gravity_tile()

        for tile_down in self.gravity_down_tiles:
            tile_down.flash_gravity_tile()

        for drop in self.drop_down_tiles:
            drop.flash_drop_fall_tile()

        for fall in self.fall_up_tiles:
            fall.flash_drop_fall_tile()

    def get_physics_mode(self):
        """
        Returns rhe type of physics to currently calculate
        :return: (str) Horizontal or Vertical
        """
        if self.scroll_direction == 'Left' or self.scroll_direction == 'Right':
            return 'Horizontal'
        elif self.scroll_direction == 'Up' or self.scroll_direction == 'Down':
            return 'Vertical'
        else:
            assert False

    def shoot_enemy_bullet(self, enemy_tile):
        """
        Fires an enemy bullet from a shootable tile
        :param enemy_tile: (GameTile) Enemy tile which shoots
        """
        pygame.mixer.Sound.play(SHOOT_BACK_SOUND)
        enemy_tile.shoot_bullet()

        if self.scroll_direction == 'Left':
            shoot_direction = 'Right'
        elif self.scroll_direction == 'Right':
            shoot_direction = 'Left'
        elif self.scroll_direction == 'Up':
            shoot_direction = 'Down'
        elif self.scroll_direction == 'Down':
            shoot_direction = 'Up'
        else:
            assert False

        new_bullet = Bullet(enemy_tile.rect.center, shoot_direction,
                            self.screen_width, self.screen_height,
                            int(round(enemy_tile.tile_width / 5)), int(round(enemy_tile.tile_height / 5)), 2)
        self.bullets.add(new_bullet)

    def spawn_initial_stars(self):
        """
        Spawns all stars on the initial screen
        """
        for n in range(NUMBER_OF_GAME_STARS):
            curr_star_size = np.random.randint(STAR_SIZE_LOWER, STAR_SIZE_UPPER)
            x_lower_bound = 0
            x_upper_bound = self.screen_width - curr_star_size
            y_lower_bound = 0
            y_upper_bound = self.screen_height - curr_star_size
            self.create_new_star(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound, curr_star_size)

    def spawn_initial_background(self):
        """
        Spawns all backgrounds on the initial screen
        """
        bg1 = Background(BG1_COLOR, self.screen_width, self.screen_height,
                         BG1_DIMENSIONS, BG1_SPAWN_UP, BG1_SPAWN_DOWN, BG1_SPAWN_LEFT, BG1_SPAWN_RIGHT,
                         speed_multiplier=1, flash_speed=1, starting_direction=self.scroll_direction)

        bg2 = Background(BG2_COLOR, self.screen_width, self.screen_height,
                         BG2_DIMENSIONS, BG2_SPAWN_UP, BG2_SPAWN_DOWN, BG2_SPAWN_LEFT, BG2_SPAWN_RIGHT,
                         speed_multiplier=3, flash_speed=3, starting_direction=self.scroll_direction)

        bg3 = Background(BG3_COLOR, self.screen_width, self.screen_height,
                         BG3_DIMENSIONS, BG3_SPAWN_UP, BG3_SPAWN_DOWN, BG3_SPAWN_LEFT, BG3_SPAWN_RIGHT,
                         speed_multiplier=2, flash_speed=2, starting_direction=self.scroll_direction)

        self.backgrounds.add(bg1)
        self.backgrounds.add(bg2)
        self.backgrounds.add(bg3)

    def calculate_star_parameters(self):
        """
        Calculate all necessary parameters to create a new star
        """
        if len(self.stars) < NUMBER_OF_GAME_STARS:
            curr_star_size = np.random.randint(STAR_SIZE_LOWER, STAR_SIZE_UPPER)

            if self.scroll_direction == 'Up':
                x_lower = 0
                x_upper = self.screen_width
                y_lower = -curr_star_size
                y_upper = -curr_star_size + 1

            elif self.scroll_direction == 'Down':
                x_lower = 0
                x_upper = self.screen_width
                y_lower = self.screen_height
                y_upper = self.screen_height + 1

            elif self.scroll_direction == 'Left':
                x_lower = -curr_star_size
                x_upper = -curr_star_size + 1
                y_lower = 0
                y_upper = self.screen_height - curr_star_size

            elif self.scroll_direction == 'Right':
                x_lower = self.screen_width
                x_upper = self.screen_width + 1
                y_lower = 0
                y_upper = self.screen_height - curr_star_size

            else:
                assert False

            self.create_new_star(x_lower, x_upper, y_lower, y_upper, curr_star_size)

    def create_new_star(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound, curr_star_size):
        """
        Creates a new star object
        :param x_lower_bound: Lower x position bound
        :param x_upper_bound: Upper x position bound
        :param y_lower_bound: Lower y position bound
        :param y_upper_bound: Upper y position bound
        :param curr_star_size: Size of the star to create
        """
        starting_x = np.random.randint(x_lower_bound, x_upper_bound)
        starting_y = np.random.randint(y_lower_bound, y_upper_bound)
        alpha_step = np.random.randint(0, 100)
        color_of_star = np.random.randint(0, 3)
        speed_of_star = np.random.randint(STAR_SCROLL_SPEED_LOWER_BOUND, STAR_SCROLL_SPEED_UPPER_BOUND + 1)

        if len(self.stars) == 0:
            star = Star(self.screen_width, self.screen_height, curr_star_size,
                        starting_x, starting_y, alpha_step, color_of_star, speed_of_star)
            self.stars.add(star)

        else:
            add_star = True
            for s in self.stars:

                bool1 = starting_x < s.rect.right
                bool2 = starting_x > s.rect.left - curr_star_size
                bool3 = starting_y < s.rect.bottom
                bool4 = starting_y > s.rect.top - curr_star_size

                if bool1 and bool2 and bool3 and bool4:
                    add_star = False
                    break

            if add_star:
                star = Star(self.screen_width, self.screen_height, curr_star_size,
                            starting_x, starting_y, alpha_step, color_of_star, speed_of_star)
                self.stars.add(star)
