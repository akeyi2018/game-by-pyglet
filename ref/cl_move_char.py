import pyglet
from pyglet.window import key
from pyglet.gl import *

class Game:
    def __init__(self):
        # ウィンドウの設定
        self.window = pyglet.window.Window(caption="Sprite Animation", width=600, height=480)
        self.window.config.alpha_size = 8
        self.window.push_handlers(self.on_draw)

        # キー入力の状態管理
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        # スプライト読み込み・初期化
        self.load_sprite_sheet()

        # キャラ移動・アニメーション状態
        self.current_animation = 'right'
        self.current_frame = 0
        self.elapsed_time = 0
        self.animation_speed = 0.1
        self.vector_x = 1
        self.vector_y = 1

        # スプライト初期位置
        self.character = pyglet.sprite.Sprite(img=self.animations[self.current_animation][self.current_frame])
        self.character.scale = 2.0
        self.character.x = self.window.width // 2
        self.character.y = self.window.height // 2

        # アップデート関数を登録
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def load_sprite_sheet(self):
        sprite_sheet = pyglet.image.load('./characters/$yuhina001.png')  # 3x4のスプライトシート
        frame_width = sprite_sheet.width // 3
        frame_height = sprite_sheet.height // 4

        frames = []
        for row in range(4):
            for col in range(3):
                x = col * frame_width
                y = row * frame_height
                frame = sprite_sheet.get_region(x, y, frame_width, frame_height)
                frames.append(frame)

        self.animations = {
            'down': frames[9:12],
            'left': frames[6:9],
            'right': frames[3:6],
            'up': frames[0:3]
        }

    def update(self, dt):
        speed = 100 * dt
        self.character.x += speed * self.vector_x
        self.character.y += speed * self.vector_y

        # ウィンドウの端で方向転換
        if self.character.x > (self.window.width - 32):
            self.vector_x = -1
            self.current_animation = 'left'
        elif self.character.x <= 0:
            self.vector_x = 1
            self.current_animation = 'right'

        if self.character.y <= 0:
            self.vector_y = 1
            self.current_animation = 'up'
        elif self.character.y > (self.window.height - 32):
            self.vector_y = -1
            self.current_animation = 'down'

        # アニメーション更新
        self.elapsed_time += dt
        if self.elapsed_time >= self.animation_speed:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.character.image = self.animations[self.current_animation][self.current_frame]

    def on_draw(self):
        self.window.clear()
        self.character.draw()

# アプリケーションを開始
if __name__ == '__main__':
    game = Game()
    pyglet.app.run()
