#! /usr/bin/python3

from tank_gs import GameSpace

if __name__ == '__main__':
    gs = GameSpace(isServer=False)
    gs.client_start()
    gs.main()
