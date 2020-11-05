import pygame
import random
from helper import *

light_sources = []

class LightSource():
    def __init__(self, pos, target=None):
        if target is None:
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = target.x + target.w // 2
            self.y = target.y + target.h // 2
        self.target = target
        self.radius = 50
        self.max_radius = self.radius * 1.2
        self.min_radius = self.radius * 0.8

    def flicker(self):
        self.radius += random.randint(0, 2) - 1
        self.radius = clamp(self.radius, self.min_radius, self.max_radius)

    def draw(self, surface,camera):
        if self.target is not None:
            self.x += (self.target.x + self.target.w // 2 - self.x) / 2
            self.y += (self.target.y + self.target.h // 2 - self.y) / 2
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x - camera.x), int(self.y - camera.y)),
                               int(self.radius))
        else:
            pygame.draw.circle(surface, (255, 255, 255), (int(light.x - camera.x), int(light.y - camera.y)),
                               int(self.radius))