import pygame
import time


class CurrentHealth:
    health_bar = pygame.image.load("ImageFiles/health_bar.png")
    health = pygame.image.load("ImageFiles/health.png")
    player_health = 100

    def __init__(self):
        self.current_health = self.player_health

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]:
            self.current_health -= 1
