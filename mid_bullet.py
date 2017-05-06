import pygame
import numpy as np
from terrain import *
import math
GRAVITY = np.asarray([0, 0.1])


class MidBullet(pygame.sprite.Sprite):
    def __init__(self, gs, pos, angle, speed, wind):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = pygame.image.load('media/mid_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        # get angle of trajectory
        self.x, self.y = pygame.mouse.get_pos()
        self.angle = 360 - math.atan2(self.y - self.rect.centery, self.x - self.rect.centerx) * 180 / math.pi
        # use angle to get x and y velocity
        self.velx = speed * math.cos(math.radians(360 - self.angle))
        self.vely = speed * math.sin(math.radians(360 - self.angle))
        self.vel = np.asarray([self.velx, self.vely])
        print("velx: " + str(self.velx) + " vely: " + str(self.vely))
        # self.vel = np.asarray([np.cos(self.angle)*speed, np.sin(self.angle)*speed], dtype='float32')
        self.wind = wind
        self.gs = gs
        self.explosiongif = 0

    def tick(self):
        # get height of ground at current x value
        # ground = 595 - int(self.gs.terrain.heights[int((self.rect.centerx / PIXEL_SIZE + 5) % self.gs.width/5)] * 5)

        ground = self.gs.height - self.gs.get_height(self.rect.centerx)

        # if not hit anything, keep going
        if self.pos[1] <= ground:
            acc = self.wind + GRAVITY
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.pos[0] = self.pos[0] % self.gs.width
            self.rect.center = self.pos
        # explode on contact
        elif self.explosiongif < 17:
            if self.explosiongif < 10:
                self.image = pygame.image.load('explosion/frames00' + str(self.explosiongif) + 'a.png')
            else:
                self.image = pygame.image.load('explosion/frames0' + str(self.explosiongif) + 'a.png')
            self.explosiongif += 1
        # remove from game when explosion is over
        else:
            self.gs.gameobjects.remove(self)

    def update(self):
        self.gs.screen.blit(self.image, self.rect)