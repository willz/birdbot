import pyglet
from pyglet.window import mouse
from game import *
import resource

window = pyglet.window.Window(resource.bg_day.width, resource.bg_day.height)

game = Game()

pyglet.clock.schedule_interval(game.update, 0.05)

@window.event
def on_draw():
    window.clear()
    resource.bg_day.blit(0, 0)
    game.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print x, y
    if game.state == 'INIT' or game.state == 'FAILED':
        if 30 < x and x < 130 and 150 < y and y < 205:
            game.reset()
            game.state = 'READY'
    elif game.state == 'READY':
        game.state = 'PLAY'
    elif game.state == 'PLAY':
        game.bird.jump()
    print game.bird.y
