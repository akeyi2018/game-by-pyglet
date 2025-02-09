import pyglet
from pyglet.window import Window

# 画像を読み込む
img = pyglet.resource.image('fortress.png')

# 画像のサイズに基づいてウィンドウのサイズを設定
window = Window(caption="Game", 
                              width=img.width, 
                              height=img.height, 
                              style=Window.WINDOW_STYLE_TRANSPARENT)

platform = pyglet.app.platform  # プラットフォーム情報を取得
display = pyglet.display.get_display()
screen = display.get_default_screen()

# ウィンドウをスクリーンの中央に配置
window_x = (screen.width - window.width) // 2
window_y = (screen.height - window.height) // 2
window.set_location(window_x, window_y)

label = pyglet.text.Label('hello world pyglet..', 
                          font_name='Times New Roman', 
                          font_size=40,
                          x=window.width // 2,
                          y=window.height // 2,
                          anchor_x='center',
                          anchor_y='center')

@window.event
def on_draw():
    window.clear()
    img.blit(x=0, y=0)  # 画像を描画
    label.draw()  # ラベルを描画

pyglet.app.run()