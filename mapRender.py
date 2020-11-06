import pygame, random, noise
from debug import *
from loader import *
from entity import *
from camera import *
from data import *


class MapRender():
    def __init__(self):
        self.entities = []
        self.collideables = []
        self.tiles = []
        self.world_map = {}

        self.seed = random.randint(0, 9999999)
        self.seed2 = random.randint(0, 9999999)
        self.scale = 50
        self.octaves = 50  # 1
        self.persistence = .5  # .5
        self.lacunarity = 2  # 2
        self.repeat = 999999999

        self.tile_size = 16
        self.chunk_size = 8

    def get_perlin_height(self, x, y):
        height = abs(
            noise.pnoise2(x / self.scale, y / self.scale, octaves=self.octaves, persistence=self.persistence,
                          lacunarity=self.lacunarity))
        height = (int(height * 1000) / 10) * 2
        return height

    def entity_from_data(self,name,x,y):
        data = entity_data[name]
        size = data['size']
        rect_size = data['rect_size']
        rect_offset = data['rect_offset']
        world_offset = data['world_offset']
        return Entity(random.choice(images[name]), x * self.tile_size + rect_offset[0]-self.tile_size*world_offset[0],
                                y * self.tile_size + rect_offset[1]-self.tile_size*world_offset[1], rect_offset[0], rect_offset[1], rect_size[0],
                                rect_size[1])

    def create_tile_at(self, x, y):
        height = self.get_perlin_height(x + self.seed, y + self.seed)
        height2 = self.get_perlin_height(x + self.seed2, y + self.seed2)
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        elements = []
        # print(height)
        if height > 55:
            img = 'stone'
            if height2 > 55:
                img = 'iron'
            elif 50 > height2 > 40:
                img = 'coal'
        elif 45 < height <= 58:
            img = 'dirt'
        elif 20 < height <= 45:
            img = 'grass'
            if random.randint(1, 50) == 1:
                new_el = self.entity_from_data('tree',x,y)
                new_el.set_barrier()
                new_el.set_type('entity')
                elements.append(new_el)
            elif random.randint(1,25) == 1:
                new_el = self.entity_from_data('branch', x, y)
                new_el.set_pickupable()
                new_el.set_type('entity')
                elements.append(new_el)
        elif 15 <= height <= 20:
            img = 'sand'
        else:
            img = 'barrier'

        type = random.choice(images[img])
        new_el = Entity(type, x * self.tile_size, y * self.tile_size, 0, 0)
        new_el.set_type('tile')
        if img == 'barrier':
            new_el.set_barrier()
        elements.append(new_el)
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
                #debug.draw_chunks(display, chunk_x, chunk_y, self.tile_size, self.chunk_size, camera)
                chunk = str(chunk_x) + ';' + str(chunk_y)
                if chunk not in self.world_map:
                    self.world_map[chunk] = self.generate_chunk(chunk_x, chunk_y)
                for en in self.world_map[chunk]:
                    if en.type == 'entity':
                        self.entities.append(en)
                    elif en.type == 'tile':
                        self.tiles.append(en)
        for en in self.entities+self.tiles:
            if en.is_barrier:
                self.collideables.append(en)
        return self.entities

    def draw_tiles(self,surface):
        for tile in self.tiles:
            tile.draw(surface)

    def draw_entities(self,surface):
        for en in sorted(self.entities, key=lambda en: en.rect.y):
            en.draw(display.display)
            # if en.type != 'tile':
            #    en.draw_rect(display.display)

map_render = MapRender()
