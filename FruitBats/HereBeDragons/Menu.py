import sys
import pygame

# setting colors to variables
WHITE = (255, 255, 255)
VIOLET = (138, 43, 226)
BLACK = (0, 0, 0)


class MenuItem(pygame.font.Font):

    def __init__(self, text, font=None, font_size=30, font_color=WHITE, (pos_x, pos_y)=(0, 0)):
        """
        Class constructor.

        Args:
            text (string): The text to display on this menu item.
            font (string, optional): Defaults to None. Filename of font to use.
            font_size (int, optional): Defaults to 30. Size of font to use.
            font_color (pygame.Color, optional): Defaults to WHITE. Colour of font to use.
            (pos_x, pos_y) (tuple, optional): Defaults to (0, 0). Position of the menu item on the screen.
        """

        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, (posx, posy)):
        """
        Looks if mouse is in the frames of the game window. If it is, returns True, otherwise returns False

        Args:
            (posx, posy) (tuple):X and Y position of mouse.
        """

        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True

        return False

    def set_position(self, x, y):
        """
        Set position of a mouse

        Args:
            x (int): X position of mouse.
            y (int): Y position of the mouse.
        """

        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        """
        Sets the font color to the given color

        Args:
            rgb_tuple (tuple): The rgb of the colour to set the font to.
        """

        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


class GameMenu:
    """
    Sets given buttons to the main menu screen

    Attributes:
        running (bool): If the game is running.
        background_image (pygame.image): Background image of the main menu
        new_game (bool): If a new game has been started.
        full_screen (bool): If the game is in full screen mode.
        settings_window (bool): If the settings window has been opened.
    """

    running = True
    background_image = None
    new_game = False
    full_screen = False
    settings_window = False

    def __init__(self, screen, font=None, font_size=30, font_color=WHITE):
        """
        Class constructor.

        Args:
            screen (pygame.Surface): The screen on which to draw the menu.
            font (string, optional): Defaults to None. Filename of font for menu text.
            font_size (int, optional): Defaults to 30. Size of font for menu text.
            font_color (pygame.Color, optonal): Defaults to WHITE. Colour for the menu text.
        """

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.background_image = pygame.image.load("ImageFiles/Background1.jpg")
        self.background_image = self.background_image.convert(32)
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.scr_width,
                                                        self.scr_height))

        self.clock = pygame.time.Clock()
        self.menu_items = ('New Game', 'Continue Game',
                           'Settings', 'Exit')
        self.funcs = {"New Game": GameMenu.start_pressed,
                      "Continue Game": GameMenu.continue_pressed,
                      "Settings": GameMenu.settings,
                      "Exit": GameMenu.exit_pressed}
        self.items = []
        key_list = self.funcs.keys()
        for index, item in enumerate(self.menu_items):
            # sets the buttons to the center of the screen

            menu_item = MenuItem(item, font, font_size, font_color)

            # total height of text block
            total_height = len(key_list) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (total_height / 2) +\
                    ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def start_pressed(self):
        """Starts a new game with character creation"""

        self.new_game = True
        self.running = False

    def continue_pressed(self):
        """Continues the game with the previous seed and progress"""

        self.new_game = False
        self.running = False

    def settings(self):
        """The settings menu. Currently just changes the game window to fullscreen."""

        # Sets the screen to full screen
        # ToDo: make a proper settings with different manageable functions
        if self.full_screen is False:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.full_screen = True
        elif self.full_screen is not False:
            self.screen = pygame.display.set_mode((self.scr_width,
                                                   self.scr_height))
            self.full_screen = False

    def exit_pressed(self):
        """Exits the game"""

        sys.exit()

    def set_mouse_visibility(self):
        """Changes the visibility of the mouse cursor."""

        # If the mouse is used - set it visibility to True
        # If not - set to False
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.

        Args:
            key (event.key): The key being pressed.
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(BLACK)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and \
                    self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and \
                    self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and \
                    self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and \
                    self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        # Sets text to italic and violet color if it is chosen
        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(VIOLET)

        # Finally check if Enter or Space is pressed
        if key == pygame.K_ESCAPE or \
                key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text](self)

    def set_mouse_selection(self, item, mpos):
        """
        Marks the MenuItem when the mouse cursor hovers on.

        Args:
            item (MenuItem): Menu item the mouse is over.
            mpos (tuple): Mouse cursor coordinates.
        """
        if item.is_mouse_selection(mpos):
            item.set_font_color(VIOLET)
            item.set_italic(True)
        else:
            item.set_font_color(BLACK)
            item.set_italic(False)

    def run(self):
        """Main loop for the main menu"""

        self.running = True
        while self.running:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_item_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mouse_position):
                            self.funcs[item.text](self)

            # Sets the mouse visible upon moving AND
            # sets current item (cur_item) to None as
            # it is used only when using keyboard keys
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background
            self.screen.blit(self.background_image, [0, 0])

            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mouse_position)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
