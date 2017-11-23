import pygame


class Button:

    """
    Button Class. This class creates a simple button that can be passed multiple functions to execute when clicked.

    Attributes:
        button (pygame.Surface): The surface used to represent the button.
        button_bounds (pygame.Rect): The rectangle formed by the button.
        parent_surface (pygame.Surface): The surface onto which to blit the button.
    """

    button = None
    button_bounds = None
    parent_surface = None

    def __init__(self, size, position, colour, parent_surface, function, function_args, message):
        """
        Constructor method. Draws a button on a surface.

        Args:
            size (tuple): Size of the button.
            position (tuple): The position at which to draw the button.
            colour (tuple): The RGB code for the colour of the button.
            parent_surface (pygame.Surface): The surface on which to draw the button.
            function (list of function names): The function to be run when the button is pressed. Note, do not use () when
                                               passing the function name or it will try and execute the function.
            function_args (list of lists): Each list within this list contains the arguments to be passed to a function. The value at [0] will be the instance of
                                           the class passing the value, so only [1] or higher should  be used.
            message (string): Message to display on the button. Currently not implemented!
        """

        self.size = size
        self.position = position
        self.colour = colour
        self.parent_surface = parent_surface
        self.function = function
        self.function_args = function_args
        self.message = message

        self.button = pygame.Surface(self.size)
        self.button_bounds = self.button.get_rect()
        self.draw()

    def on_click(self):
        """
        Method to be executed when the button is pressed. self.function is called with the arguments passed to the
        button when instantiated. The * passes all the items in button_args as arguments.
        """

        print("clicked")

        # If a function has been passed to the button, iterate through the list of functions
        if self.function is not None:
            for i in range(0, len(self.function)):

                # Check if arguments have been passed for the function, if not, call without arguments
                if self.function_args[i] is not None:
                    self.function[i](*self.function_args[i])

                else:
                    self.function[i]()

    def check_click(self, mouse_position):
        """
        Checks if the mouse cursor is within the button. This should be called whenever the mouse is clicked.

        Args:
            mouse_position (tuple): The position of the mouse on the screen at the time the mouse button was pressed.
        """

        if self.button_bounds.collidepoint(mouse_position):
            self.on_click()

    def draw(self):
        """Draws the button onto another surface"""

        self.button.fill(self.colour)
        self.button_bounds.x = self.position[0]
        self.button_bounds.y = self.position[1]
        self.parent_surface.blit(self.button, self.position)



