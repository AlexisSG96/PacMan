import pygame
from imagerect import ImageRect


class GameOver:
    def __init__(self, screen, settings):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.SIZE = self.settings.SIZE
        self.black = (0, 0, 0)

        self.image = None
        self.images = []
        self.game_over = None
        self.game_overs = []
        self.done = False

        self.prep_game_over()

        self.counter = 0

        self.game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
        self.game_over_sound.set_volume(0.3)
        self.channel = self.settings.game_over_channel

    def prep_game_over(self):
        self.images = ['pac_game_over']
        self.image = self.images[0]
        self.game_over = ImageRect(self.screen, self.image, self.SIZE * 50, self.SIZE * 20)
        r = self.game_over.rect
        w, h = r.width, r.height
        self.game_overs.append(pygame.Rect(0, 0, w, h))
        for rect in self.game_overs:
            rect.center = self.screen_rect.center

    def blit_me(self):
        if not self.channel.get_busy() and self.counter == 0:
            self.channel.play(self.game_over_sound)
            self.counter += 1
        if not self.channel.get_busy() and self.counter == 1:
            self.counter += 1
        self.screen.fill(self.black)
        for rect in self.game_overs:
            self.screen.blit(self.game_over.image, rect)
