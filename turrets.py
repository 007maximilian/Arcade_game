import arcade
from enums import SpriteDirection
from constants.physics import SHOOT_SPEED
from bullet import Bullet
import math


class Turret(arcade.Sprite):
    def __init__(self, direction, target):
        super().__init__()
        self.health = 100
        self.damage = 5
        self.timer = 0
        self.direction = direction
        self.bullets = arcade.SpriteList()
        self.target: arcade.Sprite = target
        self.switch_animation_timer = 0.05
        self.dead = False
        self.anim_frames = arcade.SpriteSheet(
            'assets/spritesheets/turret_crash.png'
        ).get_texture_grid(
            (48, 48),
            columns=7,
            count=7
        )
        self.setup_texture()
        self.curr_texture = 0
        self.texture = self.anim_frames[self.curr_texture]

    def setup_texture(self):
        if self.direction == SpriteDirection.RIGHT:
            for i in range(len(self.anim_frames)):
                self.anim_frames[i] = self.anim_frames[i].flip_horizontally()

    def shoot(self):
        if not self.dead:
            if self.direction == SpriteDirection.RIGHT:
                return Bullet(texture='assets/sprites/bullet-1.png', angle=math.degrees(math.atan2(
                    self.target.center_y - self.center_y, self.target.center_x - self.center_x
                )), x=self.center_x + self.width // 2, y=self.center_y, damage=10)
            else:
                angle = math.degrees(math.atan2(
                    self.target.center_y - self.center_y, self.target.center_x - self.center_x
                ))
                return Bullet(texture='assets/sprites/bullet-1.png', angle=angle,
                              x=self.center_x - self.width // 2, y=self.center_y, damage=self.damage)
        return None

    def update(self, delta_time, target_x, target_y):
        if not self.dead:
            self.target = arcade.Sprite()
            self.target.center_x = target_x
            self.target.center_y = target_y
            if self.count_distance() <= 48 * 12 and (
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
        else:
            if self.curr_texture != 6:
                self.timer += delta_time
                if self.timer > self.switch_animation_timer:
                    self.timer = 0
                    self.curr_texture += 1
                self.texture = self.anim_frames[self.curr_texture]
        return None

    def count_distance(self):
        return ((self.center_x - self.target.center_x) ** 2 +
                (self.center_y - self.target.center_y) ** 2) ** 0.5
