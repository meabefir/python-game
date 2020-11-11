import pygame, sys
from display import *
from player import *
from input import *
from mouse import *
from debug import *


class EventHandler():
    def update(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  ########### CLICK
            if event.button == 1:
                mouse.set_clicked()
                mouse.set_held()
            ############################## ZOOM
            elif event.button == 5:
                if player.inventory.state == 'inventory':
                    player.inventory.scroll_crafting_tiles(player.inventory.crafting_scroll_ammount)
                else:
                    if player.fly:
                        display.set_display(display.set_ratio(display.ratio - .2))
            elif event.button == 4:
                if player.inventory.state == 'inventory':
                    player.inventory.scroll_crafting_tiles(-player.inventory.crafting_scroll_ammount)
                else:
                    if player.fly:
                        display.set_display(display.set_ratio(display.ratio + .2))
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse.set_up()
            ################################ KEY PRESSED
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            input.update_held(event)
            ## ESCAPE
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_g:
                player.set_godmode()
            elif event.key == pygame.K_f:
                display.toggle_fullscreen()
        if event.type == pygame.KEYUP:
            input.update_released(event)


event_handler = EventHandler()
