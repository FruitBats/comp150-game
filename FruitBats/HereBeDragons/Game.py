# Todo: Clean up unused imports
import time
import random
import math

import pygame

from Player import Player
from TestObject import PikachuStatue
from Attack import Swipe
from Enemy import *
from Map import MapClass, MAP
from Camera import Camera
from Menu import *
from Invent import *
from Fog import Fog

from Characters import Character
from Health import *
from Projectiles import Arrow
from Helpers import Vector
from SpriteGeneration import character_creation
from SpriteGeneration import Sprite

from Objects import *

class Game:
    """
    Main Game Class.

    Attributes:
        SCREEN_WIDTH (int): Width of screen in pixels.
        SCREEN_HEIGHT (int): Height of screen in pixels.

        delta_time (float): Time passed since the last frame.
        tick_time (float): Time at the start of the frame, in seconds since the game started.
        start_time (float): Initial time.clock() value on startup (OS-dependent)
        t0 (float): Current time.

        screen (pygame.Surface): Application screen.
        camera (Camera): The movable game camera.
        objects (list of Objects): A list of all the objects currently in the game. Objects are added and removed from this list when created or destroyed.
        player (Player): Pointer to the player character object.
        map (MapClass): The game map.
        menu (Menu): The main menu.

        quitting (bool): If the application is closing. Set to true when the user closes the program.
        game_over (bool): If the player has lost the game. Set to True when the player dies.
        fog_enabled (bool): If the fog of war/day-night cycle is active. Toggled with the f key.
    """

    SCREEN_WIDTH = 800  # defines screen width
    SCREEN_HEIGHT = 600  # defines screen height

    delta_time = 0  # time passed since last frame
    tick_time = 0   # time at the start of the frame, in seconds since the game started
    start_time = 0  # initial time.clock() value on startup (OS-dependent)
    t0 = time.time()

    screen = None   # PyGame screen
    camera = None   # movable camera object
    objects = None  # list of active objects in the game
    player = None   # pointer to the player object
    map = None      # MapClass object
    menu = None

    quitting = False
    game_over = False
    fog_enabled = True  # Enable or disbale fog for testing

    def __init__(self):
        self.run()

    def run(self):
        """Runs the game -- game closes when this function ends.
           To be called on startup."""
        # Init Python
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        pygame.display.set_caption('Here Be Dragons')

        # Init and run main menu
        self.menu = GameMenu(self.screen)
        self.menu.run()

        # Init game components
        self.initalise_components()

        # Init main game parameters
        self.start_time = time.clock()
        self.delta_time = 0.0

        # Main loop
        fire_time = 0

        while not self.quitting:

            # Update timing
            last_time = self.tick_time
            self.tick_time = time.clock()

            self.delta_time = self.tick_time - last_time

            # Update fog
            self.fog.update()

            # Cap delta time to 10FPS to prevent gamebreaking bugs
            if self.delta_time >= 0.1:
                self.delta_time = 0.1

            # Perform PyGame event loop
            events = pygame.event.get()  # makes event.get a variable so it can be passed to other functions
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.quitting = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    self.fog_enabled = not self.fog_enabled

            # Checks if the player's is dead to call game over screen
            if self.health.current_health <= 0:
                self.game_over = True
                self.run_game_over()

            # Update objects (including player)
            for obj in self.objects:
                obj.update(self.delta_time, self.player, self.objects, map)

                if obj.dead:
                    # Remove object from existence
                    self.objects.remove(obj)

            # Update camera
            self.camera.update(self.delta_time, self.player, self.objects, map)

            # Render (todo: move into separate Render class?)
            self.screen.blit(self.map.img, (-self.camera.x * MAP.TILE_SIZE, -self.camera.y * MAP.TILE_SIZE))

            for obj in self.objects:
                obj.render(self.screen, self.camera)
            self.player.render(self.screen, self.camera)

            # Render fog
            if self.fog_enabled:
                self.fog.render(self)

            # Draw health bar
            self.health.update()
            self.screen.blit(self.health.health_bar, (5, 5))
            for health1 in range(self.health.current_health):
                self.screen.blit(self.health.health, (health1 + 7, 7))

            # Update inventory and render
            self.invent.update(events)
            self.invent.render_invent(self.screen, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

            # Splat to screen
            pygame.display.flip()

    def run_game_over(self):
        message = CurrentHealth(self.screen)
        key_pressed = pygame.key.get_pressed()
        while self.game_over is True:
            self.screen.fill(white)
            message.message_to_screen("Game Over", red, -20, size="large")
            message.message_to_screen("Press any key to get into menu", black, 50)
            pygame.display.update()
            if key_pressed[pygame.KEYDOWN]:
                self.game_over = False
                self.run_game()
        pygame.display.flip()

    def run_game(self):
        if self.game_over is False:
            self.run()

    def initalise_components(self):
        """
        Initialises the following game components.

        Components:
            map
            fog
            player
            invent
            health
            objects
            camera
        """

        # Init character creation screen if new game is started
        if self.menu.new_game:
            character_creation.load_creation_window(self.screen, (MAP.TILE_SIZE, MAP.TILE_SIZE))

        # Init map
        self.map = MapClass(seed=10)
        #self.map = MapClass()

        # Init fog
        self.fog = Fog(self.t0, 10, 5)

        # Init character
        self.player = Player(0.5, 0.5, self.map)
        if Sprite.deserialize("player_sprite") is not None:
            self.player.sprite = Sprite.deserialize("player_sprite").image

        # Init inventory
        self.invent = Inventory(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Init health
        self.health = CurrentHealth(self.screen)

        # Init objects and player
        self.objects = list()
        self.objects.append(self.player)  # player is always the first item

        # Init camera
        self.camera = Camera(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Add test Pikachi (Pikachodes?) (plural?)
        for i in xrange(10):
            self.objects.append(PikachuStatue(random.randint(0, 10), random.randint(0, 10)))        # Add test sword
        self.objects.append(Swipe(3, 3))

        # Spawn test arrow enemies
        for i in xrange(0, 10):
            self.objects.append(ArrowEnemy(random.randint(0, 20), random.randint(0, 20), 1, self.map))

        # self.objects.append(ChaserEnemy(3, 3))  # Testing with new enemy type
        # self.objects.append(ChaserEnemy(3, 3, self.map))  # Testing with new enemy type
        self.objects.append(Enemy(3, 3, 10, self.map))


# Startup game!
Game()
