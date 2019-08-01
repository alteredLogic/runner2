"""
Player Class
"""
from constants import *


class Player(pygame.sprite.Sprite):
    """
    Creates a player object representing the playable character
    """
    def __init__(self, tile_width, tile_height, starting_x, starting_y):
        super(Player, self).__init__()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.starting_x = starting_x
        self.starting_y = starting_y
        self.morphing = False
        self.bullet_power = 0
        self.colors1 = rgb_blender(SHOOTABLE_0_COLOR, SHOOTABLE_1_COLOR, PLAYER_MORPH_STEPS)
        self.colors2 = rgb_blender(SHOOTABLE_1_COLOR, SHOOTABLE_0_COLOR, PLAYER_MORPH_STEPS)
        self.morph_counter = 1
        self.image = pygame.Surface((self.tile_width, self.tile_height))
        self.curr_color = SHOOTABLE_0_COLOR
        self.image.fill(self.curr_color)
        self.rect = self.image.get_rect(topleft=(self.starting_x, self.starting_y))
        self.jump_speed = 0
        self.gravity_count = 2
        self.gravity_direction = 'Down'
        self.jump_count = 2
        self.in_jump = False
        self.alive = True

    def gravity_reset(self):
        """
        Reset gravity
        """
        self.gravity_count = 2

    def jump_update(self):
        """
        Update jump variables
        """
        if self.jump_count < JUMP_FRAMES:
            self.jump_speed = int(round(10 - np.log(self.jump_count)))
            self.jump_count += 1
            if self.gravity_direction == 'Down':
                self.rect.move_ip(0, -self.jump_speed)
            elif self.gravity_direction == 'Up':
                self.rect.move_ip(0, self.jump_speed)
            else:
                assert False
        else:
            self.jump_reset()

    def jump_reset(self):
        """
        Reset jump variables
        """
        self.in_jump = False
        self.jump_speed = 0
        self.jump_count = 2

    def player_reset(self):
        """
        Set player to default location and variables
        """
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.gravity_reset()
        self.jump_reset()
        self.image.set_alpha(255)
        self.gravity_direction = 'Down'
        self.alive = True

    def kill_player(self):
        """
        Kill the player
        """
        self.alive = False
        self.image.set_alpha(0)

    def change_gravity_direction(self, gravity_direction):
        """
        Changes the direction of gravity
        :param gravity_direction: (str) New gravity direction
        """
        if gravity_direction == 'Up' or gravity_direction == 'Down':
            if self.gravity_direction != gravity_direction:
                pygame.mixer.Sound.play(GRAVITY_SOUND)
                self.gravity_direction = gravity_direction
                self.gravity_reset()
                self.jump_reset()
        else:
            assert False

    def gravity_update(self):
        """
        Updates gravity variables
        """
        fall_speed = int(round(2.2*np.log(self.gravity_count)))
        if self.gravity_direction == 'Up':
            fall_speed *= -1
        # TODO use while loop, increment by 1 and vertical check each time to ensure tile jumping over and under
        self.rect.move_ip(0, fall_speed)
        self.gravity_count += 1

    def morph_update(self):
        """
        Morphs the player from one color to another, and switches the bullet power
        """
        if self.morphing and self.alive:

            if self.bullet_power == 0:

                if self.morph_counter < PLAYER_MORPH_STEPS:
                    self.curr_color = self.colors1[self.morph_counter]
                    self.image.fill(self.curr_color)
                    self.morph_counter += 1
                else:
                    self.bullet_power = 1
                    self.morph_counter = 1
                    self.morphing = False

            elif self.bullet_power == 1:

                if self.morph_counter < PLAYER_MORPH_STEPS:
                    self.curr_color = self.colors2[self.morph_counter]
                    self.image.fill(self.curr_color)
                    self.morph_counter += 1
                else:
                    self.bullet_power = 0
                    self.morph_counter = 1
                    self.morphing = False
