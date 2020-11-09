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
from mouse import *


class Tile():
    def __init__(self, x, y, name, count):
        self.count = count
        self.en = Entity(name, images[f'{name}-item'][0], x, y, 0, 0)

    def draw(self):
        self.en.draw(display.display, False)
        text.draw_number(self.count, self.en.rect.x, self.en.rect.y)


class CraftingTile():
    def __init__(self, name, x, y):
        self.name = name
        self.en = Entity(name, images['crafting-window'][0], x, y, 0, 0)
        self.tiles = []
        self.tiles.append(Tile(self.en.rect.x + 2, self.en.rect.y + 2, name, 1))
        for i in range(len(crafting[name])):
            # name = crafting[name][i][0]
            # count = crafting[name][i][1]
            name2, count = crafting[name][i]
            self.tiles.append(Tile(self.en.rect.x + 19 + i * 16, self.en.rect.y + 2, name2, count))

    def scroll(self, ammount):
        for tile in self.tiles:
            tile.en.rect.y += ammount
        self.en.rect.y += ammount

    def draw(self):
        self.en.draw(display.display, False)
        for tile in self.tiles:
            tile.draw()


class InvTile():
    def __init__(self, inv, row, col):
        self.inventory = inv
        self.row = row
        self.col = col
        self.item = None
        self.img = images['none-img'][0]
        self.item_count = 0
        self.en = Entity(None, self.img, self.inventory.inventory_en.rect.x + 5 + (self.col - 1) * 16,
                         self.inventory.inventory_en.rect.y + 5 + (5 - self.row) * 16, 0, 0, 16, 16)

    def set_item(self, item, item_count, image):
        self.item = item
        self.item_count = item_count
        self.img = image
        self.en = Entity(item, image, self.inventory.inventory_en.rect.x + 5 + (self.col - 1) * 16,
                         self.inventory.inventory_en.rect.y + 5 + (5 - self.row) * 16, 0, 0, 16, 16)

    def update_item(self, item, item_count, image):
        self.item = item
        self.item_count = item_count
        self.img = image

    def increase_count(self, item_count):
        self.item_count += item_count

    def draw(self):
        self.en = Entity(self.item, self.img, self.inventory.inventory_en.rect.x + 5 + (self.col - 1) * 16,
                         self.inventory.inventory_en.rect.y + 5 + (5 - self.row) * 16, 0, 0, 16, 16)
        if self.item is not None:
            self.en.draw(display.display, False)

            text.draw_number(self.item_count, self.en.rect.x + 16 - 4 * len(str(self.item_count)), self.en.rect.y + 8)


