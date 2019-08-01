"""
Editor Tile Class
"""
from constants import *


class EditorTile(pygame.sprite.Sprite):
    """
    Creates a tile object for the level editor
    """
    def __init__(self, row, column, tile_width, tile_height, offset_x, offset_y, kind, alpha_multiplier):
        super(EditorTile, self).__init__()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.row = row
        self.column = column
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.image = pygame.Surface((self.tile_width - EDITOR_GRID_OFFSET, self.tile_height - EDITOR_GRID_OFFSET))
        self.rect = self.image.get_rect(topleft=((self.column * self.tile_width) + self.offset_x,
                                                 (self.row * self.tile_height) + self.offset_y))
        self.alpha_counter = 0
        self.kind = kind
        self.change_color(self.kind)
        self.alpha_multiplier = alpha_multiplier

    def resize(self, tile_width, tile_height):
        """
        Resize the tile object
        :param tile_width: (int) New tile width
        :param tile_height: (int) New tile height
        """
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.image = pygame.transform.scale(self.image,
                                            (self.tile_width - EDITOR_GRID_OFFSET,
                                             self.tile_height - EDITOR_GRID_OFFSET))
        self.rect = self.image.get_rect(topleft=(self.column * tile_width, self.row * tile_height))

    def flash_editor_tile(self):
        """
        Update current tile alpha
        """
        self.image.set_alpha(int(128 + 128 * np.sin(self.alpha_counter / 35)))
        self.alpha_counter += self.alpha_multiplier

    def flash_reset_editor_tile(self):
        """
        Reset current tile alpha
        """
        self.image.set_alpha(255)
        self.alpha_counter = 0

    def change_color(self, kind):
        """
        Set current tile color
        :param kind: (int) The new color to change into
        """
        self.kind = kind
        pts = []

        if self.kind == KIND_BACKGROUND:
            self.image.fill(BACKGROUND_COLOR)

        elif self.kind == KIND_FLOOR:
            self.image.fill(FLOOR_COLOR)

        elif self.kind == KIND_SHOOTABLE_0:
            self.image.fill(SHOOTABLE_0_COLOR)

        elif self.kind == KIND_SHOOTABLE_1:
            self.image.fill(SHOOTABLE_1_COLOR)

        elif self.kind == KIND_LAVA:
            self.image.fill(LAVA_COLOR)

        elif self.kind == KIND_CEILING:
            self.image.fill(CEILING_COLOR)

        elif self.kind == KIND_FINISH:
            self.image.fill(FINISH_COLOR_1)
            half_width = round(self.tile_width / 2)
            half_height = round(self.tile_height / 2)
            pygame.draw.rect(self.image, FINISH_COLOR_2,
                             (0, 0, half_width, half_height))
            pygame.draw.rect(self.image, FINISH_COLOR_2,
                             (half_width, half_height,
                              self.tile_width - EDITOR_GRID_OFFSET, self.tile_height - EDITOR_GRID_OFFSET))

        elif self.kind == KIND_DROP_DOWN:
            self.image.fill(DROP_DOWN_COLOR)
            center_x = int(round(self.tile_width / 2))
            center_y = int(round(self.tile_height / 2))
            circle_center_pos = (center_x, center_y)
            if self.tile_width <= self.tile_height:
                radius = center_x
            else:
                radius = center_y
            pygame.draw.circle(self.image, DROP_FALL_CIRCLE_COLOR, circle_center_pos, radius)

        elif self.kind == KIND_FALL_UP:
            self.image.fill(FALL_UP_COLOR)
            center_x = int(round(self.tile_width / 2))
            center_y = int(round(self.tile_height / 2))
            circle_center_pos = (center_x, center_y)
            if self.tile_width <= self.tile_height:
                radius = center_x
            else:
                radius = center_y
            pygame.draw.circle(self.image, DROP_FALL_CIRCLE_COLOR, circle_center_pos, radius)

        elif self.kind == KIND_GRAVITY_UP:
            self.image.fill(GRAVITY_UP_COLOR)
            pts.append((0, self.tile_height - EDITOR_GRID_OFFSET))
            pts.append((self.tile_width - EDITOR_GRID_OFFSET, self.tile_height - EDITOR_GRID_OFFSET))
            pts.append((int(round((self.tile_width - EDITOR_GRID_OFFSET) / 2)), 0))
            pygame.draw.polygon(self.image, GRAVITY_ARROW_COLOR, pts)

        elif self.kind == KIND_GRAVITY_DOWN:
            self.image.fill(GRAVITY_DOWN_COLOR)
            pts.append((0, 0))
            pts.append((self.tile_width - EDITOR_GRID_OFFSET, 0))
            pts.append((int(round((self.tile_width - EDITOR_GRID_OFFSET) / 2)), self.tile_height - EDITOR_GRID_OFFSET))
            pygame.draw.polygon(self.image, GRAVITY_ARROW_COLOR, pts)
