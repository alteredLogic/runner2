"""
Constants File
"""
import pygame
import numpy as np
from pygame.locals import *

pygame.init()
pygame.mixer.init()

GAME_NAME = 'runner' + chr(0x00B2)
STARTING_SCREEN_WIDTH = 800
STARTING_SCREEN_HEIGHT = 600
STARTING_EDITOR_SCREEN_WIDTH = 1200
STARTING_EDITOR_SCREEN_HEIGHT = 600
STARTING_NUMBER_OF_MATRIX_ROWS = 24
STARTING_NUMBER_OF_MATRIX_COLUMNS = 32
NUMBER_OF_MEGA_GRID_ROWS = 10
NUMBER_OF_MEGA_GRID_COLUMNS = 10
BRIDGE_BREAK_RATE = 50
COLOR_BLEND_STEPS = 60
D_P_M = 50
NUMBER_OF_GAME_STARS = 14
NUMBER_OF_MENU_STARS = 50
STAR_SIZE_LOWER = 15
STAR_SIZE_UPPER = 35
STARTING_SPEED = 0
MAX_SPEED = 10
BULLET_SPEED = 7
JUMP_FRAMES = 50
BLOWUP_TIMER = 600
BLOWUP_COUNT = 3
PARTICLE_SPEED = 5
TEXT_FLASH_SPEED = 50
EDITOR_GRID_OFFSET = 1
MINI_GRID_X_OFFSET = 10
MINI_GRID_Y_OFFSET = 150
PLAYER_MORPH_STEPS = 30
PLAYER_STARTING_X = 100
PLAYER_STARTING_Y = 100
HORIZONTAL_SCROLL_SPEED_FAST = 4
HORIZONTAL_SCROLL_SPEED_SLOW = 2
STAR_SCROLL_SPEED_LOWER_BOUND = 1
STAR_SCROLL_SPEED_UPPER_BOUND = 30

PROPER_OFFSET = 100
PROPER_LEFT_SCROLL_X_POS = STARTING_SCREEN_WIDTH - PROPER_OFFSET
PROPER_RIGHT_SCROLL_X_POS = PROPER_OFFSET
PROPER_UP_SCROLL_Y_POS = STARTING_SCREEN_HEIGHT - PROPER_OFFSET
PROPER_DOWN_SCROLL_Y_POS = PROPER_OFFSET

RES = [(1200, 600, 12, 16), (1200, 600, 24, 32), (1200, 600, 30, 40)]
RES_LOOKUP = {(12, 16): 0, (24, 32): 1, (30, 40): 2}

RED = pygame.color.Color('red')
DARK_RED = pygame.color.Color('darkred')
YELLOW = pygame.color.Color('yellow')
BLUE = pygame.color.Color('blue')
DARK_BLUE = pygame.color.Color('darkblue')
WHITE = pygame.color.Color('white')
DARK_GREY = pygame.color.Color('darkgrey')
DARKER_GREY = pygame.color.Color('grey32')
DARK_PURPLE = pygame.color.Color('purple3')
PURPLE = pygame.color.Color('purple')
BLACK = pygame.color.Color('black')
GREEN = pygame.color.Color('green')
DARK_GREEN = pygame.color.Color('darkgreen')
ORANGE = pygame.color.Color('orange')
DIM_GRAY = pygame.color.Color('dimgray')
SNOW = pygame.color.Color('snow')
DARK_GOLDENROD = pygame.color.Color('darkgoldenrod')
BISQUE = pygame.color.Color('bisque4')
OLIVE = pygame.color.Color('olivedrab')
CYAN = pygame.color.Color('cyan')
LIGHT_BLUE3 = pygame.color.Color('lightblue3')
LIGHT_BLUE4 = pygame.color.Color('lightblue4')
IVORY = pygame.color.Color('ivory')
INDIANRED1 = pygame.color.Color('indianred1')
INDIANRED3 = pygame.color.Color('indianred3')
STEEL_BLUE3 = pygame.color.Color('steelblue3')
STEEL_BLUE4 = pygame.color.Color('steelblue4')
LIGHT_GOLDENROD3 = pygame.color.Color('lightgoldenrod3')
LIGHT_GOLDENROD4 = pygame.color.Color('lightgoldenrod4')

