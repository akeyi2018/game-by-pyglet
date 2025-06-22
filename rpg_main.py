import pyglet
from pyglet.window import key
from settings import *
from map import Map
from customerManager import CustomerManager

class Main:
    def __init__(self):
        self.window_width = len(MAP_DATA[0]) * CELL_SIZE
        self.window_height = len(MAP_DATA) * CELL_SIZE
        self.window = pyglet.window.Window(self.window_width, self.window_height)
        self.batch = pyglet.graphics.Batch()
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        # Initialize map
        self.map = Map(self.batch, self.window_height)

        # Initialize customer
        self.customer_manager = CustomerManager(self)

        # Register events
        self.window.event(self.on_draw)
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        # self.customer_manager.draw_m()     # 四角のCustomerもここで

    def update(self, dt):
        self.customer_manager.update(dt)


if __name__ == '__main__':
    game = Main()
    pyglet.app.run()
