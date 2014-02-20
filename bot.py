import pyglet
import random
import pickle
import atexit
from pybird.game import Game

class Bot:
    def __init__(self, game):
        self.game = game
        # constants
        self.WINDOW_HEIGHT = Game.WINDOW_HEIGHT
        self.PIPE_WIDTH = Game.PIPE_WIDTH
        # this flag is used to make sure at most one tap during
        # every call of run()
        self.tapped = False
        
        # pause planning until the game is finished completely
        self.pause = False
        self.game.play()

        # variables for plan

        # Do something when exiting(e.x. save the data learned)
        def do_at_exit():
            print 'The bot died'

        atexit.register(do_at_exit)


    # this method is auto called every 0.05s by the pyglet
    def run(self, dt):
        if self.game.state == 'PLAY':
            self.tapped = False
            # call plan() to execute your plan
            self.plan(self.get_state())
        elif not self.pause:
            state = self.get_state()
            bird_state = list(state['bird'])
            bird_state[2] = 'dead'
            state['bird'] = bird_state
            # do NOT allow tap
            self.tapped = True
            self.plan(state)
            self.pause = True
        if self.game.state == 'FAILED':
            # restart game
            print 'score:', self.game.record.get(), 'best: ', self.game.record.best_score
            self.game.restart()
            self.game.play()
            self.pause = False

    # get the state that robot needed
    def get_state(self):
        state = {}
        # bird's position and status(dead or alive)
        state['bird'] = (int(round(self.game.bird.x)), \
                int(round(self.game.bird.y)), 'alive')
        state['pipes'] = []
        # pipes' position
        for i in range(1, len(self.game.pipes), 2):
            p = self.game.pipes[i]
            if p.x < Game.WINDOW_WIDTH:
                # this pair of pipes shows on screen
                x = int(round(p.x))
                y = int(round(p.y))
                state['pipes'].append((x, y))
                state['pipes'].append((x, y - Game.PIPE_HEIGHT_INTERVAL))
        return state

    # simulate the click action, bird will fly higher when tapped
    # It can be called only once every time slice(every execution cycle of plan())
    def tap(self):
        if not self.tapped:
            self.game.bird.jump()
            self.tapped = True

    # That's where the robot actually works
    # NOTE Put your code here
    def plan(self, state):
        pass

if __name__ == '__main__':
    # some config
    show_window = True
    enable_sound = True

    # do NOT edit the code below
    game = Game()
    game.set_sound(enable_sound)
    pyglet.clock.schedule_interval(game.update, 0.05)
    bot = Bot(game)
    pyglet.clock.schedule_interval(bot.run, 0.05)

    if show_window:
        window = pyglet.window.Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT, vsync = False)
        @window.event
        def on_draw():
            window.clear()
            game.draw()
        pyglet.app.run()
    else:
        pyglet.app.run()
    
