import pygame
import pickle

from sprite import Sprite
from button import Button
from get_images import GetImages


class CharacterCreation:

    # index checking to save the position is probably not necessary. Character creation menu doesn't really need to save user's position

    """
    CharacterCreation class. This class displays a character creation window and allows the user to edit the apperance
    of their character.

    Attributes:
        path_to_assets (string): The file path to the assets folder. This should later be added to the constructor so it can be passed in when the class is instantiated.
        blank_component (image): A blank image that is used as a placeholder
        blank_base (image): The image used for the base of the sprite

        main_screen (pygame.Display): The character creation window
        background_colour (pygame.Colour): The colour for the main window.
        buttons (list of Buttons): A list of the Buttons on the screen.

        char_position (tuple): The position of the player_char on the screen.
        player_char (Sprite): The player character's Sprite. player_char.image used to access the image

        body_choices (list of Surfaces): The images that the player can choose from for the body component.
        hair_choices (list of Surfaces): The images that the player can choose from for the hair component.
        legs_choices (list of Surfaces): The images that the player can choose from for the legs component.

        body_index (int): The position in the body_choices array. Used to save the user's place.
        hair_index (int): The position in the hair_choices array. Used to save the user's place.
        legs_index (int): The position in the legs_choices array. Used to save the user's place.

        # These are set in __init__ so that length only has to be calculated once.
        body_choices_length (int): The length of the body_choices list.
        hair_choices_length (int): The length of the hair_choices list.
        legs_choices_length (int): The length of the legs_choices list.

        loading (bool): Sets if the program loads the player_char from a serialized file. Mainly for testing.
        running (bool): State of the pygame window. Window remains open while running is True.
    """

    # path_to_assets = "../Assets"
    path_to_assets = "SpriteGeneration/Assets"
    blank_component = pygame.image.load(path_to_assets + "/Sprites/blankComponent.png")
    blank_base = pygame.image.load(path_to_assets + "/Sprites/base/base1.png")

    main_screen = None
    background_colour = (222, 184, 135)
    buttons = []

    char_position = (326, 236)
    player_char = None

    body_choices = []
    hair_choices = []
    legs_choices = []

    body_index = -1
    hair_index = -1
    legs_index = -1

    body_choices_length = 0
    hair_choices_length = 0
    legs_choices_length = 0

    loading = False
    # loading = True
    running = True

    def __init__(self, screen, hair_list, body_list, legs_list):

        """
        Constructor method.

        Args:
            size (tuple): The size in pixels of the character creation window.
            hair_list (list of images): The images that can be chosen for the character's head.
            body_list (list of images): The images that can be chosen for the character's body.
            legs_list (list of images): The images that can be chosen for the character's legs.
        """

        self.screen = screen
        self.size = screen.get_size()

        self.hair_choices = hair_list
        self.body_choices = body_list
        self.legs_choices = legs_list

        self.body_choices_length = len(self.body_choices)
        self.hair_choices_length = len(self.hair_choices)
        self.legs_choices_length = len(self.legs_choices)

        # Get the position in the component lists from the last session.
        self.read_component_index("char_creation_index.txt")

        # Check if loading from serialized file. This should be temporary. For testing only.
        if self.loading:
            #if Sprite.deserialize("player_sprite") is not None:
            self.player_char = Sprite.deserialize("player_sprite")

        else:
            self.player_char = self.load_blank_sprite()

    def draw_win(self):

        """Main method for the class. This creates the character creation window and checks for player input."""

        print("Drawing screen for first time")

        # Initialise display
        # self.main_screen = pygame.display.set_mode(self.size)
        # self.main_screen.fill(self.background_colour)

        self.screen.fill(self.background_colour)

        self.create_buttons()
        self.update_screen()

        # Loop to keep window open and check for events
        while self.running:
            for event in pygame.event.get():

                # Each button checks if it was clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        button.check_click(pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

    def update_screen(self):

        """Updates the character creation screen. Blits the character sprite to the screen and updates it."""
        self.screen.blit(self.player_char.image, self.char_position)
        pygame.display.flip()

        print("Screen updated")

    def load_blank_sprite(self):

        """
        Instantiates a new Sprite with a blank base and blank components as placeholders and draws the sprite image.

        Returns:
            blank_sprite (Sprite): A Sprite with base image and blank components.
        """

        # Create and draw a new sprite with a base image and the last used components
        blank_sprite = Sprite((128, 128), self.background_colour, pygame.transform.scale(self.blank_base, (128, 128)), self.legs_choices[self.legs_index],
                                                                  self.body_choices[self.body_index], self.hair_choices[self.hair_index], self.blank_component, 0)
        blank_sprite.draw()
        return blank_sprite

    def scroll_components(self, component, direction):

        """
        Scrolls in a direction (backwards or forwards) through a list of component images and updates the player's sprite

        Args:
            component (string): The component to change when the player gives input (presses a 'button')
            direction (int): 1 = scrolling forward in list, -1 = scrolling backwards in list.
        """

        # Get the index of the relevant component list
        index = getattr(self, component + "_index")
        list_length = getattr(self, component + "_choices_length")
        # list_length = len(getattr(self, component + "_choices"))

        # Move through list
        if direction == 1:
            index += 1

        elif direction == -1:
            index -= 1

        # If index exceeds list bounds, reset to 0
        if (index >= list_length) or (index <= -list_length):
            print("Index at max! " + str(list_length))
            index = 0
        else:
            print("Index = " + str(index))

        # Update the index of the relevant component
        setattr(self, component + "_index", index)

        # Update component of sprite with image from location in list
        self.player_char.update([component], [getattr(self, component + "_choices")[index]])
        self.update_screen()

    def create_buttons(self):

        """
        Instantiates all the buttons needed for the character creation window.
        The buttons are positioned based on the positioning of the player character.
        Each button is also appended to the list of buttons.
        """

        # Whole section is messy. Perhaps make ScrollButton an object that inherits from Button with initial size, colour, function etc?

        # Create new buttons
        center = (self.size[0] / 2), (self.size[1] / 2)
        right = (self.char_position[0] + 150)
        left = (self.char_position[0] - 100)
        y = self.char_position[1]

        # Hair options
        button_hair = Button((50, 50), (right, y - 100), (0, 255, 0), self.screen, [self.scroll_components], [["hair", 1]], "foo")
        button_hair_back = Button((50, 50), (left, y - 100), (255, 0, 0), self.screen, [self.scroll_components], [["hair", -1]], "foo")

        # Body options
        button_body = Button((50, 50), (right, y), (0, 255, 0), self.screen, [self.scroll_components], [["body", 1]], "foo")
        button_body_back = Button((50, 50), (left, y), (255, 0, 0), self.screen, [self.scroll_components], [["body", -1]], "foo")

        # Leg options
        button_legs = Button((50, 50), (right, y + 100), (0, 255, 0), self.screen, [self.scroll_components], [["legs", 1]], "foo")
        button_legs_back = Button((50, 50), (left, y + 100), (255, 0, 0), self.screen, [self.scroll_components], [["legs", -1]], "foo")

        # Save/finish button
        # button_save = Button((100, 50), (center[0] - 50, center[1] + 200), (0, 0, 255), self.screen, [Sprite.serialize, self.exit], [["player_sprite", self.player_char], None], "foo")
        button_save = Button((100, 50), (center[0] - 50, center[1] + 200), (0, 0, 255), self.screen, [self.finalise_sprite, self.exit], [[], []], "foo")

        # Add new buttons to the list of buttons
        self.buttons.append(button_hair)
        self.buttons.append(button_hair_back)

        self.buttons.append(button_body)
        self.buttons.append(button_body_back)

        self.buttons.append(button_legs)
        self.buttons.append(button_legs_back)

        self.buttons.append(button_save)

    def save_component_index(self, save_file):

        """Creates or overwrites the save file, updating the index position when the player saved their sprite."""

        with open(save_file, "w") as f:
            f.write("hair_index " + str(self.hair_index) + "\n")
            f.write("body_index " + str(self.body_index) + "\n")
            f.write("legs_index " + str(self.legs_index) + "\n")
            f.close()

    def read_component_index(self, save_file):

        """Reads the save file and sets the appropriate index value to the saved values."""
        try:
            with open(save_file) as f:
                for line in f:
                    (key, val) = line.split()
                    setattr(self, key, int(val))

        except IOError:
            print("No index file found.")

    def finalise_sprite(self):
        self.player_char.update(["background_colour"], [(0, 0, 0, 0)])
        self.player_char.resize((64, 64))

        Sprite.serialize("player_sprite", self.player_char)

    def exit(self):

        """Closes the character creation window. This could be adapted to lead into the main game."""

        print("Window Closed")
        self.running = False


def load_creation_window(screen):
    images = GetImages("SpriteGeneration/Assets", ".png", (128, 128))
    test_window = CharacterCreation(screen, images.hair, images.body, images.legs)
    test_window.draw_win()
    test_window.save_component_index("char_creation_index.txt")

