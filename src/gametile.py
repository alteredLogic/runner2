"""
Game Tile Class
"""
from constants import *


class GameTile(pygame.sprite.Sprite):
    """
    Creates a game tile object with which the player interacts
    """
    def __init__(self, tile_width, tile_height, top_left_x, top_left_y, tile_color, kind):
        super(GameTile, self).__init__()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.kind = kind

        if (self.kind == 'Gravity Up' or self.kind == 'Gravity Down' or
                self.kind == 'Drop Down' or self.kind == 'Fall Up'):
            self.image = pygame.Surface((self.tile_width, self.tile_height), pygame.SRCALPHA)
            self.pts = []
        else:
            self.image = pygame.Surface((self.tile_width, self.tile_height))

        self.rect = self.image.get_rect(topleft=(top_left_x, top_left_y))
        self.tile_color = tile_color
        self.image.fill(self.tile_color)
        self.image.set_alpha(255)
        self.alpha_counter = 0
        self.color_counter = 0
        self.morphing_color = False

        if self.kind == 'Finish':
            half_width = int(round(self.tile_width / 2))
            half_height = int(round(self.tile_height / 2))
            pygame.draw.rect(self.image, FINISH_COLOR_2, (0, 0, half_width, half_height))
            pygame.draw.rect(self.image, FINISH_COLOR_2, (half_width, half_height, self.tile_width, self.tile_height))

        elif self.kind == 'Gravity Up':
            self.pts.append((0, self.tile_height))
            self.pts.append((self.tile_width, self.tile_height))
            self.pts.append((int(round(self.tile_width / 2)), 0))
            self.alpha_counter = np.random.randint(0, 100)
            self.flash_gravity_tile()

        elif self.kind == 'Gravity Down':
            self.pts.append((0, 0))
            self.pts.append((self.tile_width, 0))
            self.pts.append((int(round(self.tile_width / 2)), self.tile_height))
            self.alpha_counter = np.random.randint(0, 100)
            self.flash_gravity_tile()

        elif self.kind == 'Drop Down' or self.kind == 'Fall Up':
            center_x = int(round(tile_width / 2))
            center_y = int(round(tile_height / 2))
            self.circle_center_pos = (center_x, center_y)
            if self.tile_width <= self.tile_height:
                self.radius = center_x
            else:
                self.radius = center_y
            pygame.draw.circle(self.image, (0, 0, 0, 0), self.circle_center_pos, self.radius)

    def flash_gravity_tile(self):
        """
        Update gravity tile alpha
        """
        new_alpha = int(round(128 + 127 * np.sin(self.alpha_counter / 15)))
        new_color = (GRAVITY_ARROW_COLOR[0], GRAVITY_ARROW_COLOR[1], GRAVITY_ARROW_COLOR[2], new_alpha)
        pygame.draw.polygon(self.image, new_color, self.pts)
        self.alpha_counter += 0.3

    def flash_drop_fall_tile(self):
        """
        Update the drop/fall tile alpha
        """
        new_alpha = int(round(128 + 127 * np.sin(self.alpha_counter / 15)))
        new_color = (SNOW[0], SNOW[1], SNOW[2], new_alpha)
        pygame.draw.circle(self.image, new_color, self.circle_center_pos, self.radius)
        self.alpha_counter += 0.5

    def absorb_bullet(self, colors):
        """
        Enemy tile absorbs a bullet
        :param colors: (rgba) Color to switch enemy tile to
        """
        self.image.fill(colors[self.color_counter])
        self.color_counter += 1

    def shoot_bullet(self):
        """
        Enemy tile shoots a bullet
        """
        self.morphing_color = False
        self.color_counter = 0
        self.image.fill(self.tile_color)
