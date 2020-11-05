import pygame

class Debug():
    def draw_chunks(self,surface,x,y,tile_size,chunk_size,camera):
        x_start = x*tile_size*chunk_size-camera.x
        y_start = y*tile_size*chunk_size-camera.y
        x_end = (x+1) * tile_size * chunk_size-camera.x
        y_end = (y+1) * tile_size * chunk_size-camera.y
        pygame.draw.line(surface,(255,0,0),(x_start,y_start),(x_start,y_end),1)
        pygame.draw.line(surface,(255,0,0),(x_start,y_start),(x_end,y_start),1)

debug = Debug()