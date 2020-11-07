import pygame, math,time
from entity import *
from helper import *
from input import *
from mapRender import *
from camera import *
from loader import *
from data import *
from overlay import *

class Inventory():
    def __init__(self):
        self.items = []
        self.equiped = 'god'
        self.pickup_start = None
        self.action = None

    def add_item(self,en_data):
        items_to_add = (en_data['yield'][0],random.randint(en_data['yield'][1][0],en_data['yield'][1][1]))
        self.items.append(items_to_add)

    def init_pickup(self,en,chunk):
        if self.equiped not in entity_data[en.name]['gather_time']: return
        player.action = 'in_progress'
        self.action = 'pickup'
        self.en_data = entity_data[en.name]
        self.en = en
        self.en_chunk = chunk
        self.pickup_start = time.time()
        self.pickup_overlay = ActionOverlay(player, 'pickup',self.en_data['gather_time'][self.equiped])
        map_render.overlay.append(self.pickup_overlay)

    def iterate_pickup(self):
        if player.mouse.held and player.in_range_and_mouseover(self.en):
            delta_time = time.time()-self.pickup_start
            self.pickup_overlay.update(delta_time,player)
            # if mined for long enough
            if delta_time >= self.en_data['gather_time'][self.equiped]:
                # add to inv
                self.add_item(self.en_data)
                # remove it from the world map
                map_render.world_map[self.en_chunk].remove(self.en)
                # replace it with water if is tile type
                if self.en.type == 'tile':
                    x = self.en.rect.x//map_render.tile_size
                    y = self.en.rect.y//map_render.tile_size
                    map_render.world_map[self.en_chunk].append(map_render.entity_from_data('water',x,y))
                self.reset_pickup()
        else:
            self.reset_pickup()

    def reset_pickup(self):
        map_render.overlay.remove(self.pickup_overlay)
        self.pickup_overlay = None
        self.action = None
        self.pickup_start = None
        player.action = None

    def update(self):
        #print(self.items)
        if self.action == 'pickup':
            self.iterate_pickup()

class Player(Entity):
    def __init__(self, x, y, image):
        self.rect_x_offset = 2
        self.rect_y_offset = 6
        self.init_entity('player',image, x, y, self.rect_x_offset, self.rect_y_offset, 10, 10)
        self.height = 10
        self.center_x = self.rect.x + self.rect.w // 2
        self.center_y = self.rect.y + self.rect.h // 2
        self.movement = [0, 0]
        self.default_speed = 1
        self.base_speed = self.default_speed
        self.speed = self.default_speed
        self.last_facing_direction = 0
        self.collission_types = {'top': False, 'left': False, 'bottom': False, 'right': False}
        self.inventory = Inventory()

        self.z = 0
        self.z_target = self.speed
        self.bob_speed = self.speed / 5

        self.pickup_range = 50
        self.click_action = 'gather'
        self.action = None

        self.fly = False
        self.fly_speed = 10

    def set_godmode(self):
        self.fly = not self.fly
        self.base_speed = self.fly_speed if self.fly == True else self.default_speed

    def update(self,mouse):
        self.mouse = mouse
        self.inventory.update()
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
        if not self.fly:
            hit_list = self.collission_test(self.rect, collideables)
            for barrier in hit_list:
                if movement[0] > 0:
                    self.rect.right = barrier.left
                    self.collission_types['right'] = True
                if movement[0] < 0:
                    self.rect.left = barrier.right
                    self.collission_types['left'] = True

        self.rect.y += movement[1]
        if not self.fly:
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
                self.rect.x = tile.rect.x
                self.rect.y = tile.rect.y
                if self.collission_test(self.rect, map_render.collideables) == []:
                #if tile.is_barrier == False:
                    self.rect.x = tile.rect.x
                    self.rect.y = tile.rect.y
                    return

    def simulate_click(self):
        if self.action == 'in_progress':return
        chunk_xx = int(self.mouse.x // (map_render.tile_size * map_render.chunk_size))
        chunk_yy = int(self.mouse.y // (map_render.tile_size * map_render.chunk_size))
        dx = [-1,0,1]
        dy = [-1,0,1]
        if self.click_action == 'gather':
            for chunk_x in dx:
                for chunk_y in dy:
                    chunk = str(chunk_x+chunk_xx) + ';' + str(chunk_y+chunk_yy)
                    if chunk in map_render.world_map:
                        for en in map_render.world_map[chunk]:
                            if en.pickupable and self.in_range_and_mouseover(en):
                                self.inventory.init_pickup(en,chunk)
                                break

    def in_range_and_mouseover(self,en):
        return en.rect.collidepoint(self.mouse.x, self.mouse.y) and math.dist((en.center_x, en.center_y), (
                            self.center_x, self.center_y)) <= self.pickup_range

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