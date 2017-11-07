import time
import random

import pygame

from Player import Player
from TestObject import PikachuStatue
from Attack import Swipe
from Enemy import ChaserEnemy
from Map import MapClass

from SpriteGeneration import character_creation
from SpriteGeneration import Sprite

class Game:
    delta_time = 0  # time passed since last frame
    tick_time = 0   # time at the start of the frame, in seconds since
                    # the game started
    start_time = 0  # initial time.clock() value on startup (OS-dependent)
    screen = None   # PyGame screen
    objects = None  # list of active objects in the game
    player = None   # pointer to the player object
    map = None    # MapClass object
    quitting = False
    SCREEN_WIDTH = 800 #640
    SCREEN_HEIGHT = 600 #480

    new_game = True    # If the player needs to create a character or not. For testing only currently.

    def __init__(self):
        self.run()

    def run(self):
        """Runs the game -- game closes when this function ends.
           To be called on startup."""
        # Init Python
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                               self.SCREEN_HEIGHT))

        if self.new_game:
            # Character creation goes here
            character_creation.load_creation_window(self.screen)

        # Init map
        self.map = MapClass(seed=10)

        # Init character
        self.player = Player(0, 0)
        if Sprite.deserialize("player_sprite") is not None:
            self.player.sprite = Sprite.deserialize("player_sprite").image

        # Init objects and player
        self.objects = list()
        self.objects.append(self.player)  # player is always the first item

        # Add test Pikachi (Pikachodes?) (plural?)
        for i in xrange(10):
            self.objects.append(PikachuStatue(random.randint(0, 10),
                                              random.randint(0, 10)))
        # Add test sword
        self.objects.append(Swipe(3, 3))

        # Init test enemy at 5,5
        self.objects.append(ChaserEnemy(3, 3))

        # Init main game parameters
        self.start_time = time.clock()
        self.delta_time = 0.0

        # Main loop
        while not self.quitting:
            # Update timing
            last_time = self.tick_time
            self.tick_time = time.clock()

            self.delta_time = self.tick_time - last_time

            # Cap delta time to 10FPS to prevent gamebreaking bugs
            if self.delta_time >= 0.1:
                self.delta_time = 0.1

            # Perform PyGame event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                        (event.type == pygame.KEYDOWN and
                         event.key == pygame.K_ESCAPE):
                    self.quitting = True

            # Update objects (including player)
            for obj in self.objects:
                obj.update(self.delta_time, self.player, self.objects, None)

            # Render (todo: move into separate Render class?)
            self.screen.blit(self.map.img, (0, 0))


            for obj in self.objects:
                obj.render(self.screen)
            self.player.render(self.screen)

            # Splat to screen
            pygame.display.flip()

# Startup game!
Game()
