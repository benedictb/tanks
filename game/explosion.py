import pygame
from pygame.mixer import Sound

class Explosion(pygame.sprite.Sprite):
    def __init__(self,gs, pos):
        super().__init__()

        # We want the explosion to happen with its center around the impact, but 
        # it's bottom touching the impact (explode up)
        pos[0] -= 75
        pos[1] -= 156

        self.pos = pos
        self.rect = pos
        self.timer = 0
        self.gs = gs

        # Play the explosion sound.
        self.gs.explode.play()

    # A timer that keeps track of the lifetime of the explosion 
    def tick(self):
        self.timer += 1


    def update(self):
        if self.timer >= 28:
            self.gs.gameobjects.remove(self) # The explosion is over, remove it from the list
        else:
            # Else, load the correct frame of the explosion from the file. I had to break
            # apart the gif into individual png frames, than create an alpha channel based on
            # the background for each one. Worth it because the explosion looks cool
            img = pygame.image.load('./media/exp/{}.png'.format(int(self.timer / 2))) # 1/30th sec / frame
            img = img.convert_alpha()
            self.gs.screen.blit(img,self.pos)
