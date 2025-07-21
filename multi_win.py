import pyglet
from pyglet.window import key

class WindowContext:
    def __init__(self, width, height, title, manager=None):
        self.window = pyglet.window.Window(width, height, caption=title)
        self.batch = pyglet.graphics.Batch()

        # ラベルなどの描画要素をこのリストに追加して管理できる
        self.labels = []

        # ここにスプライトや他の Drawable も追加可能
        self.manager = manager  # 管理クラスからの参照（必要なら）

        # イベント登録
        self.window.push_handlers(
            on_draw=self.on_draw,
            on_key_press=self.on_key_press,
            on_close=self.on_close,
        )

        self._setup()  # 任意の初期セットアップ

    def _setup(self):
        # 例：バッチに登録するラベルを作成
        label = pyglet.text.Label("Hello Window!",
                                  x=10, y=self.window.height - 30,
                                  batch=self.batch)
        self.labels.append(label)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.window.close()
        elif symbol == key.N and self.manager is not None:
            print("WindowContext: Nキーで新しいウィンドウ作成要求")
            self.manager.create_new_window()

    def on_close(self):
        print(f"WindowContext: Window closed {self.window}")
        if self.manager:
            self.manager.unregister_window(self)

class WindowManager:
    def __init__(self):
        self.contexts = []
        self.create_new_window(400, 300, "Main Window")

    def create_new_window(self, w=300, h=200, title="Sub Window"):
        context = WindowContext(w, h, title, manager=self)
        self.contexts.append(context)

    def unregister_window(self, context):
        if context in self.contexts:
            self.contexts.remove(context)

if __name__ == '__main__':
    manager = WindowManager()
    pyglet.app.run()
