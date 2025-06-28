import pyglet 
from settings import *

class Map:
    def __init__(self, batch, window_height):
        self.map_data = MAP_DATA
        self.cell_size = CELL_SIZE
        self.batch = batch
        self.window_height = window_height
        self.tiles = []
        self.wait_pos = []
        self.customer_pos = []
        self.table_pos = []
        self.seat_pos = []

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
                elif cell == 'W':
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                                                   color=(0, 0, 255), batch=self.batch)
                    self.tiles.append(rect)
                    self.wait_pos.append((x, y))
                elif cell == 'C':
                    self.customer_pos.append((x, y))
                elif cell == 'T':
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                                                   color=(255, 255, 0), batch=self.batch)
                    self.tiles.append(rect)
                    self.table_pos.append((x, y))
                elif cell == 'S':
                    self.seat_pos.append((x,y))

        # # 待機ポジションをリバース
        self.wait_pos.reverse()

    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            return self.map_data[y][x] != 'B'
        return False