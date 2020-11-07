import pygame, random, noise
from debug import *
from loader import *
from entity import *
from camera import *
from data import *
from particleSystem import *

class MapRender():
    def __init__(self):
        self.entities = []
        self.collideables = []
        self.overlay = []
        self.tiles = []
        self.world_map = {}
        self.underworld_map = {}

        self.seed = random.randint(0, 9999999)
        self.seed2 = random.randint(0, 9999999)
        self.scale = 50
        self.octaves = 50  # 1
        self.persistence = .5  # .5
        self.lacunarity = 2  # 2
        self.repeat = 999999999

        self.tile_size = 16
        self.chunk_size = 8
        #self.tile_height = {'water':0,'sand':10,'grass':20,'dirt':30,'stone':40,'coal':50,'iron':60}

    def get_perlin_height(self, x, y):
        height = abs(
            noise.pnoise2(x / self.scale, y / self.scale, octaves=self.octaves, persistence=self.persistence,
                          lacunarity=self.lacunarity))
        height = (int(height * 1000) / 10) * 2
        return height

    def entity_from_data(self, name, x, y):
        data = entity_data[name]
        size = data['size']
        rect_size = data['rect_size']
        rect_offset = data['rect_offset']
        world_offset = data['world_offset']
        new_el = Entity(name, random.choice(images[name]),
                      x * self.tile_size + world_offset[0],
                      y * self.tile_size + world_offset[1],
                        rect_offset[0],rect_offset[1], rect_size[0],rect_size[1])
        new_el.set_barrier(data['is_barrier'])
        new_el.set_pickupable(data['is_pickupable'])
        new_el.set_height(data['height'])
        new_el.set_type(data['type'])
        return new_el

    def create_tile_at(self, x, y):
        height = self.get_perlin_height(x + self.seed, y + self.seed)
        height2 = self.get_perlin_height(x + self.seed2, y + self.seed2)
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        elements = []
        # print(height)
        if height > 60:
            img = 'stone'
            # if height2 > 55:
            #     img = 'iron'
            # elif 50 > height2 > 40:
            #     img = 'coal'
        elif 48 < height <= 66:
            img = 'dirt'
        elif 22 < height <= 48:
            img = 'grass'
            if random.randint(1, 15) == 1:
                elements.append(self.entity_from_data('tree', x, y))
            elif random.randint(1, 25) == 1:
                elements.append(self.entity_from_data('branch', x, y))
        elif 15 <= height <= 22:
            img = 'sand'
        else:
            img = 'water'

        elements.append(self.entity_from_data(img,x,y))
        return elements

    def generate_chunk(self, x, y):
        chunk_elements = []
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size + x_pos
                target_y = y * self.chunk_size + y_pos
                elements = self.create_tile_at(target_x, target_y)
                if elements != []:
                    chunk_elements += elements
        return chunk_elements

    def render_chunks(self, window_size_small, display):
        self.entities = []
        self.collideables = []
        self.tiles = []
        for y in range(window_size_small[1] // (self.tile_size * self.chunk_size) + 3):
            for x in range(window_size_small[0] // (self.tile_size * self.chunk_size) + 3):
                chunk_x = x - 1 + int(round(camera.x / (self.chunk_size * self.tile_size)))
                chunk_y = y - 1 + int(round(camera.y / (self.chunk_size * self.tile_size)))
                ### DEBUG
                if debug.active:
                    debug.draw_chunks(display, chunk_x, chunk_y, self.tile_size, self.chunk_size, camera)
                chunk = str(chunk_x) + ';' + str(chunk_y)
                if chunk not in self.world_map:
                    self.world_map[chunk] = self.generate_chunk(chunk_x, chunk_y)
                for en in self.world_map[chunk]:
                    if en.type == 'entity':
                        self.entities.append(en)
                    elif en.type == 'tile':
                        self.tiles.append(en)
        for en in self.entities + self.tiles:
            if en.is_barrier:
                self.collideables.append(en)
        return self.entities

    def draw_tiles(self, surface):
        for tile in sorted(self.tiles,key=lambda tile:tile.height):
            tile.draw(surface)
            # water particles
            if tile.name == 'water':
                if random.randint(1,5000) == 1:
                    particle_system.add_particle(tile.rect.x+random.randint(0,self.tile_size),tile.rect.y+random.randint(0,self.tile_size))
            if debug.active:
                tile.draw_rect(display.display)

    def draw_entities(self, surface):
        for en in sorted(self.entities, key=lambda en: en.height + en.rect.y):
            en.draw(surface)
            if debug.active:
                en.draw_rect(display.display)

    def draw_overlay(self,surface):
        for ol in self.overlay:
            ol.draw(surface)

map_render = MapRender()
