import pygame
import random
from helper import *
from camera import *

light_sources = []

from gameTime import *

class LightSource():
    def __init__(self, pos, radius,target=None,flickers=False):
        self.flickers = flickers
        if target is None:
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = target.x + target.w // 2
            self.y = target.y + target.h // 2
        self.target = target
        self.radius = radius
        self.finnesse = 1
        self.max_radius = self.radius * 1.2
        self.min_radius = self.radius * 0.8
        self.visibility = 100

    def draw(self, surface):
        if self.flickers:
            self.radius += random.randint(0, 2) - 1
            self.radius = clamp(self.radius, self.min_radius, self.max_radius)
        # if self.target is not None:
        #     self.x += (self.target.x + self.target.w // 2 - self.x) / 1
        #     self.y += (self.target.y + self.target.h // 2 - self.y) / 1
        #     test = pygame.Surface((int(self.max_radius * 2), int(self.max_radius * 2)))
        #     test_mid = int(self.max_radius)
        #     for i in reversed(range(self.finnesse)):
        #         color = [(255 - i * 10 - self.visibility)] * 3
        #         if game_time.gray_shade > color[0]: continue
        #         #
        #         pygame.draw.circle(test, color, (test_mid, test_mid),
        #                            int(self.radius - (self.finnesse - 1 - i) * 2))
        #     surface.blit(test,((int(self.x - camera.x-test_mid), int(self.y - camera.y-test_mid))),special_flags=pygame.BLEND_RGB_MULT)
        if self.target is not None:
            self.x += (self.target.x + self.target.w // 2 - self.x) / 1
            self.y += (self.target.y + self.target.h // 2 - self.y) / 1
            for i in reversed(range(self.finnesse)):
                color = [(255-i*10-self.visibility)]*3
                if game_time.gray_shade > color[0]: continue
                pygame.draw.circle(surface, color, (int(self.x - camera.x), int(self.y - camera.y)),
                                   int(self.radius-(self.finnesse-1-i)*2))

        else:
            light_sources.remove(self)