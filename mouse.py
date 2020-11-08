import pygame
from camera import *
from display import *
from player import *

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.clicked = False
        self.held = False

    def update(self,event = None):
        # if self.clicked or self.held:
        #     player.simulate_click()
        m_pos = pygame.mouse.get_pos()
        self.x,self.y = (m_pos[0] / display.ratio + camera.x), (m_pos[1] / display.ratio + camera.y)
        self.clicked = False

    def set_clicked(self):
        self.clicked = True
    def set_held(self):
        self.held = True
    def set_up(self):
        self.held = False

mouse = Mouse()