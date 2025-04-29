import pyglet

# マップの定義
map_01 = [
    'BBBBBBBBBBBBBBBBBBB',
    'B.................B',
    'B...P.............N',
    'B.................B',
    'B.................B',
    'B.....BBBB........B',
    'B.................B',
    'B.................B',
    'BBBBBBBBBBBBBBBBBBB',
]

# セルのサイズ
cell_size = 32  # 大きめにした方が見やすい

# ウィンドウサイズ
window_width = len(map_01[0]) * cell_size
window_height = len(map_01) * cell_size

# ウィンドウを作成
window = pyglet.window.Window(window_width, window_height)

# プレイヤー用リスト（後で動かす用）
player_sprite = None

# バッチを使って一括描画高速化
batch = pyglet.graphics.Batch()

# シェイプをまとめる
tiles = []

for y, row in enumerate(map_01):
    for x, cell in enumerate(row):
        pixel_x = x * cell_size
        # pygletは左下が(0,0)なのでY軸を逆にする
        pixel_y = window_height - (y + 1) * cell_size

        if cell == 'B':
            color = (50, 50, 50)
            rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, cell_size, cell_size, color=color, batch=batch)
            tiles.append(rect)
        elif cell == 'N':
            color = (255, 0, 0)
            rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, cell_size, cell_size, color=color, batch=batch)
            tiles.append(rect)
        elif cell == 'P':
            color = (0, 255, 0)
            # プレイヤーだけ特別扱い
            player_sprite = pyglet.shapes.Rectangle(pixel_x, pixel_y, cell_size, cell_size, color=color, batch=batch)
        else:
            # 何も描かない（空白）
            pass

@window.event
def on_draw():
    window.clear()
    batch.draw()

# 実行
pyglet.app.run()
