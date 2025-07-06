import pyglet

class SpriteSheet:
    def __init__(self, file_path, frame_cols=3, frame_rows=4):
        self.image = pyglet.image.load(file_path)
        self.frame_width = self.image.width // frame_cols
        self.frame_height = self.image.height // frame_rows
        self.frames = []

        # pygletは原点が左下なので、上から順に取得するには逆順にrowループ
        for row in range(frame_rows):
            y = self.image.height - (row + 1) * self.frame_height
            for col in range(frame_cols):
                x = col * self.frame_width
                region = self.image.get_region(x, y, self.frame_width, self.frame_height)
                self.frames.append(region)

    def get_frames(self):
        return self.frames

    def get_frame(self, index):
        return self.frames[index % len(self.frames)]
