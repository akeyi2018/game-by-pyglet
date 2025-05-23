import pyglet
from pyglet.window import key
from pyglet.gl import *

# ウィンドウの設定
window = pyglet.window.Window(caption="Sprite Animation", width=800, height=600)
window.config.alpha_size = 8

# スプライトシートを読み込む
sprite_sheet = pyglet.image.load('chara001.png')  # 12マスのPNG画像

# スプライトシートを分割（3行4列）
frames = []
frame_width = sprite_sheet.width // 3  # 1フレームの幅
frame_height = sprite_sheet.height // 4  # 1フレームの高さ
for row in range(4):
    for col in range(3):
        x = col * frame_width
        y = row * frame_height
        frame = sprite_sheet.get_region(x, y, frame_width, frame_height)
        frames.append(frame)

# アニメーション用のフレームを設定
animations = {
    'down': frames[9:12],  # 下向きのアニメーション（1行目）
    'left': frames[6:9],  # 左向きのアニメーション（2行目）
    'right': frames[3:6],  # 右向きのアニメーション（3行目）
    'up': frames[0:3]  # 上向きのアニメーション（仮設定）
}

# キャラクターの初期設定
current_animation = 'down'  # 現在のアニメーション
current_frame = 0  # 現在のフレーム
character = pyglet.sprite.Sprite(img=animations[current_animation][current_frame])
character.x = window.width // 2
character.y = window.height // 2

# キーボード入力の状態を管理
keys = key.KeyStateHandler()
window.push_handlers(keys)

# アニメーションの更新間隔
animation_speed = 0.1  # フレーム切り替えの間隔（秒）
elapsed_time = 0

def update(dt):
    global current_frame, elapsed_time, current_animation

    # キャラクターの移動
    speed = 200 * dt  # 移動速度
    if keys[key.UP]:
        character.y += speed
        current_animation = 'up'
    if keys[key.DOWN]:
        character.y -= speed
        current_animation = 'down'
    if keys[key.LEFT]:
        character.x -= speed
        current_animation = 'left'
    if keys[key.RIGHT]:
        character.x += speed
        current_animation = 'right'

    # アニメーションの更新
    elapsed_time += dt
    if elapsed_time >= animation_speed:
        elapsed_time = 0
        current_frame = (current_frame + 1) % len(animations[current_animation])
        character.image = animations[current_animation][current_frame]

@window.event
def on_draw():
    window.clear()
    character.draw()

# 更新関数を定期的に呼び出す
pyglet.clock.schedule_interval(update, 1/60.0)

# アプリケーションを実行
pyglet.app.run()