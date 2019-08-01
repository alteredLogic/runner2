"""
Star Class
"""
from constants import *


class Star(pygame.sprite.Sprite):
    """
    Creates a star object
    """
    def __init__(self, screen_width, screen_height, star_size,
                 starting_x, starting_y, alpha_step, color_of_star, scrolling_speed):
        super(Star, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.star_size = star_size
        self.image = pygame.Surface((star_size, star_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(starting_x, starting_y))
        self.alpha_counter = 0
        self.scroll_counter = 0
        self.flash_speed = 5
        self.scrolling_speed = scrolling_speed

        main_width = int(round(star_size / 4))
        main_height = int(round(star_size / 4))
        main_center_x = int(round(star_size / 2))
        main_center_y = int(round(star_size / 2))

        arm_up_width = int(round(star_size / 8))
        arm_up_height = int(round(star_size / 8))
        arm_up_center_x = int(round(star_size / 2))
        arm_up_center_y = int(round(star_size / 3))

        arm_down_width = int(round(star_size / 8))
        arm_down_height = int(round(star_size / 8))
        arm_down_center_x = int(round(star_size / 2))
        arm_down_center_y = int(round((star_size * 2) / 3))

        arm_left_width = int(round(star_size / 8))
        arm_left_height = int(round(star_size / 8))
        arm_left_center_x = int(round(star_size / 3))
        arm_left_center_y = int(round(star_size / 2))

        arm_right_width = int(round(star_size / 8))
        arm_right_height = int(round(star_size / 8))
        arm_right_center_x = int(round((star_size * 2) / 3))
        arm_right_center_y = int(round(star_size / 2))

        hand_up_width = int(round(star_size / 16))
        hand_up_height = int(round(star_size / 16))
        hand_up_center_x = int(round(star_size / 2))
        hand_up_center_y = int(round(star_size / 4))

        hand_down_width = int(round(star_size / 16))
        hand_down_height = int(round(star_size / 16))
        hand_down_center_x = int(round(star_size / 2))
        hand_down_center_y = int(round((star_size * 3) / 4))

        hand_left_width = int(round(star_size / 16))
        hand_left_height = int(round(star_size / 16))
        hand_left_center_x = int(round(star_size / 4))
        hand_left_center_y = int(round(star_size / 2))

        hand_right_width = int(round(star_size / 16))
        hand_right_height = int(round(star_size / 16))
        hand_right_center_x = int(round((star_size * 3) / 4))
        hand_right_center_y = int(round(star_size / 2))

        main_step = np.random.randint(50, 71)

        if color_of_star == RED_STAR:
            star_color = STAR_RED_COLOR
            star_arm_color = STAR_ARM_RED_COLOR
            star_hand_color = STAR_HAND_RED_COLOR

        elif color_of_star == BLUE_STAR:
            star_color = STAR_BLUE_COLOR
            star_arm_color = STAR_ARM_BLUE_COLOR
            star_hand_color = STAR_HAND_BLUE_COLOR

        elif color_of_star == WHITE_STAR:
            star_color = STAR_WHITE_COLOR
            star_arm_color = STAR_ARM_WHITE_COLOR
            star_hand_color = STAR_HAND_WHITE_COLOR

        else:
            assert False

        self.main = self.SubStar(main_width, main_height, main_center_x, main_center_y,
                                 self.image, star_color, main_step + alpha_step, self.flash_speed)

        self.arm_up = self.SubStar(arm_up_width, arm_up_height, arm_up_center_x, arm_up_center_y,
                                   self.image, star_color, 30 + alpha_step, self.flash_speed)

        self.arm_down = self.SubStar(arm_down_width, arm_down_height, arm_down_center_x, arm_down_center_y,
                                     self.image, star_arm_color, 30 + alpha_step, self.flash_speed)

        self.arm_left = self.SubStar(arm_left_width, arm_left_height, arm_left_center_x, arm_left_center_y,
                                     self.image, star_arm_color, 30 + alpha_step, self.flash_speed)

        self.arm_right = self.SubStar(arm_right_width, arm_right_height, arm_right_center_x, arm_right_center_y,
                                      self.image, star_arm_color, 30 + alpha_step, self.flash_speed)

        self.hand_up = self.SubStar(hand_up_width, hand_up_height, hand_up_center_x, hand_up_center_y,
                                    self.image, star_hand_color, alpha_step, self.flash_speed)

        self.hand_down = self.SubStar(hand_down_width, hand_down_height, hand_down_center_x, hand_down_center_y,
                                      self.image, star_hand_color, alpha_step, self.flash_speed)

        self.hand_left = self.SubStar(hand_left_width, hand_left_height, hand_left_center_x, hand_left_center_y,
                                      self.image, star_hand_color, alpha_step, self.flash_speed)

        self.hand_right = self.SubStar(hand_right_width, hand_right_height, hand_right_center_x, hand_right_center_y,
                                       self.image, star_hand_color, alpha_step, self.flash_speed)

    def update(self, screen_scroll_speed, screen_scroll_direction):
        """
        Update star placement
        :param screen_scroll_speed: Current screen scrolling speed
        :param screen_scroll_direction: Current screen scrolling direction
        """
        self.image.fill((0, 0, 0, 0))
        self.main.flash_substar()
        self.arm_up.flash_substar()
        self.arm_down.flash_substar()
        self.arm_left.flash_substar()
        self.arm_right.flash_substar()
        self.hand_up.flash_substar()
        self.hand_down.flash_substar()
        self.hand_left.flash_substar()
        self.hand_right.flash_substar()

        if screen_scroll_speed > 0:
            if screen_scroll_direction == 'Up' and self.scroll_counter >= self.scrolling_speed:
                self.scroll_counter = 0
                self.rect.move_ip(0, 1)
            elif screen_scroll_direction == 'Down' and self.scroll_counter >= self.scrolling_speed:
                self.scroll_counter = 0
                self.rect.move_ip(0, -1)
            elif screen_scroll_direction == 'Left' and self.scroll_counter >= self.scrolling_speed:
                self.scroll_counter = 0
                self.rect.move_ip(1, 0)
            elif screen_scroll_direction == 'Right' and self.scroll_counter >= self.scrolling_speed:
                self.scroll_counter = 0
                self.rect.move_ip(-1, 0)
            else:
                self.scroll_counter += 1

        if self.rect.top >= self.screen_height and screen_scroll_direction == 'Up':
            self.kill()
        elif self.rect.left >= self.screen_width and screen_scroll_direction == 'Left':
            self.kill()
        elif self.rect.bottom <= 0 and screen_scroll_direction == 'Down':
            self.kill()
        elif self.rect.right <= 0 and screen_scroll_direction == 'Right':
            self.kill()

    class SubStar:
        """
        SubStar Class
        """
        def __init__(self, tile_width, tile_height, center_x, center_y,
                     star_surface, substar_color, alpha_counter_start, flash_speed):
            self.image = pygame.Surface((tile_width, tile_height))
            self.image.fill(substar_color)
            self.rect = self.image.get_rect(center=(center_x, center_y))
            self.alpha_counter = alpha_counter_start
            self.flash_speed = flash_speed
            self.star = star_surface
            self.star.blit(self.image, self.rect)

        def flash_substar(self):
            """
            Cycles the alpha of a star component
            """
            new_alpha = int(round(127 + 128 * np.sin(self.alpha_counter / (100 / self.flash_speed))))
            self.image.set_alpha(new_alpha)
            self.alpha_counter += 1
            self.star.blit(self.image, self.rect)
