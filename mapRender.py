import pygame,random,noise
from debug import *
from loader import *
from entity import *

entities = []
world_map = {}

seed = random.randint(0, 9999999)
seed2 = random.randint(0, 9999999)
scale = 50
octaves = 50  # 1
persistence = .5  # .5
lacunarity = 2  # 2
repeat = 999999999

tile_size = 16
chunk_size = 8

def get_perlin_height(x, y):
    height = abs(
        noise.pnoise2(x / scale, y / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity))
    height = (int(height * 1000) / 10) * 2
    return height

def create_tile_at(x, y):
    height = get_perlin_height(x + seed, y + seed)
    height2 = get_perlin_height(x + seed2, y + seed2)
    chunk_x = x // chunk_size
    chunk_y = y // chunk_size
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
            new_el = Entity(images['branch'][0], x * tile_size,
                            y * tile_size, 0, 0)
            new_el.set_pickupable()
            new_el.set_type('entity')
            elements.append(new_el)
            # entities.append(new_en)
    elif 15 <= height <= 20:
        img = 'sand'
    else:
        img = ''

    if img != '':
        type = random.choice(images[img])
        new_el = Entity(type, x * tile_size, y * tile_size, 0, 0)
        new_el.set_type('tile')
        elements.append(new_el)
    return elements


def generate_chunk(x, y):
    chunk_elements = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            elements = create_tile_at(target_x, target_y)
            if elements != []:
                chunk_elements += elements
    return chunk_elements

def render_chunks(window_size_small,camera,display):
    entities = []
    for y in range(window_size_small[1] // (tile_size * chunk_size) + 3):
        for x in range(window_size_small[0] // (tile_size * chunk_size) + 3):
            chunk_x = x - 1 + int(round(camera.x / (chunk_size * tile_size)))
            chunk_y = y - 1 + int(round(camera.y / (chunk_size * tile_size)))
            debug.draw_chunks(display, chunk_x, chunk_y, tile_size, chunk_size, camera)
            chunk = str(chunk_x) + ';' + str(chunk_y)
            if chunk not in world_map:
                world_map[chunk] = generate_chunk(chunk_x, chunk_y)
            for en in world_map[chunk]:
                entities.append(en)
    return entities
                # create height map
                # type = en.type
                # if heights[type] not in entities_by_height:
                #     entities_by_height[heights[type]] = [en]
                # else:
                #     entities_by_height[heights[type]].append(en)