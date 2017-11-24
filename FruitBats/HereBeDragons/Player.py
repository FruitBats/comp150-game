# Standard imports
import math

# Third party imports
import pygame

# Project imports
from Characters import Character
from Map import *
from Collision import CollisionBox
from Helpers import *
from DynaSword import DynaSword
import Projectiles


class PlayerState:
    ALIVE = 0
    DEAD = 1


class Player(Character):
    state = PlayerState.ALIVE  # (PlayerState const) Current state
    max_speed = 7.0  # (float) The maximum running speed, in tiles/sec
    acceleration = 35.0  # (float) Rate of acceleration while running, in tiles/sec/sec
    friction = 70.0  # (float) Rate of slowdown when releasing movement keys
    velocity = None  # (Vector) Rate of movement per axis in tiles/sec
    dynasword = None  # (DynaSword) Pointer to dynasword
    respawn_timer = 0  # (float) Current time til respawn in seconds

    def __init__(self, x, y, parent_map):
        """Init: Loads default player sprite and scales it up"""
        # Load character image
        self.sprite = pygame.image.load('graphics/game_character.png')
        self.parent_map = parent_map

        # Setup collision box and sprite origin
        size = (MAP.PLAYER_SCALE, MAP.PLAYER_SCALE)

        self.sprite_origin = Vector((size[0] / 2), (size[1] / 2))
        self.collision = CollisionBox((5, 5), (size[0] - 10, size[1] - 10),
                                      True)
        self.hand_x = 4 * MAP.RATIO
        self.hand_y = 52 * MAP.RATIO

        # Do initial spawn
        self.spawn_x = x
        self.spawn_y = y

        self.respawn()

    def update(self, delta_time, player, object_list, map):
        if self.state == PlayerState.ALIVE:
            # Perform updates
            self.update_movement(delta_time, player, object_list, map)
            self.update_attacks(delta_time, player, object_list, map)
        else:
            # Initiate beauty
            self.update_majestic_death_animation(delta_time, player,
                                                 object_list, map)

    def update_movement(self, delta_time, player, object_list, map):
        # Perform character movement
        key_pressed = pygame.key.get_pressed()

        # Make a normalised vector of movement based on user input
        move = Vector(0.0, 0.0)

        if key_pressed[pygame.K_w]:
            move.y -= 1.0
        if key_pressed[pygame.K_s]:
            move.y += 1.0
        if key_pressed[pygame.K_d]:
            move.x += 1.0
        if key_pressed[pygame.K_a]:
            move.x -= 1.0

        # If the movement vector is nonzero, stretch it by the player's acceleration factor to move; otherwise, change it to an opposite vector for friction
        move_length = move.length()
        current_speed = self.velocity.length()

        # Do player acceleration
        if move_length > 0.000:
            # Scale movement vector to acceleration speed
            move.normalise(self.acceleration + self.friction)  # + deceleration to fight the friction that immediately follows

        # Do player deceleration
        deceleration_speed = self.friction

        # Cap the deceleration speed to <= current_speed (to avoid boosting in the opposite direction!)
        if current_speed < deceleration_speed * delta_time:
            deceleration_speed = current_speed / delta_time

        if current_speed > 0:
            move -= self.velocity * (deceleration_speed /
                                     self.velocity.length())

        # Accelerate or decelerate accordingly
        self.velocity += move * delta_time

        # Cap player speed
        if self.velocity.length() > self.max_speed:
            self.velocity.normalise(self.max_speed)

        # Move player by velocity
        moved = self.move(tuple(self.velocity * delta_time), object_list)

        # Stop velocity if player collided with something
        if not moved:
            self.velocity = Vector(0, 0)

    def update_attacks(self, delta_time, player, object_list, map):
        # Create sword
        # TODO: Consult Michael about this. There should be a way to call
        # game.CreateObject or something like that. Should be done on init.
        if self.dynasword is None:
            self.dynasword = DynaSword(self.x, self.y, self)
            object_list.append(self.dynasword)

        # Basic attack
        if pygame.mouse.get_pressed()[0]:
            self.dynasword.attack()
        if pygame.mouse.get_pressed()[2]:
            self.dynasword.block()
        if pygame.mouse.get_pressed()[1]:
            self.dynasword.boomerang()

    def update_majestic_death_animation(self, delta_time, player,
                                        object_list, map):
        """Fly majestically. See Object.update for argument info"""
        self.sprite_angle += 1400 * delta_time
        self.move(tuple(self.velocity * delta_time), object_list)

        self.respawn_timer -= delta_time
        if self.respawn_timer <= 0:
            # Respawn
            self.respawn()

    def die(self):
        """Called on player death"""
        if self.state == PlayerState.ALIVE:
            # Change player state to dead, reconstruct that famous Titanic scene and and setup respawn variables
            self.state = PlayerState.DEAD
            self.respawn_timer = 1
            self.velocity.point_at_angle(random.randrange(0, 360), 10)
            self.collision.solid = False

    def respawn(self):
        """Respawn function, automatically called after a player has died"""
        self.max_health = 1
        self.health = self.max_health
        self.state = PlayerState.ALIVE
        self.respawn_timer = 0
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.sprite_angle = 0
        self.velocity = Vector(0, 0)
        self.collision.solid = True