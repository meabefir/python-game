import pygame, math, time
from entity import *
from helper import *
from input import *
from mapRender import *
from camera import *
from loader import *
from data import *
from overlay import *
from text import *

font = pygame.font.SysFont('calibri',8)

class InvTile():
    def __init__(self,inv,row,col):
        self.inventory = inv
        self.row = row
        self.col = col
        self.item = None
        self.item_count = 0

    def set_item(self,item,item_count,image):
        self.item = item
        self.item_count = item_count
        self.img = image
        self.item_count_render_black = font.render(str(self.item_count),False,(0,0,0))
        self.item_count_render_white = font.render(str(self.item_count),False,(255,255,255))

    def draw(self):
        x = self.inventory.inventory_en.rect.x+5+(self.col-1)*16
        y = self.inventory.inventory_en.rect.y+5+(5-self.row)*16
        display.display.blit(self.img,(x,y))
        #display.display.blit(self.item_count_render_black,(x+16-4*len(str(self.item_count))+1,y+8+1))
        #display.display.blit(self.item_count_render_white,(x+16-4*len(str(self.item_count)),y+8))
        text.draw_number(self.item_count,x+16-4*len(str(self.item_count)),y+8)


class Inventory():
    def __init__(self):
        self.items = []
        self.equiped = 'god'
        self.pickup_start = None
        self.action = None
        self.en = None
        self.pickup_overlay = None
        self.state = 'hotbar'
        self.rows = 5
        self.cols = 10

        for row in range(self.rows):
            for col in range(self.cols):
                self.items.append(InvTile(self,row+1,col+1))
        self.set_inv_en()

    def set_inv_en(self):
        self.hotbar_en = Entity('hotbar', images['hotbar'][0],
                                display.window_size_small[0] / 2 - images['hotbar'][0].get_width() / 2,
                                display.window_size_small[1] - images['hotbar'][0].get_height(), 0, 0)
        self.inventory_en = Entity('inventory', images['inventory'][0],
                                   display.window_size_small[0] / 2 - images['inventory'][0].get_width() / 2,
                                   display.window_size_small[1] - images['inventory'][0].get_height(), 0, 0)

    def add_item(self, en_data):
        items_to_add = (en_data['yield'][0], random.randint(en_data['yield'][1][0], en_data['yield'][1][1]))
        for item in self.items:
            if item.item is None:
                item.set_item(items_to_add[0],items_to_add[1],images[f'{items_to_add[0]}-item'][0])
                break


    def init_pickup(self, en, chunk):
        if self.equiped not in entity_data[en.name]['gather_time']: return
        player.action = 'in_progress'
        self.action = 'pickup'
        self.en_data = entity_data[en.name]
        self.en = en
        self.en_chunk = chunk
        self.pickup_start = time.time()
        self.pickup_overlay = ActionOverlay(player, 'pickup', self.en_data['gather_time'][self.equiped])
        map_render.overlay.append(self.pickup_overlay)

    def iterate_pickup(self):
        if player.mouse.held and player.in_range_and_mouseover(self.en):
            delta_time = time.time() - self.pickup_start
            self.pickup_overlay.update(delta_time, player)
            # if mined for long enough
            if delta_time >= self.en_data['gather_time'][self.equiped]:
                # add to inv
                self.add_item(self.en_data)
                # remove it from the world map
                map_render.world_map[self.en_chunk].remove(self.en)
                # replace it with water if is tile type
                if self.en.type == 'tile':
                    x = self.en.rect.x // map_render.tile_size
                    y = self.en.rect.y // map_render.tile_size
                    map_render.world_map[self.en_chunk].append(map_render.entity_from_data('water', x, y))
                self.reset_pickup()
        else:
            self.reset_pickup()

    def reset_pickup(self):
        try:
            map_render.overlay.remove(self.pickup_overlay)
        except:
            pass
        self.en = None
        self.pickup_overlay = None
        self.action = None
        self.pickup_start = None
        player.action = None

    def update(self):
        #print(display.window_size_small)
        self.set_inv_en()

        if self.action == 'pickup':
            self.iterate_pickup()

        if input.key_clicked['tab']:
            self.toggle_inventory()

    def toggle_inventory(self):
        #print('from aplyer',display.window_size, display.window_size_small)
        if self.state == 'inventory':
            self.state = 'hotbar'
            player.click_action = 'gather'
        else:
            self.state = 'inventory'
            player.click_action = 'inventory'

    def draw(self):
        # draw the ui of the hotbar and inventory
        if self.state == 'hotbar':
            self.hotbar_en.draw(display.display,False)
        else:
            self.inventory_en.draw(display.display,False)
        # draw the items in the inventory
        for item in self.items:
            if item.row > 1 and self.state == 'hotbar': break
            if item.item != None:
                item.draw()


