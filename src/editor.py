"""
Editor Class
"""
from level import *
from triangle import *
from mini_grid import *


class Editor:
    """
    Creates a level editor object
    """
    def __init__(self, screen_width, screen_height, matrix_rows, matrix_columns):
        self.curr_kind = KIND_FLOOR
        self.cursor_mode = EDITOR_CURSOR_BOX

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.number_of_matrix_rows = matrix_rows
        self.number_of_matrix_columns = matrix_columns

        self.grid_width = int(round((self.screen_width * 2) / 3))
        self.grid_height = self.screen_height

        self.tile_width = int(round(self.grid_width / self.number_of_matrix_columns))
        self.tile_height = int(round(self.grid_height / self.number_of_matrix_rows))

        self.tiles = pygame.sprite.Group()
        self.tile_grid = np.zeros((self.number_of_matrix_rows, self.number_of_matrix_columns), dtype=object)

        self.mega_grid = np.zeros((NUMBER_OF_MEGA_GRID_COLUMNS, NUMBER_OF_MEGA_GRID_ROWS), dtype=object)
        for r in range(NUMBER_OF_MEGA_GRID_ROWS):
            for c in range(NUMBER_OF_MEGA_GRID_COLUMNS):
                self.mega_grid[r][c] = None

        self.build_grid()

        self.icon_tile = EditorTile(3, 37, 25, 25, 10, 17, KIND_FLOOR, 1)

        self.curr_tile = self.tile_grid[0][0]
        self.curr_tile_box = self.curr_tile
        self.curr_mega_grid = self.spawn_level_on_mega_grid(0, 0, 0, 0)

        self.mini_grid = MiniGrid(self.tile_width, self.tile_height,
                                  self.grid_width + MINI_GRID_X_OFFSET, MINI_GRID_Y_OFFSET)

        self.bg = pygame.Surface((self.grid_width, self.grid_height))
        self.bg.fill(FLOOR_COLOR)

        self.status = pygame.Surface((self.screen_width - self.grid_width, self.screen_height))
        self.status.fill(EDITOR_STATUS_COLOR)

        self.res = 1
        self.font = pygame.font.Font('./fonts/verdana.ttf', 20)

        self.txt_grid_rows = self.font.render('Grid Rows: ' + str(self.number_of_matrix_rows),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_grid_columns = self.font.render('Grid Columns: ' + str(self.number_of_matrix_columns),
                                                 True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_direction = self.font.render('Direction: ' + str(self.curr_mega_grid.scroll_direction),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_tile_kind = self.font.render('Tile Type: ' + str(self.curr_kind),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

        self.tris = pygame.sprite.Group()
        self.tri_top = Triangle(self.grid_width, self.grid_height, 'Top')
        self.tri_bottom = Triangle(self.grid_width, self.grid_height, 'Bottom')
        self.tri_left = Triangle(self.grid_width, self.grid_height, 'Left')
        self.tri_right = Triangle(self.grid_width, self.grid_height, 'Right')

    def resize_editor_grid(self, matrix_rows, matrix_columns, scroll_direction):
        """
        Resize the currently active grid
        :param matrix_rows: (int) New number of matrix rows
        :param matrix_columns: (int) New number of matrix columns
        :param scroll_direction: Scroll direction of the currently active grid
        """
        self.screen_width = 1200
        self.screen_height = 600
        self.number_of_matrix_rows = matrix_rows
        self.number_of_matrix_columns = matrix_columns

        self.grid_width = int(round((self.screen_width * 2) / 3))
        self.grid_height = self.screen_height
        self.tile_width = int(round(self.grid_width / self.number_of_matrix_columns))
        self.tile_height = int(round(self.grid_height / self.number_of_matrix_rows))

        self.curr_mega_grid.resize_level_grid(self.number_of_matrix_rows, self.number_of_matrix_columns)
        self.txt_grid_rows = self.font.render('Grid Rows: ' + str(self.number_of_matrix_rows),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_grid_columns = self.font.render('Grid Columns: ' + str(self.number_of_matrix_columns),
                                                 True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

        self.bg = pygame.transform.scale(self.bg, (self.screen_width, self.screen_height))

        self.tiles.empty()
        self.tile_grid = np.zeros((self.number_of_matrix_rows, self.number_of_matrix_columns), dtype=object)

        self.build_grid()
        self.curr_tile = self.tile_grid[self.curr_mega_grid.curr_grid_row][self.curr_mega_grid.curr_grid_column]
        self.curr_tile_box = self.curr_tile
        self.draw_colors_onto_current_grid()

        self.txt_grid_rows = self.font.render('Grid Rows: ' + str(matrix_rows),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_grid_columns = self.font.render('Grid Columns: ' + str(matrix_columns),
                                                 True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)
        self.txt_direction = self.font.render('Direction: ' + str(scroll_direction),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

    def resize_help(self):
        """
        Resizing helper function
        """
        if self.res < 2:
            self.res += 1
        else:
            self.res = 0

        self.resize_editor_grid(RES[self.res][2], RES[self.res][3], self.curr_mega_grid.scroll_direction)
        self.mini_grid.render_mini_tile(self.curr_mega_grid)

    def build_grid(self):
        """
        Builds the tile grid
        """
        for r in range(self.number_of_matrix_rows):
            for c in range(self.number_of_matrix_columns):
                tile = EditorTile(r, c, self.tile_width, self.tile_height, 0, 0, KIND_BACKGROUND, 1)
                self.tile_grid[r][c] = tile
                self.tiles.add(tile)

    def draw_colors_onto_current_grid(self):
        """
        Colors in an individual grid
        """
        matrix_rows = self.curr_mega_grid.number_of_matrix_rows
        matrix_columns = self.curr_mega_grid.number_of_matrix_columns

        curr_grid = self.curr_mega_grid.grid
        for r in range(matrix_rows):
            for c in range(matrix_columns):
                self.tile_grid[r][c].change_color(curr_grid[r][c])

    def increment_kind(self):
        """
        Increment tile kind
        """
        if self.curr_kind < KIND_GRAVITY_DOWN:
            self.curr_kind += 1
        else:
            self.curr_kind = KIND_FLOOR

        self.txt_tile_kind = self.font.render('Tile Type: ' + str(self.curr_kind),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

        if self.curr_kind == KIND_FLOOR:
            self.bg.fill(FLOOR_COLOR)
        elif self.curr_kind == KIND_SHOOTABLE_0:
            self.bg.fill(SHOOTABLE_0_COLOR)
        elif self.curr_kind == KIND_SHOOTABLE_1:
            self.bg.fill(SHOOTABLE_1_COLOR)
        elif self.curr_kind == KIND_LAVA:
            self.bg.fill(LAVA_COLOR)
        elif self.curr_kind == KIND_CEILING:
            self.bg.fill(CEILING_COLOR)
        elif self.curr_kind == KIND_FINISH:
            self.bg.fill(FINISH_COLOR_1)
        elif self.curr_kind == KIND_DROP_DOWN:
            self.bg.fill(DROP_DOWN_COLOR)
        elif self.curr_kind == KIND_FALL_UP:
            self.bg.fill(FALL_UP_COLOR)
        elif self.curr_kind == KIND_GRAVITY_UP:
            self.bg.fill(GRAVITY_UP_COLOR)
        elif self.curr_kind == KIND_GRAVITY_DOWN:
            self.bg.fill(GRAVITY_DOWN_COLOR)

        self.icon_tile.change_color(self.curr_kind)

    def decrement_kind(self):
        """
        Decrement tile kind
        """
        if self.curr_kind > KIND_FLOOR:
            self.curr_kind -= 1
        else:
            self.curr_kind = KIND_GRAVITY_DOWN

        self.txt_tile_kind = self.font.render('Tile Type: ' + str(self.curr_kind),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

        if self.curr_kind == KIND_FLOOR:
            self.bg.fill(FLOOR_COLOR)
        elif self.curr_kind == KIND_SHOOTABLE_0:
            self.bg.fill(SHOOTABLE_0_COLOR)
        elif self.curr_kind == KIND_SHOOTABLE_1:
            self.bg.fill(SHOOTABLE_1_COLOR)
        elif self.curr_kind == KIND_LAVA:
            self.bg.fill(LAVA_COLOR)
        elif self.curr_kind == KIND_CEILING:
            self.bg.fill(CEILING_COLOR)
        elif self.curr_kind == KIND_FINISH:
            self.bg.fill(FINISH_COLOR_1)
        elif self.curr_kind == KIND_DROP_DOWN:
            self.bg.fill(DROP_DOWN_COLOR)
        elif self.curr_kind == KIND_FALL_UP:
            self.bg.fill(FALL_UP_COLOR)
        elif self.curr_kind == KIND_GRAVITY_UP:
            self.bg.fill(GRAVITY_UP_COLOR)
        elif self.curr_kind == KIND_GRAVITY_DOWN:
            self.bg.fill(GRAVITY_DOWN_COLOR)

    def switch_cursor_mode(self):
        """
        Switch cursor mode
        """
        self.reset_cursor()

        if self.cursor_mode < EDITOR_CURSOR_COLUMN:
            self.cursor_mode += 1
        else:
            self.cursor_mode = EDITOR_CURSOR_BOX

        self.curr_tile_box = self.curr_tile

    def flash_editor_cursors(self):
        """
        Draws the blinking cursor
        """
        if self.cursor_mode == EDITOR_CURSOR_BOX:
            ranges = self.compute_box_ranges()
            for r in ranges[0]:
                for c in ranges[1]:
                    self.tile_grid[r][c].flash_editor_tile()

        elif self.cursor_mode == EDITOR_CURSOR_ROW:
            for c in range(self.number_of_matrix_columns):
                self.tile_grid[self.curr_tile.row][c].flash_editor_tile()

        elif self.cursor_mode == EDITOR_CURSOR_COLUMN:
            for r in range(self.number_of_matrix_rows):
                self.tile_grid[r][self.curr_tile.column].flash_editor_tile()

        self.mini_grid.flash_mini_grid_cursor(self.curr_mega_grid)

    def reset_cursor(self):
        """
        Resets the cursor alpha
        """
        if self.cursor_mode == EDITOR_CURSOR_BOX:
            ranges = self.compute_box_ranges()
            for r in ranges[0]:
                for c in ranges[1]:
                    self.tile_grid[r][c].flash_reset_editor_tile()

        elif self.cursor_mode == EDITOR_CURSOR_ROW:
            for c in range(self.number_of_matrix_columns):
                self.tile_grid[self.curr_tile.row][c].flash_reset_editor_tile()

        elif self.cursor_mode == EDITOR_CURSOR_COLUMN:
            for r in range(self.number_of_matrix_rows):
                self.tile_grid[r][self.curr_tile.column].flash_reset_editor_tile()

    def load_from_disk(self):
        """
        Load level into editor from HDD
        """
        filename = generate_filename()
        try:
            level = np.load(filename)
            self.mini_grid.reset_mini_grid_cursor(self.curr_mega_grid)
            self.mega_grid = level
            self.curr_mega_grid = self.mega_grid[0][0]
            self.resize_editor_grid(self.curr_mega_grid.number_of_matrix_rows,
                                    self.curr_mega_grid.number_of_matrix_columns,
                                    self.curr_mega_grid.scroll_direction)

            for mega_row in range(NUMBER_OF_MEGA_GRID_ROWS):
                for mega_column in range(NUMBER_OF_MEGA_GRID_COLUMNS):
                        curr_grid = self.mega_grid[mega_row][mega_column]
                        self.mini_grid.render_mini_tile(curr_grid)

        except FileNotFoundError:
            print('File not found.')

    def save_to_disk(self):
        """
        Save current editing level to HDD
        """
        filename = generate_filename()
        np.save(filename, self.mega_grid)

    def render_screen(self):
        """
        Renders the screen
        """
        screen = pygame.display.get_surface()

        # Main grid
        screen.blit(self.bg, (0, 0))
        self.tiles.draw(screen)
        self.tris.draw(screen)

        # Status screen
        screen.blit(self.status, (self.grid_width, 0))
        self.mini_grid.mini_tiles.draw(screen)
        screen.blit(self.txt_grid_rows, (self.grid_width, 0))
        screen.blit(self.txt_grid_columns, (self.grid_width, 30))
        screen.blit(self.txt_direction, (self.grid_width, 60))
        screen.blit(self.txt_tile_kind, (self.grid_width, 90))
        screen.blit(self.icon_tile.image, self.icon_tile.rect)

    def set_tile(self, new_kind):
        """
        Sets the selected tile(s) to a new value
        :param new_kind: (int) The new value to set
        """
        if new_kind == BACKGROUND_COLOR:
            pygame.mixer.Sound.play(DELETE_CURSOR_SOUND)
        else:
            pygame.mixer.Sound.play(SELECT_CURSOR_SOUND)

        mega_row = self.curr_mega_grid.mega_row
        mega_column = self.curr_mega_grid.mega_column
        curr_grid = self.mega_grid[mega_row][mega_column].grid

        if self.cursor_mode == EDITOR_CURSOR_BOX:
            ranges = self.compute_box_ranges()
            for r in ranges[0]:
                for c in ranges[1]:
                    curr_grid[r][c] = new_kind
                    self.tile_grid[r][c].change_color(new_kind)

        elif self.cursor_mode == EDITOR_CURSOR_ROW:
            for c in range(self.number_of_matrix_columns):
                curr_grid[self.curr_tile.row][c] = new_kind
                self.tile_grid[self.curr_tile.row][c].change_color(new_kind)

        elif self.cursor_mode == EDITOR_CURSOR_COLUMN:
            for r in range(self.number_of_matrix_rows):
                curr_grid[r][self.curr_tile.column] = new_kind
                self.tile_grid[r][self.curr_tile.column].change_color(new_kind)

        self.mini_grid.render_mini_tile(self.curr_mega_grid)

    def compute_box_ranges(self):
        """
        Computes the ranges within the editor box cursor
        :return: (range, range) Ranges to iterate over the current box cursor
        """
        starting_grid_row = self.curr_tile.row
        starting_grid_column = self.curr_tile.column

        ending_grid_row = self.curr_tile_box.row
        ending_grid_column = self.curr_tile_box.column

        if starting_grid_row <= ending_grid_row:
            row_range = range(starting_grid_row, ending_grid_row + 1, 1)
        else:
            row_range = range(starting_grid_row, ending_grid_row - 1, -1)

        if starting_grid_column <= ending_grid_column:
            column_range = range(starting_grid_column, ending_grid_column + 1, 1)
        else:
            column_range = range(starting_grid_column, ending_grid_column - 1, -1)

        return row_range, column_range

    def change_box_cursor_size(self, direction):
        """
        Alter the size of the box cursor
        :param direction: (str) Direction to alter the box cursor dimensions
        """
        self.reset_cursor()

        grid_row = self.curr_tile_box.row
        grid_column = self.curr_tile_box.column

        if direction == 'Up':
            if grid_row > 0:
                self.curr_tile_box = self.tile_grid[grid_row - 1][grid_column]
        elif direction == 'Down':
            if grid_row < (self.number_of_matrix_rows - 1):
                self.curr_tile_box = self.tile_grid[grid_row + 1][grid_column]
        elif direction == 'Left':
            if grid_column > 0:
                self.curr_tile_box = self.tile_grid[grid_row][grid_column - 1]
        elif direction == 'Right':
            if grid_column < (self.number_of_matrix_columns - 1):
                self.curr_tile_box = self.tile_grid[grid_row][grid_column + 1]
        else:
            assert False

    # TODO stop row from flashing when moving horizontally
    def move_cursor(self, move_direction):
        """
        Move the cursor and update the current tile variable
        :param move_direction: (str) The direction to attempt the move
        """
        self.reset_cursor()

        row = self.curr_tile.row
        column = self.curr_tile.column
        box_row = self.curr_tile_box.row
        box_column = self.curr_tile_box.column

        if move_direction == 'Up':
            if self.cursor_mode == EDITOR_CURSOR_BOX:
                if row > 0 and box_row > 0:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row - 1][column]
                    self.curr_mega_grid.curr_grid_row -= 1
                    self.curr_tile_box = self.tile_grid[box_row - 1][box_column]
            else:
                if row > 0:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row - 1][column]
                    self.curr_mega_grid.curr_grid_row -= 1
                else:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[self.number_of_matrix_rows - 1][self.curr_tile.column]
                    self.curr_mega_grid.curr_grid_row = self.number_of_matrix_rows - 1

        elif move_direction == 'Down':
            if self.cursor_mode == EDITOR_CURSOR_BOX:
                if (row < (self.number_of_matrix_rows - 1)) and (box_row < (self.number_of_matrix_rows - 1)):
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row + 1][column]
                    self.curr_mega_grid.curr_grid_row += 1
                    self.curr_tile_box = self.tile_grid[box_row + 1][box_column]
            else:
                if row < (self.number_of_matrix_rows - 1):
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row + 1][column]
                    self.curr_mega_grid.curr_grid_row += 1
                else:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[0][self.curr_tile.column]
                    self.curr_mega_grid.curr_grid_row = 0

        elif move_direction == 'Left':
            if self.cursor_mode == EDITOR_CURSOR_BOX:
                if column > 0 and box_column > 0:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][column - 1]
                    self.curr_mega_grid.curr_grid_column -= 1
                    self.curr_tile_box = self.tile_grid[box_row][box_column - 1]
            else:
                if column > 0:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][column - 1]
                    self.curr_mega_grid.curr_grid_column -= 1
                else:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][self.number_of_matrix_columns - 1]
                    self.curr_mega_grid.curr_grid_column = self.number_of_matrix_columns - 1

        elif move_direction == 'Right':
            if self.cursor_mode == EDITOR_CURSOR_BOX:
                if (column < (self.number_of_matrix_columns - 1)) and (
                        box_column < (self.number_of_matrix_columns - 1)):
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][column + 1]
                    self.curr_mega_grid.curr_grid_column += 1
                    self.curr_tile_box = self.tile_grid[box_row][box_column + 1]
            else:
                if column < (self.number_of_matrix_columns - 1):
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][column + 1]
                    self.curr_mega_grid.curr_grid_column += 1
                else:
                    pygame.mixer.Sound.play(MOVE_CURSOR_SOUND)
                    self.curr_tile = self.tile_grid[row][0]
                    self.curr_mega_grid.curr_grid_column = 0

        else:
            assert False

    def set_scroll_direction(self, scroll_direction):
        """
        Sets the scrolling direction for the current grid
        :param scroll_direction: (str) Set the scrolling direction of the current grid
        """
        self.curr_mega_grid.scroll_direction = scroll_direction
        self.txt_direction = self.font.render('Direction: ' + str(self.curr_mega_grid.scroll_direction),
                                              True, EDITOR_TEXT_COLOR, EDITOR_TEXT_BACKGROUND_COLOR)

    def set_scroll_arrows(self, new_color):
        """
        Controls the scrolling arrows
        """
        mega_row = self.curr_mega_grid.mega_row
        mega_column = self.curr_mega_grid.mega_column

        if new_color == GREEN or (mega_row > 0 and new_color == RED):
            self.tris.add(self.tri_top)
        else:
            self.tri_top.kill()

        if new_color == GREEN or (mega_row < NUMBER_OF_MEGA_GRID_ROWS - 1 and new_color == RED):
            self.tris.add(self.tri_bottom)
        else:
            self.tri_bottom.kill()

        if new_color == GREEN or (mega_column > 0 and new_color == RED):
            self.tris.add(self.tri_left)
        else:
            self.tri_left.kill()

        if new_color == GREEN or (mega_column < NUMBER_OF_MEGA_GRID_COLUMNS - 1 and new_color == RED):
            self.tris.add(self.tri_right)
        else:
            self.tri_right.kill()

        for tri in self.tris:
            tri.arrow_color = new_color

    def flash_arrows(self):
        """
        Flash the scrolling triangles
        """
        Triangle.alpha_counter += 1
        for tri in self.tris:
            tri.flash_editor_arrow()

    def clear_scroll_arrows(self):
        """
        Resets the scrolling triangles
        """
        Triangle.alpha_counter = 0
        self.tris.empty()

    def move_mega_grid(self, move_direction):
        """
        Controls scrolling the mega grid
        :param move_direction: (str) The direction to attempt to move the mega grid
        """
        mega_row = self.curr_mega_grid.mega_row
        mega_column = self.curr_mega_grid.mega_column

        if move_direction == 'Up':
            if mega_row > 0:
                self.move_mega_grid_helper(mega_row - 1, mega_column)

        elif move_direction == 'Down':
            if mega_row < NUMBER_OF_MEGA_GRID_ROWS - 1:
                self.move_mega_grid_helper(mega_row + 1, mega_column)

        elif move_direction == 'Left':
            if mega_column > 0:
                self.move_mega_grid_helper(mega_row, mega_column - 1)

        elif move_direction == 'Right':
            if mega_column < NUMBER_OF_MEGA_GRID_COLUMNS - 1:
                self.move_mega_grid_helper(mega_row, mega_column + 1)

        else:
            assert False

    def move_mega_grid_helper(self, mega_row, mega_column):
        """
        Helper function for moving the mega grid
        :param mega_row: (int) New mega grid row
        :param mega_column: (int) New mega grid column
        """

        old_grid_row = self.curr_mega_grid.curr_grid_row
        old_grid_column = self.curr_mega_grid.curr_grid_column

        self.mini_grid.reset_mini_grid_cursor(self.curr_mega_grid)
        self.curr_mega_grid = self.mega_grid[mega_row][mega_column]
        if self.curr_mega_grid is None:
            self.curr_mega_grid = self.spawn_level_on_mega_grid(mega_row, mega_column, old_grid_row, old_grid_column)

        matrix_rows = self.curr_mega_grid.number_of_matrix_rows
        matrix_columns = self.curr_mega_grid.number_of_matrix_columns
        scroll_direction = self.curr_mega_grid.scroll_direction

        self.res = RES_LOOKUP[matrix_rows, matrix_columns]
        self.resize_editor_grid(matrix_rows, matrix_columns, scroll_direction)
        self.set_scroll_arrows(RED)

    def spawn_level_on_mega_grid(self, mega_row, mega_column, starting_grid_row, starting_grid_column):
        """
        Create a new level on the mega grid
        :param mega_row: (int) Mega grid row
        :param mega_column: (int) Mega grid column
        :param starting_grid_column: (int) Starting grid column for the new grid
        :param starting_grid_row: int) Starting grid row for the new grid
        :return: Reference to the Level object
        """
        new_level = Level(self.number_of_matrix_rows, self.number_of_matrix_columns,
                          mega_row, mega_column, starting_grid_row, starting_grid_column)
        self.mega_grid[mega_row][mega_column] = new_level
        return self.mega_grid[mega_row][mega_column]
