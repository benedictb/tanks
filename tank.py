import pygame
import numpy as np


class MidTank(pygame.sprite.Sprite):
    def __init__(self, gs, pos):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = './media/mid_tank.png'
        self.gs = gs

    def tick(self):
        self.rect.center = self.pos

    def update(self):
        self.gs.screen.blit(self.image, self.rect.center)