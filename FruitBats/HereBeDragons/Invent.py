import pygame


class Inventory:

    item_list = []  # array of all possible items
    item_img_size = 32  # size of the item inventory display image
    current_inventory = []  # array of all items currently in the inventory
    invent_screen = None
    inventory_img = None
    is_i_pressed = False  # bool used to tell if the inventory should be open (True) or closed (False)

    def __init__(self, width, height):
        self.invent_screen = self.show_invent(width, height)

    def show_invent(self, width, height):
        """currently just creates a surface for the inventory, but later will show the current inventory items"""
        self.invent_screen = pygame.Surface((width, height))
        self.invent_screen.fill((0, 0, 0))
        self.invent_screen.set_colorkey((0, 0, 0))
        #item_img = pygame.image.load(self.item_list[]).convert()
        return self.invent_screen

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.is_i_pressed = not self.is_i_pressed  # if 'i' is pressed flip the bool of is_i_pressed

    def render_invent(self, screen, width, height):
        """Renders the inventory screen"""
        inventory_img = pygame.image.load("graphics/inventory_image.png").convert()
        if self.is_i_pressed:
            screen.blit(inventory_img, (int(width / 5), int(height / 5)))
