import pygame
from camera import *

class Entity():
    def __init__(self, image, rect_x, rect_y, rect_x_offset, rect_y_offset, rect_w=0, rect_h=0):
        self.init_entity(image, rect_x, rect_y, rect_x_offset, rect_y_offset, rect_w, rect_h)

    def init_entity(self, image, rect_x, rect_y, rect_x_offset, rect_y_offset, rect_w=0, rect_h=0):
        self.pickupable = False
        self.is_barrier = False
        self.type = None
        self.image = image
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        if rect_w == 0 and rect_h == 0:
            rect_w = self.w
            rect_h = self.h
        self.rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
        self.center_x = self.rect.x + self.rect.w//2
        self.center_y = self.rect.y + self.rect.h//2
        self.rect_x_offset = rect_x_offset
        self.rect_y_offset = rect_y_offset

    def set_type(self,type):
        self.type = type

    def set_pickupable(self):
        self.pickupable = True

    def set_barrier(self):
        self.is_barrier = True

    def draw_rect(self, surface):
        pygame.draw.rect(surface, (255, 0, 0),
                         (self.rect.x - camera.x, self.rect.y - camera.y, self.rect.w, self.rect.h),1)

    def draw(self, surface):
        surface.blit(self.image,
                     (self.rect.x - self.rect_x_offset - camera.x, self.rect.y - self.rect_y_offset - camera.y))
