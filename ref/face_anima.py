import pyglet
from pyglet.window import key
from pyglet.gl import *

class Game:
    def __init__(self):
        # ウィンドウの設定
        self.window = pyglet.window.Window(caption="Face Animation", width=600, height=480)
        self.window.config.alpha_size = 8
        self.window.push_handlers(self.on_draw)

        # キー入力の状態管理
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.window.push_handlers(self.on_key_press)

        # スプライト読み込み・初期化
        self.load_sprite_sheet()

        # キャラ移動・アニメーション状態
        self.current_animation = 'top'
        self.current_frame = 0
        self.elapsed_time = 0
        self.animation_speed = 0.1
        self.vector_x = 1
        self.vector_y = 1

        self.play_once = False

        # スプライト初期位置
        self.character = pyglet.sprite.Sprite(img=self.animations[self.current_animation][self.current_frame])
        self.character.scale = 2.0
        self.character.x = self.window.width // 2
        self.character.y = self.window.height // 2

        # アップデート関数を登録
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def load_sprite_sheet(self):
        sprite_sheet = pyglet.image.load('./faces/yhmv001.png')  # 2x4のスプライトシート
        frame_width = sprite_sheet.width // 4
        frame_height = sprite_sheet.height // 2

        top_frames = []    # row=0（上段）
        bottom_frames = [] # row=1（下段）

        for col in range(4):
            x = col * frame_width
            top_frame = sprite_sheet.get_region(x, frame_height, frame_width, frame_height)
            bottom_frame = sprite_sheet.get_region(x, 0, frame_width, frame_height)
            top_frames.append(top_frame)
            bottom_frames.append(bottom_frame)

        self.animations = {
            'top': top_frames,
            'bottom': bottom_frames
        }

    def on_key_press(self, symbol, modifiers):
        if symbol == key.F1:
            self.current_animation = 'top'
            self.current_frame = 0
            self.play_once = True
            self.character.image = self.animations[self.current_animation][self.current_frame]
        elif symbol == key.F2:
            self.current_animation = 'bottom'
            self.current_frame = 0
            self.play_once = True
            self.character.image = self.animations[self.current_animation][self.current_frame]

    def update(self, dt):
        speed =  dt / 2
        
        if self.play_once:
            self.elapsed_time += speed
            if self.elapsed_time >= self.animation_speed:
                self.elapsed_time = 0
                self.current_frame += 1

                # 最後のフレームまで来たら停止
                if self.current_frame >= len(self.animations[self.current_animation]):
                    self.current_frame = len(self.animations[self.current_animation]) - 1
                    self.play_once = False  # 再生終了

                self.character.image = self.animations[self.current_animation][self.current_frame]

    def on_draw(self):
        self.window.clear()
        self.character.draw()

# アプリケーションを開始
if __name__ == '__main__':
    game = Game()
    pyglet.app.run()
