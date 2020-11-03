import pygame
from helper import *

class Player():
    def __init__(self,x,y):
        self.image = pygame.image.load('images/player/player.png')
        self.rect = pygame.Rect(x,y,14,14)
        self.rect_x_offset = 0
        self.rect_y_offset = 0
        self.movement = [0,0]
        self.speed = 3
        self.last_facing_direction = 0

    def update(self,key_held):
        self.movement = [0,0]
        for key, value in key_held.items():
            if value == True:
                if key == 'w':
                    self.movement[1] -= self.speed
                elif key == 's':
                    self.movement[1] += self.speed
                elif key == 'a':
                    self.movement[0] -= self.speed
                elif key == 'd':
                    self.movement[0] += self.speed
        if self.movement[0] != 0:
            self.last_facing_direction = sign(self.movement[0])
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]

    def draw(self,surface,scroll):
        # pygame.draw.rect(surface, (255, 0, 0),
        #                  (self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.w, self.rect.h))
        surface.blit(pygame.transform.flip(self.image, not self.last_facing_direction, 0),(self.rect.x-self.rect_x_offset-scroll[0],self.rect.y-self.rect_y_offset-scroll[1]))