import sys
import pygame

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=WHITE, (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y

    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False

    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y

    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)


class GameMenu:

    running = True
    background_image = None

    def __init__(self, screen, font=None,
                 font_size=30, font_color=WHITE):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.background_image = pygame.image.load("ImageFiles/Background.png")
        self.background_image = self.background_image.convert(32)
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.scr_width, self.scr_height))

        self.clock = pygame.time.Clock()
        self.funcs = {"New Game": GameMenu.start_pressed,
                      "Quit": GameMenu.quit_pressed}
        self.items = []
        key_list = self.funcs.keys()
        for index, item in enumerate(key_list):
            menu_item = MenuItem(item, font, font_size, font_color)

            # total height of text block
            total_height = len(key_list) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (total_height / 2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def start_pressed(self):
        self.running = False

    def quit_pressed(self):
        sys.exit()

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys
        """
        for item in self.items:
            # Return all to neutral
            item.set_italic(False)
            item.set_font_color(WHITE)

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

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(GREEN)

        # Finally check if Enter os Space is pressed
        if key == pygame.K_ESCAPE or \
                key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text](self)

    def set_mouse_selection(self, item, mpos):
        """
        Marks the MenuItem the mouse cursor hovers on.
        """
        if item.is_mouse_selection(mpos):
            item.set_font_color(GREEN)
            item.set_italic(True)
        else:
            item.set_font_color(WHITE)
            item.set_italic(False)

    def run(self):
        self.running = True
        while self.running:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)

            mpos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_item_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text](self)

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background
            self.screen.blit(self.background_image, [0, 0])

            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()
