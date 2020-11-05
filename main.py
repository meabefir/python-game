import pygame, sys, random, os, noise, math
from helper import *
from input import *
from player import *
from lightSource import *
from camera import *
from entity import *
from debug import *
from mapRender import *
from loader import *

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

###############################################################################
colors = {'aqua': (198, 252, 255)}

heights = {'tile': 10, 'entity': 20}

load_images('images/tiles', 'images/entities', 'images/player')

input = Input()
player = Player(0, 0, images['player'][0])
camera = Camera(0, 0)
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
    #entities_by_height = {}

    entities = render_chunks(window_size_small,camera,display)

    for en in sorted(entities, key=lambda en: heights[en.type]):
        en.draw(display, camera.offset)
        if en.type != 'tile':
            en.draw_rect(display, camera)

    ################## DRAW PLAYER
    player.draw(display, camera)

    ############################################## SHADOW
    shadow = pygame.Surface(window_size_small)
    shadow.set_colorkey((255, 255, 255))
    shadow.fill((0, 0, 0))

    for light in light_sources:
        light.flicker()
        light.draw(shadow, camera)
    # DRAW SHADOW OVER EVERYTHING ELSE
    # display.blit(shadow, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  ########### CLICK
            if event.button == 1:
                chunk_x = int(mx // (tile_size * chunk_size))
                chunk_y = int(my // (tile_size * chunk_size))
                player.simulate_click(mx, my, chunk_x, chunk_y, world_map)
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
                print(seed, offset)
        if event.type == pygame.KEYUP:
            input.update_released(event)

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
