import arcade
from constants.physics import (
    COYOTE_TIME, JUMP_BUFFER, JUMP_PAD_BOOST,
    MAX_JUMPS, GRAVITY, MOVE_SPEED, JUMP_SPEED,
    LADDER_SPEED, CAMERA_LERP
) # everything yep
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from _hero import Hero
from guns import PistolGun


class GameView(arcade.View):
    def on_show_view(self): # jus like init in arcade.View
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.hero: None | Hero = None # need to write someday
        self.player_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()
        self.gun_list = arcade.SpriteList()
        self.gui_camera = arcade.camera.Camera2D()
        self.world_camera = arcade.camera.Camera2D()

        self.engine: None | arcade.PhysicsEnginePlatformer = None
        self.left = self.right = self.up = self.down = self.jump_pressed = False
        self.jump_buffer_timer = 0.0
        self.time_since_ground = 999.0
        self.jumps_left = MAX_JUMPS

        self.setup()
    
    def setup(self):
        # someday need to write sth like tilemap loading..

        # initialize better after tilemaps
        self.world_height = 5000
        self.world_width = 5000

        # example jus for testing
        for i in range(2):
            sprite = arcade.Sprite()
            sprite.texture = arcade.load_texture(':resources:images/tiles/grass.png')
            sprite.center_y = TILE_SIZE // 2
            sprite.center_x = TILE_SIZE // 2 + i * TILE_SIZE
            sprite.scale = 0.375 # 48/128
            self.collision_list.append(sprite)
        
        self.hero = Hero()
        self.hero.center_x = 48
        self.hero.center_y = 200
        self.player_list.append(self.hero)

        self.gun = PistolGun(self.hero)
        self.gun_list.append(self.gun)
        self.hero.gun = self.gun

        self.engine = arcade.PhysicsEnginePlatformer(
            self.hero,
            walls=self.collision_list,
            gravity_constant=GRAVITY
        ) # MAKE PLATFROMS YEE + LADDERS
    
    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.player_list.draw()
        self.gun_list.draw()
        self.collision_list.draw() # delete when max will make tilemap

        # self.gui_camera.use() <- if theres text on the screen (after it draw batch)
    
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