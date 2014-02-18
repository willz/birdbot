import pyglet
import resource

class Bird(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Bird, self).__init__(*args, **kwargs)
        self.GRAVITY_ACC = 400
        self.ANGULAR_ACC = 300
        self.speed = 0
        self.ang_speed = 0

    def update(self, dt):
        # bird only moves up and down, so the speed is the y speed
        self.speed += self.GRAVITY_ACC * dt
        self.y -= self.speed * dt
        self.rotate(dt)

    def rotate(self, dt):
        self.ang_speed += self.ANGULAR_ACC * dt
        self.rotation += self.ang_speed * dt
        if self.rotation > 90:
            self.rotation = 90

    # tapping the screen, the bird will jump up
    def jump(self):
        if self.speed > 0:
            self.speed = 0
        self.speed -= 50
        self.y += 20
        self.ang_speed = 0
        self.rotation = -30
        resource.tap_sound.play()


        

