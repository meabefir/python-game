import pygame, sys, random, os, noise, math
from helper import *
from display import *
from eventHandler import *
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
from particleSystem import *

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
    #display.display.fill(colors['aqua'])

    ################################### MOUSE INPUT
    mouse.update()

    player.update(mouse)
    camera.update()

    ################################### RENDER MAP

    map_render.draw_tiles(display.display)
    map_render.entities.append(player)
    map_render.draw_entities(display.display)
    map_render.draw_overlay(display.display)

    player.update_highlight()

    map_render.render_chunks(display.window_size_small, display.display)

    particle_system.update()

    ################################### GAME TIME
    game_time.update()

    player.ui_draw()

    input.update()
    for event in pygame.event.get():
        event_handler.update(event)


    display.screen.blit(pygame.transform.scale(display.display, display.window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)
