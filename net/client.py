from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from game.mid_bullet import MidBullet
from game.tank import MidTank
import pickle
from game.terrain import *
from game.health import ErrorBars
from game.wind import Wind

FIRSTPORT = 50000
TANKPORT = 50001
BULLETPORT = 50002
TERRAINPORT = 50003


class FirstConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        self.gs.firstConnection = self
        self.gs.connections[0] = True

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        # print(dlist)
        # print(dir(self.gs))
        heights = dlist[2]
        self.gs.terrain = Terrain.from_heights(self.gs, heights)
        self.gs.player2 = MidTank(self.gs, dlist[0])
        self.gs.player1 = MidTank(self.gs, dlist[1])
        self.bars = ErrorBars(self.gs)
        self.gs.wind = dlist[3]
        self.gs.windarrow = Wind(self.gs, self.gs.wind)

        self.gs.gameobjects.append(self.gs.terrain)
        self.gs.gameobjects.append(self.bars)
        self.gs.gameobjects.append(self.gs.player1)
        self.gs.gameobjects.append(self.gs.player2)


class BulletConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        self.gs.bulletConnection = self
        self.gs.connections[1] = True

    def dataReceived(self, data):
        # create bullet locally
        dlist = pickle.loads(data)
        self.gs.gameobjects.append(MidBullet.from_network(self.gs, dlist[0], dlist[1], dlist[2]))


class TankConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        self.gs.tankConnection = self
        self.gs.connections[2] = True

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        pos = dlist[0]
        health = dlist[1]
        self.gs.player2.pos = pos
        self.gs.player2.health = health


class TerrainConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        self.gs.terrainConnection = self
        self.gs.connections[3] = True
        print(self.gs.connections)

    def dataReceived(self, data):
        data = pickle.loads(data)
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