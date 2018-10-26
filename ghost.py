"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from imagerect import ImageRect


class Ghost:
    def __init__(self, screen, settings, ghost_type):
        self.screen = screen
        self.settings = settings
        self.ghost_type = ghost_type
        self.out = settings.get_out

        self.SIZE = settings.SIZE
        self.image = None
        self.images = None
        self.image_index = None
        self.blue_frames = None
        self.blue_index = None
        self.death_frames = None
        self.death_index = None
        self.vulnerable_index = None
        self.rect = None
        self.ghost = None
        self.ghosts = []
        self.eye = None
        self.eyes = []
        self.escapee = None
        self.escapees = []
        self.last_frame = 0
        self.vulnerable_frame = 0
        self.switch_frame = 0
        self.initialize_images()

        self.x_direction = settings.ghost_x
        self.y_direction = settings.ghost_y
        self.collide_x = False

        for rect in self.ghosts:
            self.x = float(rect.x)
            self.y = float(rect.y)

        self.outside = False
        self.vuln_flag = False
        self.dead = False
        self.stop = False
        self.wait = False
        self.power_pill = False
        self.counter = 0

        self.walk = pygame.mixer.Sound('sounds/pacman_siren.wav')
        self.walk.set_volume(0.3)
        self.run = pygame.mixer.Sound('sounds/pacman_large_pellet.wav')
        self.run.set_volume(0.3)
        self.run_channel = self.settings.ghost_run_channel
        self.walk_channel = self.settings.ghost_walk_channel

    def initialize_images(self):
        if self.ghost_type == 1:
            self.images = ['Inky_0',
                           'Inky_2',
                           'Inky_1',
                           'Inky_3']
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
            r = self.ghost.rect
            w, h = r.width, r.height
            self.ghosts.append(pygame.Rect(18*self.SIZE, 22*self.SIZE, w, h))
        elif self.ghost_type == 2:
            self.images = ['Blinky_0',
                           'Blinky_2',
                           'Blinky_1',
                           'Blinky_3']
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
            r = self.ghost.rect
            w, h = r.width, r.height
            self.ghosts.append(pygame.Rect(27*self.SIZE, 22*self.SIZE, w, h))
        elif self.ghost_type == 3:
            self.images = ['Clyde_0',
                           'Clyde_2',
                           'Clyde_1',
                           'Clyde_3']
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
            r = self.ghost.rect
            w, h = r.width, r.height
            self.ghosts.append(pygame.Rect(18*self.SIZE, 25*self.SIZE, w, h))
        else:
            self.images = ['Pinky_0',
                           'Pinky_2',
                           'Pinky_1',
                           'Pinky_3']
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
            r = self.ghost.rect
            w, h = r.width, r.height
            self.ghosts.append(pygame.Rect(27*self.SIZE, 25*self.SIZE, w, h))
        self.blue_frames = ['Vulnerable_Ghost',
                            'Vulnerable_Ghost_1']
        self.vulnerable_index = 0
        self.image = self.blue_frames[self.vulnerable_index]
        self.escapee = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.escapee.rect
        w, h = r.width, r.height
        self.escapees.append(pygame.Rect(0, 0, w, h))
        self.death_frames = ['Eyes_Up',
                             'Eyes_Right',
                             'Eyes_Down',
                             'Eyes_Left']
        self.death_index = 0
        self.image = self.images[self.death_index]
        self.eye = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.eye.rect
        w, h = r.width, r.height
        self.eyes.append(pygame.Rect(0, 0, w, h))
        self.last_frame = pygame.time.get_ticks()

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False

    def begin_death(self):
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = pygame.time.get_ticks()
        # self.channel.play(self.death_sound)

    def update(self, maze):
        time_test = pygame.time.get_ticks()
        if not self.dead:
            if abs(self.last_frame - time_test) > 1000:
                self.last_frame = time_test
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]
                self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        if self.dead:
            if abs(self.last_frame - time_test) > 1000:
                self.last_frame = time_test
                self.death_index = (self.death_index + 1) % len(self.death_frames)
                self.image = self.death_frames[self.death_index]
                self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
                self.counter += 1
            if self.counter == 2:
                self.power_pill = False
            self.go_home()
        if not self.dead and not self.stop and not self.power_pill:
            if not self.walk_channel.get_busy():
                self.walk_channel.play(self.walk)
            if self.ghost_type == 1:
                self.inky_route(maze, time_test)
            if self.ghost_type == 2:
                self.blinky_route(maze, time_test)
            if self.ghost_type == 3:
                self.clyde_route(maze, time_test)
            if self.ghost_type == 4:
                self.pinky_route(maze, time_test)
        if not self.dead and not self.stop and self.power_pill:
            if not self.run_channel.get_busy():
                self.run_channel.play(self.run)
            if not self.vuln_flag:
                self.vuln_flag = True
                self.image = self.blue_frames[0]
                self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
            if abs(self.vulnerable_frame - time_test) > 5000:
                if abs(self.switch_frame - time_test) > 1000:
                    self.switch_frame = time_test
                    self.vulnerable_index = (self.vulnerable_index + 1) % len(self.blue_frames)
                    self.image = self.blue_frames[self.vulnerable_index]
                    self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
                    self.counter += 1
                if self.counter == 6:
                    self.power_pill = False
                    self.vuln_flag = False
                    self.vulnerable_index = 0
                    self.counter = 0
            if self.ghost_type == 1:
                self.inky_route(maze, time_test)
            if self.ghost_type == 2:
                self.blinky_route(maze, time_test)
            if self.ghost_type == 3:
                self.clyde_route(maze, time_test)
            if self.ghost_type == 4:
                self.pinky_route(maze, time_test)
        # if not self.dead and self.stop and not self.power_pill:
        if self.stop:
            self.power_pill = False
            self.dead = False
            for rect in self.ghosts:
                if self.wait:
                    if self.ghost_type == 1:
                        self.x = 18*self.SIZE
                        self.y = 22*self.SIZE
                        rect.x = self.x
                        rect.y = self.y
                    if self.ghost_type == 2:
                        self.x = 27*self.SIZE
                        self.y = 22*self.SIZE
                        rect.x = self.x
                        rect.y = self.y
                    if self.ghost_type == 3:
                        self.x = 18*self.SIZE
                        self.y = 25*self.SIZE
                        rect.x = self.x
                        rect.y = self.y
                    if self.ghost_type == 4:
                        self.x = 27*self.SIZE
                        self.y = 25*self.SIZE
                        rect.x = self.x
                        rect.y = self.y
                    self.wait = False

    def inky_route(self, maze, time):
        if not self.collide_x:
            self.x += 1 * self.x_direction
            for rect in self.ghosts:
                rect.x = self.x
                if self.check_box_position(rect) and self.time_check():
                    self.y -= self.out
                    rect.y = self.y
                else:
                    for rbrick in maze.bricks:
                        if rect.colliderect(rbrick):
                            self.collide_x = True
                            if self.x_direction > 0:
                                self.x = self.x - 3
                                rect.x = self.x
                            elif self.x_direction < 0:
                                self.x = self.x + 3
                                rect.x = self.x
                            if time % 2 == 0:
                                self.x_direction *= -1
        if self.collide_x:
            self.y += 1 * self.y_direction
            for rect in self.ghosts:
                rect.y = self.y
                for rbrick in maze.bricks:
                    if rect.colliderect(rbrick):
                        if self.y_direction > 0:
                            self.y = self.y - 3
                            rect.y = self.y
                        elif self.y_direction < 0:
                            self.y = self.y + 3
                            rect.y = self.y
                        self.collide_x = False
                        if time % 2 == 0:
                            self.y_direction *= -1

    def blinky_route(self, maze, time):
        if not self.collide_x:
            self.x += 1 * self.x_direction
            for rect in self.ghosts:
                rect.x = self.x
                if self.check_box_position(rect) and self.time_check():
                    self.y -= self.out
                    rect.y = self.y
                else:
                    for rbrick in maze.bricks:
                        if rect.colliderect(rbrick):
                            self.collide_x = True
                            if self.x_direction > 0:
                                self.x = self.x - 3
                                rect.x = self.x
                            elif self.x_direction < 0:
                                self.x = self.x + 3
                                rect.x = self.x
                            if time % 2 == 0:
                                self.x_direction *= -1
        if self.collide_x:
            self.y += 1 * self.y_direction
            for rect in self.ghosts:
                rect.y = self.y
                for rbrick in maze.bricks:
                    if rect.colliderect(rbrick):
                        if self.y_direction > 0:
                            self.y = self.y - 3
                            rect.y = self.y
                        elif self.y_direction < 0:
                            self.y = self.y + 3
                            rect.y = self.y
                        self.collide_x = False
                        if time % 2 == 0:
                            self.y_direction *= -1

    def clyde_route(self, maze, time):
        if not self.collide_x:
            self.x += 1 * self.x_direction
            for rect in self.ghosts:
                rect.x = self.x
                if self.check_box_position(rect) and self.time_check():
                    self.y -= self.out
                    rect.y = self.y
                else:
                    for rbrick in maze.bricks:
                        if rect.colliderect(rbrick):
                            self.collide_x = True
                            if self.x_direction > 0:
                                self.x = self.x - 3
                                rect.x = self.x
                            elif self.x_direction < 0:
                                self.x = self.x + 3
                                rect.x = self.x
                            if time % 2 == 0:
                                self.x_direction *= -1
        if self.collide_x:
            self.y += 1 * self.y_direction
            for rect in self.ghosts:
                rect.y = self.y
                for rbrick in maze.bricks:
                    if rect.colliderect(rbrick):
                        if self.y_direction > 0:
                            self.y = self.y - 3
                            rect.y = self.y
                        elif self.y_direction < 0:
                            self.y = self.y + 3
                            rect.y = self.y
                        self.collide_x = False
                        if time % 2 == 0:
                            self.y_direction *= -1

    def pinky_route(self, maze, time):
        if not self.collide_x:
            self.x += 1 * self.x_direction
            for rect in self.ghosts:
                rect.x = self.x
                if self.check_box_position(rect) and self.time_check():
                    self.y -= self.out
                    rect.y = self.y
                else:
                    for rbrick in maze.bricks:
                        if rect.colliderect(rbrick):
                            self.collide_x = True
                            if self.x_direction > 0:
                                self.x = self.x - 3
                                rect.x = self.x
                            elif self.x_direction < 0:
                                self.x = self.x + 3
                                rect.x = self.x
                            if time % 2 == 0:
                                self.x_direction *= -1
        if self.collide_x:
            self.y += 1 * self.y_direction
            for rect in self.ghosts:
                rect.y = self.y
                for rbrick in maze.bricks:
                    if rect.colliderect(rbrick):
                        if self.y_direction > 0:
                            self.y = self.y - 3
                            rect.y = self.y
                        elif self.y_direction < 0:
                            self.y = self.y + 3
                            rect.y = self.y
                        self.collide_x = False
                        if time % 2 == 0:
                            self.y_direction *= -1

    def check_box_position(self, rect):
        if rect.collidepoint((47*self.SIZE/2, 24*self.SIZE)):
            return True
        if rect.collidepoint((47*self.SIZE/2, 23*self.SIZE)):
            return True
        if rect.collidepoint((47*self.SIZE/2, 22*self.SIZE)):
            return True
        if rect.collidepoint(((47*self.SIZE/2)+2, 22*self.SIZE)):
            return True
        if rect.collidepoint(((47*self.SIZE/2)-2, 22*self.SIZE)):
            return True
        if rect.collidepoint(((47*self.SIZE/2)+4, 21*self.SIZE)):
            return True
        if rect.collidepoint(((47*self.SIZE/2)-4, 21*self.SIZE)):
            return True

    def time_check(self):
        time = pygame.time.get_ticks()
        if time > 5500 and not self.outside:
            self.outside = True
            return True

    @staticmethod
    def check_ghost_shield_collision(rect, maze):
        for rshield in maze.shields:
            if rect.colliderect(rshield) or rect.contains(rshield):
                return True
            else:
                return False

    def go_home(self):
        for rect in self.ghosts:
            """Left side of map"""
            for i in range(1, 4):
                for j in range(1, 4):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(3, 8):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(7, 10):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(9, 15):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(33, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(35, 39):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(38, 41):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(43, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(48, 51):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(45, 51):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(3, 7):
                for j in range(38, 41):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(43, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(40, 44):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(7, 10):
                for j in range(43, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(4, 10):
                for j in range(1, 4):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(7, 10):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(12, 15):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(9, 12):
                for j in range(1, 8):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(9, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(43, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(11, 20):
                for j in range(1, 4):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(11, 15):
                for j in range(7, 10):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(23, 26):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(16, 23):
                for j in range(7, 10):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(19, 22):
                for j in range(3, 8):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(12, 18):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                            self.y += 1 * abs(self.y_direction)
                            rect.y = self.y
                for j in range(33, 39):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                            self.y -= 1 * abs(self.y_direction)
                            rect.y = self.y
                for j in range(45, 51):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                            self.y += 1 * abs(self.y_direction)
                            rect.y = self.y
            for i in range(14, 17):
                for j in range(8, 13):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(12, 15):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(30, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(40, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(16, 20):
                for j in range(7, 10):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(12, 15):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(43, 46):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(1, 9):
                for j in range(23, 26):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(3, 20):
                for j in range(48, 51):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(21, 26):
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(48, 51):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            """Right side of map"""
            for i in range(25, 28):
                for j in range(1, 4):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(4, 8):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(12, 18):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(34, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(35, 38):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(43, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(44, 51):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(27, 31):
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(12, 15):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(43, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(30, 33):
                for j in range(7, 13):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(12, 15):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(30, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(39, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(27, 36):
                for j in range(1, 4):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(32, 36):
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(23, 26):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(35, 38):
                for j in range(1, 4):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(4, 9):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(9, 24):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y += 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(23, 26):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(26, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(37, 46):
                for j in range(23, 26):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(37, 41):
                for j in range(43, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(40, 43):
                for j in range(38, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(39, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(43, 46):
                for j in range(1, 4):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(3, 8):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(9, 15):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(33, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(34, 41):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
                for j in range(43, 46):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(44, 51):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(37, 44):
                for j in range(1, 4):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(7, 10):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(12, 15):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
                for j in range(33, 36):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(27, 44):
                for j in range(48, 51):
                    if rect.collidepoint(i * self.SIZE, j * self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x

            """Inside Middle"""
            for i in range(15, 22):
                for j in range(18, 21):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(25, 33):
                for j in range(18, 21):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(15, 23):
                for j in range(29, 31):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(24, 31):
                for j in range(29, 31):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(14, 17):
                for j in range(21, 31):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(30, 33):
                for j in range(21, 31):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.y -= 1 * abs(self.y_direction)
                        rect.y = self.y
            for i in range(15, 15):
                for j in range(23, 33):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x += 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(32, 33):
                for j in range(23, 33):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x -= 1 * abs(self.x_direction)
                        rect.x = self.x
            for i in range(22, 25):
                for j in range(17, 21):
                    if rect.collidepoint(i*self.SIZE, j*self.SIZE):
                        self.x = 23 * self.SIZE
                        rect.x = self.x
                        self.y = 24 * self.SIZE
                        rect.y += self.y
                        self.dead = False

    def blitme(self):
        for rect in self.ghosts:
            self.screen.blit(self.ghost.image, rect)
