import pygame
from imagerect import ImageRect


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13

    def __init__(self, screen, mazefile, brickfile, blueportalfile, orangeportalfile, shieldfile, pointfile, powerfile):
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
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.shield = ImageRect(screen, shieldfile, sz, sz)
        # Q blue E Orange
        self.bluePortal = ImageRect(screen, blueportalfile, 5 * sz, 15 * sz)
        self.orangePortal = ImageRect(screen, orangeportalfile, 15 * sz, 5 * sz)
        self.point = ImageRect(screen, pointfile, int(0.5*sz), int(0.5*sz))
        self.powerPill = ImageRect(screen, powerfile, int(sz), int(sz))
        self.delatx = self.delaty = Maze.BRICK_SIZE

        self.build()
        self.shield_on = True
        self.last_time_tick = pygame.time.get_ticks()
        self.temp_time = 0

    def __str__(self): return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        rshield = self.shield.rect
        rblue = self.bluePortal.rect
        rorange = self.orangePortal.rect
        rpoint = self.point.rect
        rpower = self.powerPill.rect
        w, h = r.width, r.height
        wshield, hshield = rshield.width, rshield.height
        wblue, hblue = rblue.width, rblue.height
        worange, horange = rorange.width, rorange.height
        wpoint, hpoint = rpoint.width, rpoint.height
        wpower, hpower = rpower.width, rpower.height
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

    def restore_shield(self):
        rshield = self.shield.rect
        wshield, hshield = rshield.width, rshield.height
        dx, dy = self.delatx, self.delaty
        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row[ncol]
                if col == 'S':
                    self.shields.append(pygame.Rect(ncol * dx, nrow * dy, wshield, hshield))

    # self.brick.blit(rect)
    def blitme(self):
        time = pygame.time.get_ticks()
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
        if time - self.last_time_tick < 5000:
            for rect in self.shields:
                self.screen.blit(self.shield.image, rect)
        else:
            self.temp_time += pygame.time.get_ticks()
            self.shields.clear()
            self.shield_on = False

        if self.temp_time > 6000 and self.shield_on:
            self.temp_time = 0
            self.restore_shield()
            self.last_time_tick = time


