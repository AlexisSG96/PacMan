import pygame
# from expandfile import ExpandFile
from button import Button
from settings import Settings
from eventloop import EventLoop
from game_stats import GameStats
from scoreboard import Scoreboard
from ghost import Ghost
from player import Player
from maze import Maze


class Game:
    BLACK = (0, 0, 0)

    def __init__(self):
        pygame.init()
        self.settings = ai_settings = Settings()
        self.screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
        pygame.display.set_caption('Pacman Portal')
        self.play_button = Button(ai_settings=ai_settings, screen=self.screen, msg='Play Game')

        self.stats = GameStats(settings=ai_settings)
        self.sb = Scoreboard(settings=ai_settings, screen=self.screen, stats=self.stats)

        # self.expandfile = ExpandFile('images/pacman_maze.txt', expandby=4)
        self.maze = Maze(self.screen, mazefile='images/pacman_maze.txt', brickfile='brick', blueportalfile='bluePortal',
                         orangeportalfile='orangePortal', shieldfile='shield', pointfile='point', powerfile='power',
                         cherryfile='cherry')

        self.blueGhost = Ghost(screen=self.screen, settings=ai_settings, ghost_type=1)
        self.redGhost = Ghost(screen=self.screen, settings=ai_settings, ghost_type=2)
        self.orangeGhost = Ghost(screen=self.screen, settings=ai_settings, ghost_type=3)
        self.pinkGhost = Ghost(screen=self.screen, settings=ai_settings, ghost_type=4)
        self.player = Player(screen=self.screen, settings=ai_settings, stats=self.stats, sb=self.sb,
                             inky=self.blueGhost, blinky=self.redGhost,
                             clyde=self.orangeGhost, pinky=self.pinkGhost)

    def __str__(self): return 'Game(Pacman Portal), maze='+str(self.maze)+')'

    def play(self):
        eloop = EventLoop(finished=True, settings=self.settings)

        while eloop.finished:
            eloop.check_play_button(self.stats, self.sb, self.play_button)
            if not self.stats.game_active:
                self.play_button.draw_button()
            pygame.display.flip()
        while self.settings.begin.get_busy():
            self.settings.begin.get_busy()
        while not eloop.finished:
            eloop.check_events(self.stats, self.player)
            self.update_screen()
            self.player_ghost_update()

    def update_screen(self):
        self.screen.fill(self.BLACK)
        self.maze.blitme()
        self.player.blitme()
        self.blueGhost.blitme()
        self.redGhost.blitme()
        self.orangeGhost.blitme()
        self.pinkGhost.blitme()
        self.sb.show_score()
        pygame.display.flip()

    def player_ghost_update(self):
        self.player.update(self.maze)
        self.blueGhost.update(self.maze)
        self.redGhost.update(self.maze)
        self.orangeGhost.update(self.maze)
        self.pinkGhost.update(self.maze)


game = Game()
game.play()

# 213-294-3177
# Dr. McCarthy
