#! /usr/bin/python3

import pygame
import numpy as np
import random
SQUARE_SIDE = 5
ROCK_LEVEL = 20

# Not sure if this is a sprite..
class Terrain(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs
        self.screenHeight = gs.height
        self.screenWidth = gs.width
        self.heights = [10] * int(self.screenWidth/SQUARE_SIDE)
        self.gen_terrain()
        self.dirt = (117, 76, 16)
        self.rock = (141, 155, 141)
        self.grass = (48, 219, 48)
        # print(self.heights)

    def tick(self):
        pass

    def update(self):
        for i, h in enumerate(self.heights):
            i*= SQUARE_SIDE

            for k in range(ROCK_LEVEL,h):
                self.gs.screen.fill(self.dirt, ((i,self.screenHeight-k), (SQUARE_SIDE, SQUARE_SIDE)))

            for j in range(0,ROCK_LEVEL+random.randint(-5,5)):
                self.gs.screen.fill(self.rock, ((i,self.screenHeight-j), (SQUARE_SIDE, SQUARE_SIDE)))

            for l in range(h-ROCK_LEVEL, h):
                self.gs.screen.fill(self.grass, ((i, self.screenHeight - l), (SQUARE_SIDE, SQUARE_SIDE)))

    def gen_terrain(self):
        self.heights[0] = 100
        self.heights[-1] = 100
        length = int(self.screenWidth / SQUARE_SIDE)
        mid = int(length/2)
        for i in range(1,mid):
            prev = self.heights[i-1]
            addition = random.uniform(-8,10)
            self.heights[i] = int(addition + prev)

        for j in range(length-2, mid, -1):
            prev = self.heights[j+1]
            addition = random.uniform(-8,10)
            self.heights[j] = int(addition+prev)

        self.heights[mid] = int((self.heights[mid+1] + self.heights[mid-1]) / 2)
        self.heights *= SQUARE_SIDE






