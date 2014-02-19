import pyglet
from pybird.window import *

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
        # NOTE put the instance variable you need here

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
        pass
        

if __name__ == '__main__':
    bot = Bot()
    pyglet.clock.schedule_interval(bot.run, 0.1)
    pyglet.app.run()
    
