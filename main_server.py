#! /usr/bin/python3
from game.tank_gs import GameSpace
from net.server import *

if __name__ == '__main__':

    gs = GameSpace(isServer=True)
    # gs.server_start()
    gs.main()

