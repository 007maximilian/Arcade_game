import arcade
from arcade.gui import UILabel, UITextureButton, UIManager, UIBoxLayout, UIAnchorLayout


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game = game_view
        self.manager = UIManager()
        self.manager.enable()
        self.cont_button, self.cont_button_h = arcade.SpriteSheet(
            'assets/ui/button_cont.png'
        ).get_texture_grid(
            (750, 180),
            columns=2,
            count=2
        )
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)
        self.button = UITextureButton(
            texture=self.cont_button,
            texture_hovered=self.cont_button_h
        )
        self.label = UILabel(
            font_size=50,
            text_color=arcade.color.WHITE,
            text='paused',
            width=200,
            align='center'
        )
        self.button.on_click = self.return_game
        self.box_layout.add(self.label)
        self.box_layout.add(self.button)
        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
    
    def on_show_view(self):
        print('changed to pause state')

    def on_draw(self):
        self.clear()
        self.manager.draw()
    
    def return_game(self, event):
        self.manager.disable()
        from game import temp_gameview
        self.window.pop_handlers()