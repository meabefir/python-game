import pygame
from loader import *
from display import *

class Text():
    def __init__(self):
        self.digit_img = []
        for i in range(10):
            self.digit_img.append(images[f'{i}'][0])

    def draw_number(self,number,x,y):
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img[int(ch)],(x+4*i,y))

text = Text()