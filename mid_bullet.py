import pygame
import numpy as np
GRAVITY = np.asarray([0, -2])


class MidBullet(pygame.sprite.Sprite):
    def __init__(self,gs,pos, angle, speed, wind):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = './media/mid_bullet.png'
        self.vel = np.asarray([np.cos(angle)*speed,-np.sin(angle)*speed], dtype='float32')
        self.wind = wind
        self.gs = gs

    def tick(self):
        acc = self.wind + GRAVITY
        self.vel += acc
        self.pos += self.vel
        self.pos[0] = self.pos[0] % 1000
        self.rect.center = self.pos

    def update(self):
        self.gs.screen.blit(self.image, self.rect)