ABSORB_BULLET_SOUND = pygame.mixer.Sound('./sounds/absorb_bullet.wav')
DEATH_SOUND = pygame.mixer.Sound('./sounds/die.wav')
FALL_SOUND = pygame.mixer.Sound('./sounds/fall.wav')
GRAVITY_SOUND = pygame.mixer.Sound('./sounds/gravity_sound.wav')
JUMP_SOUND = pygame.mixer.Sound('./sounds/jump.wav')
MENU_MOVE_SOUND = pygame.mixer.Sound('./sounds/menu_move.wav')
MENU_SELECT_SOUND = pygame.mixer.Sound('./sounds/menu_select.wav')
SHOOT_SOUND = pygame.mixer.Sound('./sounds/shoot.wav')
SHOOT_BACK_SOUND = pygame.mixer.Sound('./sounds/shoot_back.wav')
WIN_SOUND = pygame.mixer.Sound('./sounds/win.wav')
DESTROY_BLOCK = pygame.mixer.Sound('./sounds/destroy_block.wav')
MOVE_CURSOR_SOUND = pygame.mixer.Sound('./sounds/move_cursor.wav')
SELECT_CURSOR_SOUND = pygame.mixer.Sound('./sounds/select_cursor.wav')
DELETE_CURSOR_SOUND = pygame.mixer.Sound('./sounds/delete_cursor.wav')


BACKGROUND_COLOR = BLACK
SHOOTABLE_0_COLOR = BISQUE
SHOOTABLE_1_COLOR = YELLOW
LAVA_COLOR = DARK_RED
SCROLL_ARROW_COLOR = RED
DIRECTION_ARROW_COLOR = GREEN
CEILING_COLOR = BLUE
FLOOR_COLOR = DARK_GREEN
FINISH_COLOR_1 = WHITE
FINISH_COLOR_2 = BLACK
DROP_DOWN_COLOR = DARK_PURPLE
FALL_UP_COLOR = STEEL_BLUE3
DROP_FALL_CIRCLE_COLOR = BISQUE
GRAVITY_UP_COLOR = DIM_GRAY
GRAVITY_DOWN_COLOR = DIM_GRAY
GRAVITY_ARROW_COLOR = SNOW
EDITOR_TEXT_COLOR = DARK_GOLDENROD
EDITOR_TEXT_BACKGROUND_COLOR = DARKER_GREY
EDITOR_STATUS_COLOR = DARKER_GREY
MENU_TEXT_COLOR = OLIVE
MENU_TEXT_BACKGROUND_COLOR = BLACK
ENEMY_BULLET_COLOR = CYAN
MOON_COLOR = LIGHT_GOLDENROD3
MOON_SPOT_COLOR = LIGHT_GOLDENROD4

STAR_RED_COLOR = INDIANRED1
STAR_ARM_RED_COLOR = INDIANRED3
STAR_HAND_RED_COLOR = SNOW

STAR_BLUE_COLOR = LIGHT_BLUE4
STAR_ARM_BLUE_COLOR = LIGHT_BLUE3
STAR_HAND_BLUE_COLOR = SNOW

STAR_WHITE_COLOR = IVORY
STAR_ARM_WHITE_COLOR = SNOW
STAR_HAND_WHITE_COLOR = WHITE

RED_STAR = 0
BLUE_STAR = 1
WHITE_STAR = 2


BG1_COLOR = PURPLE
BG2_COLOR = DARK_GREY
BG3_COLOR = ORANGE

