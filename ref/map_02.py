import pyglet

# マップの定義
map_01 = [
    'BBBBBBBBBBBBBBBBBBB',
    'B.................B',
    'B...............P.N',
    'B.................B',
    'B.................B',
    'B.....BBBB........B',
    'B.................B',
    'B.................B',
    'B.................B',
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

# バッチを使って一括描画
batch = pyglet.graphics.Batch()

# キーボード入力のため
from pyglet.window import key
keys = key.KeyStateHandler()
window.push_handlers(keys)

# シェイプをまとめる
tiles = []
player_sprite = None
player_grid_x = 0
player_grid_y = 0

for y, row in enumerate(map_01):
    for x, cell in enumerate(row):
        pixel_x = x * cell_size
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
            player_sprite = pyglet.shapes.Rectangle(pixel_x, pixel_y, cell_size, cell_size, color=color, batch=batch)
            player_grid_x = x
            player_grid_y = y
        else:
            pass

@window.event
def on_draw():
    window.clear()
    batch.draw()

# プレイヤー移動処理
def update(dt):
    global player_grid_x, player_grid_y

    move_x = 0
    move_y = 0

    if keys[key.LEFT]:
        move_x = -1
    elif keys[key.RIGHT]:
        move_x = 1
    elif keys[key.UP]:
        move_y = -1  # マップ上は上に行くと行番号が減る
    elif keys[key.DOWN]:
        move_y = 1

    new_x = player_grid_x + move_x
    new_y = player_grid_y + move_y

    # 範囲内＆ブロックではない場合だけ移動
    if (0 <= new_x < len(map_01[0])) and (0 <= new_y < len(map_01)):
        if map_01[new_y][new_x] != 'B':
            player_grid_x = new_x
            player_grid_y = new_y

            # 座標更新
            player_sprite.x = player_grid_x * cell_size
            player_sprite.y = window_height - (player_grid_y + 1) * cell_size

# updateを60FPSで呼び続ける
pyglet.clock.schedule_interval(update, 1/30.0)

# 実行
pyglet.app.run()
