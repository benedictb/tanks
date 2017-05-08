import pygame

PARALLAX = 2

# This is a messy class for the moving background


class Background(pygame.sprite.Sprite):
    def __init__(self, gs):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.screenHeight = gs.height
        self.screenWidth = gs.width

        # I needed 4 rectangles to make it work, up to three are displayed at once on the screen
        self.image = pygame.image.load('./media/bg.jpg')
        self.rimage = pygame.image.load('./media/bg_reverse.jpg')
        self.rect = self.image.get_rect()
        self.rrect = self.rimage.get_rect()

        self.bimage = pygame.image.load('./media/bg.jpg')
        self.brimage = pygame.image.load('./media/bg_reverse.jpg')
        self.brect = self.image.get_rect()
        self.brrect = self.rimage.get_rect()

        self.size = self.rect.size

        self.rect.left, self.rect.top = (0,0)
        self.rrect.left, self.rrect.top = (0+self.size[0],0)

        self.brect.left, self.rect.top = (0 + 2 * self.size[0] ,0)
        self.brrect.left, self.rrect.top = (0 + 3* self.size[0], 0)

        self.rects = [self.rect, self.rrect, self.brect, self.brrect]

        self.gs = gs

    def tick(self):
        pass

    # The parallax global defines how much it shifts
    def shift_left(self):
        for r in self.rects:
            r.left += PARALLAX

        self.check_bounds()

    def shift_right(self):
        for r in self.rects:
            r.left -= PARALLAX

        self.check_bounds()

    # this function makes sure we haven't run out of background
    def check_bounds(self):
        # examine later
        if self.rect.left >= 0:
            for r in self.rects:
                r.left -= 2 * self.size[0]

        elif self.brrect.left <= self.screenWidth - self.size[0]:
            for r in self.rects:
                r.left += 2 * self.size[0]

    # Update just writes each of the pictures
    def update(self):
        self.gs.screen.blit(self.image, self.rect)
        self.gs.screen.blit(self.rimage, self.rrect)
        self.gs.screen.blit(self.bimage, self.brect)
        self.gs.screen.blit(self.brimage, self.brrect)