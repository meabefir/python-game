import pygame
from display import *
from helper import *
from lightSource import *
from mapRender import *

class GameTime():
    def __init__(self):
        self.time = 2000
        self.day_length = 2400
        self.sunset = 2000
        self.sunrise = 500
        self.gray_shade = 255
        self.min_gray_shade = 0
        self.max_grey_shade = 255
        self.time_speed = .5

    def update(self):
        #print(self.time)
        self.increment_time()
        self.set_gray_shade()

        black = pygame.Surface(display.window_size_small)
        pygame.draw.rect(black, (self.gray_shade,self.gray_shade,self.gray_shade), (0, 0, display.window_size_small[0], display.window_size_small[1]))

        if self.time >= self.sunset or self.time <= self.sunrise+self.max_grey_shade/self.time_speed:
            for light in light_sources:
                if light.target in map_render.entities:
                    light.draw(black)

        display.display.blit(black, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    def increment_time(self):
        self.time += self.time_speed
        if self.time > self.day_length:
            self.time = 0

    def set_gray_shade(self):
        if self.time > self.sunset or self.time < self.sunrise:
            self.gray_shade -= self.time_speed
        else:
            self.gray_shade += self.time_speed
        self.gray_shade = clamp(self.gray_shade, self.min_gray_shade, self.max_grey_shade)

game_time = GameTime()