import pygame, sys, random, os, noise, math
from helper import *
from display import *
from input import *
from player import *
from lightSource import *
from camera import *
from entity import *
from debug import *
from mapRender import *
from loader import *
from gameTime import *
from mouse import *

clock = pygame.time.Clock()
pygame.init()

###############################################################################
colors = {'aqua': (198, 252, 255)}

heights = {'tile': 10, 'entity': 20}

map_render.render_chunks(display.window_size_small, display.display)
player.move_on_land()
camera.set_target(player)


light_sources.append(LightSource((0, 0), player.rect))
############################################################ GAME LOOP
while True:
    display.display.fill(colors['aqua'])

    ################################### MOUSE INPUT
    mouse.update()

    player.update()
    camera.update()

    ################################### RENDER MAP

    map_render.draw_tiles(display.display)
    map_render.entities.append(player)
    map_render.draw_entities(display.display)


    map_render.render_chunks(display.window_size_small, display.display)

    ################################### GAME TIME
    game_time.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  ########### CLICK
            if event.button == 1:
                player.simulate_click()
            ############################## ZOOM
            elif event.button == 5:
                display.set_display(display.set_ratio(display.ratio-.2))
            elif event.button == 4:
                display.set_display(display.set_ratio(display.ratio+.2))
            ################################ MOVEMENT INPUT
        if event.type == pygame.KEYDOWN:
            input.update_held(event)
            ## ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYUP:
            input.update_released(event)

    display.screen.blit(pygame.transform.scale(display.display, display.window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
