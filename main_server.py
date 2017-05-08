#! /usr/bin/python3
from tank_gs import GameSpace
from server import *

if __name__ == '__main__':
    FIRSTPORT = 50000
    TANKPORT = 50001
    BULLETPORT = 50002
    TERRAINPORT = 50003

    gs = GameSpace()
    gs.main()

