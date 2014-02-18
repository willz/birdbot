import pyglet

class Pipe(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Pipe, self).__init__(*args, **kwargs)
        self.SPEED = 80 
        self.scored = False

    def update(self, dt):
        # bird only moves up and down, so the speed is the y speed
        self.x -= self.SPEED * dt
