import pyglet

class Customer:
    def __init__(self, start_pos, target_pos, window_height, cell_size, color, batch):
        self.grid_x, self.grid_y = start_pos
        self.target_pos_x, self.target_pos_y = target_pos
        self.cell_size = cell_size
        self.window_height = window_height
        
        # Rectangleオブジェクトを作成し、バッチに登録
        self.sprite = pyglet.shapes.Rectangle(
            x=self.grid_x * cell_size,
            y=self.window_height - (self.grid_y + 1) * cell_size,
            width=cell_size,
            height=cell_size,
            color=color,
            batch=batch
        )

        self.moving = False
        self.move_duration = 0.2
        self.move_timer = 0.0
        # self.reached_target = False
        self.start_pixel = (self.sprite.x, self.sprite.y)

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
                
                if (self.grid_x, self.grid_y) == (self.target_pos_x, self.target_pos_y):
                    self.reached_target = True
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

    @property
    def reached_final_target(self):
        return (self.grid_x, self.grid_y) == (self.target_pos_x, self.target_pos_y)
