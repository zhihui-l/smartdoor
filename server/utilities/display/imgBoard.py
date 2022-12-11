

import pygame
import numpy as np
from entity import Entity

class ImgBoard(Entity):
    img = None
    position = [0,0]
    size = 25
    def __init__(self, position = [0,0], size = 25, speed = [0,0], enable = True):
        self.speed = np.array(speed)
        self.size = size
        self.position = position
        self.enable = enable


    def refresh(self, img):
        if self.enable:
            self.img = img
            self.surface = pygame.transform.scale(self.img, (self.size*2,self.size*2))
            self.rect = self.surface.get_rect()
            self.rect.center = self.position
