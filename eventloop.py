import pygame
import sys


class EventLoop:
    def __init__(self, finished, settings):
        self.finished = finished
        self.settings = settings
        self.begin = pygame.mixer.Sound('sounds/pacman_beginning.wav')
        self.begin.set_volume(0.2)
        self.channel = self.settings.begin

    def __str__(self):
        return 'eventloop, filename=' + str(self.finished) + ')'

    @staticmethod
    def check_events(stats, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats.save_high_score()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.moving_right = True
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.moving_down = True
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.moving_left = True
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.moving_up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.moving_right = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.moving_down = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.moving_left = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.moving_up = False

    def check_play_button(self, stats, sb, play_button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stats.save_high_score()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
                if button_clicked and not stats.game_active:
                    pygame.mouse.set_visible(False)
                    stats.reset_stats()
                    stats.game_active = True
                    self.finished = False
                    sb.prep_player_score()
                    pygame.mixer.stop()
                    self.channel.play(self.begin)
                    while self.channel.get_busy():
                        self.channel.get_busy()
