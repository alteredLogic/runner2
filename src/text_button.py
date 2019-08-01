"""
Text Button Class
"""
from constants import *


class TextButton(pygame.sprite.Sprite):
    """
    Creates a text button object for the main menu
    """
    def __init__(self, text, text_size, font, x_pos, y_pos,
                 text_color, text_background_color, border_size, border_color):
        super(TextButton, self).__init__()
        self.colors_text = rgb_blender(OLIVE, STEEL_BLUE4, TEXT_FLASH_SPEED)
        self.colors_background = rgb_blender(BACKGROUND_COLOR, DARKER_GREY, TEXT_FLASH_SPEED)
        self.color_cycle = 0
        self.color_cycle_up = True
        self.font = pygame.font.Font(font, text_size)
        self.text = text
        self.border_size = border_size
        self.txt = self.font.render(self.text, True, text_color, text_background_color)

        size_needed = self.font.size(self.text)

        self.image = pygame.Surface((size_needed[0] + border_size, size_needed[1] + border_size))
        self.image.fill(border_color)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        self.coords = (int(round(border_size / 2)), int(round(border_size / 2)))
        self.image.blit(self.txt, self.coords)

    def cycle_color(self):
        """
        Cycle currently selected menu button colors
        """
        if self.color_cycle < TEXT_FLASH_SPEED - 1 and self.color_cycle_up:
            self.color_cycle += 1
        else:
            self.color_cycle_up = False

        if self.color_cycle > 0 and not self.color_cycle_up:
            self.color_cycle -= 1
        else:
            self.color_cycle_up = True

        self.txt = self.font.render(self.text, True, OLIVE, self.colors_background[self.color_cycle])
        self.image.blit(self.txt, self.coords)

    def reset_color(self):
        """
        Reset menu button colors
        """
        self.color_cycle = 0
        self.color_cycle_up = True
        self.txt = self.font.render(self.text, True, OLIVE, BACKGROUND_COLOR)
        self.image.blit(self.txt, self.coords)
