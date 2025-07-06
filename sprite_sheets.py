import pyglet

class SpriteSheet:
    def __init__(self, file_path, frame_cols=3, frame_rows=4):
        self.image = pyglet.image.load(file_path)
        self.frame_width = self.image.width // frame_cols
        self.frame_height = self.image.height // frame_rows
        self.animations = {}  # 方向別アニメーション辞書

        directions = ['up', 'left', 'right', 'down']

        for row, direction in enumerate(directions):
            y = self.image.height - (row + 1) * self.frame_height
            frames = []
            for col in range(frame_cols):
                x = col * self.frame_width
                region = self.image.get_region(x, y, self.frame_width, self.frame_height)
                frames.append(region)
            self.animations[direction] = frames

    def get_frames(self, direction):
        return self.animations.get(direction, self.animations['down'])
