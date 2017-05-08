#! /usr/bin/python3
from tank_gs import GameSpace
from server import *

if __name__ == '__main__':

    gs = GameSpace(isServer=True)
    # gs.server_start()
    gs.main()

