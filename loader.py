import pygame,os,sys

# def resource_path(relative_path):
#     if hasattr(sys, '_MEIPASS'):
#         return os.path.join(sys._MEIPASS, relative_path)
#    return os.path.join(os.path.abspath("."), relative_path)

def load_animations(path):
    for f, sf, files in os.walk(path):
        for file in files:
            animation_name = file.split('_')[0]
            file_path = path + '\\' + file
            if animation_name in animations:
                animations[animation_name].append(pygame.image.load(file_path))
            else:
                animations[animation_name] = [pygame.image.load(file_path)]

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

animations = {}
images = {}
load_images('images/tiles', 'images/entities', 'images/player','images/overlay','images/items','images/digits')
load_animations('animations')