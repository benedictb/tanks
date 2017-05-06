import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self,gs, pos):
        super().__init__()
        # self.image = pygame.image.load('media/frame_0_delay-0.06s.png')
        pos[0] -= 75
        pos[1] -= 156

        self.pos = pos
        self.timer = 0
        self.gs = gs

    def tick(self):
        self.timer += 1

    def update(self):
        if self.timer >= 28:
            self.gs.gameobjects.remove(self)
        else:
            img = pygame.image.load('./media/exp/{}.png'.format(int(self.timer / 2)))
            # img = pygame.image.load('./media/ezgif-2-fa08374492-gif-png/0.png'.format(int(self.timer / 2)))
            img = img.convert_alpha()
            self.gs.screen.blit(img,self.pos)
        # if self.timer <= 0:
        #     self.gs.gameObjects.remove(self)
        # else:
        #     self.gs.screen.blit(self.image, self.rect)
