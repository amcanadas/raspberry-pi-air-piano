# -*- coding: utf-8 -*-

import json
import os, inspect, sys
import pygame
import cv2,numpy

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

scale = ['low_c',
         'c_sharp',
         'd',
         'd_sharp',
         'e',
         'f',
         'f_sharp',
         'g',
         'g_sharp',
         'a',
         'a_sharp',
         'b',
         'high_c']

config = None

def get_app_path():
    local_file = inspect.getfile(sys.modules[__name__])
    return os.path.dirname(local_file)

def read_config():
    global config
    with open(get_app_path()+'/config/config.json') as json_data_file:
        config = json.load(json_data_file)

def load_image(name):
    """
    Loads image into pygame and converts into a faster to render object
    """
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    return image, image.get_rect()

def pygame_camera_draw(cam):
    rect, camera_image= cam.get_pygame_image()
    screen=pygame.display.get_surface()
    screen.blit(camera_image, rect)
