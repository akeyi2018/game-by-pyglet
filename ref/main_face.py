import pyglet

from face_animation import FaceAnimation

win = pyglet.window.Window(400, 300)
face = FaceAnimation()

@win.event
def on_draw():
    win.clear()
    face.sprite.draw()

@win.event
def on_mouse_press(x, y, button, modifiers):
    face.on_click(x, y)

def update(dt):
    face.update(dt)

pyglet.clock.schedule_interval(update, 1/60)
pyglet.app.run()
