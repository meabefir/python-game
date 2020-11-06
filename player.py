import pygame, math
from entity import *
from helper import *
from input import *
from mouse import *
from mapRender import *
from camera import *
from loader import *

class Inventory():
    def __init__(self):
        self.items = []
    def add_item(self,item):
        self.items.append(item)

class Player(Entity):
    def __init__(self, x, y, image):
        self.init_entity(image, x, y, 2, 6, 10, 10)
        self.center_x = self.rect.x + self.rect.w // 2
        self.center_y = self.rect.y + self.rect.h // 2
        self.movement = [0, 0]
        self.base_speed = 2
        self.speed = self.base_speed
        self.last_facing_direction = 0
        self.collission_types = {'top': False, 'left': False, 'bottom': False, 'right': False}
        self.inventory = Inventory()

        self.z = 0
        self.z_target = self.speed
        self.bob_speed = self.speed / 5

        self.pickup_range = 50
        self.click_action = 'gather'

    def update(self):
        self.get_movement()

        self.move(self.movement, [en.rect for en in map_render.collideables])

        # change facing direction
        if self.movement[0] != 0:
            self.last_facing_direction = sign(self.movement[0])

        self.center_x = self.rect.x + self.rect.w // 2
        self.center_y = self.rect.y + self.rect.h // 2

        self.bob()

    def collission_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, movement, collideables):
        self.rect.x += movement[0]
        hit_list = self.collission_test(self.rect, collideables)
        for barrier in hit_list:
            if movement[0] > 0:
                self.rect.right = barrier.left
                self.collission_types['right'] = True
            if movement[0] < 0:
                self.rect.left = barrier.right
                self.collission_types['left'] = True

        self.rect.y += movement[1]
        hit_list = self.collission_test(self.rect, collideables)
        for barrier in hit_list:
            if movement[1] > 0:
                self.rect.bottom = barrier.top
                self.collission_types['bottom'] = True
            if movement[1] < 0:
                self.rect.top = barrier.bottom
                self.collission_types['top'] = True

    def move_on_land(self):
        for chunk,content in map_render.world_map.items():
            for tile in content:
                if tile.is_barrier == False:
                    self.rect.x = tile.rect.x
                    self.rect.y = tile.rect.y
                    return

    def simulate_click(self):
        chunk_xx = int(mouse.x // (map_render.tile_size * map_render.chunk_size))
        chunk_yy = int(mouse.y // (map_render.tile_size * map_render.chunk_size))
        dx = [-1,0,1]
        dy = [-1,0,1]
        if self.click_action == 'gather':
            for chunk_x in dx:
                for chunk_y in dy:
                    chunk = str(chunk_x+chunk_xx) + ';' + str(chunk_y+chunk_yy)
                    for en in map_render.world_map[chunk]:
                        if en.pickupable and en.rect.collidepoint(mouse.x, mouse.y) and math.dist((en.center_x, en.center_y), (
                        self.center_x, self.center_y)) <= self.pickup_range:
                            self.inventory.add_item(en)
                            map_render.world_map[chunk].remove(en)
                            break

    def get_movement(self):
        self.movement = [0, 0]
        for key, value in input.key_held.items():
            if value == True:
                if key == 'w':
                    self.movement[1] -= self.speed
                elif key == 's':
                    self.movement[1] += self.speed
                elif key == 'a':
                    self.movement[0] -= self.speed
                elif key == 'd':
                    self.movement[0] += self.speed
                elif key == 'shift':
                    self.speed = self.base_speed * 2
            else:
                if key == 'shift':
                    self.speed = self.base_speed

    def bob(self):
        if self.movement[0] != 0 or self.movement[1] != 0:
            if self.z_target != 0:
                self.z += self.bob_speed
                if self.z >= self.z_target:
                    self.z_target = 0
            else:
                self.z -= self.bob_speed
                if self.z <= 0:
                    self.z_target = self.base_speed
        else:
            if self.z > 0:
                self.z -= self.bob_speed

    def draw(self, surface):
        self.draw_rect(surface)
        img = pygame.transform.flip(self.image, not self.last_facing_direction, 0)
        surface.blit(img,
                     (
                         self.rect.x - self.rect_x_offset - camera.x,
                         self.rect.y - self.rect_y_offset - self.z - camera.y))

player = Player(0, 0, images['player'][0])