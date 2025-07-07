import pyglet

class DoorButton:
    def __init__(self, x, y, cell_size, batch, on_click):
        self.sprite = pyglet.shapes.Rectangle(
            x , y, cell_size, cell_size,
            color=(255, 0, 0), batch=batch
        )
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.on_click = on_click
        self.is_open = False  # 初期状態：閉じている

    def hit_test(self, mx, my):
        return (
            self.x <= mx < self.x + self.cell_size and
            self.y <= my < self.y + self.cell_size
        )

    def click(self):
        self.is_open = not self.is_open
        grid_x = self.x // self.cell_size
        grid_y = self.y // self.cell_size

        if self.is_open:
            self.sprite.color = (0, 255, 0)  # 開：緑
            self.on_click(grid_x, grid_y, True)   # 開けた
        else:
            self.sprite.color = (255, 0, 0)  # 閉：赤
            self.on_click(grid_x, grid_y, False)  # 閉めた
