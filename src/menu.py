"""
Menu Class
"""
from star import *
from text_button import *


class Menu:
    """
    Creates an object containing the main menu
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.full_bg = pygame.Surface((self.screen_width, self.screen_height))
        self.full_bg.fill(BACKGROUND_COLOR)

        self.moon_x = 600
        self.moon_counter = 0

        self.mode = MODE_GAME

        self.font = pygame.font.Font('./fonts/verdana.ttf', 20)

        self.stars_over_moon = pygame.sprite.Group()
        self.stars_under_moon = pygame.sprite.Group()
        self.all_stars = pygame.sprite.Group()

        for n in range(NUMBER_OF_MENU_STARS):
            curr_star_size = np.random.randint(STAR_SIZE_LOWER, STAR_SIZE_UPPER)
            x_lower_bound = 0
            x_upper_bound = self.screen_width - curr_star_size
            y_lower_bound = 0
            y_upper_bound = self.screen_height - curr_star_size
            self.create_new_star(x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound, curr_star_size)

        self.txt_title = TextButton(GAME_NAME, 100, './fonts/verdana.ttf', 195, 100,
                                    OLIVE, BACKGROUND_COLOR, 8, OLIVE)
        self.txt_game = TextButton('Play', 30, './fonts/verdana.ttf', 360, 350,
                                   OLIVE, BACKGROUND_COLOR, 8, OLIVE)
        self.txt_editor = TextButton('Level Editor', 30, './fonts/verdana.ttf', 305, 450,
                                     OLIVE, BACKGROUND_COLOR, 8, OLIVE)

        pygame.mixer.music.load('./sounds/intro.wav')
        pygame.mixer.music.play()

    def update_stars_and_moon(self):
        """
        Updates the stars and moon
        """
        self.moon_counter += 1
        if self.moon_counter == 25:
            self.moon_x -= 1
            self.moon_counter = 0

        if len(self.all_stars) < NUMBER_OF_MENU_STARS:
            curr_star_size = np.random.randint(STAR_SIZE_LOWER, STAR_SIZE_UPPER)
            self.create_new_star(self.screen_width, self.screen_width + 1,
                                 0, self.screen_height - curr_star_size,
                                 curr_star_size)

    def render_screen(self):
        """
        Renders the screen
        """
        screen = pygame.display.get_surface()

        screen.blit(self.full_bg, (0, 0))
        self.stars_under_moon.draw(screen)

        pygame.draw.circle(screen, LIGHT_GOLDENROD3, (self.moon_x, 200), 150)
        pygame.draw.circle(screen, LIGHT_GOLDENROD4, (self.moon_x + 70, 130), 30)

        self.stars_over_moon.draw(screen)
        screen.blit(self.txt_title.image, self.txt_title.rect)
        screen.blit(self.txt_game.image, self.txt_game.rect)
        screen.blit(self.txt_editor.image, self.txt_editor.rect)

    def flash_text_buttons(self):
        """
        Flash currently selected menu button
        """
        if self.mode == MODE_GAME:
            self.txt_game.cycle_color()
        elif self.mode == MODE_EDITOR:
            self.txt_editor.cycle_color()
        else:
            assert False

    def move_up(self):
        """
        Move menu up
        """
        if self.mode == MODE_EDITOR:
            pygame.mixer.Sound.play(MENU_MOVE_SOUND)
            self.txt_editor.reset_color()
            self.mode = MODE_GAME

    def move_down(self):
        """
        Move menu down
        """
        if self.mode == MODE_GAME:
            pygame.mixer.Sound.play(MENU_MOVE_SOUND)
            self.txt_game.reset_color()
            self.mode = MODE_EDITOR

    def create_new_star(self, x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound, curr_star_size):
        """
        Creates a new star object
        :param x_lower_bound: Lower x position bound
        :param x_upper_bound: Upper x position bound
        :param y_lower_bound: Lower y position bound
        :param y_upper_bound: Upper y position bound
        :param curr_star_size: Size of the star to create
        """
        starting_x = np.random.randint(x_lower_bound, x_upper_bound)
        starting_y = np.random.randint(y_lower_bound, y_upper_bound)
        alpha_step = np.random.randint(0, 100)
        color_of_star = np.random.randint(0, 3)
        speed_of_star = np.random.randint(STAR_SCROLL_SPEED_LOWER_BOUND, STAR_SCROLL_SPEED_UPPER_BOUND + 1)

        if len(self.all_stars) == 0:
            star = Star(self.screen_width, self.screen_height, curr_star_size,
                        starting_x, starting_y, alpha_step, color_of_star, speed_of_star)
            if np.random.randint(0, 2):
                self.stars_over_moon.add(star)
                self.all_stars.add(star)
            else:
                self.stars_under_moon.add(star)
                self.all_stars.add(star)

        else:
            add_star = True
            for s in self.all_stars:

                bool1 = starting_x < s.rect.right
                bool2 = starting_x > s.rect.left - curr_star_size
                bool3 = starting_y < s.rect.bottom
                bool4 = starting_y > s.rect.top - curr_star_size

                if bool1 and bool2 and bool3 and bool4:
                    add_star = False
                    break

            if add_star:
                star = Star(self.screen_width, self.screen_height, curr_star_size,
                            starting_x, starting_y, alpha_step, color_of_star, speed_of_star)
                if np.random.randint(0, 2):
                    self.stars_over_moon.add(star)
                    self.all_stars.add(star)
                else:
                    self.stars_under_moon.add(star)
                    self.all_stars.add(star)
