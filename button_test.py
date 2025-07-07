import pyglet
from pyglet.window import mouse

class Button:
    def __init__(self, x, y, width, height, text, batch, on_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click

        self.rect = pyglet.shapes.Rectangle(
            x, y, width, height, color=(100, 150, 255), batch=batch
        )
        self.label = pyglet.text.Label(
            text, font_size=12, color=(0, 0, 0, 255),
            x=x + width // 2, y=y + height // 2,
            anchor_x='center', anchor_y='center', batch=batch
        )

    def hit_test(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

    def click(self):
        self.on_click()


class MyWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=640, height=480)
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label('', x=10, y=450, batch=self.batch)

        # ボタン作成
        self.buttons = [
            Button(100, 200, 150, 40, "クリック！", self.batch, self.button_clicked)
        ]
        self.ct = 0

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            for btn in self.buttons:
                if btn.hit_test(x, y):
                    btn.click()

    def button_clicked(self):
        self.ct += 1
        self.label.text = f"Counts: {self.ct}"
        # print("ボタンが押されました！")


if __name__ == '__main__':
    win = MyWindow()
    pyglet.app.run()
