import pygame
import sys

from Menu import GameMenu

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()


class CurrentHealth:
    health_bar = pygame.image.load("ImageFiles/health_bar.png")
    health = pygame.image.load("ImageFiles/health.png")
    player_health = 100
    smallfont = pygame.font.SysFont("comicsansms", 25)
    medfont = pygame.font.SysFont("comicsansms", 50)
    largefont = pygame.font.SysFont("comicsansms", 80)
    winning = True

    def __init__(self, screen):
        self.current_health = self.player_health
        self.screen = screen

    def text_objects(self, text, color, size):
        text_surface = None

        if size == "small":
            text_surface = self.smallfont.render(text, True, color)
        elif size == "medium":
            text_surface = self.medfont.render(text, True, color)
        elif size == "large":
            text_surface = self.largefont.render(text, True, color)

        return text_surface, text_surface.get_rect()

    def message_to_screen(self, text, color, y_displace=0, size="small"):
        text_surf, text_rect = self.text_objects(text, color, size)
        text_rect.center = (800 / 2), (600 / 2) + y_displace
        self.screen.blit(text_surf, text_rect)

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_1]:
            self.current_health -= 5
