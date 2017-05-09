import pickle

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol

from game.mid_bullet import MidBullet


class FirstConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # save connection variable for later use
        self.gs.firstConnection = self
        data = [0] * 4

        # store player data + wind in list to be sent to client to create game objects
        data[0] = self.gs.player1.pos
        data[1] = self.gs.player2.pos
        data[2] = self.gs.heights
        data[3] = self.gs.wind

        # pickle data for ease of transmitting
        dstring = pickle.dumps(data)

        # write data to client
        self.transport.write(dstring)

        # update connection status in list
        self.gs.connections[0] = True


class BulletConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # save connection variable for later use
        self.gs.bulletConnection = self

        # update connection status in list
        self.gs.connections[1] = True

    def dataReceived(self, data):
        # create bullet locally
        dlist = pickle.loads(data)
        # create local bullet object using x, y, and velocity data and add to gameobject list
        self.gs.gameobjects.append(MidBullet.from_network(self.gs, dlist[0], dlist[1], dlist[2]))


class TankConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # save connection variable for later use
        self.gs.tankConnection = self

        # update connection status in list
        self.gs.connections[2] = True

    def dataReceived(self, data):
        dlist = pickle.loads(data)
        pos = dlist[0]
        health = dlist[1]

        # update enemy tank object with client position and health
        self.gs.player2.pos = pos
        self.gs.player2.health = health


class TerrainConnection(Protocol):
    def __init__(self, gs):
        self.gs = gs

    def connectionMade(self):
        # save connection variable for later use
        self.gs.terrainConnection = self

        # update connection status in list
        self.gs.connections[3] = True

    def dataReceived(self, data):
        data = pickle.loads(data)

        # update destroyed terrain blocks received from x, y coordinates of missile impact
        self.gs.remove_blocks(data[0], data[1])


class FirstFactory(Factory):
    def __init__(self, gs):
        self.myconn = FirstConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class BulletFactory(Factory):
    def __init__(self, gs):
        self.myconn = BulletConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class TankFactory(Factory):
    def __init__(self, gs):
        self.myconn = TankConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn


class TerrainFactory(Factory):
    def __init__(self, gs):
        self.myconn = TerrainConnection(gs)

    def buildProtocol(self, addr):
        return self.myconn