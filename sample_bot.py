import pyglet
from pybird.window import *
import random

class Bot:
    def __init__(self):
        # constants
        self.WINDOW_HEIGHT = game.WINDOW_HEIGHT
        self.PIPE_WIDTH = game.PIPE_WIDTH
        # this flag is used to make sure at most one tap during
        # every call of run()
        self.tapped = False
        
        # pause planning until the game is finished completely
        self.pause = False
        game.play()

        # variables for plan
        self.Q = {}
        self.alpha = 0.7
        self.explore = 0
        self.pre_s = (9999, 9999)
        self.pre_a = 'do_nothing'

    # this method is auto called every 0.1s by the pyglet
    def run(self, dt):
        if game.state == 'PLAY':
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
        if game.state == 'FAILED':
            # restart game
            game.restart()
            game.play()
            self.pause = False

    # get the state that robot needed
    def get_state(self):
        state = {}
        # bird's position and status(dead or alive)
        state['bird'] = (int(round(game.bird.x)), int(round(game.bird.y)), 'alive')
        state['pipes'] = []
        # pipes' position
        for i in range(1, len(game.pipes), 2):
            p = game.pipes[i]
            if p.x < game.WINDOW_WIDTH:
                # this pair of pipes shows on screen
                x = int(round(p.x))
                y = int(round(p.y))
                state['pipes'].append((x, y))
                state['pipes'].append((x, y - game.PIPE_HEIGHT_INTERVAL))
        return state

    # simulate the click action, bird will fly higher when tapped
    # It can be called only once every time slice(every execution cycle of plan())
    def tap(self):
        if not self.tapped:
            game.bird.jump()
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
            p = state['pipes'][i]
            if bird_x <= p[0] + self.PIPE_WIDTH:
                dis_h = p[0] + self.PIPE_WIDTH - bird_x
                dis_v = p[1] - bird_y
                break
        dis_h /= 8
        dis_v /= 8
        print dis_v
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
    bot = Bot()
    pyglet.clock.schedule_interval(bot.run, 0.1)
    pyglet.app.run()
    
