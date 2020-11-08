import pygame,time
from images import *
from mapRender import *
from camera import *

pygame.init()

class ActionOverlay():
    def __init__(self,target,type,full):
        self.target = target
        self.type = type
        self.current = 0
        self.full = full
        self.border_img = images['action-overlay-border'][0]
        self.bar_img = images['action-overlay-bar'][0]
        self.rect = pygame.Rect(self.target.rect.x-self.target.rect_x_offset,self.target.rect.y+self.target.rect.h+2,14,6)

    def update(self,current,player):
        self.current = current
        self.rect.x = self.target.rect.x-self.target.rect_x_offset
        self.rect.y = self.target.rect.y+self.target.rect.h+2

    def draw(self,surface):
        bar_width = int((self.current/self.full)*10)+1
        surface.blit(self.border_img,(self.rect.x-camera.x,self.rect.y-camera.y))
        surface.blit(pygame.transform.scale(self.bar_img,(bar_width,2)),(self.rect.x-camera.x+2,self.rect.y-camera.y+2))

class InfoOverlay():
    def __init__(self):
        self.duration = 5
        self.created_at = time.time()
        self.font = pygame.font.SysFont('calibri',5)
