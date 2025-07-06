import pyglet
import os
import random
import glob
from sprite_sheets import SpriteSheet

class Customer:
    
    _id_counter = 0  # クラス変数で一意なIDを管理

    def __init__(self, start_pos, state, window_height, cell_size, color, batch):
        self.id = Customer._id_counter  # 各顧客に一意のIDを付与
        Customer._id_counter += 1

        self.grid_x, self.grid_y = start_pos
        self.target_pos_x, self.target_pos_y = start_pos
        self.cell_size = cell_size
        self.window_height = window_height
        self.state = state
        self.color = color

        # image_list = ["goblin.png", "kappa.png"]
        # selected_image = random.choice(image_list)

        self.character_folder = "./ref/characters"
        image_files = glob.glob(os.path.join(self.character_folder, "*.png"))
        selected_image = random.choice(image_files) if image_files else None

        if os.path.exists(selected_image):
            sheet = SpriteSheet(selected_image)
            self.frames = sheet.get_frames()
            self.sprite = pyglet.sprite.Sprite(
            img=self.frames[0],
            x=self.grid_x * cell_size,
            y=self.window_height - (self.grid_y + 1) * cell_size,
            batch=batch
            )
            self.current_frame = 0
            self.elapsed_time = 0
            self.animation_speed = 0.15
            # self.sprite.scale = scale
        else:
            # Rectangleオブジェクトを作成し、バッチに登録
            self.sprite = pyglet.shapes.Rectangle(
                x=self.grid_x * cell_size,
                y=self.window_height - (self.grid_y + 1) * cell_size,
                width=cell_size,
                height=cell_size,
                color=self.color,
                batch=batch
            )

        self.moving = False
        self.move_duration = 0.2
        self.move_timer = 0.0
        self.start_pixel = (self.sprite.x, self.sprite.y)

        # 退店処理
        self.stay_timer = 0.0


    @property
    def is_moving(self):
        return self.moving

    def start_moving_to(self, new_x, new_y):
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
        if self.moving:
            self.move_timer += dt
            t = min(self.move_timer / self.move_duration, 1.0)
            sx, sy = self.start_pixel
            dx, dy = self.dest_pixel
            
            # Rectangleの位置を更新
            self.sprite.x = sx + (dx - sx) * t
            self.sprite.y = sy + (dy - sy) * t

            if t >= 1.0:
                self.moving = False
                self.grid_x, self.grid_y = self.target_grid
                
        else:
            if self.grid_x != self.target_pos_x:
                step_x = 1 if self.target_pos_x > self.grid_x else -1
                next_x = self.grid_x + step_x
                if game_map.is_walkable(next_x, self.grid_y):
                    self.start_moving_to(next_x, self.grid_y)
                    return

            if self.grid_y != self.target_pos_y:
                step_y = 1 if self.target_pos_y > self.grid_y else -1
                next_y = self.grid_y + step_y
                if game_map.is_walkable(self.grid_x, next_y):
                    self.start_moving_to(self.grid_x, next_y)

    def update(self, dt, game_map):
        self.move_target(game_map, dt)

        # アニメーション更新（移動 or idle）
        if hasattr(self, 'frames'):
            self.elapsed_time += dt
            if self.elapsed_time >= self.animation_speed:
                self.elapsed_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.sprite.image = self.frames[self.current_frame]

    def set_new_target(self, target_x, target_y):
        self.target_pos_x = target_x
        self.target_pos_y = target_y

    @property
    def reached_final_target(self):
        """目的到着判定"""
        return (self.grid_x, self.grid_y) == (self.target_pos_x, self.target_pos_y)
