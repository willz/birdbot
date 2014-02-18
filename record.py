import pyglet

class Record:
    def __init__(self):
        # score
        self.best_score = 0
        self.cur_score = 0

    def get(self):
        return self.cur_score

    def inc(self):
        self.cur_score += 1

    def reset(self):
        self.cur_score = 0

    def save(self):
        if self.cur_score > self.best_score:
            self.best_score = self.cur_score

    # draw a number image using the digit images. imgs[i] should
    # correspond to digit i
    @staticmethod
    def draw_num(num, imgs, x, y):
        if num == 0:
            s = pyglet.sprite.Sprite(imgs[0], x, y)
            s.draw()
        w = imgs[0].width
        vals = []
        while num:
            r = num % 10
            vals.insert(0, r)
            num /= 10
        seq = []
        batch = pyglet.graphics.Batch()
        for i in range(len(vals)):
            s = pyglet.sprite.Sprite(imgs[vals[i]], x + i * w, y, batch = batch)
            seq.append(s)
        batch.draw()

        
