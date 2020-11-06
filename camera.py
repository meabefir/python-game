from display import *

class Camera():
    def __init__(self,x,y):
        self.true_x = x
        self.true_y = y
        self.x = int(self.true_x)
        self.y = int(self.true_y)
        self.target = None
        self.lerp_speed = 1

    def set_target(self,target):
        self.target = target

    def update(self):
        self.true_x += (self.target.rect.x - self.true_x - display.window_size_small[0] / 2 + self.target.rect.w // 2) / self.lerp_speed
        self.true_y += (self.target.rect.y - self.true_y - display.window_size_small[1] / 2 + self.target.rect.h // 2) / self.lerp_speed
        self.x = int(self.true_x)
        self.y = int(self.true_y)
        self.offset = (self.x,self.y)

camera = Camera(0,0)