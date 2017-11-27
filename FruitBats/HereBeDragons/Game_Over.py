import pygame

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)


class GameOver:
    """
    Displaying a 'game over' screen upon death

    Attributes:
        fonts with different text size
    """
    small_font = pygame.font.SysFont("comicsansms", 25)
    medium_font = pygame.font.SysFont("comicsansms", 50)
    large_font = pygame.font.SysFont("comicsansms", 80)

    def __init__(self, scr_width, scr_height, screen, in_game):
        self.screen_width = scr_width
        self.screen_height = scr_height
        self.screen = screen
        self.in_game = in_game

    def text_objects(self, text, color, size):
        text_surface = None

        # Sets the text to the chosen text size
        if size == "small":
            text_surface = self.small_font.render(text, True, color)
        elif size == "medium":
            text_surface = self.medium_font.render(text, True, color)
        elif size == "large":
            text_surface = self.large_font.render(text, True, color)

        return text_surface, text_surface.get_rect()

    def message_to_screen(self, text, color, y_displace=0, size="small"):

        # Sets the given text to the screen upon death
        text_surf, text_rect = self.text_objects(text, color, size)
        text_rect.center = (self.screen_width / 2),\
                           (self.screen_height / 2) + y_displace
        self.screen.blit(text_surf, text_rect)

    def game_over(self):
        key_pressed = pygame.key.get_pressed()
        if self.in_game is False:
            self.screen.fill(white)
            self.message_to_screen("Game Over", red, -20, size="large")
            self.message_to_screen("Press any key to return into menu",
                                   black, 50)
            pygame.display.update()
            if key_pressed[pygame.KEYDOWN]:
                self.in_game = True
            pygame.display.flip()
