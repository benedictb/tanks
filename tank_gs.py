#! /usr/bin/python3
# Thomas Franceschi
# Ben Becker

import pygame
from terrain import Terrain
from tank import MidTank
from mid_bullet import MidBullet
from background import Background
from pygame.locals import *
import time

class GameSpace():

    def get_height(self, x):
        x = x % self.width
        col =  [1 if i else 0 for i in self.gmap[x,:] ]
        # print(col)
        # h = 1
        for i in range(0, self.height):
            # print(i)
            if not col[i]:
                return i
        return 1

        # col = [1 for i in self.gmap[x,:] if i]
        # return sum(col)

    def remove_from_gmap(self,x1,x2,y1,y2):
        self.gmap[x1:x2,y1:y2] = 0

    def main(self):
        # init gamespace
        pygame.init()
        self.size = self.width, self.height = 1750, 600
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)
        self.game_over = False

        # init gameobjects
        self.clock = pygame.time.Clock()

        self.terrain = Terrain(gs)
        self.player1 = MidTank(self,MidTank(self, ([50, 300])))
        self.gameobjects = []
        self.gameobjects.append(self.terrain)
        self.gameobjects.append(self.player1)
        self.gameobjects.append(MidTank(self, ([1700, 300])))

        pygame.key.set_repeat(1, 30)

        # start game loop
        while 1:
            start = time.time()
            self.clock.tick(60)

            if self.game_over:
                return 1
            # read user input
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[K_w]:
                        #print("jump!")
                        self.player1.vel[1] += 50
                    if keys[K_a]:
                        self.gameobjects[1].pos[0] -= 4
                        #self.bg.shift_left()
                    if keys[K_d]:
                        self.gameobjects[1].pos[0] += 4
                        #self.bg.shift_right()
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        pos = self.player1.get_pos()
                        obj = MidBullet.from_local(self, pos, 10)
                        self.gameobjects.append(obj)
                        # self.bulletConnection.transport.write((pos, obj.vel))

            #blank out screen
            self.screen.fill(self.black)

            # call tick on each object
            for gameobject in self.gameobjects:
                gameobject.tick()

            # update screen
            for gameobject in self.gameobjects:
                gameobject.update()

            pygame.display.flip()

            end = time.time()
            print(end-start)

