import pygame,math
from entity import *
from helper import *

class Player(Entity):
    def __init__(self, x, y, image):
        self.init_entity(image, x, y, 3, 10, 8, 8)
        self.center_x = self.rect.x + self.rect.w//2
        self.center_y = self.rect.y + self.rect.h//2
        self.movement = [0, 0]
        self.speed = 2
        self.last_facing_direction = 0

        self.z = 0
        self.z_target = self.speed
        self.bob_speed = self.speed / 5

        self.inventory = []
        self.pickup_range = 50
        self.click_action = 'gather'

    def update(self, key_held):
        self.get_movement(key_held)

        # change facing direction
        if self.movement[0] != 0:
            self.last_facing_direction = sign(self.movement[0])
        self.rect.x += self.movement[0]
        self.rect.y += self.movement[1]
        self.center_x = self.rect.x + self.rect.w // 2
        self.center_y = self.rect.y + self.rect.h // 2

        self.bob()

    def simulate_click(self,mx,my,entities):
        if self.click_action == 'gather':
            for en in entities:
                if en.rect.collidepoint(mx,my) and math.dist((en.center_x,en.center_y),(self.center_x,self.center_y)) <= self.pickup_range and en.pickupable:
                    self.inventory.append(en)
                    entities.remove(en)

    def get_movement(self, key_held):
        self.movement = [0, 0]
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

    def bob(self):
        if self.movement[0] != 0 or self.movement[1] != 0:
            if self.z_target != 0:
                self.z += self.bob_speed
                if self.z >= self.z_target:
                    self.z_target = 0
            else:
                self.z -= self.bob_speed
                if self.z <= 0:
                    self.z_target = self.speed
        else:
            if self.z > 0:
                self.z -= self.bob_speed

    def draw(self, surface, camera_xy):
        camera_x, camera_y = camera_xy
        self.draw_rect(surface, camera_xy)
        img = pygame.transform.flip(self.image, not self.last_facing_direction, 0)
        surface.blit(img,
                     (
                         self.rect.x - self.rect_x_offset - camera_x,
                         self.rect.y - self.rect_y_offset - self.z - camera_y))
