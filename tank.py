import pygame
import numpy as np
GRAVITY = np.asarray([0, 2])

class MidTank(pygame.sprite.Sprite):
    def __init__(self, gs, pos):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = pygame.image.load('mid_tank.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.gs = gs
        self.vel = np.asarray([0, 1])
        self.acc = GRAVITY

    def tick(self):
        #if self.rect.centery <= 300:
        #    self.vel += self.acc
        #    self.pos += self.vel
        #    self.rect.center = self.pos
        #else:
        #    self.vel = ([0, 0])
        self.pos[0] = self.pos[0] % 1000
        self.rect.centery = 550 - self.gs.gameobjects[0].heights[(self.rect.centerx / 5 + 5) % 200] * 5
        print("height:" + str(self.gs.gameobjects[0].heights[self.rect.centerx / 5]))

    def round(self, y):
        return int( 5 * round(float(y)/5))


    def update(self):
        self.gs.screen.blit(self.image, self.rect.center)