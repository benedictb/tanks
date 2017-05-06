import pygame
import numpy as np
from explosion import Explosion
from terrain import *
import math
GRAVITY = np.asarray([0, 0.1])
EXPLOSION_SIZE = 9

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
        #print("velx: " + str(self.velx) + " vely: " + str(self.vely))
        # self.vel = np.asarray([np.cos(self.angle)*speed, np.sin(self.angle)*speed], dtype='float32')
        self.wind = wind
        self.gs = gs
        self.explosiongif = 0

    def tick(self):
        # get height of ground at current x value
        # ground = 595 - int(self.gs.terrain.heights[int((self.rect.centerx / PIXEL_SIZE + 5) % self.gs.width/5)] * 5)

        ground = self.gs.height - self.gs.get_height(self.rect.centerx)

        # if not hit anything, keep going
        if self.gs.gmap[self.pos[0], self.gs.height - self.pos[1]] == 0:
            acc = self.wind + GRAVITY
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.pos[0] = self.pos[0] % self.gs.width
            self.rect.center = self.pos
        # explode on contact
        else:
            self.gs.gmap[self.pos[0] - EXPLOSION_SIZE*PIXEL_SIZE:self.pos[0]+EXPLOSION_SIZE*PIXEL_SIZE, self.gs.height - self.pos[1] - EXPLOSION_SIZE*PIXEL_SIZE:self.gs.height - self.pos[1]+EXPLOSION_SIZE*PIXEL_SIZE] = 0
            self.gs.terrain.create_surface()
            self.gs.gameobjects.append(Explosion(self.gs, self.pos))
            self.gs.gameobjects.remove(self)


    def update(self):
        self.gs.screen.blit(self.image, self.rect)