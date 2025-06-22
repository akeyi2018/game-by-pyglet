import pyglet
from map import Map
from settings import *

class Customer:
    def __init__(self, parent):
        self.parent = parent
        self.cell_size = CELL_SIZE
        self.window_height = self.parent.window_height

        self.moving = False
        self.move_duration = 0.2
        self.move_timer = 0.0

        self.customer_pos_list = self.parent.map.customer_pos  # 複数のお客出発点
        self.wait_pos_list = self.parent.map.wait_pos          # 複数の待機場所

        self.index = 0  # 現在の移動対象インデックス
        self.active = False  # この客が移動中かどうか

        self.reached_target = True  # 最初は待機中（移動していない）

        # 初期位置を customer_pos[0] に設定
        self.grid_x, self.grid_y = self.customer_pos_list[0]
        

         # spriteの生成（適宜画像に差し替え）
        self.sprite = pyglet.shapes.Rectangle(
            self.grid_x * self.cell_size,
            self.window_height - (self.grid_y + 1) * self.cell_size,
            self.cell_size,
            self.cell_size,
            color=(0, 255, 255),
            batch=self.parent.batch
        )
        self.sprite.x = self.grid_x * self.cell_size
        self.sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size

    def start_next_customer(self):
        """次の客をスタートさせる"""
        if self.index >= len(self.customer_pos_list):
            return  # 全員移動済み

        self.grid_x, self.grid_y = self.customer_pos_list[self.index]
        self.sprite.x = self.grid_x * self.cell_size
        self.sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size

        self.target_pos_x, self.target_pos_y = self.wait_pos_list[self.index]

        self.start_moving_to(self.grid_x, self.grid_y)  # 移動開始用の初期化
        self.reached_target = False
        self.active = True

    def start_moving_to(self, new_x, new_y):
        """移動の初期化"""
        self.start_grid = (self.grid_x, self.grid_y)
        self.target_grid = (new_x, new_y)

        self.start_pixel = (self.sprite.x, self.sprite.y)
        self.dest_pixel = (
            new_x * self.cell_size,
            self.window_height - (new_y + 1) * self.cell_size
        )

        self.move_timer = 0.0
        self.moving = True

    def move_target(self, game_map, dt):
        if not self.active:
            return

        if self.moving:
            self.move_timer += dt
            t = min(self.move_timer / self.move_duration, 1.0)
            sx, sy = self.start_pixel
            dx, dy = self.dest_pixel
            self.sprite.x = sx + (dx - sx) * t
            self.sprite.y = sy + (dy - sy) * t

            if t >= 1.0:
                self.moving = False
                self.grid_x, self.grid_y = self.target_grid

                if (self.grid_x, self.grid_y) == (self.target_pos_x, self.target_pos_y):
                    print(f"Customer {self.index} 着席しました。")
                    self.reached_target = True
                    self.active = False
                    self.index += 1
        else:
            # X方向
            if self.grid_x != self.target_pos_x:
                step_x = 1 if self.target_pos_x > self.grid_x else -1
                next_x = self.grid_x + step_x
                if game_map.is_walkable(next_x, self.grid_y):
                    self.start_moving_to(next_x, self.grid_y)
                    return

            # Y方向
            if self.grid_y != self.target_pos_y:
                step_y = 1 if self.target_pos_y > self.grid_y else -1
                next_y = self.grid_y + step_y
                if game_map.is_walkable(self.grid_x, next_y):
                    self.start_moving_to(self.grid_x, next_y)

    def update(self, dt):
        if self.reached_target and self.index < len(self.customer_pos_list):
            self.start_next_customer()
        self.move_target(self.parent.map, dt)
