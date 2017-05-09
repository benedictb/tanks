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

    # Either create the map from random.. or from the list of heights
    @staticmethod
    def random(gs):
        t = Terrain(gs)
        gs.heights = t.gen_terrain()
        gs.gmap = t.gen_gmap(gs.heights)
        t.create_surface(gs.gmap)
        return t

    # Heights is a managable amount of data to pass through the network. We can 
    # create the same map using helper functions
    @staticmethod
    def from_heights(gs, heights):
        t = Terrain(gs)
        gs.heights = heights
        gs.gmap = t.gen_gmap(heights)
        t.create_surface(gs.gmap)
        return t

    def tick(self):
        pass

    # IF the cell is valid (cell[0] == True), THEN draw it. gmap is a matrix representing the gamespace
    def create_surface(self, gmap):
        for i in range(0, len(gmap),5):
            for j in range (0, len(gmap[i]),5):
                cell = gmap[i,j]
                if cell == 1: # Fill with rock 
                    self.image.fill(self.rock, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                elif cell == 2: # with dirt
                    self.image.fill(self.dirt, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                elif cell == 3: # with grass
                    self.image.fill(self.grass, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
                elif cell == 0: # probably redundant but with black
                    self.image.fill(self.black, ((i, self.screenHeight - j), (PIXEL_SIZE, PIXEL_SIZE)))
        self.image.set_alpha(150)

    def update(self):
        self.gs.screen.blit(self.image, self.image.get_rect())

    def gen_terrain(self):

        # Try generating a map, if it doesn't fit, try again (should'nt happen more than once, mayyybe twice 
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
            self.heights = self.gen_terrain()
            self.gen_gmap(self, self.heights)

    def remove_terrain_blocks(self, x1, x2, y1, y2):
        self.image.fill(self.black, ((x1, y1), (x2-x1,y2-y1)))
        self.image.set_alpha(0)


