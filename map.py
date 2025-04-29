import pyglet 

class Map:
    def __init__(self, map_data, cell_size, batch, window_height):
        self.map_data = map_data
        self.cell_size = cell_size
        self.batch = batch
        self.window_height = window_height
        self.tiles = []
        self.npc_positions = []
        self.player_start = (0, 0)

        self.load_map()

    def load_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                pixel_x = x * self.cell_size
                pixel_y = self.window_height - (y + 1) * self.cell_size

                if cell == 'B':
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                                                   color=(50, 50, 50), batch=self.batch)
                    self.tiles.append(rect)
                elif cell == 'N':
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                                                   color=(255, 0, 0), batch=self.batch)
                    self.tiles.append(rect)
                    self.npc_positions.append((x, y))
                elif cell == 'P':
                    self.player_start = (x, y)

    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            return self.map_data[y][x] != 'B'
        return False