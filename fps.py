import time
from text import *
from display import *

class FPS():
    def __init__(self):
        self.time_now = time.time()
        self.delta_time = 1
        self.fps_this_frame = 1

    def update(self):
        self.delta_time = time.time()-self.time_now
        self.time_now = time.time()
        self.fps_this_frame = int(1/self.delta_time)
        self.draw()

    def draw(self):
        text.draw_number(self.fps_this_frame,2,display.window_size_small[1]-10)

fps = FPS()