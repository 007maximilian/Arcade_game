import arcade
from enums import SpriteDirection
from constants.physics import SHOOT_SPEED
from bullet import Bullet
import math


class Turret(arcade.Sprite):
    def __init__(self, direction, target):
        super().__init__()
        self.health = 20
        self.damage = 5
        self.timer = 0
        self.direction = direction
        self.bullets = arcade.SpriteList()
        self.target: arcade.Sprite = target
        self.setup_texture()

    def setup_texture(self):
        if self.direction == SpriteDirection.RIGHT:
            self.texture = arcade.load_texture('assets/baked/turret_mussle.png').flip_horizontally()
        else:
            self.texture = arcade.load_texture('assets/baked/turret_mussle.png')

    def shoot(self):
        if self.direction == SpriteDirection.RIGHT:
            return Bullet(texture='assets/sprites/bullet-1.png', angle=math.degrees(math.atan2(
                self.target.center_y - self.center_y, self.target.center_x - self.center_x
            )), x=self.center_x + self.width // 2, y=self.center_y)
        else:
            angle = math.degrees(math.atan2(
                self.target.center_y - self.center_y, self.target.center_x - self.center_x
            ))
            print(angle)
            return Bullet(texture='assets/sprites/bullet-1.png', angle=angle,
                          x=self.center_x - self.width // 2, y=self.center_y)

    def update(self, delta_time, target_x, target_y):
        self.target = arcade.Sprite()
        self.target.center_x = target_x
        self.target.center_y = target_y
        if self.count_distance() <= 48 * 8 and (
                (self.direction == SpriteDirection.RIGHT and self.center_x <= self.target.center_x) or
                (self.direction == SpriteDirection.LEFT and self.center_x >= self.target.center_x)
        ):
            self.timer += delta_time
            if self.timer > SHOOT_SPEED:
                bullet = self.shoot()
                self.timer = 0
                self.bullets.append(bullet)
                return bullet
        else:
            self.timer = 0
        return None

    def count_distance(self):
        return ((self.center_x - self.target.center_x) ** 2 +
                (self.center_y - self.target.center_y) ** 2) ** 0.5
