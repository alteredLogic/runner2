"""
Triangle Class
"""
from constants import *


class Triangle(pygame.sprite.Sprite):
    """
    Creates a directional triangle object for the level editor
    """
    alpha_counter = 0

    def __init__(self, screen_width, screen_height, position):
        super(Triangle, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pts = []
        self.arrow_color = RED

        if position == 'Top':
            self.tri_width = int(round(self.screen_width / 8))
            self.tri_height = int(round(self.screen_height / 16))
            center_x = int(round(self.screen_width / 2))
            center_y = int(round(self.screen_height / 8))

            self.pts.append((0, self.tri_height))
            self.pts.append((self.tri_width, self.tri_height))
            self.pts.append((int(round(self.tri_width / 2)), 0))

        elif position == 'Bottom':
            self.tri_width = int(round(self.screen_width / 8))
            self.tri_height = int(round(self.screen_height / 16))
            center_x = int(round(self.screen_width / 2))
            center_y = int(round(self.screen_height * 7 / 8))

            self.pts.append((0, 0))
            self.pts.append((self.tri_width, 0))
            self.pts.append((int(round(self.tri_width / 2)), self.tri_height))

        elif position == 'Left':
            self.tri_width = int(round(self.screen_height / 16))
            self.tri_height = int(round(self.screen_width / 8))
            center_x = int(round(self.screen_width / 8))
            center_y = int(round(self.screen_height / 2))

            self.pts.append((self.tri_width, 0))
            self.pts.append((self.tri_width, self.tri_height))
            self.pts.append((0, int(round(self.tri_height / 2))))

        elif position == 'Right':
            self.tri_width = int(round(self.screen_height / 16))
            self.tri_height = int(round(self.screen_width / 8))
            center_x = int(round(self.screen_width * 7 / 8))
            center_y = int(round(self.screen_height / 2))

            self.pts.append((0, 0))
            self.pts.append((0, self.tri_height))
            self.pts.append((self.tri_width, int(round(self.tri_height / 2))))
        else:
            assert False

        self.image = pygame.Surface((self.tri_width, self.tri_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        pygame.draw.polygon(self.image, self.arrow_color, self.pts)

    def resize(self, tile_width, tile_height):
        """
        Resize the triangle object
        :param tile_width: (int) New triangle width
        :param tile_height: (int) New triangle height
        """
        pass

    def flash_editor_arrow(self):
        """
        Update current tile alpha
        """
        new_alpha = int(round(128 + 127 * np.sin(self.alpha_counter / 15)))
        new_color = (self.arrow_color[0], self.arrow_color[1], self.arrow_color[2], new_alpha)
        pygame.draw.polygon(self.image, new_color, self.pts)

    def editor_arrow_flash_reset(self):
        """
        Reset current tile alpha
        """
        pygame.draw.polygon(self.image, self.arrow_color, self.pts)
