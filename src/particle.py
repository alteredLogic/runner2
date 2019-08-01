"""
Particle Class
"""
from constants import *


class Particle(pygame.sprite.Sprite):
    """
    Creates a particle object used during the death animation
    """
    def __init__(self, screen_width, screen_height, tile_width, tile_height,
                 starting_x, starting_y, corner, parent_color):
        super(Particle, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.image = pygame.Surface((self.tile_width, self.tile_height))
        self.image.fill(parent_color)
        self.rect = self.image.get_rect(topleft=(self.starting_x, self.starting_y))
        self.corner = corner
        self.x_count = 1
        self.y_count = 0

        self.rng1 = np.random.randint(2, 5)
        self.rng2 = np.random.randint(2, 5)
        self.rng3 = np.random.randint(1, 3)
        self.rng4 = np.random.randint(1, 3)

    def update(self):
        """
        Update death particles
        """
        if self.y_count > 0:
            if PARTICLE_SPEED <= self.y_count:
                self.rect.move_ip(0, -PARTICLE_SPEED)
                self.y_count -= PARTICLE_SPEED
            else:
                self.rect.move_ip(0, -self.y_count)
                self.y_count = 0

        elif self.y_count < 0:
            if PARTICLE_SPEED <= abs(self.y_count):
                self.rect.move_ip(0, PARTICLE_SPEED)
                self.y_count += PARTICLE_SPEED
            else:
                self.rect.move_ip(0, self.y_count)
                self.y_count = 0

        else:
            if self.corner == 'Top Right' or self.corner == 'Bottom Right':
                self.rect.move_ip(1, 0)

            elif self.corner == 'Top Left' or self.corner == 'Bottom Left':
                self.rect.move_ip(-1, 0)

            else:
                assert False

            # Math to model the particle arcs
            if self.corner == 'Bottom Left' or self.corner == 'Bottom Right':
                old_y = int(round((((2 * D_P_M) ** 2) - ((self.x_count - 1) - (2 * D_P_M)) ** 2) / (self.rng1 * D_P_M)))
                new_y = int(round((((2 * D_P_M) ** 2) - (self.x_count - (2 * D_P_M)) ** 2) / (self.rng2 * D_P_M)))

            elif self.corner == 'Top Left' or self.corner == 'Top Right':
                old_y = int(round(((D_P_M * 2) - ((self.x_count - 1) - D_P_M) ** 2) / (self.rng3 * D_P_M)))
                new_y = int(round(((D_P_M ** 2) - (self.x_count - D_P_M) ** 2) / (self.rng4 * D_P_M)))

            else:
                assert False

            self.y_count = new_y - old_y
            self.x_count += 1

        if self.rect.right < 0:
            self.kill()
        if self.rect.left > self.screen_width:
            self.kill()
        if self.rect.bottom < 0:
            self.kill()
        if self.rect.top > self.screen_height:
            self.kill()
