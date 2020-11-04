import pygame, sys, random, os, noise, math
from helper import *
from input import *
from player import *
from lightSource import *
from camera import *
from entity import *

clock = pygame.time.Clock()
pygame.init()
window_size = (900, 600)
ratio = 2
screen = pygame.display.set_mode(window_size)

def set_display(ratio):
    window_size_small = (int(window_size[0] // ratio), int(window_size[1] // ratio))
    display = pygame.Surface(window_size_small)
    return display, window_size_small

display, window_size_small = set_display(ratio)

def load_images(*args):
    print("LOADING IMAGES")
    for path in args:
        for f, sf, files in os.walk(path):
            for file in files:
                name = file.split('_')[0].split('.')[0]
                file_path = f + '\\' + file
                img = pygame.image.load(file_path)
                if name in images:
                    images[name].append(img)
                else:
                    images[name] = [img]

################################### WORLD GEN ##############################
def get_perlin_height(x,y):
    height = abs(
        noise.pnoise2(x / scale, y / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity))
    height = (int(height * 1000) / 10) * 2
    return height

def create_tile_at(x, y):
    height = get_perlin_height(x+seed,y+seed)
    height2 = get_perlin_height(x+seed2,y+seed2)
    chunk_x = x//chunk_size
    chunk_y = y//chunk_size

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
        if random.randint(1,50) == 1:
            new_en = Entity(images['branch'][0],x*tile_size+random.randint(0,tile_size),y*tile_size+random.randint(0,tile_size),0,0)
            new_en.set_pickupable()
            chunk = str(chunk_x)+';'+str(chunk_y)
            #world_map[chunk].append
            entities.append(new_en)
    elif 15 <= height <= 20:
        img = 'sand'
    else:
        img = ''

    if img != '':
        type = random.choice(images[img])
        return ((x, y), type)
    else:
        return None


def generate_chunk(x, y):
    chunk_tiles = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile = create_tile_at(target_x, target_y)
            if tile is not None:
                chunk_tiles.append(tile)
    return chunk_tiles

###############################################################################
colors = {'aqua': (198, 252, 255)}

images = {}
load_images('images/tiles','images/entities','images/player')
print(images)

########################## RANDOM GENERATION
seed = random.randint(0,9999999)
seed2 = random.randint(0,9999999)
scale = 50
octaves = 50  # 1
persistence = .5  # .5
lacunarity = 2  # 2
repeat = 999999999
tile_size = 16
chunk_size = 50
# generate some random tiles


light_sources = []
tiles = []
entities = []
world_map = {}


input = Input()
player = Player(0,0,images['player'][0])
camera = Camera(0,0)
camera.set_target(player)
light_sources.append(LightSource((0, 0), player.rect))

############################################################ GAME LOOP
while True:
    display.fill(colors['aqua'])

    ################################### MOUSE INPUT
    m_pos = pygame.mouse.get_pos()
    mx, my = (m_pos[0] / ratio + camera.x), (m_pos[1] / ratio + camera.y)

    player.update(input.key_held)
    camera.update(window_size_small)

    # dinamically display tiles
    tiles = []
    for y in range(window_size_small[1] // (tile_size * chunk_size) + 3):
        for x in range(window_size_small[0] // (tile_size * chunk_size) + 3):
            chunk_x = x - 1 + int(round(camera.x / (chunk_size * tile_size)))
            chunk_y = y - 1 + int(round(camera.y / (chunk_size * tile_size)))
            chunk = str(chunk_x) + ';' + str(chunk_y)
            if chunk not in world_map:
                world_map[chunk] = generate_chunk(chunk_x, chunk_y)
            for tile in world_map[chunk]:
                tiles.append(tile)

    # draw the tiles
    for tile in tiles:
        display.blit(tile[1], (int(tile[0][0] * tile_size - camera.x), int(tile[0][1] * tile_size - camera.y)))

    for en in entities:
        en.draw(display,camera.offset)
        en.draw_rect(display,camera.offset)

    ################## DRAW PLAYER
    player.draw(display,camera.offset)

    ############################################## SHADOW
    shadow = pygame.Surface(window_size_small)
    shadow.set_colorkey((255, 255, 255))
    shadow.fill((0, 0, 0))

    for light in light_sources:
        light.flicker()
        light.draw(shadow,camera)
    # DRAW SHADOW OVER EVERYTHING ELSE
    #display.blit(shadow, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: ########### CLICK
            if event.button == 1:
                player.simulate_click(mx,my,entities)
            ############################## ZOOM
            elif event.button == 5:
                ratio -= .2
                ratio = clamp(ratio, .1, 5)
                display, window_size_small = set_display(ratio)
            elif event.button == 4:
                ratio += .2
                ratio = clamp(ratio, .1, 5)
                display, window_size_small = set_display(ratio)
            ################################ MOVEMENT INPUT
        if event.type == pygame.KEYDOWN:
            input.update_held(event)
            ## ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            ## INFO
            if event.key == pygame.K_i:
                print(seed,offset)
        if event.type == pygame.KEYUP:
            input.update_released(event)

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
