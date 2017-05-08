from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from game.mid_bullet import MidBullet
from game.tank import MidTank
import pickle
from game.terrain import *


class FirstConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        print(dir(self.gs))
        self.gs.player2 = MidTank(self.gs, dlist[0])
        self.gs.player1 = MidTank(self.gs, dlist[1])
        self.gs.gameobjects.append(self.gs.player1)
        self.gs.gameobjects.append(self.gs.player2)
        heights = dlist[2]
        self.gs.terrain = Terrain.from_heights(self.gs, heights)
        self.gs.gameobjects.append(self.gs.terrain)
        self.gs.wind = dlist[3]


class BulletConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        pass

    def dataReceived(self, data):
        # create bullet locally
        dlist = pickle.loads(data)
        self.gs.gameobjects.append(MidBullet.from_network(self, dlist[0], dlist[1]))

class TankConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        pos = dlist[0]
        health = dlist[1]
        self.gs.player2.pos = pos
        self.gs.player2.health = health


class TerrainConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def dataReceived(self, data):
        data = pickle.loads(data)
        self.gs.remove_blocks(data)


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