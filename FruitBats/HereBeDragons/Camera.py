from Map import MAP


class Camera:
    x = 0            # x in tiles
    y = 0            # y in tiles
    view_width = 0   # viewport width in pixels
    view_height = 0  # viewport height in pixels

    def __init__(self, view_width, view_height):
        self.view_width = view_width
        self.view_height = view_height

    def update(self, delta_time, player, object_list, map):
        self.x = player.x - (float(self.view_width - player.sprite.get_width())
                             / 2 / MAP.TILE_SIZE)
        self.y = player.y - (float(self.view_height - player.sprite.get_height())
                             / 2 / MAP.TILE_SIZE)

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x + self.view_width / MAP.TILE_SIZE >= MAP.SIZE_X:
            self.x = MAP.SIZE_X - (self.view_width / MAP.TILE_SIZE)
        if self.y + self.view_height / MAP.TILE_SIZE >= MAP.SIZE_Y:
            self.y = MAP.SIZE_Y - (self.view_height / MAP.TILE_SIZE)
