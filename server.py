from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class FirstConnection(Protocol):
    def __init__(self):
        pass

class BulletConnection(Protocol):
    def __init__(self):
        pass

class TankConnection(Protocol):
    def __init__(self):
        pass

class TerrainConnection(Protocol):
    def __init__(self):
        pass

class FirstFactory(Factory):
    def __init__(self):
        self.myconn = FirstConnection()

    def buildProtocol(self, addr):
        return self.myconn

class BulletFactory(Factory):
    def __init__(self):
        self.myconn = BulletConnection()

    def buildProtocol(self, addr):
        return self.myconn

class TankFactory(Factory):
    def __init__(self):
        self.myconn = TankConnection()

    def buildProtocol(self, addr):
        return self.myconn


class TerrainFactory(Factory):
    def __init__(self):
        self.myconn = TerrainConnection()

    def buildProtocol(self, addr):
        return self.myconn