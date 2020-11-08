import pygame,os

def load_images(*args):
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

images = {}
load_images('images/tiles', 'images/entities', 'images/player','images/overlay','images/pickups','images/digits')