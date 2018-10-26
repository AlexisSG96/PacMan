"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame.font
from imagerect import ImageRect


class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.SIZE = self.settings.SIZE
        self.stats = stats

        self.BLACK = (0, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.font = pygame.font.SysFont(None, self.SIZE * 2)

        self.score = None
        self.rscore = None
        self.score_img = None
        self.rscore_img = None

        self.level = None
        self.rlevel = None
        self.level_img = None
        self.rlevel_img = None

        self.images = []
        self.image = None
        self.live = None
        self.lives_1 = []
        self.lives_2 = []
        self.lives_3 = []
        self.text = None
        self.rtext = None

        self.prep_player_score_and_level()
        self.prep_player_lives()

    def prep_player_score_and_level(self):
        rounded_score = int(round(self.stats.player_score, -1))
        score_temp = "{:,}".format(rounded_score)
        score_str = 'Score: '
        self.score = self.font.render(score_str, True, self.WHITE, self.BLACK)
        self.score_img = self.font.render(str(score_temp), True, self.YELLOW, self.BLACK)

        rounded_score = int(round(self.stats.level))
        score_temp = "{:,}".format(rounded_score)
        level_str = 'Level: '
        self.level = self.font.render(level_str, True, self.WHITE, self.BLACK)
        self.level_img = self.font.render(str(score_temp), True, self.YELLOW, self.BLACK)

        self.rscore = self.score.get_rect()
        self.rscore.left = self.screen_rect.left + (self.screen_rect.right/16)
        self.rscore.bottom = self.screen_rect.bottom - self.SIZE
        self.rscore_img = self.score_img.get_rect()
        self.rscore_img.left = self.rscore.right
        self.rscore_img.bottom = self.screen_rect.bottom - self.SIZE

        self.rlevel = self.level.get_rect()
        self.rlevel.x = self.screen_rect.width/2 - self.SIZE * 12
        self.rlevel.bottom = self.screen_rect.bottom - self.SIZE
        self.rlevel_img = self.level_img.get_rect()
        self.rlevel_img.left = self.rlevel.right
        self.rlevel_img.bottom = self.screen_rect.bottom - self.SIZE

    def prep_player_lives(self):
        score_str = 'Lives Left: '
        self.text = self.font.render(score_str, True, self.WHITE, self.BLACK)
        self.rtext = self.text.get_rect()
        self.rtext.bottom = self.screen_rect.bottom - self.SIZE
        self.rtext.x = self.screen_rect.width/2 - self.SIZE * 4

        self.images = ['pacman2']
        self.image = self.images[0]
        self.live = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.live.rect
        w, h = r.width, r.height
        self.lives_1.append(pygame.Rect(0, 0, w, h))
        self.lives_2.append(pygame.Rect(0, 0, w, h))
        self.lives_3.append(pygame.Rect(0, 0, w, h))
        for rect in self.lives_1:
            rect.x = self.screen_rect.width/2 + self.SIZE * 3
            rect.y = self.screen_rect.bottom - self.SIZE * 2.5
        for rect in self.lives_2:
            rect.x = self.screen_rect.width/2 + self.SIZE * 5
            rect.y = self.screen_rect.bottom - self.SIZE * 2.5
        for rect in self.lives_3:
            rect.x = self.screen_rect.width/2 + self.SIZE * 7
            rect.y = self.screen_rect.bottom - self.SIZE * 2.5

    def update_score(self):
        print(str(self.stats.player_score))

    def show_score(self):
        self.screen.blit(self.score, self.rscore)
        self.screen.blit(self.score_img, self.rscore_img)
        self.screen.blit(self.level, self.rlevel)
        self.screen.blit(self.level_img, self.rlevel_img)
        self.screen.blit(self.text, self.rtext)
        if self.stats.lives_left == 3:
            for rect in self.lives_1:
                self.screen.blit(self.live.image, rect)
            for rect in self.lives_2:
                self.screen.blit(self.live.image, rect)
            for rect in self.lives_3:
                self.screen.blit(self.live.image, rect)
        if self.stats.lives_left == 2:
            for rect in self.lives_1:
                self.screen.blit(self.live.image, rect)
            for rect in self.lives_2:
                self.screen.blit(self.live.image, rect)
        if self.stats.lives_left == 1:
            for rect in self.lives_1:
                self.screen.blit(self.live.image, rect)