class Inventory():
    def __init__(self):
        self.items_tiles = []
        self.items = {}
        self.crafting_tiles = []
        self.default_tool = 'god'
        self.equiped = self.default_tool
        self.equiped_tile = None
        self.pickup_start = None
        self.action = None
        self.en = None
        self.pickup_overlay = None
        self.state = 'hotbar'
        self.rows = 5
        self.cols = 10
        self.crafting_scroll_ammount = 8
        self.crafting_current_scroll = 0

        self.picked_inv_tile = None

        self.set_inv_en()
        for row in range(self.rows):
            for col in range(self.cols):
                self.items_tiles.append(InvTile(self, row + 1, col + 1))

    def set_inv_en(self):
        self.hotbar_en = Entity('hotbar', images['hotbar'][0],
                                display.window_size_small[0] / 2 - images['hotbar'][0].get_width() / 2,
                                display.window_size_small[1] - images['hotbar'][0].get_height(), 0, 0)
        self.inventory_en = Entity('inventory', images['inventory'][0],
                                   display.window_size_small[0] / 2 - images['inventory'][0].get_width() / 2,
                                   display.window_size_small[1] - images['inventory'][0].get_height(), 0, 0)

    def scroll_crafting_tiles(self, ammount):
        self.crafting_current_scroll += ammount
        for crafting_tile in self.crafting_tiles:
            crafting_tile.scroll(ammount)

    def add_item(self, item_to_add, item_count):
        item_image = images[f'{item_to_add}-item'][0]
        for item in self.items_tiles:
            # stacking items over other items
            if item.item == item_to_add:
                to_add_now = min(stack_size[item_to_add] - item.item_count, item_count)
                item.increase_count(to_add_now)
                item_count -= to_add_now
                try:
                    self.items[item_to_add] += to_add_now
                except:
                    self.items[item_to_add] = to_add_now
                finally:
                    self.create_crafting_tiles()
                if item_count == 0:
                    break
            # if were still left with items but no more stacking
        if item_count > 0:
            for item in self.items_tiles:
                if item.item is None:
                    to_add_now = min(stack_size[item_to_add], item_count)
                    item_count -= to_add_now
                    try:
                        self.items[item_to_add] += to_add_now
                    except:
                        self.items[item_to_add] = to_add_now
                    finally:
                        self.create_crafting_tiles()
                    item.set_item(item_to_add, to_add_now, item_image)
                    if item_count == 0:
                        break
        print(self.items)

    def add_item_from_data(self, en_data):
        for i in range(len(en_data['yield'])):
            # print(en_data['yield'][i])
            chance = en_data['yield'][i][2]
            if random.random() * 100 <= chance:
                item_to_add = en_data['yield'][i][0]
                item_count = random.randint(en_data['yield'][i][1][0], en_data['yield'][i][1][1])
                self.add_item(item_to_add, item_count)
                # if low change was hit, only yield items from that loot table
                break
        # print(self.items)

    def delete_item(self, item, count):
        for inv_tile in self.items_tiles:
            if count == 0:
                return
            if inv_tile.item == item:
                to_remove = min(inv_tile.item_count, count)
                inv_tile.item_count -= to_remove
                count -= to_remove
                self.items[item] -= to_remove
                if inv_tile.item_count == 0:
                    inv_tile.update_item(None, 0, images['none-img'][0])

    def craft(self, name):
        for item, count in crafting[name]:
            self.delete_item(item, count)
        self.add_item(name, 1)
        self.create_crafting_tiles()

    def create_crafting_tiles(self):
        self.crafting_tiles = []
        for item, recipe in crafting.items():
            for ingredient in recipe:
                name, count = ingredient
                if name not in self.items or self.items[name] < count:
                    break
            else:
                self.crafting_tiles.append(
                    CraftingTile(item, display.window_size_small[0] - 72,
                                 self.crafting_current_scroll + 2 + len(self.crafting_tiles) * 20))

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
                self.add_item_from_data(self.en_data)
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

    def mouse_over_inv_tile(self):
        for inv_tile in self.items_tiles:
            if inv_tile.en.rect.collidepoint((mouse.window_x, mouse.window_y)):
                if inv_tile.item is not None or self.picked_inv_tile is not None:
                    return inv_tile
        return None

    def set_equiped(self):
        for i in range(10):
            if input.key_clicked[str(i)]:
                if i > 0:
                    i -= 1
                else:
                    i = 9
                self.equiped = self.items_tiles[i].item if self.items_tiles[i].item is not None else self.default_tool
                self.equiped_tile = self.items_tiles[i] if self.items_tiles[i].item is not None else None
        if input.key_clicked['q']:
            self.equiped = self.default_tool
            self.equiped_tile = None

    def check_crafting(self):
        for crafting_tile in self.crafting_tiles:
            if crafting_tile.en.rect.collidepoint(mouse.window_x, mouse.window_y):
                self.craft(crafting_tile.name)
                break

    def update(self):
        self.set_inv_en()
        self.set_equiped()
        # print(self.equiped)

        if self.action == 'pickup':
            self.iterate_pickup()

        # toggle inventory
        if input.key_clicked['tab']:
            self.toggle_inventory()

        # craft items if inventory open
        if self.state == 'inventory' and mouse.clicked:
            self.check_crafting()

        # pick inventory tile
        if mouse.clicked and self.state == 'inventory':
            over = self.mouse_over_inv_tile()
            if over is not None:
                # print(over.row,over.col)
                if self.picked_inv_tile is None:
                    self.picked_inv_tile = over
                else:
                    self.change_inv_tiles(self.picked_inv_tile, over)

    def change_inv_tiles(self, tile1, tile2):
        if tile1 == self.equiped_tile or tile2 == self.equiped_tile:
            self.equiped_tile = None
            self.equiped = self.default_tool
        self.picked_inv_tile = None
        tile2_item, tile2_item_count, tile2_image = tile2.item, tile2.item_count, tile2.img

        tile2.update_item(tile1.item, tile1.item_count, tile1.img)
        tile1.update_item(tile2_item, tile2_item_count, tile2_image)

    def toggle_inventory(self):
        # print('from aplyer',display.window_size, display.window_size_small)
        if self.state == 'inventory':
            self.state = 'hotbar'
            player.click_action = 'gather'
            self.picked_inv_tile = None
            self.crafting_current_scroll = 0
        else:
            self.create_crafting_tiles()
            self.state = 'inventory'
            player.click_action = 'inventory'

    def draw(self):
        # draw the ui of the hotbar and inventory
        if self.state == 'hotbar':
            self.hotbar_en.draw(display.display, False)
        else:  # draw inventory and craftables
            self.inventory_en.draw(display.display, False)
            for crafting_tile in self.crafting_tiles:
                crafting_tile.draw()

        # draw the items in the inventory
        for item in self.items_tiles:
            if item.row > 1 and self.state == 'hotbar': break
            item.draw()
            if self.picked_inv_tile == item:  ######### highlight selected item
                pygame.draw.rect(display.display, colors['purple'],
                                 (item.en.rect.x, item.en.rect.y, 16, 16), 1)
        # draw highlight for held item
        if self.equiped_tile is not None:
            pygame.draw.rect(display.display, colors['purple'],
                             (self.equiped_tile.en.rect.x, self.equiped_tile.en.rect.y, 16, 16), 1)


class Player(Entity):
    def __init__(self, x, y, image):
        self.rect_x_offset = 2
        self.rect_y_offset = 10
        self.init_entity('player', image, x, y, self.rect_x_offset, self.rect_y_offset, 10, 4)
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
                                if self.inventory.equiped not in entity_data[en.name]['gather_time']: break
                                pygame.draw.rect(display.display, colors['purple'],
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
                        self.stamina = clamp(self.stamina - self.stamina_drain, 0, self.max_stamina)
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
        display.display.blit(images['stamina-border-background'][0], (2, 2))
        display.display.blit(pygame.transform.scale(images['stamina-bar'][0], (int(self.stamina), 4)), (4, 4))
        display.display.blit(images['stamina-border'][0], (2, 2))

    def draw(self, surface):
        # self.draw_rect(surface)
        img = pygame.transform.flip(self.image, not self.last_facing_direction, 0)
        surface.blit(img,
                     (
                         self.rect.x - self.rect_x_offset - camera.x,
                         self.rect.y - self.rect_y_offset - self.z - camera.y))


player = Player(0, 0, images['player'][0])
