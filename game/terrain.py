#! /usr/bin/python3

import pygame
import numpy as np
import random
import time
PIXEL_SIZE = 5
ROCK_LEVEL = 5


class Terrain(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs
        self.screenHeight = gs.height
        self.screenWidth = gs.width
        self.heights = [10] * int(self.screenWidth / PIXEL_SIZE)
        image = pygame.Surface((self.screenWidth, self.screenHeight), pygame.SRCALPHA, 32)
        self.image = image.convert_alpha()

        # These are the colors for the different types of tile. Changeable
        self.dirt = (117, 76, 16, 255)
        self.rock = (141, 155, 141, 255)
        self.grass = (48, 219, 48, 255)
        self.black = (0, 0, 0, 0)
        # self.gmap = gmap

    @staticmethod
    def random(gs):
        t = Terrain(gs)
        heights = t.gen_terrain()
        gs.heights = heights
        gmap = t.gen_gmap(heights)
        t.create_surface(gmap)
        gs.gmap = gmap
        return t

    # @staticmethod
    # def from_gmap(gs,gmap):
    #     t = Terrain(gs)
    #     t.create_surface(gmap)
    #     gs.gmap = gmap
    #     return t

    @staticmethod
    def from_heights(gs, heights):
        t = Terrain(gs)
        gmap = t.gen_gmap(heights)
        t.create_surface(gmap)
        gs.gmap = gmap
        return t


    def tick(self):
        pass

    # IF the cell is valid (cell[0] == True), THEN draw it. gmap is a matrix representing the gamespace
    def create_surface(self, gmap):
        for i in range(0, len(gmap),5):
            for j in range (0, len(gmap[i]),5):
                cell = gmap[i,j]
                if cell == 1:
                    # self.gs.screen.set_at((i,self.screenHeight-j), self.rock)
                    self.image.fill(self.rock, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                elif cell == 2:
                    self.image.fill(self.dirt, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                    # self.gs.screen.set_at((i,self.screenHeight-j), self.dirt)
                elif cell == 3:
                    self.image.fill(self.grass, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                    # self.gs.screen.set_at((i,self.screenHeight-j), self.grass)
                elif cell == 0:
                    self.image.fill(self.black, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
        self.image.set_alpha(150)

    def update(self):
        self.gs.screen.blit(self.image, self.image.get_rect())

    def gen_terrain(self):

        # Try generating a map, if it doesn't fit, try again (should'nt happen more than once
        self.heights[0] = 100 # Left and right start the same way
        self.heights[-1] = 100
        length = int(self.screenWidth / PIXEL_SIZE)
        height = int(self.screenHeight / PIXEL_SIZE)
        mid = int(length/2)

        # Generate the graph with a random step, with a higher probabability of going up in the middle
        for i in range(1,mid):
            prev = self.heights[i-1]
            addition = random.uniform(-8,13)
            self.heights[i] = int(addition + prev)

        for j in range(length-2, mid, -1):
            prev = self.heights[j+1]
            addition = random.uniform(-8,13)
            self.heights[j] = int(addition+prev)

        # Make a adjustment in the middle in case there's a gap. This could be better
        self.heights[mid] = int((self.heights[mid+1] + self.heights[mid-1]) / 2)
        return np.floor_divide(np.asarray(self.heights, dtype=int), PIXEL_SIZE).tolist()

    def gen_gmap(self, heights):
        try:
            # This is a map of the tiles
            self.heights = heights
            gmap = np.zeros((self.screenWidth, self.screenHeight))

            # The next loops define which sort of tile they are (what color)
            for i, h in enumerate(self.heights):
                i = i*5

                for j in range(ROCK_LEVEL,h):
                    j = j*PIXEL_SIZE
                    # gmap[i,j,0] = 1
                    gmap[i:i+PIXEL_SIZE,j:j+PIXEL_SIZE] = 2 #self.dirt

                for j in range(0, ROCK_LEVEL + random.randint(0, 2)):
                    j = j*PIXEL_SIZE
                    # gmap[i,j,0] = 1
                    gmap[i:i+PIXEL_SIZE, j:j+PIXEL_SIZE] = 1 #self.rock

                for j in range(h - ROCK_LEVEL, h):
                    j = j*PIXEL_SIZE
                    # gmap[i,j,0] = 1
                    gmap[i:i+PIXEL_SIZE, j:j+PIXEL_SIZE] = 3 #self.grass

            return gmap
        except IndexError:
            self.gen_gmap(heights)

    def remove_blocks(self, x1, x2, y1, y2):
        self.image.fill(self.black, ((x1, y1), (x2-x1,y2-y1)))
        self.image.set_alpha(0)


