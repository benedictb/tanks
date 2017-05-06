#! /usr/bin/python3
# Thomas Franceschi
# Ben Becker


from terrain import *
from tank import *
from mid_bullet import *
from pygame.locals import *

class GameSpace():
    def main(self):
        # init gamespace
        pygame.init()
        self.size = self.width, self.height = 1000, 600
        self.black = 0, 0, 0
        self.screen = pygame.display.set_mode(self.size)

        # init gameobjects
        self.clock = pygame.time.Clock()
        self.gameobjects = []
        self.gameobjects.append(Terrain(self))
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
                    if keys[K_d]:
                        self.gameobjects[1].pos[0] += 4
                if event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pressed()
                    if mouse[0]:
                        print("fire")
                        pos = self.gameobjects[1].get_pos()
                        self.gameobjects.append(MidBullet(self, pos, 0, 25, 0))
                        # fire cannon

            #blank out screen
            self.screen.fill(self.black)

            # call tick on each object
            for gameobject in self.gameobjects:
                gameobject.tick()

            # update screen
            for gameobject in self.gameobjects:
                gameobject.update()
                # self.screen.blit(gameobject.image, gameobject.rect)
            pygame.display.flip()

if __name__ == '__main__':
    gs = GameSpace()
    gs.main()
