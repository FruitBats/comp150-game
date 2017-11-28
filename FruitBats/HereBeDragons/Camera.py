from Map import MAP
from Player import *


class Camera:
    """Camera object, defining the position and proportions of the camera in the game world.

        Attributes:
            x, y (float): Coordinates of the camera, measured in tiles
            view_width, view_height (float): Dimensions of the viewport, in pixels
    """
    x = 0
    y = 0
    view_width = 0
    view_height = 0

    def __init__(self, (view_width, view_height)):
        """Sets up the camera
            Args:
                (view_width, view_height): Dimensions of the camera viewport
        """
        self.view_width = view_width
        self.view_height = view_height

    def update(self, player):
        """Per-frame update: Moves camera to player, capping at the edges of the map
            Args:
                player (Player reference): The player
        """
        if player.state == PlayerState.ALIVE:
            self.x = player.x + float(-player.sprite.get_width() - self.view_width) / MAP.TILE_SIZE / 2
            self.y = player.y + float(-player.sprite.get_height() - self.view_height) / MAP.TILE_SIZE / 2
            if player.sprite_origin is not None:
                self.x = player.x + (-float(player.sprite_origin.x - player.sprite.get_width() / 2) - (float(self.view_width) / 2)) / MAP.TILE_SIZE
                self.y = player.y + (-float(player.sprite_origin.y - player.sprite.get_height() / 2) - (float(self.view_height) / 2)) / MAP.TILE_SIZE

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.view_width / MAP.TILE_SIZE >= MAP.SIZE_X:
            self.x = MAP.SIZE_X - (self.view_width / MAP.TILE_SIZE)
        if self.y + self.view_height / MAP.TILE_SIZE >= MAP.SIZE_Y:
            self.y = MAP.SIZE_Y - (self.view_height / MAP.TILE_SIZE)
