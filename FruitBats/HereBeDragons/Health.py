import pygame


red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()


class CurrentHealth:
    """Loads health bar images and updates it when being hit
    Now it only decreases upon key press.
    ToDo: set enemies's power AND
    scale red health bar accordingly to its maximum health

    Attributes:
        health_bar (pygame.image): red health bar image
        health (pygame.image): green (current) player's health
        player_health: manually set player maximum health
        """
    health_bar = pygame.image.load("ImageFiles/health_bar.png")
    health = pygame.image.load("ImageFiles/health.png")
    player_health = 100

    def __init__(self, screen):
        # Setting current player's health to maximum health
        self.current_health = self.player_health
        self.screen = screen

    def update(self):
        # Updates player's current health upon key press
        # ToDo: set enemies's power instead
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]:
            self.current_health -= 5
