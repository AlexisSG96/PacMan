"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from imagerect import ImageRect


class Player:
    def __init__(self, screen, settings, stats, sb, inky, blinky, clyde, pinky):
        self.screen = screen
        self.settings = settings
        self.stats = stats
        self.sb = sb
        self.inky = inky
        self.blinky = blinky
        self.clyde = clyde
        self.pinky = pinky
        self.SIZE = self.settings.SIZE

        self.last_frame = 0
        self.dead_frame = 0
        self.image_index = None
        self.image = None
        self.left_images = []
        self.right_images = []
        self.up_images = []
        self.down_images = []
        self.dead_images = []
        self.player = None
        self.players = []
        self.dead_player = None
        self.dead_players = []
        self.initialize_images()

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.x_direction = self.settings.player_x
        self.y_direction = self.settings.player_y

        for rect in self.players:
            self.x = float(rect.x)
            self.y = float(rect.y)

        self.dead = False

        # Sound
        self.player_death_sound = pygame.mixer.Sound('sounds/pacman_death.wav')
        self.player_death_sound.set_volume(0.5)
        self.player_chomp = pygame.mixer.Sound('sounds/pacman_chomp.wav')
        self.player_chomp.set_volume(0.3)
        self.player_eat = pygame.mixer.Sound('sounds/pacman_eatghost.wav')
        self.player_eat.set_volume(0.3)
        self.fruit = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')
        self.fruit.set_volume(0.3)
        self.channel = self.settings.player_channel

    def initialize_images(self):
        self.left_images = ['pacman0',
                            'pacman1']
        self.right_images = ['pacman2',
                             'pacman3']
        self.up_images = ['pacman4',
                          'pacman5']
        self.down_images = ['pacman6',
                            'pacman7']
        self.dead_images = ['pacman',
                            'pacman4',
                            'pacman5']
        self.image_index = 0
        self.image = self.left_images[self.image_index]
        self.player = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.player.rect
        w, h = r.width, r.height
        self.players.append(pygame.Rect(21 * self.SIZE, 29 * self.SIZE, w, h))

        self.image = self.left_images[self.image_index]
        self.dead_player = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.player.rect
        w, h = r.width, r.height
        self.players.append(pygame.Rect(21 * self.SIZE, 29 * self.SIZE, w, h))

    def update(self, maze):
        time = pygame.time.get_ticks()
        if not self.dead:
            for rect in self.players:
                if self.check_box_position(rect):
                    self.y -= 2
                    rect.y = self.y
                self.check_boundaries(rect)
                self.check_ghost_collision(rect)
                self.check_pick_up(rect, maze)
                if self.moving_right:
                    self.check_last_frame(time, self.right_images)
                    self.x += self.x_direction
                    rect.x = self.x
                    for rect2 in maze.bricks:
                        if rect.colliderect(rect2):
                            self.x = self.x - 2
                            rect.x = self.x
                if self.moving_down:
                    self.check_last_frame(time, self.down_images)
                    self.y += self.y_direction
                    rect.y = self.y
                    for rect2 in maze.bricks:
                        if rect.colliderect(rect2):
                            self.y = self.y - 2
                            rect.y = self.y
                if self.moving_left:
                    self.check_last_frame(time, self.left_images)
                    self.x -= self.x_direction
                    rect.x = self.x
                    for rect2 in maze.bricks:
                        if rect.colliderect(rect2):
                            self.x = self.x + 2
                            rect.x = self.x
                if self.moving_up:
                    self.check_last_frame(time, self.up_images)
                    self.y -= self.y_direction
                    rect.y = self.y
                    for rect2 in maze.bricks:
                        if rect.colliderect(rect2):
                            self.y = self.y + 2
                            rect.y = self.y
        elif self.dead:
            time_test = pygame.time.get_ticks()
            self.inky.stop = True
            self.blinky.stop = True
            self.clyde.stop = True
            self.pinky.stop = True
            if abs(time_test - self.last_frame) > 550:
                if self.dead_frame < len(self.dead_images):
                    self.image = self.dead_images[self.dead_frame]
                    self.last_frame = time_test
                    self.player = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
                    self.dead_frame += 1
                else:
                    for rect in self.players:
                        self.x, self.y = 21 * self.SIZE, 29 * self.SIZE
                        rect.x, rect.y = self.x, self.y
                    self.inky.reset_ghost()
                    self.blinky.reset_ghost()
                    self.clyde.reset_ghost()
                    self.pinky.reset_ghost()
                    self.stats.lives_left -= 1
                    self.dead = False
                    self.dead_frame = 0
                    self.image_index = 0
                    self.image = self.left_images[self.image_index]
                    self.last_frame = time_test
                    self.player = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)

    def check_last_frame(self, time_test, images):
        if abs(self.last_frame - time_test) > 100:
            self.last_frame = time_test
            self.image_index = (self.image_index + 1) % len(images)
            self.image = images[self.image_index]
            self.player = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)

    def check_boundaries(self, rect):
        if self.x < 0:
            self.x = self.settings.screen_width - self.SIZE
            rect.x = self.x
        if self.x > self.settings.screen_width:
            self.x = 0
            rect.x = self.x

    def check_box_position(self, rect):
        if rect.collidepoint((25*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((26*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((27*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((28*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((24*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((23*self.SIZE, 21*self.SIZE)):
            return True
        if rect.collidepoint((22*self.SIZE, 21*self.SIZE)):
            return True

    def check_ghost_collision(self, rect):
        for rghost in self.inky.ghosts:
            if rect.colliderect(rghost) and not self.inky.power_pill and not self.pinky.dead:
                pygame.mixer.stop()
                self.channel.queue(self.player_death_sound)
                self.dead = True
                self.image_index = 0
                self.image = self.dead_images[self.image_index]
                self.last_frame = pygame.time.get_ticks()
            if rect.colliderect(rghost) and self.inky.power_pill and not self.inky.dead:
                self.stats.player_score += 100
                self.sb.prep_player_score_and_level()
                self.channel.play(self.player_eat)
                self.inky.dead = True
        for rghost in self.blinky.ghosts:
            if rect.colliderect(rghost) and not self.blinky.power_pill and not self.pinky.dead:
                pygame.mixer.stop()
                self.channel.queue(self.player_death_sound)
                self.dead = True
                self.image_index = 0
                self.image = self.dead_images[self.image_index]
                self.last_frame = pygame.time.get_ticks()
            if rect.colliderect(rghost) and self.blinky.power_pill and not self.blinky.dead:
                self.stats.player_score += 100
                self.sb.prep_player_score_and_level()
                self.channel.play(self.player_eat)
                self.blinky.dead = True
        for rghost in self.clyde.ghosts:
            if rect.colliderect(rghost) and not self.clyde.power_pill and not self.pinky.dead:
                pygame.mixer.stop()
                self.channel.queue(self.player_death_sound)
                self.dead = True
                self.image_index = 0
                self.image = self.dead_images[self.image_index]
                self.last_frame = pygame.time.get_ticks()
            if rect.colliderect(rghost) and self.clyde.power_pill and not self.clyde.dead:
                self.stats.player_score += 100
                self.sb.prep_player_score_and_level()
                self.channel.play(self.player_eat)
                self.clyde.dead = True
        for rghost in self.pinky.ghosts:
            if rect.colliderect(rghost) and not self.pinky.power_pill and not self.pinky.dead:
                pygame.mixer.stop()
                self.channel.queue(self.player_death_sound)
                self.dead = True
                self.image_index = 0
                self.image = self.dead_images[self.image_index]
                self.last_frame = pygame.time.get_ticks()
            if rect.colliderect(rghost) and self.pinky.power_pill and not self.pinky.dead:
                self.stats.player_score += 100
                self.sb.prep_player_score_and_level()
                self.channel.play(self.player_eat)
                self.pinky.dead = True

    @staticmethod
    def check_high_score(stats):
        """Check if high score needs to be updated."""
        if stats.player_score > stats.high_score:
            stats.high_score = stats.player_score

    def check_pick_up(self, rect, maze):
        counter = 0
        for rpoint in maze.points:
            if rect.colliderect(rpoint):
                if not self.channel.get_busy():
                    self.channel.play(self.player_chomp)
                self.stats.player_score += 50
                self.check_high_score(self.stats)
                self.sb.prep_player_score_and_level()
                maze.points.pop(counter)
            counter += 1
            if len(maze.points) == 0:
                self.reset_player()
                self.inky.reset_ghost()
                self.blinky.reset_ghost()
                self.clyde.reset_ghost()
                self.pinky.reset_ghost()
                self.stats.level += 1
                self.settings.increase_speed()
                maze.build()
        counter = 0
        for rcherry in maze.cherries:
            if rect.colliderect(rcherry):
                if self.channel.get_busy():
                    pygame.mixer.pause()
                    self.channel.play(self.fruit)
                    pygame.mixer.unpause()
                self.stats.player_score += 150
                self.check_high_score(self.stats)
                self.sb.prep_player_score_and_level()
                maze.cherries.pop(counter)
            counter += 1
        counter = 0
        for rpower in maze.powerPills:
            if rect.colliderect(rpower):
                maze.powerPills.pop(counter)
                self.inky.power_pill = True
                self.inky.vulnerable_frame = pygame.time.get_ticks()
                self.blinky.power_pill = True
                self.blinky.vulnerable_frame = pygame.time.get_ticks()
                self.clyde.power_pill = True
                self.clyde.vulnerable_frame = pygame.time.get_ticks()
                self.pinky.power_pill = True
                self.pinky.vulnerable_frame = pygame.time.get_ticks()
            counter += 1

    def reset_player(self):
        for rect in self.players:
            self.x, self.y = 21 * self.SIZE, 29 * self.SIZE
            rect.x, rect.y = self.x, self.y

    def blitme(self):
        for rect in self.players:
            self.screen.blit(self.player.image, rect)
