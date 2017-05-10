#! /usr/bin/python3

from game.tank_gs import GameSpace

if __name__ == '__main__':
    gs = GameSpace(isServer=False)
    gs.main()
