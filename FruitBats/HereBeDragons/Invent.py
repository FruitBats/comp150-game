import pygame


class Inventory:
    """
    Inventory Class. Unfinished. When done, this class will be responsible for drawing the inventory screen and tracking which items
    are currently held by the player. Inventory screen can be opened and closed with "I" key.

    Attributes:
        item_list (list of Items): A list all possible items in the game.
        item_img_size (int): The size the item images will be when viewed in inventory.
        current_inventory (list of Items): A list of the items currently in the inventory.
        invent_screen (pygame.Surface): The inventory screen.
        invent_img (string): The filepath for the inventory background image.
        is_i_pressed (bool): If the I key has been pressed, opening the inventory.
    """

    item_list = []  # array of all possible items
    item_img_size = 32  # size of the item inventory display image
    current_inventory = []  # array of all items currently in the inventory
    invent_screen = None
    inventory_img = None
    is_i_pressed = False  # bool used to tell if the inventory should be open (True) or closed (False)

    def __init__(self, width, height):
        """
        Constructor.

        Args:
            width (int): Width of inventory screen in pixels.
            height (int): Height of inventory screen in pixels.
        """

        self.invent_screen = self.show_invent(width, height)

    def show_invent(self, width, height):
        """
        Currently just creates a surface for the inventory, but later will show the current inventory items.

        Args:
            width (int): The width of the inventory screen in pixels.
            height (int): The height of the inventory screen in pixels.
        """

        self.invent_screen = pygame.Surface((width, height))
        self.invent_screen.fill((0, 0, 0))
        self.invent_screen.set_colorkey((0, 0, 0))
        #item_img = pygame.image.load(self.item_list[]).convert()
        return self.invent_screen

    def update(self, events):
        """
        Updates the state of the inventory screen - shown or hidden - when the user pressed the I key.

        Args:
            events (event): The main game events.
        """

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.is_i_pressed = not self.is_i_pressed  # if 'i' is pressed flip the bool of is_i_pressed

    def render_invent(self, screen, width, height):
        """
        Renders the inventory screen to a destination surface.

        Args:
            screen (pygame.Surface): The destination surface to render the inventory on.
            width (int): Width of destination surface in pixels.
            height (int): Height of destination surface in pixels.
        """

        inventory_img = pygame.image.load("graphics/inventory_image.png").convert()
        if self.is_i_pressed:
            screen.blit(inventory_img, (int(width / 5), int(height / 5)))
