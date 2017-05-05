import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.timer = 20

    def tick(self):
        self.timer -= 1

    def update(self):
        if self.timer <= 0:
            self.gs.gameObjects.remove(self)
        else:
            self.gs.screen.blit(self.image, self.rect)
