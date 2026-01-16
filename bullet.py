import arcade
from constants.physics import BULLET_SPEED
import math


class Bullet(arcade.Sprite):
    def __init__(self, x, y, angle, texture):
        super().__init__(texture, center_x=x, center_y=y)
        self.change_x = math.cos(math.radians(angle)) * BULLET_SPEED
        self.change_y = math.sin(math.radians(angle)) * BULLET_SPEED
    
    def update(self, delta_time):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time