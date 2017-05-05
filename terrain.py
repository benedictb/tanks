import pygame
import numpy as np
import random.uniform
SQUARE_SIDE = 100

# Not sure if this is a sprite..
class Terrain(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs
        self.generate_terrain()
        self.dirt = (117, 76, 16)
        self.rock = (141, 155, 141)
        self.grass = (48, 219, 48)
        self.screenHeight = gs.height
        self.screenWidth = gs.width
        self.heights = [10] * screenWidth


    def tick(self):
        pass

    def update(self):
        for i, h in enumerate(self.heights):

            x = i*SQUARE_SIDE
            pygame.draw.rect(self.gs.screen,self.rock,(x,self.screenHeight, SQUARE_SIDE, SQUARE_SIDE),0)
            for j in range(1,h):
                pygame.draw.rect(self.gs.screen,self.dirt, (x, self.screenHeight-j, SQUARE_SIDE, SQUARE_SIDE), 0)
            pygame.draw.rect(self.gs.screen, self.grass, (x, self.screenHeight-h, SQUARE_SIDE, SQUARE_SIDE),0)



    def generate_terrain(self):
        pass

    def gen_terrain(self):
        self.heights[0] = 10
        mid = self.screenWidth /2
        for i in range(0,mid):
            prev = self.heights[i-1]
            addition = random.uniform(-1,1) * (1/(mid-i)) * np.sin((mid-i))
            self.heights[i] = addition + prev

        for i in range(0,mid):
            prev = self.heights[mid + i-1]
            addition = - random.uniform(-1,1) * (1/(mid-i)) * np.sin((mid-i))
            self.heights[i+mid] = addition + prev


