import pyglet
import imgui
from imgui.integrations.pyglet import PygletRenderer

window = pyglet.window.Window(width=800, height=600)
imgui.create_context()
impl = PygletRenderer(window)

@window.event
def on_draw():
    window.clear()
    impl.render(imgui.get_draw_data())

def update(dt):
    imgui.new_frame()
    imgui.begin("ウィンドウ")
    if imgui.button("クリック！"):
        print("押された！")
    imgui.end()
    imgui.render()

pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
