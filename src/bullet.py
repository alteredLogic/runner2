"""
Bullet Class
"""
from constants import *


class Bullet(pygame.sprite.Sprite):
    """
    Creates a bullet object
    """
    def __init__(self, player_center, scroll_direction,
                 screen_width, screen_height, bullet_width, bullet_height, power):
        super(Bullet, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.bullet_size = (bullet_width, bullet_height)
        self.power = power
        self.image = pygame.Surface(self.bullet_size)

        if self.power == 0:
            self.image.fill(SHOOTABLE_0_COLOR)
        elif self.power == 1:
            self.image.fill(SHOOTABLE_1_COLOR)
        elif self.power == 2:
            self.image.fill(ENEMY_BULLET_COLOR)
        else:
            assert False

        self.rect = self.image.get_rect(center=player_center)
        self.speed = BULLET_SPEED
        self.direction = scroll_direction

    def update(self):
        """
        Updates a bullet's position
        """
        if self.direction == 'Up':
            self.rect.move_ip(0, -self.speed)
        elif self.direction == 'Down':
            self.rect.move_ip(0, self.speed)
        elif self.direction == 'Left':
            self.rect.move_ip(-self.speed, 0)
        elif self.direction == 'Right':
            self.rect.move_ip(self.speed, 0)
        else:
            assert False

        if self.rect.left > self.screen_width:
            self.kill()
        elif self.rect.right < 0:
            self.kill()
        elif self.rect.top < 0:
            self.kill()
        elif self.rect.bottom > self.screen_height:
            self.kill()
