"""
Background Class
"""
import pygame
import numpy as np


class Background(pygame.sprite.Sprite):
    """
    Creates a background tile object
    """
    def __init__(self, bg_color, screen_width, screen_height, dimensions,
                 spawn_up, spawn_down, spawn_left, spawn_right,
                 speed_multiplier, flash_speed, starting_direction):
        super(Background, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.Surface(dimensions)
        self.image.fill(bg_color)

        self.spawn_up = spawn_up
        self.spawn_down = spawn_down
        self.spawn_left = spawn_left
        self.spawn_right = spawn_right

        self.speed_multiplier = speed_multiplier
        self.flash_speed = flash_speed
        self.counter = 1
        self.alpha_counter = 0

        if starting_direction == 'Up':
            self.rect = self.image.get_rect(topleft=self.spawn_up)
        elif starting_direction == 'Down':
            self.rect = self.image.get_rect(topleft=self.spawn_down)
        elif starting_direction == 'Left':
            self.rect = self.image.get_rect(topleft=self.spawn_left)
        elif starting_direction == 'Right':
            self.rect = self.image.get_rect(topleft=self.spawn_right)
        else:
            assert False

    def update(self, curr_speed, scroll_direction):
        """
        Update background tiles
        :param curr_speed: (int) Current int game scrolling speed
        :param scroll_direction: (str) Current in game scrolling direction
        """
        self.image.set_alpha(int(round(32 + 32 * np.sin(self.alpha_counter / (100 / self.flash_speed)))))
        self.alpha_counter += 1

        if curr_speed == 0:
            move_multiplier = np.inf
        elif curr_speed == 1:
            move_multiplier = 7
        elif curr_speed == 2:
            move_multiplier = 4
        elif curr_speed == 3:
            move_multiplier = 3
        elif curr_speed == 4:
            move_multiplier = 2
        elif curr_speed == 5:
            move_multiplier = 1
        elif curr_speed == 6:
            move_multiplier = 0.5
        elif curr_speed == 7:
            move_multiplier = 0.33
        elif curr_speed == 8:
            move_multiplier = 0.25
        elif curr_speed == 9:
            move_multiplier = 0.2
        elif curr_speed == 10:
            move_multiplier = 0.15
        else:
            move_multiplier = 0.1

        if move_multiplier < 1:
            self.counter = 1
            pixel_jump = int(round(self.speed_multiplier / move_multiplier))
            if scroll_direction == 'Up':
                self.rect.move_ip(0, pixel_jump)
            elif scroll_direction == 'Down':
                self.rect.move_ip(0, -pixel_jump)
            elif scroll_direction == 'Left':
                self.rect.move_ip(pixel_jump, 0)
            elif scroll_direction == 'Right':
                self.rect.move_ip(-pixel_jump, 0)
            else:
                assert False
        else:
            if int(round(self.counter * self.speed_multiplier)) >= move_multiplier:
                if scroll_direction == 'Up':
                    self.rect.move_ip(0, 1)
                elif scroll_direction == 'Down':
                    self.rect.move_ip(0, -1)
                elif scroll_direction == 'Left':
                    self.rect.move_ip(1, 0)
                elif scroll_direction == 'Right':
                    self.rect.move_ip(-1, 0)
                else:
                    assert False

                self.counter = 1
            else:
                self.counter += 1

        if self.rect.top >= self.screen_height and scroll_direction == 'Up':
            self.rect = self.image.get_rect(topleft=self.spawn_up)
        elif self.rect.left >= self.screen_width and scroll_direction == 'Left':
            self.rect = self.image.get_rect(topleft=self.spawn_left)
        elif self.rect.bottom <= 0 and scroll_direction == 'Down':
            self.rect = self.image.get_rect(topleft=self.spawn_down)
        elif self.rect.right <= 0 and scroll_direction == 'Right':
            self.rect = self.image.get_rect(topleft=self.spawn_right)
