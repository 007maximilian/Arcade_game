import arcade
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from menu import MenuView

window: None | arcade.Window = None


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    # i gonna think thats all
    arcade.run()


if __name__ == "__main__":
    main()