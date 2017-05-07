import pygame
import numpy as np
from explosion import Explosion
from terrain import *
import math
GRAVITY = np.asarray([0, 0.1])
EXPLOSION_SIZE = 8*PIXEL_SIZE

class MidBullet(pygame.sprite.Sprite):
    def __init__(self, gs, pos, angle, speed, wind):
        super().__init__()
        self.pos = np.asarray(pos)
        self.startx = self.pos[0]
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
        self.isFiring = True

    def tick(self):
        ground = self.gs.height - self.gs.get_height(self.rect.centerx)

        # if not hit anything, keep going
        if not self.hit_detect():
            acc = self.wind + GRAVITY
            self.vel[0] += acc[0]
            self.vel[1] += acc[1]
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.pos[0] = self.pos[0] % self.gs.width
            self.rect.center = self.pos
        # explode on contact
        else:
            self.gs.remove_from_gmap(self.pos[0] - EXPLOSION_SIZE,
                                     self.pos[0] + EXPLOSION_SIZE,
                                     self.gs.height - self.pos[1] - EXPLOSION_SIZE,
                                     self.gs.height - self.pos[1]+EXPLOSION_SIZE)

            # self.gs.terrain.create_surface()
            self.gs.terrain.remove_blocks(self.pos[0] - EXPLOSION_SIZE,
                                          self.pos[0] + EXPLOSION_SIZE,
                                          self.pos[1] - EXPLOSION_SIZE,
                                          self.pos[1] + EXPLOSION_SIZE)

            self.gs.gameobjects.append(Explosion(self.gs, self.pos))
            self.gs.gameobjects.remove(self)

    def hit_detect(self):
        # if bullet is above screen, definitely no hit
        if self.pos[1] <= 0:
            return 0
        elif self.pos[1] >= 600:
            self.gs.gameobjects.remove(self)
        # if bullet hits player 2, hit
        elif pygame.sprite.collide_rect(self, self.gs.gameobjects[2]) and self.isFiring:
            print("HIT")
            self.isFiring = False
            self.gs.gameobjects[2].health -= 50
            print("enemy health: " + str(self.gs.gameobjects[2].health))
            return 1
        elif pygame.sprite.collide_rect(self, self.gs.gameobjects[2]):
            return 1
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