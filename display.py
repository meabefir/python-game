import pygame
from helper import *
pygame.init()

class Display():
    def __init__(self):
        self.ratio = 4
        self.window_size_small = (900,600)
        self.window_size = (900, 600)
        self.max_zoom = 8
        self.min_zoom = .1
        self.is_fullscreen = False
        self.monitor_height =pygame.display.Info().current_h
        self.monitor_size = [int(self.monitor_height*1.5),int(self.monitor_height)]
        self.screen = pygame.display.set_mode(self.window_size,pygame.RESIZABLE)
        self.set_display(self.ratio)

    def set_display(self,ratio):
        self.window_size_small = (int(self.window_size[0] // self.ratio), int(self.window_size[1] // self.ratio))
        self.display = pygame.Surface(self.window_size_small)

    def set_ratio(self,new_ratio):
        self.ratio = clamp(new_ratio,self.min_zoom,self.max_zoom)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.window_size = self.monitor_size
            self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
            self.set_display(self.ratio)
        else:
            self.window_size = self.window_size_small
            self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
            self.set_display(self.ratio)


display = Display()
