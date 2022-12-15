

import pygame
import numpy as np
from entity import Entity
from text import Text

class Test_queue(Entity):
    queue = None
    title = None
    number = 0
    def __init__(self, title = Text('Default Title'), number = 3, position = [100, 120], size = (100, 200), speed = [0,0]):
        self.speed = np.array(speed)
        self.queue = []
        self.title = title
        self.number = number
        self.rect = pygame.Rect((position[0]-size[0]/2, position[1]-size[1]/2), size)
        self.refresh()


    def push(self, text):
        self.queue.append(text)
        self.refresh()

    def refresh(self):
        self.surface = pygame.Surface(self.rect.size)
        to_top = 20
        self.title.rect.center = self.rect.size[0]/2, to_top
        self << self.title
        for text in self.queue[-1:-self.number-1:-1]:
            to_top += self.rect.size[1] / (self.number+1)
            text.rect.center = self.rect.size[0]/2, to_top
            self << text



