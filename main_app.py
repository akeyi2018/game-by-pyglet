import pyglet
from pyglet.window import key
from pyglet.gl import *
from character import Character

class MainWin(pyglet.window.Window):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption("Game")
        # スクリーン
        self.set_screen = pyglet.display.get_display().get_default_screen()
        # Windowのロケーション設定
        self.set_location(((self.screen.width - self.width) // 2),
                          ((self.screen.height - self.height) //2))

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(0)
        self.people_layer = pyglet.graphics.Group(1)
        self.set_background()
        self.char = Character(self)

    def set_background(self):
        self.bg_image = pyglet.image.load('fortress.png')
        self.width = self.bg_image.width
        self.height = self.bg_image.height
        self.sprite = pyglet.sprite.Sprite(self.bg_image, x=0, y=0, 
                                           batch=self.batch,
                                           group=self.background)


    def on_draw(self):
        self.clear()
        self.batch.draw()


if __name__ == "__main__":
    main_win = MainWin()
    pyglet.app.run()

