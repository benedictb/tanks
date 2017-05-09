from game.terrain import *
import numpy as np
from game.mid_bullet import MidBullet
import pickle

GRAVITY = np.asarray([0, .1])
MAXBULLET = 5
HEALTH = 1000

class MidTank(pygame.sprite.Sprite):
    def __init__(self, gs, pos):
        super().__init__()
        self.pos = np.asarray(pos)
        self.image = pygame.image.load('media/mid_tank.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.gs = gs
        self.vel = np.asarray([0, 0],dtype=np.float)
        self.acc = GRAVITY
        self.health = HEALTH
        self.bcount = 0

        print(self.rect.size)

    def tick(self):
        # apply acceleration to velocity
        self.vel += self.acc

        # apply velocity to position
        self.pos += self.vel.astype(np.int)

        # apply wind to x position
        self.pos[0] = self.pos[0] % self.gs.width

        h = self.gs.get_height(self.pos[0]+25)

        # if on ground, tied height to ground + no y velocity
        if self.pos[1] >= self.gs.height - 45 - h:
            self.pos[1] = (self.gs.height-45) - h
            self.vel[1] = 0

        # set sprite center to position
        self.rect.center = self.pos

        # if health is 0, game over. Remove object from game
        if self.health <= 0:
            self.gs.gameobjects.remove(self)
            self.gs.game_over = True

    def get_pos(self):
        return [self.pos[0], self.pos[1]]

    def update(self):
        m = pygame.mouse.get_pos()

        if m[0] > self.pos[0]:
            rev = pygame.transform.flip(self.image, True, False)
            self.gs.screen.blit(rev, self.rect.center)
        else:
            self.gs.screen.blit(self.image, self.rect.center)

    def launch(self):
        if self.bcount < MAXBULLET:
            self.bcount+=1
            pos = self.get_pos()
            obj = MidBullet.from_local(self.gs, pos, 10, False)
            self.gs.gameobjects.append(obj)

            data = [0] * 3
            data[0] = pos
            data[1] = obj.vel
            data[2] = True
            dstring = pickle.dumps(data)
            self.gs.bulletConnection.transport.write(dstring)