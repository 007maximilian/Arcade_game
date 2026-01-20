import arcade
from enums import SpriteDirection
from constants.physics import SHOOT_SPEED
from bullet import Bullet


class Turret(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 20
        self.damage = 5
        self.timer = 0
        self.direction = SpriteDirection.RIGHT

    def shoot(self):
        pass


    def update(self, delta_time):
        self.timer += delta_time
        if self.timer > SHOOT_SPEED:
            self.shoot()
            self.timer = 0