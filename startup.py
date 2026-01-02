import arcade
from pyglet.graphics import Batch
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT
from game import MainGame


class StartupView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.batch = Batch()
    
    def on_draw(self):
        text = arcade.Text(
            "game pon da",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center",
            batch=self.batch
        )
        self.batch.draw()
    
    def on_key_press(self, key, modifiers):
        game = MainGame()
        game.setup()
        self.window.show_view(game)