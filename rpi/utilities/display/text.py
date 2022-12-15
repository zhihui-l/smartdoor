

import pygame
import numpy as np
from entity import Entity

class Text(Entity):
    text = ''
    color = 255,255,255
    size = 25
    position = [0,0]
    def __init__(self, text = 'default', color = (255,255,255), position = [0,0], size = 25, speed = [0,0]):
        self.speed = np.array(speed)
        self.text = text
        self.color = color
        self.size = size
        self.position = position
        self.refresh()


    def refresh(self):
        self.surface = pygame.font.SysFont('Corbel',self.size, True).render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.rect.center = self.position
