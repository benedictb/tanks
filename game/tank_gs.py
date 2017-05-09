#! /usr/bin/python3
# Thomas Franceschi
# Ben Becker

import pygame
from game.terrain import Terrain
from game.tank import MidTank
from game.mid_bullet import MidBullet
from pygame.locals import *
import time
from twisted.internet import reactor
import net.client as client
import net.server as server
from twisted.internet.task import LoopingCall
import pickle
import twisted
from pygame.mixer import Sound
from game.health import ErrorBars

FIRSTPORT = 50000
TANKPORT = 50001
BULLETPORT = 50002
TERRAINPORT = 50003

PIXEL_SIZE = 5
EXPLOSION_SIZE = 8*PIXEL_SIZE

class GameSpace():
    def __init__(self, isServer=True):
        self.isServer = isServer
        self.connections = [False] * 4
        self.gameobjects = []
        self.size = self.width, self.height = 1750, 600
        self.screen = pygame.display.set_mode(self.size)
        self.black = 0, 0, 0
        self.game_over = False

        # init gameobjects
        self.clock = pygame.time.Clock()
        self.count = 0
        self.run = False
        pygame.mixer.pre_init(22100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('media/music.mp3')
        pygame.mixer.music.play()
        self.explode = Sound('media/explode.wav')
        self.launch = Sound('media/launch.wav')

    def remove_blocks(self, x, y):
        self.remove_from_gmap(x - EXPLOSION_SIZE,
                                 x + EXPLOSION_SIZE,
                                 self.height - y - EXPLOSION_SIZE,
                                 self.height - y + EXPLOSION_SIZE)

        self.terrain.remove_terrain_blocks(x - EXPLOSION_SIZE,
                                      x + EXPLOSION_SIZE,
                                      y - EXPLOSION_SIZE,
                                      y + EXPLOSION_SIZE)

    def get_height(self, x):
        x = x % self.width
        col = [1 if i else 0 for i in self.gmap[x,:] ]

        for i in range(0, self.height):
            if not col[i]:
                return i
        return 1


    def remove_from_gmap(self,x1,x2,y1,y2):
        self.gmap[x1:x2,y1:y2] = 0

    def main(self):
        # set up client and server respectively
        if self.isServer:
            self.terrain = Terrain.random(self)
            self.player1 = MidTank(self, ([50, 300]))
            self.player2 = MidTank(self, ([1700, 300]))
            self.bars = ErrorBars(self)

            self.gameobjects.append(self.terrain)
            self.gameobjects.append(self.bars)
            self.gameobjects.append(self.player1)
            self.gameobjects.append(self.player2)
            self.server_start()
        else:
            self.client_start()

    # start game loop
    def game_loop(self):

        # Make sure all connections have been made before starting
        if not self.run:
            if all(self.connections):
                self.run = True
            return


        start = time.time()
        # self.clock.tick(60)
        self.count += 1

        if self.game_over:
            return 1
        # read user input
        for event in pygame.event.get():
            if event.type == QUIT:
                return 0

            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.player1.vel[1] += 50
            elif keys[K_a]:
                self.player1.vel[0] = -1
            elif keys[K_d]:
                self.player1.vel[0] = 1
            else:
                self.player1.vel[0] = 0

            if event.type == MOUSEBUTTONDOWN or event.type == K_DOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0] or keys[K_SPACE]:
                    self.launch.play()
                    pos = self.player1.get_pos()
                    obj = MidBullet.from_local(self, pos, 10, False)
                    self.gameobjects.append(obj)

                    data = [0] * 3
                    data[0] = pos
                    data[1] = obj.vel
                    data[2] = True
                    dstring = pickle.dumps(data)
                    self.bulletConnection.transport.write(dstring)

        # send tank data
        tankdata = [0] * 2
        tankdata[0] = self.player1.get_pos()
        tankdata[1] = self.player1.health
        ptankdata = pickle.dumps(tankdata)
        self.tankConnection.transport.write(ptankdata)

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
        # print(end-start)

    def server_start(self):
        reactor.listenTCP(FIRSTPORT, server.FirstFactory(self))
        reactor.listenTCP(TANKPORT, server.TankFactory(self))
        reactor.listenTCP(BULLETPORT, server.BulletFactory(self))
        reactor.listenTCP(TERRAINPORT, server.TerrainFactory(self))

        lc = LoopingCall(self.game_loop)
        lc.start(1/60).addErrback(twisted.python.log.err)
        reactor.run()

    def client_start(self):
        self.firstConnection = reactor.connectTCP('localhost',FIRSTPORT, client.FirstFactory(self))
        self.tankConnection = reactor.connectTCP('localhost',TANKPORT, client.TankFactory(self))
        self.bulletConnection = reactor.connectTCP('localhost', BULLETPORT, client.BulletFactory(self))
        self.terrainConnection = reactor.connectTCP('localhost', TERRAINPORT, client.TerrainFactory(self))

        lc = LoopingCall(self.game_loop)
        lc.start(1/60).addErrback(twisted.python.log.err)
        reactor.run()

