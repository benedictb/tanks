import pygame


# Not sure if this is a sprite..
class Terrain(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs
        self.generate_terrain()

    def tick(self):
        pass

    def update(self):
        self.gs.screen.blit(self.image, self.rect)

    def generate_terrain(self):
        pass
