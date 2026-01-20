import arcade
import math
from enums import SpriteDirection
from bullet import Bullet


class Gun(arcade.Sprite):
    def __init__(self, hero, w, h, spritesheet, columns, frames):
        super().__init__()
        self.owner = hero
        self.spritesheet = arcade.SpriteSheet(
            spritesheet
        )
        self.textures = self.spritesheet.get_texture_grid(
            (w, h),
            columns=columns,
            count=frames
        )
        self.texture = self.textures[0]
        self.curr_index = 0
        self.offset_x = 0
        self.offset_y = 0
        self.direction = SpriteDirection.RIGHT

    def flip(self):
        for i in range(len(self.textures)):
            self.textures[i] = self.textures[i].flip_horizontally()


class Pistol(Gun):
    def __init__(self, owner):
        super().__init__(owner, 48, 48, 'assets/spritesheets/glock_pistol.png', 4, 4)
        self.radius = self.width // 2
        self.damage = 10

    def update(self, delta_time):
        self.direction = self.owner.direction
        self.texture = self.textures[self.curr_index]
        if self.direction == SpriteDirection.RIGHT:
            self.center_x = self.owner.center_x + self.offset_x - 23
        else:
            self.center_x = self.owner.center_x - self.offset_x + 23
        self.center_y = self.owner.center_y + self.offset_y

    def rotate(self, angle):
        if self.direction == SpriteDirection.RIGHT:
            self.angle = 360 - math.degrees(angle)
            self.offset_x = self.owner.width // 2 + math.cos(angle) * self.radius
            self.offset_y = math.sin(angle) * self.radius
        else:
            angle = math.pi - angle
            self.angle = math.degrees(angle)
            self.offset_x = self.owner.width // 2 + math.cos(angle) * self.radius
            self.offset_y = math.sin(angle) * self.radius
    
    def shoot(self):
        angle = math.radians(self.angle)
        bullet = Bullet(texture='assets/sprites/bullet-1.png', angle=360 - self.angle,
                        x=self.center_x + self.width // 2 * math.cos(360 - angle),
                        y=self.center_y + self.height // 2 * math.sin(360 - angle), damage=10)
        return bullet
