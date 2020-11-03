import pygame, sys, random, os, noise, math
from helper import *
from input import *
from player import *

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

def load_images():
    for f, sf, files in os.walk('images/tiles'):
        for file in files:
            name = file.split('_')[0]
            file_path = f + '\\' + file
            img = pygame.image.load(file_path)
            if name in images:
                images[name].append(img)
            else:
                images[name] = [img]


class LightSource():
    def __init__(self, pos, target=None):
        if target is None:
            self.x = pos[0]
            self.y = pos[1]
        else:
            self.x = target.x + target.w // 2
            self.y = target.y + target.h // 2
        self.target = target
        self.radius = 50
        self.max_radius = self.radius * 1.2
        self.min_radius = self.radius * 0.8

    def flicker(self):
        self.radius += random.randint(0, 2) - 1
        self.radius = clamp(self.radius, self.min_radius, self.max_radius)

    def draw(self, surface):
        if self.target is not None:
            self.x += (self.target.x + self.target.w // 2 - self.x) / 2
            self.y += (self.target.y + self.target.h // 2 - self.y) / 2
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x - scroll[0]), int(self.y - scroll[1])),
                               int(light.radius))
        else:
            pygame.draw.circle(surface, (255, 255, 255), (int(light.x - scroll[0]), int(light.y - scroll[1])),
                               int(light.radius))

def get_perlin_height(x,y):
    height = abs(
        noise.pnoise2(x / scale, y / scale, octaves=octaves, persistence=persistence, lacunarity=lacunarity))
    height = (int(height * 1000) / 10) * 2
    return height

def create_tile_at(x, y):
    height = get_perlin_height(x+seed,y+seed)
    height2 = get_perlin_height(x+seed2,y+seed2)

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


world_map = {}
alpha = 0

colors = {'aqua': (198, 252, 255)}

images = {}
load_images()

########################## RANDOM GENERATION
seed = random.randint(0,9999999)
seed2 = random.randint(0,9999999)
scale = 50
octaves = 50  # 1
persistence = .5  # .5
lacunarity = 2  # 2
repeat = 999999999
tile_size = 16
chunk_size = 8
# generate some random tiles
tiles = []

light_sources = []
# scroll = [-window_size[0]//(2*ratio),-window_size[1]//(2*ratio)]
scroll = [0, 0]
true_scroll = [0, 0]
scroll_ammount = 5
keys = {'w': False, 's': False, 'a': False, 'd': False}

################ PLAYER
# player_img = pygame.image.load('images/player/player.png')
# player_rect = pygame.Rect(0, 0, player_img.get_width(), player_img.get_height())
# player_speed = 3
# movement = [0, 0]
# last_facing_direction = 0

############################################################ GAME LOOP

input = Input()
player = Player(0,0)
light_sources.append(LightSource((0, 0), player.rect))

while True:
    display.fill(colors['aqua'])

    player.update(input.key_held)


    true_scroll[0] += (player.rect.x - true_scroll[0] - window_size_small[0] / 2 + player.rect.w // 2)  # /10
    true_scroll[1] += (player.rect.y - true_scroll[1] - window_size_small[1] / 2 + player.rect.h // 2)  # /10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # dinamically display tiles
    tiles = []
    for y in range(window_size_small[1] // (tile_size * chunk_size) + 3):
        for x in range(window_size_small[0] // (tile_size * chunk_size) + 3):
            chunk_x = x - 1 + int(round(scroll[0] / (chunk_size * tile_size)))
            chunk_y = y - 1 + int(round(scroll[1] / (chunk_size * tile_size)))
            chunk = str(chunk_x) + ';' + str(chunk_y)
            if chunk not in world_map:
                world_map[chunk] = generate_chunk(chunk_x, chunk_y)
            for tile in world_map[chunk]:
                tiles.append(tile)

    # draw the tiles
    for tile in tiles:
        display.blit(tile[1], (int(tile[0][0] * tile_size - scroll[0]), int(tile[0][1] * tile_size - scroll[1])))

    m_pos = pygame.mouse.get_pos()
    mx, my = (m_pos[0] / ratio + scroll[0]), (m_pos[1] / ratio + scroll[1])

    # SHADOW
    over = pygame.Surface(window_size_small)
    over.set_colorkey((255, 255, 255))
    over.fill((0, 0, 0))

    for light in light_sources:
        light.flicker()
        light.draw(over)

    ################## DRAW PLAYER
    player.draw(display,scroll)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            ### create light source
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # light_sources.append(LightSource((mx,my)))
                player.rect.x = mx
                player.rect.y = my
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
            # if chr(event.key) in 'wasd':
            #     keys[chr(event.key)] = True
            ## ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            ## INFO
            if event.key == pygame.K_i:
                print(seed,offset)
        if event.type == pygame.KEYUP:
            input.update_released(event)
            # if chr(event.key) in 'wasd':
            #     keys[chr(event.key)] = False

    # DRAW SHADOW OVER EVERYTHING ELSE
    #display.blit(over, (0, 0))

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
