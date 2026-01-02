import arcade
from constants.window import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from startup import StartupView

window: arcade.Window | None = None


def main():
    global window
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)
    view = StartupView()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()