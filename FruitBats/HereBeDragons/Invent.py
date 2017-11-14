import pygame

class Inventory:

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480
    item_list = []
    item_img_size = 32
    current_inventory = []
    invent_screen = None
    inventory_img = None
    is_i_pressed = False

    def __init__(self):
        self.invent_screen = self.show_invent()

    def show_invent(self):
        self.invent_screen = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.invent_screen.fill((0, 0, 0))
        self.invent_screen.set_colorkey((0, 0, 0))
        #item_img = pygame.image.load(self.item_list[]).convert()
        return self.invent_screen

    def update(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_i] and self.is_i_pressed == False:
            self.is_i_pressed = True
        elif key_pressed[pygame.K_i] and self.is_i_pressed == True:
            self.is_i_pressed = False

    def render_invent(self, screen):
        inventory_img = pygame.image.load("graphics/inventory_image.png").convert()
        if self.is_i_pressed == True:
            screen.blit(inventory_img, (int(self.SCREEN_WIDTH / 6), int(self.SCREEN_HEIGHT / 5)))
