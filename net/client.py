from game.constants import *
import pickle

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol

from game.mid_bullet import MidBullet
from game.tank import MidTank
from game.terrain import Terrain
from game.health import ErrorBars
from game.wind import Wind


# Connection to initiate client game objects
class FirstConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # save connection variable for later use
        self.gs.firstConnection = self

        # update connection status in list
        self.gs.connections[0] = True

    def dataReceived(self, data):
        # make sure no old game objects
        self.gs.gameobjects.clear()
        dlist = pickle.loads(data)
        heights = dlist[2]

        # create terrain from passed through heights data
        self.gs.terrain = Terrain.from_heights(self.gs, heights)

        # create tank objects from position data
        self.gs.player2 = MidTank(self.gs, dlist[0])
        self.gs.player1 = MidTank(self.gs, dlist[1])

        # create health bars
        self.bars = ErrorBars(self.gs)

        # set wind so same for both players
        self.gs.wind = dlist[3]

        # create wind arrow for client
        self.gs.windarrow = Wind(self.gs, self.gs.wind)

        # add all objects to client gameobject list
        self.gs.gameobjects.append(self.gs.terrain)
        self.gs.gameobjects.append(self.bars)
        self.gs.gameobjects.append(self.gs.player1)
        self.gs.gameobjects.append(self.gs.player2)
        self.gs.game_over = False

# Connection to pass bullet data on fire
class BulletConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # set bullet connection variable for later use
        self.gs.bulletConnection = self

        # update connection status in list
        self.gs.connections[1] = True

    def dataReceived(self, data):
        dlist = pickle.loads(data)

        # create local bullet object using x, y, and velocity data and add to gameobject list
        self.gs.gameobjects.append(MidBullet.from_network(self.gs, dlist[0], dlist[1], dlist[2]))


class TankConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # set tank connection variable for later use
        self.gs.tankConnection = self

        # update connection status in list
        self.gs.connections[2] = True

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        pos = dlist[0]
        health = dlist[1]

        # update position and health of opponent
        self.gs.player2.pos = pos
        self.gs.player2.health = health


class TerrainConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # set terrain connection variable for later use
        self.gs.terrainConnection = self

        # update connection status in list
        self.gs.connections[3] = True

    def dataReceived(self, data):
        data = pickle.loads(data)

        # update destroyed terrain blocks received from x, y coordinates of missile impact
        self.gs.remove_blocks(data[0],data[1])


class FirstFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = FirstConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class BulletFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = BulletConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class TankFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = TankConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class TerrainFactory(ClientFactory):
    def __init__(self, gs):
        self.myconn = TerrainConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn