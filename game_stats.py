"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.lives_left = 0
        self.high_score = 0
        self.player_score = 0
        self.level = 0
        self.reset_stats()
        self.get_high_score()
        self.game_active = False

    def reset_stats(self):
        self.lives_left = self.settings.lives_limit
        self.player_score = 0
        self.level = 1

    def get_high_score(self):
        with open('high_score.txt', 'r') as file:
            self.high_score = int(file.readline())

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))
