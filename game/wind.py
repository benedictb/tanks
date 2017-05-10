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

        # A simple arrow for the wind, in the direction of the wind. Grabbed from stackoverflow
        pygame.draw.polygon(self.surface, self.blue,
                        ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

        # Scale it to our needs
        self.ss = pygame.transform.scale(self.surface, (30,30))
        
        # Rotate it in the angle of the wind
        self.rot = pygame.transform.rotate(self.ss, angle)
        self.gs.gameobjects.append(self)

    def tick(self):
        pass

    def update(self):
        self.gs.screen.blit(self.rot, (self.gs.width-50, 100))

