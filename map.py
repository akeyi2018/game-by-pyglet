import pyglet
import random 
from settings import *
from door import DoorButton
from pyglet.window import mouse


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
        self.table_image = pyglet.image.load('./res/table.png')
        self.floor_image = pyglet.image.load('./res/floor_carpet.png')
        self.kusa = pyglet.image.load('./res/sougen.png')
        self.buttons = []
        self.load_map()
        self.open_doors = set()  # ← 開いたドアのグリッド座標を保存

        

    def load_map(self):
        for y, row in enumerate(self.map_data):
            for x, cell in enumerate(row):
                pixel_x = x * self.cell_size
                pixel_y = self.window_height - (y + 1) * self.cell_size

                # フロア
                floor = pyglet.sprite.Sprite(img=self.floor_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                floor.scale = 2.0

                # テーブル
                table = pyglet.sprite.Sprite(img=self.table_image,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                table.scale = 2.0

                # 店外（草原）
                kusa = pyglet.sprite.Sprite(img=self.kusa,
                                                 x=pixel_x, y=pixel_y,
                                                 batch=self.batch)
                kusa.scale = 2.0

                if cell == 'B':
                    rect = pyglet.shapes.Rectangle(pixel_x, pixel_y, self.cell_size, self.cell_size,
                                                   color=(50, 50, 50), batch=self.batch)
                    self.tiles.append(rect)
                elif cell == 'D':
                    self.buttons.append(
                        DoorButton(pixel_x, pixel_y, CELL_SIZE, self.batch, self.button_clicked))
                    
                elif cell == 'W':
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
                    self.tiles.append(table)
                    self.table_pos.append((x, y))
                elif cell == 'S':
                    self.tiles.append(floor)
                    self.seat_pos.append((x,y))
                elif cell == '.':
                    self.tiles.append(floor)
                elif cell == 'F':
                    self.tiles.append(kusa)


        # # 待機ポジションをリバース
        self.wait_pos.reverse()
        # 退店位置
        self.exit_pos_list = self.get_exit_positions()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            # print(self.buttons)
            for btn in self.buttons:
                # print(btn)
                if btn.hit_test(x,y):
                    btn.click()


    # def button_clicked(self, x, y, is_open):
        
    #     if is_open:
    #         print(f"【ドア開】({x}, {y})")
    #         self.open_doors.add((x, y))
    #     else:
    #         print(f"【ドア閉】({x}, {y})")
    #         self.open_doors.discard((x, y))  # 通行不可に戻す

    def button_clicked(self, x, y, is_open):
        # yを反転させる
        corrected_y = len(self.map_data) - 1 - y
        # print(f"[ドア {'開' if is_open else '閉'}] Grid座標: ({x}, {corrected_y})")
        if is_open:
            self.open_doors.add((x, corrected_y))
        else:
            self.open_doors.discard((x, corrected_y))



    # def is_walkable(self, x, y):
    #     if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
    #         if self.map_data[y][x] == 'B' or self.map_data[y][x] == 'T':
    #             return False
    #         else:
    #             return True
            
    # def is_walkable(self, x, y):
    #     if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
    #         cell = self.map_data[y][x]
    #         if cell == 'B' or cell == 'T':
    #             return False
    #         elif cell == 'D':
    #             return (x, y) in self.open_doors  # ← ドアが開いていれば通行可
    #         else:
    #             return True
    #     return False
    
    def is_walkable(self, x, y):
        # print(f"Walkableチェック: ({x}, {y}) -> ", end="")
        if 0 <= y < len(self.map_data) and 0 <= x < len(self.map_data[0]):
            cell = self.map_data[y][x]
            if cell == 'B' or cell == 'T':
                # print("✗ 壁またはテーブル")
                return False
            elif cell == 'D':
                walkable = (x, y) in self.open_doors
                # print(f"{'✓ 通行可' if walkable else '✗ 通行不可'} (ドア)")
                return walkable
            else:
                # print("✓ 通行可")
                return True
        # print("✗ 範囲外")
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
                for x, cell in enumerate(row) if cell == 'O']
    
    def get_entrance_positions(self):
        return [(x, y) for y, row in enumerate(self.map_data)
                for x, cell in enumerate(row) if cell == 'L']
    

