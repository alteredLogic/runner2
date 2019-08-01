"""
Mini Grid Class
"""
from editortile import *
import pygame.gfxdraw


class MiniGrid:
    """
    Creates a mini grid object for the level editor
    """

    def __init__(self, tile_width, tile_height, top_left_x, top_left_y):
        self.mini_tile_width = int(round((tile_width * 3) / 2))
        self.mini_tile_height = int(round((tile_height * 3) / 2))
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y

        self.mini_tiles = pygame.sprite.Group()
        self.mini_grid = np.zeros((NUMBER_OF_MEGA_GRID_ROWS, NUMBER_OF_MEGA_GRID_COLUMNS), dtype=object)

        for r in range(NUMBER_OF_MEGA_GRID_ROWS):
            for c in range(NUMBER_OF_MEGA_GRID_COLUMNS):
                tile = EditorTile(r, c, self.mini_tile_width, self.mini_tile_height,
                                  self.top_left_x, self.top_left_y, KIND_BACKGROUND, 2)
                self.mini_grid[r][c] = tile
                self.mini_tiles.add(tile)

    def flash_mini_grid_cursor(self, curr_mega_grid):
        """
        Flashes the mini grid cursor
        :param curr_mega_grid: (Level) Active grid within mega grid
        """
        mini_row = curr_mega_grid.mega_row
        mini_column = curr_mega_grid.mega_column
        self.mini_grid[mini_row][mini_column].flash_editor_tile()

    def reset_mini_grid_cursor(self, curr_mega_grid):
        """
        Resets the mini grid cursor alpha
        :param curr_mega_grid: (Level) Active grid within mega grid
        """
        mini_row = curr_mega_grid.mega_row
        mini_column = curr_mega_grid.mega_column
        self.mini_grid[mini_row][mini_column].flash_reset_editor_tile()

    def render_mini_tile(self, curr_level):
        """
        Draws the a mega tile grid onto the corresponding mini tile grid
        :param curr_level:
        """
        if curr_level is None:
            return

        mega_row = curr_level.mega_row
        mega_column = curr_level.mega_column
        matrix_rows = curr_level.number_of_matrix_rows
        matrix_columns = curr_level.number_of_matrix_columns

        curr_mini_grid_tile = self.mini_grid[mega_row][mega_column]
        curr_mini_grid_tile.image = pygame.transform.scale(curr_mini_grid_tile.image, (matrix_columns, matrix_rows))
        curr_mini_grid_tile.image.fill(BACKGROUND_COLOR)

        for grid_row in range(matrix_rows):
            for grid_column in range(matrix_columns):

                kind = curr_level.grid[grid_row][grid_column]

                if kind == KIND_BACKGROUND:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, BACKGROUND_COLOR)
                elif kind == KIND_FLOOR:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, FLOOR_COLOR)
                elif kind == KIND_SHOOTABLE_0:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, SHOOTABLE_0_COLOR)
                elif kind == KIND_SHOOTABLE_1:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, SHOOTABLE_1_COLOR)
                elif kind == KIND_LAVA:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, LAVA_COLOR)
                elif kind == KIND_CEILING:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, CEILING_COLOR)
                elif kind == KIND_FINISH:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, FINISH_COLOR_1)
                elif kind == KIND_DROP_DOWN:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, DROP_DOWN_COLOR)
                elif kind == KIND_FALL_UP:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, FALL_UP_COLOR)
                elif kind == KIND_GRAVITY_UP:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, GRAVITY_UP_COLOR)
                elif kind == KIND_GRAVITY_DOWN:
                    pygame.gfxdraw.pixel(curr_mini_grid_tile.image, grid_column, grid_row, GRAVITY_DOWN_COLOR)
                else:
                    assert False

        curr_mini_grid_tile.image = pygame.transform.scale(curr_mini_grid_tile.image,
                                                           (self.mini_tile_width - EDITOR_GRID_OFFSET,
                                                            self.mini_tile_height - EDITOR_GRID_OFFSET))
