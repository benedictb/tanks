import pygame
import numpy as np
from terrain import *
import math
GRAVITY = np.asarray([0, 0.75])


class MidBullet(pygame.sprite.Sprite):
    def __init__(self, gs, pos, angle, speed, wind):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = pygame.image.load('mid_bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.x, self.y = pygame.mouse.get_pos()
        self.angle = 360 - math.atan2(self.y - self.rect.centery, self.x - self.rect.centerx) * 180 / math.pi

        self.velx = speed * math.cos(math.radians(360 - self.angle))
        self.vely = speed * math.sin(math.radians(360 - self.angle))
        self.vel = np.asarray([self.velx, self.vely])
        print("velx: " + str(self.velx) + " vely: " + str(self.vely))
        #self.vel = np.asarray([np.cos(self.angle)*speed, np.sin(self.angle)*speed], dtype='float32')
        #self.vel = np.asarray([20, -20]) #testing
        self.wind = wind
        self.gs = gs

    def tick(self):
        ground = 595 - int(self.gs.gameobjects[0].heights[(self.rect.centerx / PIXEL_SIZE + 5) % 199] * 5)
        if self.pos[1] <= ground:
            acc = self.wind + GRAVITY
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            #self.rect.move(self.velx, self.vely)
            self.pos[0] = self.pos[0] % 1000
            self.rect.center = self.pos

    def update(self):
        self.gs.screen.blit(self.image, self.rect)