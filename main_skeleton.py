"""Skeleton file -- INFORMATIONAL FILE -- not a part of the actual program!
This describes how to use the classes but not how they're implemented
Up for review: revise as necessary
"""

class Game:
    delta_time = 0  # time passed since last frame
    tick_time = 0  # time at the start of the frame, in seconds since the game started
    screen = None  # pygame screen
    objects = None  # list of active objects in the game
    player = None  # pointer to the player object
    quitting = False

    # Game startup
    def __init__(self):
    # Run: called when game starts up
    def run(self):
    # Quit the game
    def quit(self):
    # Resize game window, dimensions is a Tuple for width and height
    def resize_window(self, dimensions):

"""
Sprite Class. This class contains methods for drawing, updating and saving a sprite as a single image.
Attributes:
    image (pygame.Surface): This is the image for the sprite in the form of a surface which can be redrawn if the sprite is updated.
"""
class Sprite:
    # The image used for the sprite
    image = 0

    # Initialise new sprite with component images
    def __init__(self, size, base, legs, body, head, feet, weapon):
        """
        Constructor for sprite class.
        Args:
            size (tuple): The size of the sprite in pixels.
            base (image file): The image to use for the sprite base.
            legs (image file): The image to use for the sprite's legs.
            body (image file): The image to use for the sprite's body.
            head (image file): The image to use for the sprite's head.
            feet (image file): The image to use for the sprite's feet.
            weapon (image file): The image to use for the sprite's weapon. Note that in the current implementation this
                            is always passed a placeholder of 0, as weapon sprites have not been added to the assets folder.
                            Similarily, the weapon image is not blitted to the sprite image in the draw functions, as there is no image.
        """

    # Draw component images onto a base surface then save the surface as a single sprite
    def draw(self):
        """Draws the sprite's component images onto a PyGame surface and assigns it to the image property."""

    # Draw component images onto a base surface then save the surface as a single sprite
    def draw_with_position(self, base_pos, body_pos, legs_pos, head_pos):
        """
        Draws the sprite's component images onto a PyGame surface at
        specified positions and assigns the surface to the image property.
        Args:
            base_pos (tuple): Position of the base image.
            body_pos (tuple): Position of the body image.
            legs_pos (tuple): Position of the legs image.
            head_pos (tuple): Position of the head image.
        """

    # Takes a list of properties (string) to update and a list of values (images) corresponding to each property
    def update(self, to_update, new_values):
        """
        Updates the sprite image. Can be called with multiple values to change at once.
        Args:
            to_update (list of strings): The components to change, referencing the sprite properties.
            new_values (list of images): The new images for the components being changed .
        """

    # Renders the sprite to screen_surface (Surface) at position (Tuple)
    def render(self, screen_surface, position):

    # Save sprite with incrementing filename based on a .txt file of existing names
    def save_with_id(self, save_path, file_type):
        """
        Saves the sprite image to file with a unique name and records the name used in a text document.
        Whenever a sprite is saved the text document is checked to ensure that the same name is not used twice.
        If the document does not exist, one will be created.
        Args:
              save_path (string): The file path in which to save the image.
              file_type (string): The file extension to use when saving the image.
        """

""" CollisionParams: defines dimensions, offsets, etc of a collision box
                     used by objects."""
class CollisionParams:
    shape = 0  # Todo: Add sphere collision etc?
    x = 0  # X offset of collision box in tiles (relative to parent object)
    y = 0  # Y offset of collision box in tiles
    width = 0  # Width of collision box in tiles
    height = 0  # Height of collision box in tiles
    solid = False

    def __init__(self, solid, x, y, width, height)
    """init: initialises parameters, simple as"""

""" ObjectClass: main base class for objects that move and/or interact"""
class Object:
    x = 0  # in tile units (1.0 = 1 tile)
    y = 0  # in tile units
    x_velocity = 0.0  # rate of movement per axis in tiles/sec
    y_velocity = 0.0
    sprite = None  # current object sprite (todo: animations etc)
    collision = CollisionParams()  # collision dimensions, whether solid, etc

    def __init__(self)

    # primary (overloadable) functions
    def update(self, delta_time, player, object_list, map)
    """update: called once per frame
            delta_time = time passed since last frame in seconds,
            player = reference to the player
            object_list = list of all other objects,
            map = pointer to map class for collision checking, hazards etc
    """
    def render(self, screen)
    """render: called once per frame by GameClass during rendering
            screen = the surface to render to
    """

    # general functions
    def move(self, x, y)
    """move: moves this object by an offset of x and y
       if a collision occurs and this object is solid, the movement is blocked
    """

# CharacterClass: Class used for game characters including players and enemies
# todo individual sprite components?
class Character(Object):
    etc = 0  # Todo

# PlayerClass: Includes player movement characteristics, maybe HP, etc?
# todo expand based on battle mechanics, interactions, etc etc
class Player(Character):
    max_speed = 7.0  # The maximum running speed, in tiles/sec
    acceleration = 35.0  # Rate of acceleration while running, in tiles/sec/sec
    friction = 90.0  # Rate of slowdown when releasing movement keys
    sprite_parts = list() # etc

"""Fully extendible mapclass, image size and spawn weights can be edited"""
class MAP
    TILE_SIZE = 80  # size of game tiles in pixels

class MapClass:

    def __init__(self, seed=0):
        """Initilizes Map class with a seed"""

    def map_render(self):
        """Renders map array into img surface"""

    def create_sea(self):
        """Checks each on x,1 and 1,y to see if a sea starts, 1 is used as the array has a boarder"""

    def sea_flow_y(self, y):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on y axis"""

    def sea_flow_x(self, x):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on x axis"""

    def sea_render(self):
        """Blits sea images depending on what other places adjacent are seas and sand to some of the edges"""

    def sea_check(self, x, y):
        """Checks adjacent tiles for seas"""
