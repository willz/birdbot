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
        self.Q = {}
        self.alpha = 0.7
        self.explore = 0
        self.pre_s = (9999, 9999)
        self.pre_a = 'do_nothing'

        self.Q = pickle.load(open('dict_Q'))

        def save_Q():
            pickle.dump(self.Q, open('dict_Q', 'wb'))

        atexit.register(save_Q)

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
        bird_x = state['bird'][0]
        bird_y = state['bird'][1]
        if len(state['pipes']) == 0:
            # no pipes seen, we can use a simple rule to keep bird
            # fly forward
            if bird_y < self.WINDOW_HEIGHT / 2:
                self.tap()
            return
        # calc distance between bird and next pipe
        dis_h = 9999
        dis_v = 9999
        reward = -1000 if state['bird'][2] == 'dead' else 1
        for i in range(1, len(state['pipes']), 2):
            # the buttom pipe
            p = state['pipes'][i]
            if bird_x <= p[0] + self.PIPE_WIDTH:
                dis_h = p[0] + self.PIPE_WIDTH - bird_x
                dis_v = p[1] - bird_y
                break
        # zoom out to reduce learn time
        scale = 4
        dis_h /= scale
        dis_v /= scale
        # update Q(s, a)
        self.Q.setdefault((dis_h, dis_v), {'tap': 0, 'do_nothing': 0})
        self.Q.setdefault(self.pre_s, {'tap': 0, 'do_nothing': 0})
        tap_v = self.Q[(dis_h, dis_v)]['tap']
        nothing_v = self.Q[(dis_h, dis_v)]['do_nothing']
        self.Q[self.pre_s][self.pre_a] += self.alpha * (reward + \
                max(tap_v, nothing_v) - self.Q[self.pre_s][self.pre_a])
        
        self.pre_s = (dis_h, dis_v)
        # choose action
        if random.randint(0, self.explore) > 100:
            self.pre_a = "do_nothing" if random.randint(0, 1) else "tap"
        else:
            tap_v = self.Q[self.pre_s]['tap']
            nothing_v = self.Q[self.pre_s]['do_nothing']
            self.pre_a = "do_nothing" if tap_v <= nothing_v else "tap"
        if self.pre_a == 'tap':
            self.tap()
        else:
            pass
            #print 'do_nothing'
        #print self.Q

        if self.explore:
            self.explore -= 1
        

if __name__ == '__main__':
    show_window = True
    enable_sound = True
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
    
