from game.constants import *
import math
import pygame

class Wind(pygame.sprite.Sprite):
    def __init__(self, gs, wind):
        self.blue = (126, 174, 252)
        self.wind = wind
        self.gs = gs
        self.surface = pygame.Surface((400,400))
        angle = 360 - math.atan2(wind[1],wind[0]) * 180 / math.pi


        pygame.draw.polygon(self.surface, self.blue,
                        ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

        self.ss = pygame.transform.scale(self.surface, (30,30))
        self.rot = pygame.transform.rotate(self.ss, angle)
        self.gs.gameobjects.append(self)

    def tick(self):
        pass

    def update(self):
        self.gs.screen.blit(self.rot, (self.gs.width-50, 100))

