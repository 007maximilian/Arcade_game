import arcade
from enums import SpriteDirection
from guns import Pistol
import math


class Hero(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture('assets/sprites/character.png')
        self.scale=1.0
        self.direction = SpriteDirection.RIGHT
        self.keys = set()
        self.gun: None | Pistol = None
    
    def update(self, delta_time):
        if self.change_x < 0 and self.direction == SpriteDirection.RIGHT:
            self.direction = SpriteDirection.LEFT
            self.texture = self.texture.flip_horizontally()
            if self.gun is not None:
                self.gun.flip()
                gun_angle = self.gun.angle
                gun_pi_angle = math.radians(360 - gun_angle)
                self.gun.direction = self.direction
                self.gun.rotate(gun_pi_angle)
        elif self.change_x > 0 and self.direction == SpriteDirection.LEFT:
            self.direction = SpriteDirection.RIGHT
            self.texture = self.texture.flip_horizontally()
            if self.gun is not None:
                self.gun.flip()
                gun_angle = self.gun.angle
                gun_pi_angle = math.pi - math.radians(gun_angle)
                self.gun.direction = self.direction
                self.gun.rotate(gun_pi_angle)