class Player(Entity):
    def __init__(self, x, y, image):
        self.rect_x_offset = 2
        self.rect_y_offset = 6
        self.init_entity('player', image, x, y, self.rect_x_offset, self.rect_y_offset, 10, 10)
        self.height = 10
        self.center_x = self.rect.x + self.rect.w // 2
        self.center_y = self.rect.y + self.rect.h // 2
        self.movement = [0, 0]

        self.max_stamina = 50
        self.stamina = self.max_stamina
        self.stamina_drain = .5
        self.stamina_regen = .05

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

    def update(self, mouse):
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

    def update_highlight(self):
        chunk_xx = int(self.mouse.x // (map_render.tile_size * map_render.chunk_size))
        chunk_yy = int(self.mouse.y // (map_render.tile_size * map_render.chunk_size))
        dx = [-1, 0, 1]
        dy = [-1, 0, 1]
        if self.click_action == 'gather':
            for chunk_x in dx:
                for chunk_y in dy:
                    chunk = str(chunk_x + chunk_xx) + ';' + str(chunk_y + chunk_yy)
                    if chunk in map_render.world_map:
                        for en in map_render.world_map[chunk]:
                            if en.pickupable and self.in_range_and_mouseover(en):
                                pygame.draw.rect(display.display, (255, 0, 0),
                                                 (en.rect.x - camera.x, en.rect.y - camera.y, en.rect.w, en.rect.h), 1)
                                if self.mouse.held and self.inventory.en != en:
                                    self.inventory.reset_pickup()
                                    self.inventory.init_pickup(en, chunk)
                                return

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
        hit_list = self.collission_test(self.rect, collideables)
        if hit_list != [] and not self.fly:
            self.speed = 0

    def move_on_land(self):
        for chunk, content in map_render.world_map.items():
            for tile in content:
                self.rect.x = tile.rect.x
                self.rect.y = tile.rect.y
                if self.collission_test(self.rect, map_render.collideables) == []:
                    # if tile.is_barrier == False:
                    self.rect.x = tile.rect.x
                    self.rect.y = tile.rect.y
                    return

    def in_range_and_mouseover(self, en):
        return en.rect.collidepoint(self.mouse.x, self.mouse.y) and math.dist((en.center_x, en.center_y), (
            self.center_x, self.center_y)) <= self.pickup_range

    def get_movement(self):
        self.movement = [0, 0]
        for key, value in input.key_held.items():
            # IF KEYS HELD
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
                    if self.movement[0] != 0 or self.movement[1] != 0:
                        self.stamina = clamp(self.stamina-self.stamina_drain,0,self.max_stamina)
                    if self.stamina > 0:
                        self.speed = self.base_speed * 2
                    else:
                        self.speed = self.base_speed
            else:
                # IF KEYS NOT HELD
                if key == 'shift':
                    self.stamina = clamp(self.stamina + self.stamina_regen, 0, self.max_stamina)
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

    def ui_draw(self):
        self.inventory.draw()
        self.draw_stamina()

    def draw_stamina(self):
        display.display.blit(images['stamina-border'][0],(2,2))
        display.display.blit(pygame.transform.scale(images['stamina-bar'][0],(int(self.stamina),4)),(4,4))

    def draw(self, surface):
        # self.draw_rect(surface)
        img = pygame.transform.flip(self.image, not self.last_facing_direction, 0)
        surface.blit(img,
                     (
                         self.rect.x - self.rect_x_offset - camera.x,
                         self.rect.y - self.rect_y_offset - self.z - camera.y))


player = Player(0, 0, images['player'][0])
