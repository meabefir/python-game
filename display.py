import pygame
from helper import *

pygame.init()

class Display():
    def __init__(self):
        self.monitor_height = pygame.display.Info().current_h
        self.monitor_width = pygame.display.Info().current_w
        self.screen_ratio = self.monitor_width / self.monitor_height
        self.monitor_size = [int(self.monitor_width), int(self.monitor_height)]
        self.ratio = 5

        #self.window_size_default = self.monitor_size
        self.window_size_default = (int(600*self.screen_ratio), 600)
        self.window_size_small = self.window_size_default
        self.window_size = self.window_size_default
        self.max_zoom = 8
        self.min_zoom = .1
        self.is_fullscreen = not False

        self.toggle_fullscreen()

    def set_display(self, ratio):
        self.window_size_small = (int(self.window_size[0] // self.ratio), int(self.window_size[1] // self.ratio))
        #print(self.window_size, self.window_size_small)
        self.display = pygame.Surface(self.window_size_small)

    def set_ratio(self, new_ratio):
        self.ratio = clamp(new_ratio, self.min_zoom, self.max_zoom)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.window_size = (int(self.monitor_width*.83),int(self.monitor_height*.83))
            self.screen = pygame.display.set_mode(self.window_size, pygame.FULLSCREEN)
            self.set_display(self.ratio)
        else:
            self.window_size = self.window_size_default
            self.screen = pygame.display.set_mode(self.window_size)
            self.set_display(self.ratio)


display = Display()
