import pyglet
from pyglet.window import key

# 定数
CELL_SIZE = 32
MAP_DATA = [
    'BBBBBBBBBBBBBBBBBBB',
    'B.................B',
    'B...............P.N',
    'B.................B',
    'B.................B',
    'B.....BBBB........B',
    'B.................B',
    'B.................B',
    'BBBBBBBBBBBBBBBBBBB',
]


class Player:
    def __init__(self, start_x, start_y, cell_size, batch, window_height):
        self.grid_x = start_x
        self.grid_y = start_y
        self.cell_size = cell_size
        self.window_height = window_height
        self.sprite = pyglet.shapes.Rectangle(
            self.grid_x * cell_size,
            self.window_height - (self.grid_y + 1) * cell_size,
            cell_size,
            cell_size,
            color=(0, 255, 0),
            batch=batch
        )

    def move(self, dx, dy, game_map: Map):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if game_map.is_walkable(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            self.sprite.x = self.grid_x * self.cell_size
            self.sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size


class Main:
    def __init__(self):
        self.window_width = len(MAP_DATA[0]) * CELL_SIZE
        self.window_height = len(MAP_DATA) * CELL_SIZE
        self.window = pyglet.window.Window(self.window_width, self.window_height)
        self.batch = pyglet.graphics.Batch()
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        # Initialize map
        self.map = Map(MAP_DATA, CELL_SIZE, self.batch, self.window_height)

        # Initialize player
        px, py = self.map.player_start
        self.player = Player(px, py, CELL_SIZE, self.batch, self.window_height)

        # Register events
        self.window.event(self.on_draw)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def update(self, dt):
        dx = dy = 0
        if self.keys[key.LEFT]:
            dx = -1
        elif self.keys[key.RIGHT]:
            dx = 1
        elif self.keys[key.UP]:
            dy = -1
        elif self.keys[key.DOWN]:
            dy = 1

        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.map)


if __name__ == '__main__':
    game = Main()
    pyglet.app.run()
