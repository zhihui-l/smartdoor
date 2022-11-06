import pygame
import numpy as np
from surface import Surface

class Entity(Surface):
    speed = [2, 2]
    mass = 200
    rect = None
    enable = True
    def __init__(self, surface, rect, speed = [2, 2], mass = 200):
        self.surface = surface
        self.rect = rect
        self.speed = np.array(speed)
        self.mass = mass


    def move(self, pos = None):
        if pos != None:
            self.rect = self.rect.move(pos)    
        else:
            self.rect = self.rect.move(self.speed.astype(int))


    def collide(self, other):
        m1, m2 = self.mass, other.mass
        M = m1 + m2
        r1 = np.array([self.rect.centerx, self.rect.centery])
        r2 = np.array([other.rect.centerx, other.rect.centery])
        d = np.linalg.norm(r1 - r2)**2
        v1, v2 = np.array(self.speed), np.array(other.speed)
        u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
        u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
        self.speed = u1
        other.speed = u2
        self.move()
        self.move()
        self.move()
        other.move()
        other.move()
        other.move()


    def getDistance(self, other):
        if type(other) == list:
            if other[0] == None:
                return abs(self.rect.centery - other[1])
            if other[1] == None:
                return abs(self.rect.centerx - other[0])
            return np.linalg.norm(np.array([self.rect.centerx-other[0], self.rect.centery-other[1]]))
        return np.linalg.norm(np.array([self.rect.centerx-other.rect.centerx, self.rect.centery-other.rect.centery]))


    def top(self):
        return self.rect.top
    def bottom(self):
        return self.rect.bottom
    def left(self):
        return self.rect.left
    def right(self):
        return self.rect.right


    def collidepoint(self, pos):
        if self.enable:
            return self.rect.collidepoint(pos)
        else:
            return False


    def __sub__(self, other):
        return self.getDistance(other)


    def __pow__(self, other):
        self.collide(other)

