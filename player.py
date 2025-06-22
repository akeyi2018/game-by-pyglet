import pyglet
from map import Map

class Player:
    def __init__(self, start_x, start_y, cell_size, batch, window_height):
        self.grid_x = start_x
        self.grid_y = start_y
        self.cell_size = cell_size
        self.window_height = window_height

        self.ct = 0

        self.target_pos_x, self.target_pos_y = 6 , 4

        self.sprite = pyglet.shapes.Rectangle(
            self.grid_x * cell_size,
            self.window_height - (self.grid_y + 1) * cell_size,
            cell_size,
            cell_size,
            color=(0, 255, 0),
            batch=batch
        )

        # アニメーション用
        self.moving = False
        self.move_duration = 0.2  # 移動にかける秒数
        self.move_timer = 0.0

        # アニメーション用座標をタプルで管理
        self.start_pixel = (self.sprite.x, self.sprite.y)
        self.dest_pixel = (self.sprite.x, self.sprite.y)
        self.start_grid = (self.grid_x, self.grid_y)
        self.target_grid = (self.grid_x, self.grid_y)

        # 着席
        self.reached_target = True

    def move(self, dx, dy, game_map: Map):
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy
        if game_map.is_walkable(new_x, new_y):
            self.grid_x = new_x
            self.grid_y = new_y
            self.sprite.x = self.grid_x * self.cell_size
            self.sprite.y = self.window_height - (self.grid_y + 1) * self.cell_size

    def start_moving_to(self, new_x, new_y):
        """アニメーション開始（X・Yの移動に対応）"""
        # アニメーション開始前のグリッド座標
        self.start_grid = (self.grid_x, self.grid_y)
        # 目標グリッド座標
        self.target_grid = (new_x, new_y)

        # ピクセル座標
        self.start_pixel = (self.sprite.x, self.sprite.y)
        self.dest_pixel = (
            new_x * self.cell_size,
            self.window_height - (new_y + 1) * self.cell_size
        )

        self.move_timer = 0.0
        self.moving = True

    def move_target(self, game_map: Map, dt):

        # アニメーションでゆっくり動くようにしている
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

                # 着席判定
                if self.grid_x == self.target_pos_x and self.grid_y == self.target_pos_y:
                    if not self.reached_target:
                        print("着席しました。")
                        self.reached_target = True

            return

        # X方向に移動
        if self.grid_x != self.target_pos_x:
            step_x = 1 if self.target_pos_x > self.grid_x else -1
            next_x = self.grid_x + step_x
            if game_map.is_walkable(next_x, self.grid_y):
                self.start_moving_to(next_x, self.grid_y)
                return  # 1マスずつ移動

        # Y方向に移動
        if self.grid_y != self.target_pos_y:
            step_y = 1 if self.target_pos_y > self.grid_y else -1
            next_y = self.grid_y + step_y
            if game_map.is_walkable(self.grid_x, next_y):
                self.start_moving_to(self.grid_x, next_y)

            
    def update(self, keys, game_map, dt):
        dx = dy = 0
        from pyglet.window import key
        if keys[key.LEFT]:
            dx = -1
        elif keys[key.RIGHT]:
            dx = 1
        elif keys[key.UP]:
            dy = -1
        elif keys[key.DOWN]:
            dy = 1
        elif keys[key.T]:
            self.move_target(game_map, dt)

        # Tキーで自動移動開始（再スタートできる）
        if keys[key.T]:
            self.reached_target = False  # ← ここがポイント

        # 自動移動中のみmove_targetを呼ぶ
        if not self.reached_target:
            self.move_target(game_map, dt)


        if dx != 0 or dy != 0:
            self.move(dx, dy, game_map)
