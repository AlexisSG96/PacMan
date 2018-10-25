import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13

    def __init__(self, screen, mazefile, brickfile, blueportalfile, orangeportalfile, shieldfile, pointfile, powerfile,
                 cherryfile):
        self.screen = screen
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.bricks = []
        self.shields = []
        self.orangePortals = []
        self.bluePortals = []
        self.points = []
        self.powerPills = []
        self.cherries = []
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.shield = ImageRect(screen, shieldfile, sz, sz)
        # Q blue E Orange
        self.bluePortal = ImageRect(screen, blueportalfile, 5 * sz, 15 * sz)
        self.orangePortal = ImageRect(screen, orangeportalfile, 15 * sz, 5 * sz)
        self.point = ImageRect(screen, pointfile, int(0.5*sz), int(0.5*sz))
        self.powerPill = ImageRect(screen, powerfile, int(sz), int(sz))
        self.cherry = ImageRect(screen, cherryfile, sz, sz)
        self.delatx = self.delaty = Maze.BRICK_SIZE

        self.build()

    def __str__(self): return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        rshield = self.shield.rect
        rblue = self.bluePortal.rect
        rorange = self.orangePortal.rect
        rpoint = self.point.rect
        rpower = self.powerPill.rect
        rcherry = self.cherry.rect
        w, h = r.width, r.height
        wshield, hshield = rshield.width, rshield.height
        wblue, hblue = rblue.width, rblue.height
        worange, horange = rorange.width, rorange.height
        wpoint, hpoint = rpoint.width, rpoint.height
        wpower, hpower = rpower.width, rpower.height
        wcherry, hcherry = rcherry.width, rcherry.height
        dx, dy = self.delatx, self.delaty

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'X':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                elif col == 'S':
                    self.shields.append(pygame.Rect(ncol * dx, nrow * dy, wshield, hshield))
                    # print(self.shields[0].x)
                    # print(self.shields[0].y)
                elif col == 'Q':
                    self.bluePortals.append(pygame.Rect(ncol * dx, nrow * dy, wblue, hblue))
                elif col == 'E':
                    self.orangePortals.append(pygame.Rect(ncol * dx, nrow * dy, worange, horange))
                elif col == 'P':
                    self.points.append(pygame.Rect(ncol * dx, nrow * dy, wpoint, hpoint))
                elif col == 'O':
                    self.powerPills.append(pygame.Rect(ncol * dx, nrow * dy, wpower, hpower))
                elif col == 'C':
                    self.cherries.append(pygame.Rect(ncol * dx, nrow * dy, wcherry, hcherry))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.bluePortals:
            self.screen.blit(self.bluePortal.image, rect)
        for rect in self.orangePortals:
            self.screen.blit(self.orangePortal.image, rect)
        for rect in self.points:
            self.screen.blit(self.point.image, rect)
        for rect in self.powerPills:
            self.screen.blit(self.powerPill.image, rect)
        for rect in self.shields:
            self.screen.blit(self.shield.image, rect)
        for rect in self.cherries:
            self.screen.blit(self.cherry.image, rect)
