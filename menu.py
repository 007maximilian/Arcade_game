import arcade
from pyglet.graphics import Batch
from constants.window import SCREEN_HEIGHT, SCREEN_WIDTH


class MenuView(arcade.View):
    def on_show_view(self):
        self.batch = Batch()
        arcade.set_background_color(arcade.color.BLACK)
        text = arcade.Text(
            'heres title pon da',
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            20,
            batch=self.batch,
            anchor_x='center',
            anchor_y='center'
        )
    
    def on_draw(self):
        self.batch.draw()