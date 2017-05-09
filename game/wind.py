import pygame

class Wind(pygame.sprite.Sprite):
    def __init__(self, gs, wind):
        self.blue = (126, 174, 252)
        self.wind = wind
        self.gs = gs

    def tick(self):
        pass

    def update(self):
        # pygame.draw.polygon(window, self.blue ,
        #                     ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)))

        pass