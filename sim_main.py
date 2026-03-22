import pyglet
from pyglet.window import key
from settings import *
from map import Map
from customer_manager import CustomerManager
from seat_manager import SeatManager
import time
import loguru

class Main():
    def __init__(self, title='SIM CAFE'):
        
        # windowの初期化
        self.window_width = len(MAP_DATA[0]) * CELL_SIZE
        self.window_height = len(MAP_DATA) * CELL_SIZE
        self.window = pyglet.window.Window(
            self.window_width, 
            self.window_height, title, resizable=True)
        self.batch = pyglet.graphics.Batch()

        # Initialize map
        self.map = Map(self.batch)

        # Initialize customer
        self.customer_manager = CustomerManager(self)

        # seat manager
        self.seat_manager = SeatManager(self)

        # Register events
        self.window.event(self.on_draw)
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

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
        self.seat_manager.update(dt)      

if __name__ == '__main__':
    # ログの初期化
    # ログファイルに出力する設定（例: customer_lifecycle.log）
    loguru.logger.add("customer_lifecycle.log", format="{time} {message}", level="INFO")
    # customer_lifecycle.logの中身をクリアする
    with open("customer_lifecycle.log", "w") as log_file:
        log_file.write("")  # 空文字を書き込んでファイルをクリア
    # ログをコンソールに出力しないようにする
    loguru.logger.remove(0)
    game = Main()
    pyglet.app.run()
