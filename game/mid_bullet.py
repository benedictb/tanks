import pygame
import numpy as np
from game.explosion import Explosion
from game.terrain import *
import math
GRAVITY = np.asarray([0, 0.1])
# EXPLOSION_SIZE = 9

import pygame
import numpy as np
from game.explosion import Explosion
from game.terrain import *
import math
import pickle

GRAVITY = np.asarray([0, 0.1])
EXPLOSION_SIZE = 8*PIXEL_SIZE

class MidBullet(pygame.sprite.Sprite):
    def __init__(self, gs, pos, vel):
        super().__init__()
        self.gs = gs
        self.image = pygame.image.load('media/mid_bullet.png')
        self.pos = np.asarray(pos)
        self.vel = vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.startx = self.pos[0]
        self.isFiring = True


    @staticmethod
    def from_local(gs, pos, speed):
        x, y = pygame.mouse.get_pos()
        angle = 360 - math.atan2(y - pos[1], x - pos[0]) * 180 / math.pi
        velx = speed * math.cos(math.radians(360 - angle))
        vely = speed * math.sin(math.radians(360 - angle))
        vel = np.asarray([velx, vely])
        obj = MidBullet(gs,pos,vel)
        return obj

    @staticmethod
    def from_network(gs, pos, vel):
        obj = MidBullet(gs, pos, vel)
        return obj

    def tick(self):
        ground = self.gs.height - self.gs.get_height(self.rect.centerx)

        # if not hit anything, keep going
        if not self.hit_detect():
            acc = GRAVITY
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.pos[0] = self.pos[0] % self.gs.width
            self.rect.center = self.pos
        # explode on contact
        else:
            self.gs.remove_blocks(self.pos[0], self.pos[1])
            data = pickle.dumps(self.pos)
            self.gs.terrainConnection.transport.write(data)
            self.gs.gameobjects.append(Explosion(self.gs, self.pos))
            self.gs.gameobjects.remove(self)

    def hit_detect(self):
        # if bullet is above screen, definitely no hit

        if self.pos[1] <= 0:
            return 0
        elif self.pos[1] >= 600:
            self.gs.gameobjects.remove(self)
        # if bullet hits player 2, hit
        # elif pygame.sprite.collide_rect(self, self.gs.player2) and self.isFiring:
        #     print("HIT")
        #     self.isFiring = False
        #     self.gs.player2.health -= 50
        #     print("enemy health: " + str(self.gs.player2.health))
        #     return 1
        # elif pygame.sprite.collide_rect(self, self.gs.player2):
        #     return 1
        # if bullet hits ground, hit detect
        elif self.gs.gmap[self.pos[0], self.gs.height - self.pos[1]] != 0:
            self.isFiring = False
            return 1
        # if bullets hits nothing, no hit detect
        else:
            return 0

    def update(self):
        m = pygame.mouse.get_pos()

        if m[0] < self.startx:
            rev = pygame.transform.flip(self.image, True, False)
            self.gs.screen.blit(rev, self.rect.center)
        else:
            self.gs.screen.blit(self.image, self.rect.center)

