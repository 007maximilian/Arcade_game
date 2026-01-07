import arcade
from enums import SpriteDirection


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/sprites/character.png')
        self.scale=1.0
        self.direction = SpriteDirection.RIGHT
        self.keys = set()
    
    def update(self, delta_time):
        if self.change_x < 0 and self.direction == SpriteDirection.RIGHT:
            self.direction = SpriteDirection.LEFT
            self.texture = self.texture.flip_horizontally()
        elif self.change_x > 0 and self.direction == SpriteDirection.LEFT:
            self.direction = SpriteDirection.RIGHT
            self.texture = self.texture.flip_horizontally()