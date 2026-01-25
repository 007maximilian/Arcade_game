import arcade
from pyglet.graphics import Batch
from constants.window import SCREEN_HEIGHT, SCREEN_WIDTH
from game import GameView
from arcade.gui import UITextureButton, UIManager, UILabel
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout


class MenuView(arcade.View):
    def on_show_view(self):
        self.batch = Batch()
        arcade.set_background_color(arcade.color.BLACK)
        self.manager = UIManager()
        self.manager.enable()
        self.but_texture, self.but_texture_hovered = arcade.SpriteSheet(
            'assets/ui/button_start.png'
        ).get_texture_grid(
            (300, 90),
            columns=2,
            count=2
        )
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.label = UILabel(
            font_size=50,
            text_color=arcade.color.WHITE,
            text="unt1tl3d",
            width=200,
            align="center"
        )
        self.button = UITextureButton(
            texture=self.but_texture,
            texture_hovered=self.but_texture_hovered
        )
        self.button.on_click = self.change_view
        self.box_layout.add(self.label)
        self.box_layout.add(self.button)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
    
    def on_draw(self):
        self.batch.draw()
        self.manager.draw()
    
    def change_view(self, event):
        self.manager.disable()
        game_view = GameView()
        self.window.show_view(game_view)