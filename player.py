import pyglet
from map import Map

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
            
    def update(self, keys, game_map):
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

        if dx != 0 or dy != 0:
            self.move(dx, dy, game_map)