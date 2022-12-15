import pygame
import numpy as np
from entity import Entity

class Ball(Entity):
    radius = 50
    def __init__(self, speed = [2,2], radius = 50, surface = pygame.image.load("assets/img/ball.png")):
        self.speed = np.array(speed)
        self.radius = radius
        self.mass = self.radius**2
        self.surface = pygame.transform.scale(surface, (self.radius*2,self.radius*2))
        self.rect = self.surface.get_rect()


    def top(self):
        return self.rect.centery - self.radius
    def bottom(self):
        return self.rect.centery + self.radius
    def left(self):
        return self.rect.centerx - self.radius
    def right(self):
        return self.rect.centerx + self.radius



