import pyglet

class FaceAnimation:
    def __init__(self):
        self.load_sprite_sheet()
        self.sprite = pyglet.sprite.Sprite(self.animations['face'][0], x=100, y=100)

        self.current_animation = 'face'
        self.current_frame = 0
        self.elapsed_time = 0
        self.animation_speed = 0.1
        self.playing = False  # ← クリックで再生フラグ

    def load_sprite_sheet(self):
        sprite_sheet = pyglet.image.load('./faces/yhmv162b.png')
        frame_width = sprite_sheet.width // 4
        frame_height = sprite_sheet.height // 2

        frames = []
        y = frame_height  # 上段のみ使用
        for i in range(4):
            x = i * frame_width
            region = sprite_sheet.get_region(x, y, frame_width, frame_height)
            frames.append(region)

        self.animations = {'face': frames}

    def on_click(self, x, y):
        if self.sprite.x <= x <= self.sprite.x + self.sprite.width and \
           self.sprite.y <= y <= self.sprite.y + self.sprite.height:
            self.playing = True
            self.current_frame = 0
            self.elapsed_time = 0

    def update(self, dt):
        if self.playing:
            self.elapsed_time += dt
            if self.elapsed_time >= self.animation_speed:
                self.elapsed_time = 0
                self.current_frame += 1
                if self.current_frame >= len(self.animations[self.current_animation]):
                    # 1周終了 → 最初のフレームに戻す
                    self.playing = False
                    self.current_frame = 0
                self.sprite.image = self.animations[self.current_animation][self.current_frame]
