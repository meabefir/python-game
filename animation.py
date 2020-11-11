import pygame
from loader import animations as loader_animations

class Animation():
    def __init__(self,animations,frame_update_interval):
        self.load_animations(animations)
        self.animation_frame = 0
        self.current_animation = None
        self.previous_animation = None
        self.frame_update_interval = frame_update_interval
        self.set_current_animation(list(self.animations.keys())[0])

    def load_animations(self,animations):
        self.animations = {}
        for animation in animations:
            for image in loader_animations[animation]:
                if animation in self.animations:
                    self.animations[animation].append(image)
                else:
                    self.animations[animation] = [image]

    def iterate_animation_frame(self):
        next_animation_frame = self.animation_frame + 1 / self.frame_update_interval[self.current_animation]
        if next_animation_frame < len(self.animations[self.current_animation]):
            self.animation_frame = next_animation_frame
        else:
            self.animation_frame = 0

    def set_current_animation(self,new_animation):
        self.previous_animation = self.current_animation
        self.current_animation = new_animation
        if self.previous_animation != self.current_animation:
            self.animation_frame = 0