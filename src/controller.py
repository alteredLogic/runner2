"""
Controller Class
"""
from game import *
from editor import *
from menu import *


class Controller:
    """
    Controller object to take in and map player input
    """
    def __init__(self):

        if not pygame.joystick.get_count():
            pygame.quit()
            exit('No joystick found.')

        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()
        self.num_joy_buttons = self.joy.get_numbuttons()
        self.num_joy_axes = self.joy.get_numaxes()
        self.joy_buttons = np.zeros(self.num_joy_buttons, dtype=bool)
        self.joy_axes = np.zeros(self.num_joy_axes, dtype=float)

        self.up_button = False
        self.down_button = False
        self.left_button = False
        self.right_button = False
        self.button0 = False
        self.button1 = False
        self.button2 = False
        self.button3 = False
        self.button4 = False
        self.button5 = False
        self.button6 = False
        self.button7 = False
        self.button8 = False
        self.button9 = False

        self.mode = MODE_MENU

        pygame.display.set_mode((STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT))
        #pygame.display.set_mode((STARTING_SCREEN_WIDTH * 2, 900), flags=(FULLSCREEN | HWACCEL))

        self.menu = Menu(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT)

        self.game = Game(STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT)

        self.editor = Editor(STARTING_EDITOR_SCREEN_WIDTH, STARTING_EDITOR_SCREEN_HEIGHT,
                             STARTING_NUMBER_OF_MATRIX_ROWS, STARTING_NUMBER_OF_MATRIX_COLUMNS)

    def update_game(self):
        """
        Game update function
        """
        # Jump
        if self.joy_buttons[1]:
            if not self.button1:
                self.button1 = True
                self.game.start_jump()
            else:
                self.game.jump_continue()
        else:
            if self.button1:
                self.button1 = False
                self.game.end_jump()

        # Speed change
        if self.joy_buttons[2]:
            if not self.button2:
                self.button2 = True
        else:
            self.button2 = False

        # Right D-pad
        if self.joy_axes[0] > 0.5:
            if not self.right_button:
                self.right_button = True
            if self.game.get_physics_mode() == 'Vertical':
                if self.button2:
                    self.game.player.rect.move_ip(HORIZONTAL_SCROLL_SPEED_FAST, 0)
                else:
                    self.game.player.rect.move_ip(HORIZONTAL_SCROLL_SPEED_SLOW, 0)
        else:
            self.right_button = False

        # Left D-pad
        if self.joy_axes[0] < -0.5:
            if not self.left_button:
                self.left_button = True
            if self.game.get_physics_mode() == 'Vertical':
                if self.button2:
                    self.game.player.rect.move_ip(-HORIZONTAL_SCROLL_SPEED_FAST, 0)
                else:
                    self.game.player.rect.move_ip(-HORIZONTAL_SCROLL_SPEED_SLOW, 0)
        else:
            self.left_button = False

        # Down D-pad
        if self.joy_axes[1] > 0.5:
            if not self.down_button:
                self.down_button = True
        else:
            self.down_button = False

        # Up D-pad
        if self.joy_axes[1] < -0.5:
            if not self.up_button:
                self.up_button = True
        else:
            self.up_button = False

        self.game.player_bounds_check()

        # Change bullet power
        if self.joy_buttons[3]:
            if not self.button3:
                self.button3 = True
                self.game.player.morphing = True
        else:
            self.button3 = False

        # Shoot bullet
        if self.joy_buttons[0]:
            if not self.button0:
                self.button0 = True
                self.game.shoot_bullet()
        else:
            self.button0 = False

        # Decrease Speed
        if self.joy_buttons[4]:
            if not self.button4:
                self.button4 = True
                if self.game.speed > 0:
                    self.game.speed -= 1
        else:
            self.button4 = False

        # Increase Speed
        if self.joy_buttons[5]:
            if not self.button5:
                self.button5 = True
                if self.game.speed < MAX_SPEED:
                    self.game.speed += 1
        else:
            self.button5 = False

        # Unused
        if self.joy_buttons[6]:
            if not self.button6:
                self.button6 = True

        else:
            self.button6 = False

        # Unused
        if self.joy_buttons[7]:
            if not self.button7:
                self.button7 = True

        else:
            self.button7 = False

        # Reset game
        if self.joy_buttons[8]:
            if not self.button8:
                self.button8 = True
                self.game.reset()
        else:
            self.button8 = False

        # Unused
        if self.joy_buttons[9]:
            if not self.button9:
                self.button9 = True

        else:
            self.button9 = False

    def update_editor(self):
        """
        Takes in user input for the level editor
        """
        # Removes tiles from the current grid
        if self.joy_buttons[0]:
            if not self.button0:
                self.button0 = True
                self.editor.set_tile(KIND_BACKGROUND)
        else:
            self.button0 = False

        # Places a tile into the current grid
        if self.joy_buttons[1]:
            if not self.button1:
                self.button1 = True
                self.editor.set_tile(self.editor.curr_kind)
        else:
            self.button1 = False

        # Switches the cursor mode
        if self.joy_buttons[2]:
            if not self.button2:
                self.button2 = True
                self.editor.switch_cursor_mode()
        else:
            self.button2 = False

        # Changes the grid size
        if self.joy_buttons[3]:
            if not self.button3:
                self.button3 = True
                self.editor.resize_help()
        else:
            self.button3 = False

        # Increment tile type
        if self.joy_buttons[4]:
            if not self.button4:
                self.button4 = True
                self.editor.increment_kind()
        else:
            self.button4 = False

        # OLD Increment tile type
        # Alter box cursor size
        if self.joy_buttons[5]:
            if not self.button5:
                self.button5 = True
                # self.editor.increment_kind()
        else:
            self.button5 = False

        # Set scrolling direction for the current grid
        if self.joy_buttons[6] and not self.button7:
            if not self.button6:
                self.button6 = True
                self.editor.set_scroll_arrows(GREEN)
            self.editor.flash_arrows()
        else:
            if self.button6:
                self.button6 = False
                self.editor.clear_scroll_arrows()

        # Scroll between grid on the mega grid
        if self.joy_buttons[7] and not self.button6:
            if not self.button7:
                self.button7 = True
                self.editor.set_scroll_arrows(RED)
            self.editor.flash_arrows()
        else:
            if self.button7:
                self.button7 = False
                self.editor.clear_scroll_arrows()

        # Load from disk
        if self.joy_buttons[8]:
            if not self.button8:
                self.button8 = True
                self.editor.load_from_disk()
        else:
            self.button8 = False

        # Save to disk
        if self.joy_buttons[9]:
            if not self.button9:
                self.button9 = True
                self.editor.save_to_disk()
        else:
            self.button9 = False

        # Move cursor right
        if self.joy_axes[0] > 0.5:
            if not self.right_button:
                self.right_button = True
                if self.button5 and self.editor.cursor_mode == EDITOR_CURSOR_BOX:
                    self.editor.change_box_cursor_size('Right')
                elif self.button6:
                    self.editor.set_scroll_direction('Right')
                elif self.button7:
                    self.editor.move_mega_grid('Right')
                else:
                    self.editor.move_cursor('Right')
        else:
            self.right_button = False

        # Move cursor left
        if self.joy_axes[0] < -0.5:
            if not self.left_button:
                self.left_button = True
                if self.button5 and self.editor.cursor_mode == EDITOR_CURSOR_BOX:
                    self.editor.change_box_cursor_size('Left')
                elif self.button6:
                    self.editor.set_scroll_direction('Left')
                elif self.button7:
                    self.editor.move_mega_grid('Left')
                else:
                    self.editor.move_cursor('Left')
        else:
            self.left_button = False

        # Move cursor down
        if self.joy_axes[1] > 0.5:
            if not self.down_button:
                self.down_button = True
                if self.button5 and self.editor.cursor_mode == EDITOR_CURSOR_BOX:
                    self.editor.change_box_cursor_size('Down')
                elif self.button6:
                    self.editor.set_scroll_direction('Down')
                elif self.button7:
                    self.editor.move_mega_grid('Down')
                else:
                    self.editor.move_cursor('Down')
        else:
            self.down_button = False

        # Move cursor up
        if self.joy_axes[1] < -0.5:
            if not self.up_button:
                self.up_button = True
                if self.button5 and self.editor.cursor_mode == EDITOR_CURSOR_BOX:
                    self.editor.change_box_cursor_size('Up')
                elif self.button6:
                    self.editor.set_scroll_direction('Up')
                elif self.button7:
                    self.editor.move_mega_grid('Up')
                else:
                    self.editor.move_cursor('Up')
        else:
            self.up_button = False

    def update_menu(self):
        """
        Processes user input for the menu
        """
        # Select mode
        if self.joy_buttons[0]:
            if not self.button0:
                self.button0 = True
        else:
            self.button0 = False

        # Select mode
        if self.joy_buttons[1]:
            if not self.button1:
                self.button1 = True
                self.change_mode(self.menu.mode)
        else:
            self.button1 = False

        # Unused
        if self.joy_buttons[2]:
            if not self.button2:
                self.button2 = True
        else:
            self.button2 = False

        # Unused
        if self.joy_buttons[3]:
            if not self.button3:
                self.button3 = True
        else:
            self.button3 = False

        pass
        # Unused
        if self.joy_buttons[4]:
            if not self.button4:
                self.button4 = True
        else:
            self.button4 = False

        # Unused
        if self.joy_buttons[5]:
            if not self.button5:
                self.button5 = True
        else:
            self.button5 = False

        # Unused
        if self.joy_buttons[6]:
            if not self.button6:
                self.button6 = True
        else:
            self.button6 = False

        # Unused
        if self.joy_buttons[7]:
            if not self.button7:
                self.button7 = True
        else:
            self.button7 = False

        # Unused
        if self.joy_buttons[8]:
            if not self.button8:
                self.button8 = True
        else:
            self.button8 = False

        # Unused
        if self.joy_buttons[9]:
            if not self.button9:
                self.button9 = True
        else:
            self.button9 = False

        # Move cursor right
        if self.joy_axes[0] > 0.5:
            if not self.right_button:
                self.right_button = True
                
        else:
            self.right_button = False

        # Move cursor left
        if self.joy_axes[0] < -0.5:
            if not self.left_button:
                self.left_button = True
                
        else:
            self.left_button = False

        # Move cursor down
        if self.joy_axes[1] > 0.5:
            if not self.down_button:
                self.down_button = True
                self.menu.move_down()
        else:
            self.down_button = False

        # Move cursor up
        if self.joy_axes[1] < -0.5:
            if not self.up_button:
                self.up_button = True
                self.menu.move_up()
        else:
            self.up_button = False

    def get_joystick_pressed(self):
        """
        Get currently pressed joystick buttons
        """
        for b in range(self.num_joy_buttons):
            self.joy_buttons[b] = self.joy.get_button(b)

        for a in range(self.num_joy_axes):
            self.joy_axes[a] = self.joy.get_axis(a)

    def change_mode(self, mode):
        """
        Switches game mode from menu
        :param mode: (str) Mode to switch to
        """
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.Sound.play(MENU_SELECT_SOUND)
        self.mode = mode
        if self.mode == MODE_GAME or self.mode == MODE_MENU:
            # noinspection PyArgumentList
            pygame.mixer.music.set_endevent(PLAY_GAME_MUSIC)
            #pygame.display.set_mode((STARTING_SCREEN_WIDTH, STARTING_SCREEN_HEIGHT))
        elif self.mode == MODE_EDITOR:
            pygame.display.set_mode((STARTING_EDITOR_SCREEN_WIDTH, STARTING_EDITOR_SCREEN_HEIGHT))
        else:
            assert False
