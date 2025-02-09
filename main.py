import pyglet

# 画像を読み込む
img = pyglet.resource.image('fortress.png')

# 画像のサイズに基づいてウィンドウのサイズを設定
window = pyglet.window.Window(width=img.width, height=img.height)

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