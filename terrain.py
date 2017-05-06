#! /usr/bin/python3

import pygame
import numpy as np
import random
PIXEL_SIZE = 5
ROCK_LEVEL = 5
PARALLAX = 2

# Not sure if this is a sprite..
class Terrain(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs
        self.screenHeight = gs.height
        self.screenWidth = gs.width
        self.heights = [10] * int(self.screenWidth / PIXEL_SIZE)
        self.dirt = (117, 76, 16)
        self.rock = (141, 155, 141)
        self.grass = (48, 219, 48)
        self.gen_terrain()

        # print(self.heights)

    def tick(self):
        pass

    def update(self):
        for i in range(0, len(self.gs.gmap)):
            for j in range (0, len(self.gs.gmap[i])):
                cell = self.gs.gmap[i,j]
                if cell[0]:
                    self.gs.screen.fill(cell[1:], ((i * PIXEL_SIZE, self.screenHeight - j * PIXEL_SIZE), (PIXEL_SIZE, PIXEL_SIZE)))




    def gen_terrain(self):
        try:
            self.heights[0] = 100
            self.heights[-1] = 100
            length = int(self.screenWidth / PIXEL_SIZE)
            height = int(self.screenHeight / PIXEL_SIZE)
            mid = int(length/2)
            for i in range(1,mid):
                prev = self.heights[i-1]
                addition = random.uniform(-8,13)
                self.heights[i] = int(addition + prev)

            for j in range(length-2, mid, -1):
                prev = self.heights[j+1]
                addition = random.uniform(-8,13)
                self.heights[j] = int(addition+prev)

            self.heights[mid] = int((self.heights[mid+1] + self.heights[mid-1]) / 2)
            self.heights = np.floor_divide(np.asarray(self.heights, dtype=int), PIXEL_SIZE)

            gmap = np.zeros((length, height, 4))

            for i, h in enumerate(self.heights):

                for j in range(ROCK_LEVEL,h):
                    gmap[i,j,0] = 1
                    gmap[i,j,1:] = self.dirt

                for j in range(0, ROCK_LEVEL + random.randint(0, 2)):
                    gmap[i,j,0] = 1
                    gmap[i,j,1:] = self.rock

                for j in range(h - ROCK_LEVEL, h):
                    gmap[i,j,0] = 1
                    gmap[i,j,1:] = self.grass

            self.gs.gmap = gmap
        except IndexError:
            self.gen_terrain()



class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.screenHeight = gs.height
        self.screenWidth = gs.width
        self.image = pygame.image.load('./media/bg.jpg')
        self.rimage = pygame.image.load('./media/bg_reverse.jpg')
        self.rect = self.image.get_rect()
        self.rrect = self.rimage.get_rect()

        self.bimage = pygame.image.load('./media/bg.jpg')
        self.brimage = pygame.image.load('./media/bg_reverse.jpg')
        self.brect = self.image.get_rect()
        self.brrect = self.rimage.get_rect()

        self.size = self.rect.size

        self.rect.left, self.rect.top = (0,0)
        self.rrect.left, self.rrect.top = (0+self.size[0],0)

        self.brect.left, self.rect.top = (0 + 2 * self.size[0] ,0)
        self.brrect.left, self.rrect.top = (0 + 3* self.size[0], 0)

        self.rects = [self.rect, self.rrect, self.brect, self.brrect]

        self.gs = gs

    def tick(self):
        pass

    def shift_left(self):
        for r in self.rects:
            r.left += PARALLAX

        self.check_bounds()

    def shift_right(self):
        for r in self.rects:
            r.left -= PARALLAX

        self.check_bounds()

    def check_bounds(self):

        # examine later
        if self.rect.left >= 0:
            for r in self.rects:
                r.left -= 2 * self.size[0]

        elif self.brrect.left <= self.screenWidth - self.size[0]:
            for r in self.rects:
                r.left += 2 * self.size[0]

    def update(self):
        self.gs.screen.blit(self.image, self.rect)
        self.gs.screen.blit(self.rimage, self.rrect)
        self.gs.screen.blit(self.bimage, self.brect)
        self.gs.screen.blit(self.brimage, self.brrect)