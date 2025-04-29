import pyglet


class Character:

    def __init__(self, parent):

        self.parent = parent
        # スプライトシートを読み込む
        self.sprite_sheet = pyglet.image.load('chara001.png')  # 12マスのPNG画像

        # アニメーション設定
        self.set_animation()

        # キャラクターの初期設定
        self.current_animation = 'down'  # 現在のアニメーション
        self.current_frame = 0  # 現在のフレーム

        # キャラの移動ベクトル
        self.vector_x = 1
        self.vector_y = 1

        self.animation_speed = 0.1
        self.elapsed_time = 0

        self.sprite = pyglet.sprite.Sprite(
            img=self.animations[self.current_animation][self.current_frame],
            x=self.parent.width // 2, 
            y=self.parent.height // 2,
            batch=self.parent.batch,
            group=self.parent.people_layer)
        
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)


    def set_animation(self):
        # スプライトシートを分割（3行4列）
        frames = []
        frame_width = self.sprite_sheet.width // 3  # 1フレームの幅
        frame_height = self.sprite_sheet.height // 4  # 1フレームの高さ
        for row in range(4):
            for col in range(3):
                x = col * frame_width
                y = row * frame_height
                frame = self.sprite_sheet.get_region(x, y, frame_width, frame_height)
                frames.append(frame)

        # アニメーション用のフレームを設定
        self.animations = {
            'down': frames[9:12],  # 下向きのアニメーション（1行目）
            'left': frames[6:9],  # 左向きのアニメーション（2行目）
            'right': frames[3:6],  # 右向きのアニメーション（3行目）
            'up': frames[0:3]  # 上向きのアニメーション（仮設定）
        }

    def update(self, dt):
        speed = 100 * dt
        self.sprite.x += speed * self.vector_x
        self.sprite.y += speed * self.vector_y

        # 壁で反転
        if self.sprite.x > (self.parent.width - 32):
            self.vector_x = -1
            self.current_animation = 'left'
        elif self.sprite.x <= 0:
            self.vector_x = 1
            self.current_animation = 'right'

        if self.sprite.y <= 0:
            self.vector_y = 1
            self.current_animation = 'up'
        elif self.sprite.y > (self.parent.height - 32):
            self.vector_y = -1
            self.current_animation = 'down'

        # アニメーション更新
        self.elapsed_time += dt
        if self.elapsed_time >= self.animation_speed:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.current_animation])
            self.sprite.image = self.animations[self.current_animation][self.current_frame]
