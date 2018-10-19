"""
Name: Alexis Steven Garcia
Project: PacMan Portal
Date: October 18, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame.font


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

        self.prep_player_score()

    def prep_player_score(self):
        rounded_score = int(round(self.stats.player_score, -1))
        score_temp = "{:,}".format(rounded_score)
        score_str = 'Score: '
        self.score = self.font.render(score_str, True, self.WHITE, self.BLACK)
        self.score_img = self.font.render(str(score_temp), True, self.YELLOW, self.BLACK)

        self.rscore = self.score.get_rect()
        self.rscore.left = self.screen_rect.left + (self.screen_rect.right/16)
        self.rscore.bottom = self.screen_rect.bottom - self.SIZE
        self.rscore_img = self.score_img.get_rect()
        self.rscore_img.left = self.rscore.right
        self.rscore_img.bottom = self.screen_rect.bottom - self.SIZE + 2

    def update_score(self):
        print(str(self.stats.player_score))

    def show_score(self):
        self.screen.blit(self.score, self.rscore)
        self.screen.blit(self.score_img, self.rscore_img)
