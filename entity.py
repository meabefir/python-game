import pygame

class Entity():
    def init_entity(self,rect_x,rect_y,rect_w,rect_h,rect_x_offset,rect_y_offset,image_path):
        self.rect = pygame.Rect(rect_x,rect_y,rect_w,rect_h)
        self.image = pygame.image.load(image_path)
        self.rect_x_offset = rect_x_offset
        self.rect_y_offset = rect_y_offset