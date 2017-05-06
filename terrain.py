#! /usr/bin/python3

import pygame
import numpy as np
import random
PIXEL_SIZE = 5
ROCK_LEVEL = 3

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
        for i in range(0, len(self.gmap)):
            for j in range (0, len(self.gmap[i])):
                cell = self.gmap[i,j]
                if cell[0]:
                    self.gs.screen.fill(cell[1:], ((i * PIXEL_SIZE, self.screenHeight - j * PIXEL_SIZE), (PIXEL_SIZE, PIXEL_SIZE)))




    def gen_terrain(self):
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

        self.gmap = gmap


