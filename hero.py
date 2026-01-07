import arcade


class Hero(arcade.Sprite):
    def __init__(self):
        self.texture = arcade.load_texture('assets/sprites/charcater.png')
        self.scale=1.0