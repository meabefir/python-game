import pygame
from camera import *
from display import *

class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self,event = None):
        m_pos = pygame.mouse.get_pos()
        self.x,self.y = (m_pos[0] / display.ratio + camera.x), (m_pos[1] / display.ratio + camera.y)

mouse = Mouse()