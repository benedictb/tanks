import pygame
from terrain import *
import numpy as np
GRAVITY = np.asarray([0, 2])

class MidTank(pygame.sprite.Sprite):
    def __init__(self, gs, pos):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = pygame.image.load('media/mid_tank.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.gs = gs
        self.vel = np.asarray([0, 0])
        self.acc = GRAVITY
        self.health = 1000
        print(self.rect.size)

    def tick(self):
        #if self.rect.centery <= 300:
        #    self.vel += self.acc
        #    self.pos += self.vel
        #    self.rect.center = self.pos
        #else:
        #    self.vel = ([0, 0])
        self.vel += self.acc
        self.pos += self.vel
        self.pos[0] = self.pos[0] % self.gs.width

        h = self.gs.get_height(self.pos[0]+25)

        if self.pos[1] >= h:
            self.pos[1] = (self.gs.height-45) - h

        # self.pos[1] = 555 - int(self.gs.terrain.heights[int((self.rect.centerx / PIXEL_SIZE + 5) % 350 )] * 5)
        self.rect.center = self.pos
        if self.health <= 0:
            pass
            #print("GAME OVER")



    def get_pos(self):
        return [self.pos[0], self.pos[1]]


    def update(self):
        m = pygame.mouse.get_pos()

        if m[0] > self.pos[0]:
            rev = pygame.transform.flip(self.image, True, False)
            self.gs.screen.blit(rev, self.rect.center)
        else:
            self.gs.screen.blit(self.image, self.rect.center)