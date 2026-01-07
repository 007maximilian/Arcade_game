import arcade
from constants.physics import (
    COYOTE_TIME, JUMP_BUFFER, JUMP_PAD_BOOST,
    MAX_JUMPS, GRAVITY, MOVE_SPEED, JUMP_SPEED,
    LADDER_SPEED, CAMERA_LERP
) # everything yep
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


class GameView(arcade.View):
    def on_show_view(self): # jus like init in arcade.View
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.hero: None | arcade.Sprite = None # need to write someday
        self.player_list = arcade.SpriteList()
        self.collision_list = arcade.SpriteList()

        self.setup()
    
    def setup(self):
        # someday need to write sth like tilemap loading..

        self.engine = arcade.PhysicsEnginePlatformer(
            self.hero,
            walls=self.collision_list,
            gravity_constant=GRAVITY
        ) # MAKE PLATFROMS YEE + LADDERS
    
    def on_update(self, delta_time):
        # write update
        self.engine.update()