import arcade
from constants.physics import (
    COYOTE_TIME, JUMP_BUFFER, JUMP_PAD_BOOST,
    MAX_JUMPS, GRAVITY, MOVE_SPEED, JUMP_SPEED,
    LADDER_SPEED, CAMERA_LERP
) # everything yep
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, TILE_SCALING
from _hero import Hero
from enums import SpriteDirection
from guns import Pistol
import math
from pyglet.graphics import Batch


class GameView(arcade.View):
    def on_show_view(self): # jus like init in arcade.View
        arcade.set_background_color(arcade.color.GRAY)
        self.player_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.gui_camera = arcade.camera.Camera2D()
        self.world_camera = arcade.camera.Camera2D()
        self.hero: None | Hero = None

        self.engine: None | arcade.PhysicsEnginePlatformer = None
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

        self.bullet_list = arcade.SpriteList()
        self.breakable = arcade.SpriteList()
        self.deadable = arcade.SpriteList()
        self.specials = arcade.SpriteList()

        self.setup()
    
    def setup(self):
        self.hero = Hero()
        self.hero.center_x = 48
        self.hero.center_y = 200
        self.player_list.append(self.hero)
        # someday need to write sth like tilemap loading...
        # initialize better after tilemaps
        self.world_height = 5000
        self.world_width = 5000

        self.gun = Pistol(self.hero)
        self.gun_list.append(self.gun)
        self.hero.gun = self.gun
        self.gun.rotate(0)

        self.tilemap = arcade.load_tilemap("assets/maps/test_map.tmx", scaling=TILE_SCALING)
        self.collision_list = self.tilemap.sprite_lists['collision']
        self.deadable = self.tilemap.sprite_lists['deadable']
        self.specials = self.tilemap.sprite_lists['specials']
        self.breakable = self.tilemap.sprite_lists['breakable']
        self.walls = self.tilemap.sprite_lists['walls']

        self.engine = arcade.PhysicsEnginePlatformer(
            self.hero,
            walls=self.collision_list,
            gravity_constant=GRAVITY
        ) # MAKE PLATFORMS YEE

        self.die_sound = arcade.load_sound(':resources:/sounds/hit2.wav')

        self.count = 0

        self.batch = Batch()

        self.text = arcade.Text(
            f'Count: {self.count}',
            10, SCREEN_HEIGHT - 30,
            arcade.color.GOLD,
            20,
            batch=self.batch
        )
    
    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.player_list.draw()
        self.gun_list.draw()
        self.breakable.draw()
        self.specials.draw()
        self.walls.draw()
        self.deadable.draw()
        self.bullet_list.draw()

        self.gui_camera.use()
        self.batch.draw()
    
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
            if self.hero.change_y > 0:
                self.hero.change_y *= 0.45
    
    def on_update(self, delta_time):
        move = 0
        if self.left and not self.right:
            move = -MOVE_SPEED
        elif self.right and not self.left:
            move = MOVE_SPEED
        self.hero.change_x = move

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

        self.engine.update()
        self.player_list.update()
        self.gun_list.update()
        self.bullet_list.update()

        target_x = self.hero.center_x
        target_y = self.hero.center_y

        half_viewport_w = self.width / 2
        half_viewport_h = self.height / 2

        target_x = max(half_viewport_w, min(target_x, self.world_width - half_viewport_w))
        target_y = max(half_viewport_h, min(target_y, self.world_height - half_viewport_h))

        target = (target_x, target_y)
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position, target, CAMERA_LERP
        )

        hit_list: list[arcade.Sprite] = arcade.check_for_collision_with_list(
            self.hero, self.deadable
        )
        if hit_list:
            arcade.play_sound(self.die_sound)
            self.respawn_player()

        for sprite in self.bullet_list:
            _hit_list = arcade.check_for_collision_with_list(
                sprite, self.walls
            )
            if _hit_list:
                sprite.remove_from_sprite_lists()
                break
            hit_list = arcade.check_for_collision_with_list(sprite, self.breakable)
            if hit_list:
                sprite.remove_from_sprite_lists()
            for sp in hit_list:
                self.breakable.remove(sp)
                all_sprites = arcade.get_sprites_at_exact_point(
                    (sp.center_x, sp.center_y), self.collision_list
                )
                for _sp in all_sprites:
                    _sp.remove_from_sprite_lists()

        hit_bottles = arcade.check_for_collision_with_list(
            self.hero, self.specials
        )
        for bottle in hit_bottles:
            bottle.remove_from_sprite_lists()
            self.count += 1
            self.text.text = f'Score: {self.count}'


    def respawn_player(self):
        self.hero.center_x = 48
        self.hero.center_y = 200

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        gun_x = self.gun.center_x
        gun_y = self.gun.center_y
        abs_x = self.world_camera.position[0] - self.width / 2 + x
        abs_y = self.world_camera.position[1] - self.height / 2 + y
        x_diff = abs_x - gun_x
        y_diff = abs_y - gun_y
        angle = math.atan2(y_diff, x_diff)
        self.gun.rotate(angle)
    
    def on_mouse_press(self, x, y, button, modifiers):
        bullet = self.gun.shoot()
        if self.hero.direction == SpriteDirection.LEFT:
            bullet.angle = 180 + bullet.angle
            bullet.change_x = -bullet.change_x
            bullet.change_y = -bullet.change_y
        self.bullet_list.append(bullet)