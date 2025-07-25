import pyglet
from pyglet.window import key
from settings import *
from map import Map
from customerManager import CustomerManager
from seat_manager import SeatManager
import time

class Main():
    def __init__(self, title='SIM CAFE'):
        
        self.log_file = open("customer_lifecycle.log", "w", encoding="utf-8")
        self.start_time = time.time()

        # ログ関数を作って渡す
        self.log = self._create_logger()

        self.window_width = len(MAP_DATA[0]) * CELL_SIZE
        self.window_height = len(MAP_DATA) * CELL_SIZE
        self.window = pyglet.window.Window(
            self.window_width, 
            self.window_height, title, resizable=True)
        self.batch = pyglet.graphics.Batch()

        # Initialize map
        self.map = Map(self.batch, self.window_height)

        # Initialize customer
        self.customer_manager = CustomerManager(self, log_func=self.log)

        # seat manager
        self.seat_manager = SeatManager(self, log_func=self.log)

        # Register events
        self.window.event(self.on_draw)
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def _create_logger(self):
        def log(message: str):
            timestamp = round(time.time() - self.start_time, 2)
            self.log_file.write(f"[{timestamp}] {message}\n")
            self.log_file.flush()
        return log

    def close(self):
        self.log_file.close()

    def on_draw(self):
        self.window.clear()
        if self.batch is not None:
            try:
                self.batch.draw()
            except Exception as e:
                print(f"[ERROR] Batch drawing failed: {e}")

    def on_mouse_press(self,x,y,button, modifiers):
        self.map.on_mouse_press(x,y,button,modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.window.close()
        elif symbol == key.N:
            print("WindowContext: Nキーで新しいウィンドウ作成要求")

    def update(self, dt):
        self.customer_manager.update(dt)
        self.seat_manager.update(dt)      # 座席までの移動処理

if __name__ == '__main__':
    game = Main()
    pyglet.app.run()
