#! /usr/bin/python3
# Thomas Franceschi
# Ben Becker


from terrain import *
from tank import *
from mid_bullet import *
from pygame.locals import *

class GameSpace():

    def get_height(self, x):
        x =  x % self.width
        col = [1 for i in self.gmap[x,:] if i]
        return sum(col)

    def main(self):
        # init gamespace
        pygame.init()
        self.size = self.width, self.height = 1750, 600
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

        # init gameobjects
        self.clock = pygame.time.Clock()
        self.bg = Background(self)
        self.terrain = Terrain(gs)
        self.gameobjects = []
        self.gameobjects.append(self.terrain)
        self.gameobjects.append(MidTank(self, ([0, 300])))

        pygame.key.set_repeat(1, 30)

        # start game loop
        while 1:
            self.clock.tick(60)
            # read user input
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 0
                if event.type == KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[K_w]:
                        print("jump!")
                        self.gameobjects[1].pos[1] -= 50
                    if keys[K_a]:
                        self.gameobjects[1].pos[0] -= 4
                        self.bg.shift_left()
                    if keys[K_d]:
                        self.gameobjects[1].pos[0] += 4
                        self.bg.shift_right()
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        print("fire")
                        pos = self.gameobjects[1].get_pos()
                        # pos[0]+=5; pos[1]+=5
                        self.gameobjects.append(MidBullet(self, pos, 0, 10, 0))
                        # fire cannon

            #blank out screen
            self.screen.fill(self.black)

            # call tick on each object
            for gameobject in self.gameobjects:
                gameobject.tick()

            # update screen
            self.bg.update()
            for gameobject in self.gameobjects:
                gameobject.update()

            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
