import pygame
from helper import *

class Display():
    def __init__(self):
        self.ratio = 2
        self.window_size = (900, 600)
        self.max_zoom = 5
        self.min_zoom = .1
        self.screen = pygame.display.set_mode(self.window_size)
        self.set_display(self.ratio)

    def set_display(self,ratio):
        self.window_size_small = (int(self.window_size[0] // self.ratio), int(self.window_size[1] // self.ratio))
        self.display = pygame.Surface(self.window_size_small)

    def set_ratio(self,new_ratio):
        self.ratio = clamp(new_ratio,self.min_zoom,self.max_zoom)

display = Display()
#
# def set_display(new_ratio):
#     print(new_ratio)
#     global ratio
#     global display
#     global window_size_small
#     ratio = new_ratio
#     window_size_small = (int(window_size[0] // ratio), int(window_size[1] // ratio))
#     display = pygame.Surface(window_size_small)
#
# ratio = 2
# window_size = (900, 600)
# screen = pygame.display.set_mode(window_size)
# display = None
# window_size_small = None
# set_display(2)
