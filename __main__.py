import pyglet
import resource
from pyglet.window import mouse
from game import *

game = Game()

pyglet.clock.schedule_interval(game.update, Game.TIME_INTERVAL)

# create window
window = pyglet.window.Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT, vsync = False)

@window.event
def on_draw():
    window.clear()
    game.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        pass
    if game.state == 'INIT' or game.state == 'FAILED':
        if 30 < x and x < 130 and 150 < y and y < 205:
            game.restart()
            game.state = 'READY'
    elif game.state == 'READY':
        game.play()
    elif game.state == 'PLAY':
        game.bird.jump()

pyglet.app.run()
