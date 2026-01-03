import arcade
from constants.window import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from constants.physics_constants import (
    COYOTE_TIME, JUMP_BUFFER, MAX_JUMPS, GRAVITY,
    MOVE_SPEED, JUMP_SPEED, CAMERA_LERP
)
import math


class Bullet(arcade.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y, speed=800, damage=10):
        super().__init__()
        self.texture = arcade.load_texture(":resources:/images/space_shooter/laserBlue01.png")
        self.center_x = start_x
        self.center_y = start_y
        self.speed = speed
        self.damage = damage
        
        # Рассчитываем направление
        x_diff = target_x - start_x
        y_diff = target_y - start_y
        angle = math.atan2(y_diff, x_diff)
        # И скорость
        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed
        # Если текстура ориентирована по умолчанию вправо, то поворачиваем пулю в сторону цели
        # Для другой ориентации нужно будет подправить угол
        self.angle = math.degrees(-angle)  # Поворачиваем пулю
        
    def update(self, delta_time):
        # Удаляем пулю, если она ушла за экран
        if (self.center_x < 0 or self.center_x > SCREEN_WIDTH or
            self.center_y < 0 or self.center_y > SCREEN_HEIGHT):
            self.remove_from_sprite_lists()

        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time


class MainGame(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.walls = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.engine: None | arcade.PhysicsEnginePlatformer = None
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS
    
    def setup(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.wall_structure = arcade.load_texture(":resources:images/tiles/grass.png")
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    sprite = arcade.Sprite()
                    sprite.texture = self.wall_structure
                    sprite.center_x = j * TILE_SIZE + TILE_SIZE // 2
                    sprite.center_y = SCREEN_HEIGHT - i * TILE_SIZE - TILE_SIZE // 2
                    sprite.scale = 0.3125
                    self.walls.append(sprite)
        self.player = arcade.Sprite()
        self.player_texture = arcade.load_texture(":resources:images/enemies/ladybug.png")
        self.player.texture = self.player_texture
        self.player.scale = 0.3125
        self.player.center_x = 100
        self.player.center_y = 260
        self.player_list.append(self.player)

        self.engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            walls=self.walls,
            gravity_constant=GRAVITY
        )
        self.camera = arcade.camera.Camera2D()
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.walls.draw()
        self.player_list.draw()
        self.bullet_list.draw()
    
    def on_key_press(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = True
        elif key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            self.jump_pressed = True
            self.jump_buffer_timer = JUMP_BUFFER
    
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.A):
            self.left = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down = False
        elif key in (arcade.key.SPACE, arcade.key.UP, arcade.key.W):
            self.jump_pressed = False
            if self.player.change_y > 0:
                self.player.change_y *= 0.45
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                x - (SCREEN_WIDTH // 2 - self.player.center_x),
                y - (SCREEN_HEIGHT // 2 - self.player.center_y)
            )
            self.bullet_list.append(bullet)
    
    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.player.change_x = move

        grounded = self.engine.can_jump(y_distance=6)
        if grounded:
            self.time_since_ground = 0
            self.jumps_left = MAX_JUMPS
        else:
            self.time_since_ground += delta_time

        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= delta_time

        want_jump = self.jump_pressed or (self.jump_buffer_timer > 0)
        if want_jump:
            can_coyote = (self.time_since_ground <= COYOTE_TIME)
            if grounded or can_coyote:
                self.engine.jump(JUMP_SPEED)
                self.jump_buffer_timer = 0
        
        position = (
            self.player.center_x,
            self.player.center_y
        )
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            position,
            CAMERA_LERP
        )

        self.engine.update()
        self.bullet_list.update()
