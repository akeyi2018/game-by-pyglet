import pyglet

class MainWin(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_caption("Game")
        # 画像を読み込む
        self.image = pyglet.image.load('fortress.png')

        self.width = self.image.width
        self.height = self.image.height
        self.set_screen = pyglet.display.get_display().get_default_screen()

        self.set_location(((self.screen.width - self.width) // 2),
                          ((self.screen.height - self.height) //2))
        
        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.Group(0)
        
        self.sprite = pyglet.sprite.Sprite(self.image, x=0, y=0, 
                                           batch=self.batch,
                                           group=self.background)

        self.label = pyglet.text.Label('hello world pyglet..', 
                          font_name='Times New Roman', 
                          font_size=40,
                          x=self.image.width // 2,
                          y=self.image.height // 2,
                          anchor_x='center',
                          anchor_y='center', batch=self.batch)

    def on_draw(self):
        self.clear()
        self.batch.draw()

if __name__ == "__main__":
    main_win = MainWin()
    pyglet.app.run()