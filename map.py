import pyglet
import random 
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
        self.table_image = pyglet.image.load('table.png')
        self.grade_image = pyglet.image.load('table2.jpg')
        self.floor_image = pyglet.image.load('floor_carpet.png')
        self.kusa = pyglet.image.load('sougen.png')
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
                    floor = pyglet.sprite.Sprite(img=self.floor_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(floor)
                    self.wait_pos.append((x, y))
                elif cell == 'L':
                    self.cust_label = pyglet.text.Label(
                        text=f"来客数: 0",
                        font_name='Arial',
                        font_size=16,
                        x=100, y=pixel_y + 30,
                        anchor_x='left', anchor_y='top',
                        color=(255, 255, 255, 255),
                        batch=self.batch
                    )
                    self.tiles.append(self.cust_label)
                elif cell == 'T':
                    # rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                    #                                color=(255, 255, 0), batch=self.batch)
                    table = pyglet.sprite.Sprite(img=self.table_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(table)
                    self.table_pos.append((x, y))
                elif cell == 'G':
                    # rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                    #                                color=(255, 255, 0), batch=self.batch)
                    table = pyglet.sprite.Sprite(img=self.grade_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(table)
                elif cell == 'S':
                    floor = pyglet.sprite.Sprite(img=self.floor_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(floor)
                    self.seat_pos.append((x,y))
                elif cell == '.':
                    floor = pyglet.sprite.Sprite(img=self.floor_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(floor)
                elif cell == 'F':
                    kusa = pyglet.sprite.Sprite(img=self.kusa,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                    self.tiles.append(kusa)


        # # 待機ポジションをリバース
        self.wait_pos.reverse()
        # 退店位置
        self.exit_pos_list = self.get_exit_positions()


    def is_walkable(self, x, y):
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            return self.map_data[y][x] != 'B'
        return False
    
    def get_random_customer_positions(self, num_customers, area_rows=(1, 4)):
        available = []

        for y in range(area_rows[0], area_rows[1]):
            for x in range(len(self.map_data[0])):
                if self.map_data[y][x] == 'F':
                    available.append((x, y))

        random.shuffle(available)
        result = available[:num_customers]
        return result
    
    def get_exit_positions(self):
        return [(x, y) for y, row in enumerate(self.map_data)
                for x, cell in enumerate(row) if cell == 'D']
    
    def get_entrance_positions(self):
        return [(x, y) for y, row in enumerate(self.map_data)
                for x, cell in enumerate(row) if cell == 'L']
