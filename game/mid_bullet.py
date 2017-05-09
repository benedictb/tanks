import numpy as np
import pygame
import math
import pickle

from game.explosion import Explosion
from game.terrain import Terrain

PIXEL_SIZE = 5
GRAVITY = np.asarray([0, 0.1])
EXPLOSION_SIZE = 8*PIXEL_SIZE

# MidBullet because the initial intent was to create multiple tank classes with different bullets.
# If this had happened, this would become a parent class for each of the bullet types
class MidBullet(pygame.sprite.Sprite):
    def __init__(self, gs, pos, vel, isEnemy):
        super().__init__()
        self.gs = gs
        self.image = pygame.image.load('media/mid_bullet.png')
        self.pos = np.asarray(pos)
        self.vel = vel
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.startx = self.pos[0]
        self.isFiring = True
        self.isEnemy = isEnemy

    # If we're creating a bullet locally, we find direction with the mouse
    @staticmethod
    def from_local(gs, pos, speed, isEnemy):
        x, y = pygame.mouse.get_pos()
        angle = 360 - math.atan2(y - pos[1], x - pos[0]) * 180 / math.pi
        velx = speed * math.cos(math.radians(360 - angle))
        vely = speed * math.sin(math.radians(360 - angle))
        vel = np.asarray([velx, vely])
        obj = MidBullet(gs,pos,vel, isEnemy)
        return obj

    # If we're creating a bullet via network, we already have the velocity
    @staticmethod
    def from_network(gs, pos, vel, isEnemy):
        obj = MidBullet(gs, pos, vel, isEnemy)
        return obj


    def tick(self):
        ground = self.gs.height - self.gs.get_height(self.rect.centerx)

        # if not hit anything, keep going
        if not self.hit_detect():
            acc = GRAVITY + self.gs.wind
            self.vel += acc # Used numpy objects for easy matrix operations (N dimensionality!)
            self.pos += self.vel.astype(np.int)
            self.pos[0] = self.pos[0] % self.gs.width
            self.rect.center = self.pos
        
        # explode on contact
        else:
            # To avoid double explosions, we only remove blocks on one game, then 
            # send which blocks to remove to the other. Small overhead for this, only 2 ints of data
            if self.isEnemy:
                self.gs.player2.bcount -= 1
            else:
                self.gs.player1.bcount -= 1

            if self.gs.isServer:
                self.gs.remove_blocks(self.pos[0], self.pos[1]) # remove the blocks from the map
                data = pickle.dumps(self.pos) # serialize the data (might be overkill here but we wanted to be consistent)
                self.gs.terrainConnection.transport.write(data)
            self.gs.gameobjects.append(Explosion(self.gs, self.pos)) # create a new explosion object as a result

            # If there are too many bullets on the screen this might throw and exception
            try:
                self.gs.gameobjects.remove(self) # get rid of the bullet
            except ValueError:
                pass

    def hit_detect(self):
        # if bullet is above screen, definitely no hit

        # Don't care if above screen
        if self.pos[1] <= 0:
            return 0
        # But if its below, kill the bullet
        elif self.pos[1] >= 600:
            self.gs.gameobjects.remove(self)

        # Check if its the enemy
        if not self.isEnemy:
            # If bullet hits player 2, hit with 'collide'
            if pygame.sprite.collide_rect(self, self.gs.player2) and self.isFiring:
                print("HIT")
                self.isFiring = False
                self.gs.player2.health -= 50
                print("Player Health: " + str(self.gs.player1.health))
                print("Enemy Health: " + str(self.gs.player2.health))
                print("~~~~~~~~~~~~~~~~~")
                return 1
            # If already hit, don't worry about adding more damage
            elif pygame.sprite.collide_rect(self, self.gs.player2):
                return 1
        
        elif self.isEnemy:
            # if bullet hits player 1, hit with 'collide'
            if pygame.sprite.collide_rect(self, self.gs.player1) and self.isFiring:
                print("HIT")
                self.isFiring = False
                self.gs.player1.health -= 50
                print("Player Health: " + str(self.gs.player1.health))
                print("Enemy Health: " + str(self.gs.player2.health))
                return 1
            elif pygame.sprite.collide_rect(self, self.gs.player1):
                return 1

        # if bullet hits ground, hit detect
        if self.gs.gmap[self.pos[0], self.gs.height - self.pos[1]] != 0:
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

