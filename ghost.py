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
        self.last_frame = None
        self.rect = None
        self.ghost = None
        self.ghosts = []
        self.eye = None
        self.eyes = []
        self.escapee = None
        self.escapees = []
        self.initialize_images()

        self.x_direction = settings.ghost_x
        self.y_direction = settings.ghost_y
        self.collide_x = False

        for rect in self.ghosts:
            self.x = float(rect.x)
            self.y = float(rect.y)
        self.dead = False
        self.stop = False

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
        self.blue_frames = ['Vulnerable_Ghost']
        self.image = self.blue_frames[self.image_index]
        self.escapee = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.escapee.rect
        w, h = r.width, r.height
        self.escapees.append(pygame.Rect(0, 0, w, h))
        self.death_frames = ['Eyes_Up',
                             'Eyes_Right',
                             'Eyes_Down,'
                             'Eyes_Left']
        self.image = self.images[self.image_index]
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
                self.death_index += 1
                if self.death_index >= len(self.death_frames):
                    self.ghost = self.ghost = ImageRect(self.screen, self.images[0], self.SIZE * 2, self.SIZE * 2)
                    self.dead = False
                else:
                    self.image = self.death_frames[self.death_index]
                    self.ghost = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        if not self.stop:
            if self.ghost_type == 1:
                self.inky_route(maze, time_test)
            if self.ghost_type == 2:
                self.blinky_route(maze, time_test)
            if self.ghost_type == 3:
                self.clyde_route(maze, time_test)
            if self.ghost_type == 4:
                self.pinky_route(maze, time_test)
        if self.stop:
            for rect in self.ghosts:
                rect.x = self.x
                rect.y = self.y
            if self.ghost_type == 1:
                self.x = 18*self.SIZE
                self.y = 22*self.SIZE
            if self.ghost_type == 1:
                self.x = 27*self.SIZE
                self.y = 22*self.SIZE
            if self.ghost_type == 1:
                self.x = 18*self.SIZE
                self.y = 25*self.SIZE
            if self.ghost_type == 1:
                self.x = 27*self.SIZE
                self.y = 25*self.SIZE

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

    @staticmethod
    def time_check():
        time = pygame.time.get_ticks()
        if time > 5500:
            return True

    @staticmethod
    def check_ghost_shield_collision(rect, maze):
        for rshield in maze.shields:
            if rect.colliderect(rshield) or rect.contains(rshield):
                return True
            else:
                return False

    def blitme(self):
        for rect in self.ghosts:
            self.screen.blit(self.ghost.image, rect)