KIND_BACKGROUND = 0
KIND_FLOOR = 1
KIND_SHOOTABLE_0 = 2
KIND_SHOOTABLE_1 = 3
KIND_LAVA = 4
KIND_CEILING = 5
KIND_FINISH = 6
KIND_DROP_DOWN = 7
KIND_FALL_UP = 8
KIND_GRAVITY_UP = 9
KIND_GRAVITY_DOWN = 10

MODE_MENU = 0
MODE_GAME = 1
MODE_EDITOR = 2

EDITOR_CURSOR_BOX = 0
EDITOR_CURSOR_ROW = 1
EDITOR_CURSOR_COLUMN = 2


MUSIC = False
RESET = USEREVENT
BLOWUP = USEREVENT + 1
BLEND = USEREVENT + 2
PLAY_GAME_MUSIC = USEREVENT + 3
RESET_EVENT = pygame.event.Event(RESET, {})

BG1_DIMENSIONS = (int(round((STARTING_SCREEN_WIDTH * 7) / 8)), int(round((STARTING_SCREEN_HEIGHT * 5) / 6)))

BG1_SPAWN_UP = (int(round(STARTING_SCREEN_WIDTH / 10)), -BG1_DIMENSIONS[1] - 100)
BG1_SPAWN_DOWN = (int(round(STARTING_SCREEN_WIDTH / 8)), STARTING_SCREEN_HEIGHT + 100)
BG1_SPAWN_LEFT = (-BG1_DIMENSIONS[0] - 100, int(round(STARTING_SCREEN_HEIGHT / 6)))
BG1_SPAWN_RIGHT = (STARTING_SCREEN_WIDTH + 100, int(round(STARTING_SCREEN_HEIGHT / 6)))


BG2_DIMENSIONS = (int(round(STARTING_SCREEN_WIDTH / 2)), int(round(STARTING_SCREEN_HEIGHT / 2)))

BG2_SPAWN_UP = (int(round(STARTING_SCREEN_WIDTH / 2)), -BG2_DIMENSIONS[1] - 75)
BG2_SPAWN_DOWN = (int(round(STARTING_SCREEN_WIDTH / 3)), STARTING_SCREEN_HEIGHT + 75)
BG2_SPAWN_LEFT = (-BG2_DIMENSIONS[0] - 75, int(round(STARTING_SCREEN_HEIGHT / 4)))
BG2_SPAWN_RIGHT = (STARTING_SCREEN_WIDTH + 75, int(round(STARTING_SCREEN_HEIGHT / 4)))


BG3_DIMENSIONS = (int(round(STARTING_SCREEN_WIDTH / 4)), int(round(STARTING_SCREEN_HEIGHT / 3)))

BG3_SPAWN_UP = (int(round((STARTING_SCREEN_WIDTH * 4) / 7)), -BG1_DIMENSIONS[1] - 75)
BG3_SPAWN_DOWN = (int(round((STARTING_SCREEN_WIDTH * 2) / 7)), STARTING_SCREEN_HEIGHT + 50)
BG3_SPAWN_LEFT = (-BG3_DIMENSIONS[0] - 50, int(round(STARTING_SCREEN_HEIGHT * 2 / 5)))
BG3_SPAWN_RIGHT = (STARTING_SCREEN_WIDTH + 50, int(round(STARTING_SCREEN_HEIGHT * 2 / 5)))


def generate_filename():
    """
    Generates a name for the .npy file
    :return: (str) Path and filename
    """
    return './levels/level.npy'


def rgb_blender(starting_rgb, ending_rgb, number_of_steps):
    """
    Blends one color into another
    :param starting_rgb: (rgba) Starting color
    :param ending_rgb: (rgba) Ending color
    :param number_of_steps: Total number of colors in the gradient
    :return: (ndarray) Matrix of colors
    """
    colors = np.linspace(starting_rgb, ending_rgb, number_of_steps)
    ret = np.zeros(colors.shape, dtype=int)

    for row in range(colors.shape[0]):
        for column in range(colors.shape[1]):
            ret[row][column] = int(round(colors[row][column]))

    return ret
