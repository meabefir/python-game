import pygame,math
from camera import *
from display import *

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.window_x = 0
        self.window_y = 0
        self.clicked = False
        self.held = False

    def update(self, event=None):
        m_pos = pygame.mouse.get_pos()
        self.x, self.y = (m_pos[0] / display.ratio + camera.x), (m_pos[1] / display.ratio + camera.y)
        self.window_x, self.window_y = (m_pos[0] / display.ratio, m_pos[1] / display.ratio)
        self.clicked = False

    def set_clicked(self):
        self.clicked = True

    def set_held(self):
        self.held = True

    def set_up(self):
        self.held = False

    def distance_from_player(self,player):
        return math.dist((self.x,self.y),(player.center_x,player.center_y))


mouse = Mouse()
