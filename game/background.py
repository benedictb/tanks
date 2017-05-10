from game.constants import *
import pygame


# This turned out to be too slow to work, but it still worth including.
# This class is a shifting background, which depends on the players movement.


class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.screenHeight = gs.height
        self.screenWidth = gs.width

        # I needed 4 rectangles to make it work, up to three are displayed at once on the screen.
        # bg_full is 4 such rectangles stiched together.

        # The way it is set up is Normal - Mirror - Normal - Mirror. This way it looks like it
        # flows together. 
        self.image = pygame.image.load('./media/bg_full.png')
        self.rect = self.image.get_rect()
        self.gs = gs
        self.width = int(self.rect.size[0] / 4) # width of a "single" background
        self.height = self.rect.size[1]

    def tick(self):
        pass

    # The parallax global defines how much it shifts
    def shift_left(self):
        self.rect.left += PARALLAX
        self.check_bounds()

    def shift_right(self):
        self.rect.left -= PARALLAX
        self.check_bounds()

    # this function makes sure we haven't run out of background
    def check_bounds(self):
        # If too far left, shift over all the way to the other normal rectangle
        if self.rect.left >= 0:
            self.rect.left -= 2 * self.width

        # If too far right, shift back 
        elif self.rect.left + self.width*4 <= self.screenWidth:
            self.rect.left += 2 * self.width

    # Update just blits the correct selection of the pictures
    def update(self):
        self.gs.screen.blit(self.image, (0, 0), ( -self.rect[0],0 ,self.screenWidth, self.screenHeight))
