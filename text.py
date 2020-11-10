import pygame
from loader import *
from display import *

class Text():
    def __init__(self):
        self.digit_img_white = []
        self.digit_img_black = []
        for i in range(10):
            self.digit_img_white.append(images[f'{i}-white'][0])
        for i in range(10):
            self.digit_img_black.append(images[f'{i}-black'][0])

    def draw_number(self,number,x,y):
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img_black[int(ch)],(x+4*i+1,y))
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img_black[int(ch)],(x+4*i,y+1))
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img_black[int(ch)],(x+4*i-1,y))
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img_black[int(ch)],(x+4*i,y-1))
        for i,ch in enumerate(str(number)):
            display.display.blit(self.digit_img_white[int(ch)],(x+4*i,y))

text = Text()