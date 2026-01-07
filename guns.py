import arcade
from enums import SpriteDirection


class DefaultGun(arcade.Sprite):
    def __init__(self, owner=None):
        super().__init__()
        self.scale = 0.5
        self.direction = SpriteDirection.RIGHT
        self.owner = owner
    
    def process_spritesheet(self, path, columns, frame_w, frame_h):
        self.spritesheet = arcade.load_spritesheet(path)
        return self.spritesheet.get_texture_grid(
            (frame_w, frame_h),
            columns=columns,
            count=columns
        )

    def init_offset(self, offset_x):
        self.offset = offset_x


class PistolGun(DefaultGun):
    def __init__(self, owner=None):
        super().__init__(owner=owner)
        self.textures = self.process_spritesheet(
            'assets/spritesheets/glok_pistol.png',
            4,
            48, 48
        )
        print(type(self.width))
        self.init_offset(24 + 24 * 0.5)
        self.texture = self.textures[0]
        self.curr_texture = 0
    
    def flip(self):
        for i in range(len(self.textures)):
            self.textures[i] = self.textures[i].flip_horizontally()
    
    def update(self, delta_time):
        self.texture = self.textures[self.curr_texture]
        self.direction = self.owner.direction
        if self.direction == SpriteDirection.RIGHT:
            self.center_x = self.owner.center_x + self.offset
        else:
            self.center_x = self.owner.center_x - self.offset
        self.center_y = self.owner.center_y
