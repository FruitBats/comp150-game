# Todo: Clean up unused imports
import time
import random
import math

import pygame

from Player import Player
from TestObject import PikachuStatue
from Attack import Swipe
from Enemy import ChaserEnemy
from Enemy import Enemy # Mango testing
from Map import MapClass, MAP
from Camera import Camera
from Menu import *
from Invent import *
from Fog import Fog
from Helpers import Vector
from Projectiles import Arrow

from SpriteGeneration import character_creation
from SpriteGeneration import Sprite


class Game:
    delta_time = 0  # time passed since last frame
    tick_time = 0   # time at the start of the frame, in seconds since
                    # the game started
    start_time = 0  # initial time.clock() value on startup (OS-dependent)
    t0 = time.time()
    screen = None   # PyGame screen
    camera = None   # movable camera object
    objects = None  # list of active objects in the game
    player = None   # pointer to the player object
    map = None      # MapClass object
    quitting = False
    menu = None
    SCREEN_WIDTH = 800  # 640
    SCREEN_HEIGHT = 600  # 480

    new_game = True    # If the player needs to create a character or not. For testing only currently.

    def __init__(self):
        self.run()

    def run(self):
        """Runs the game -- game closes when this function ends.
           To be called on startup."""
        # Init Python
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        pygame.display.set_caption('Frontier')

        menu = GameMenu(self.screen)
        menu.run()

        if self.new_game:
            # Character creation goes here
            character_creation.load_creation_window(self.screen)

        # Init map
        self.map = MapClass(seed=10)

        # Init fog
        self.fog = Fog()

        # Init character
        self.player = Player(0, 0)
        if Sprite.deserialize("player_sprite") is not None:
            self.player.sprite = Sprite.deserialize("player_sprite").image

        # Init inventory
        self.invent = Inventory()

        # Init objects and player
        self.objects = list()
        self.objects.append(self.player)  # player is always the first item

        # Init camera
        self.camera = Camera(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        # Add test Pikachi (Pikachodes?) (plural?)
        for i in xrange(10):
            pika = PikachuStatue(random.randint(0, 10), random.randint(0, 10))
            self.objects.append(pika)
            pika.debug_render_hitbox = True
        # Add test sword
        self.objects.append(Swipe(3, 3))

        # Init test enemy at 5,5
        # self.objects.append(ChaserEnemy(3, 3))  # Testing with new enemy type
        #self.objects.append(Enemy(3, 3, 10))

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

            # Change day to true or false every #seconds, calls fog function to update surface
            seconds = 10
            t1 = time.time()
            dt = t1 - self.t0  # gets difference in start time and current time
            if dt >= seconds:
                self.fog.day = not self.fog.day
                self.t0 = t1  # resets timer variable
                self.fog.lift_fog()

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
                obj.update(self.delta_time, self.player, self.objects, map)

            # Update camera
            self.camera.update(self.delta_time, self.player, self.objects, map)

            # Render (todo: move into separate Render class?)
            self.screen.blit(self.map.img, (-self.camera.x * MAP.TILE_SIZE, -self.camera.y * MAP.TILE_SIZE))

            for obj in self.objects:
                obj.render(self.screen, self.camera)
            self.player.render(self.screen, self.camera)

            # Render fog
            #self.fog.render_fog(self)

            # Test fire arrow
            fire_time -= self.delta_time
            if fire_time <= 0:
                fire_time = 1
                distance = 3
                ang = float(random.randrange(0, 360, 1))
                spawn_pos = (self.player.x + math.sin(math.radians(ang)) * distance, self.player.y + math.cos(math.radians(ang)) * distance)
                velocity = Vector(0, 0)
                velocity.point_at_angle(ang - 180, 5)
                self.objects.append(Arrow(spawn_pos, tuple(velocity), ang))

            # Update inventory
            self.invent.update()
            self.invent.render_invent(self.screen)

            # Splat to screen
            pygame.display.flip()

# Startup game!
Game()
