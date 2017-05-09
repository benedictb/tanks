import pygame

BARWIDTH = 100
BARHEIGHT = 25
MAXHEALTH = 1000

class ErrorBars(pygame.sprite.Sprite):
    def __init__(self, gs):
        super().__init__()
        self.gs = gs

        self.myx = 25
        self.theirx = self.gs.width - (25 + BARWIDTH)
        self.Y = 25

        self.myhealth = self.gs.player1.health
        self.theirhealth = self.gs.player2.health

        self.red = (239, 11, 11)
        ## Got text interface from stackoverflow
        myfont = pygame.font.SysFont("monospace", 15)

        # render text
        self.melabel = myfont.render("YOU", 1, self.red)
        self.themlabel = myfont.render("THEM", 1, self.red)

        self.surface = pygame.Surface((self.gs.width, self.Y + BARHEIGHT))
        mybar = int(max(min(self.myhealth / float(MAXHEALTH) * BARWIDTH, BARWIDTH), 0))
        thembar = int(max(min(self.theirhealth / float(MAXHEALTH) * BARWIDTH, BARWIDTH), 0))
        pygame.draw.rect(self.surface, self.red, (self.myx, self.Y, mybar, BARHEIGHT), 0)
        pygame.draw.rect(self.surface, self.red, (self.theirx, self.Y, thembar, BARHEIGHT), 0)



    def tick(self):
        if self.myhealth != self.gs.player1.health or self.theirhealth != self.gs.player2.health:
            self.surface.fill((0,0,0))
            self.myhealth = self.gs.player1.health
            self.theirhealth = self.gs.player2.health

            # Grabbed this error bar expression from stackoverflow as well
            mybar = int(max(min(self.myhealth / float(MAXHEALTH) * BARWIDTH, BARWIDTH), 0))
            thembar = int(max(min(self.theirhealth / float(MAXHEALTH) * BARWIDTH, BARWIDTH), 0))
            pygame.draw.rect(self.surface, self.red, (self.myx, self.Y, mybar, BARHEIGHT), 0)
            pygame.draw.rect(self.surface, self.red, (self.theirx, self.Y, thembar, BARHEIGHT), 0)


    def update(self):
        self.gs.screen.blit(self.surface, self.surface.get_rect())
        self.gs.screen.blit(self.themlabel, (self.gs.width - 65,10))
        self.gs.screen.blit(self.melabel, (25,10))