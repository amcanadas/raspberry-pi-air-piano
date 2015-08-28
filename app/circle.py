# -*- coding: utf-8 -*-
import pygame
from util import *

class Circle(pygame.sprite.Sprite):
    """
    A circle sprite class for defining piano rect.
    """
    def __init__(self,x,y,name):
        """
        Input:
        :x: :y: position values for "dot"
        :name: name of the corner
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.is_pressed = False
        self.x = x
        self.y = y
        self.size = 25
        self.half_size = self.size / 2
        self.image = pygame.Surface((self.size,self.size)).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect().move(x-self.half_size,y-self.half_size)
        self.unpressed()

    def pressed(self):
        self.is_pressed=True
        self._draw(RED)

    def unpressed(self):
        self.is_pressed=False
        self._draw(BLUE)

    def _draw(self, color):
        pygame.draw.ellipse(self.image, color, self.image.get_rect(), 4)
        pygame.draw.line(self.image, WHITE, (0,self.half_size),(self.size,self.half_size))
        pygame.draw.line(self.image, WHITE, (self.half_size,0),(self.half_size,self.size))
