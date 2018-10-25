"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from imagerect import ImageRect


class StartScreen:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.SIZE = self.settings.SIZE
        self.screen_rect = screen.get_rect()
        self.BLACK = (0, 0, 0)

        self.image = None
        self.image_index = 0
        self.right_images = []
        self.rightpac = None
        self.rright = None
        self.left_images = []
        self.leftpac = None
        self.rleft = None
        self.inky_images = []
        self.inky = None
        self.rinky = None
        self.blinky_images = []
        self.blinky = None
        self.rblinky = None
        self.clyde_images = []
        self.clyde = None
        self.rclyde = None
        self.pinky_images = []
        self.pinky = None
        self.rpinky = None
        self.vuln_images = []
        self.vuln_1 = None
        self.vuln_2 = None
        self.vuln_3 = None
        self.vuln_4 = None
        self.rvuln_1 = None
        self.rvuln_2 = None
        self.rvuln_3 = None
        self.rvuln_4 = None

        self.width, self.height = 200, 50
        self.text_color = (255, 255, 0)
        self.black = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 120)
        self.intro_font = pygame.font.SysFont(None, 40)
        self.pacman = 'PACMAN'
        self.pacman_image = self.font.render(self.pacman, True, self.text_color, self.black)
        self.rpacman = self.pacman_image.get_rect()
        self.rpacman.center = self.screen_rect.center
        self.rpacman.y = self.rpacman.y - self.screen_rect.height/4 - self.settings.SIZE
        self.intro_inky = "Meet Inky: "
        self.int_ink_img = self.intro_font.render(self.intro_inky, True, self.text_color, self.black)
        self.rint_ink = self.int_ink_img.get_rect()
        self.rint_ink.center = self.screen_rect.center
        self.rint_ink.x -= self.SIZE * 2
        self.intro_blinky = "Meet Blinky: "
        self.int_blink_img = self.intro_font.render(self.intro_blinky, True, self.text_color, self.black)
        self.rint_blink = self.int_blink_img.get_rect()
        self.rint_blink.center = self.screen_rect.center
        self.rint_blink.x -= self.SIZE * 2
        self.intro_clyde = "Meet Clyde: "
        self.int_clyde_img = self.intro_font.render(self.intro_clyde, True, self.text_color, self.black)
        self.rint_clyde = self.int_clyde_img.get_rect()
        self.rint_clyde.center = self.screen_rect.center
        self.rint_clyde.x -= self.SIZE * 2
        self.intro_pinky = "Meet Pinky: "
        self.int_pink_img = self.intro_font.render(self.intro_pinky, True, self.text_color, self.black)
        self.rint_pink = self.int_pink_img.get_rect()
        self.rint_pink.center = self.screen_rect.center
        self.rint_pink.x -= self.SIZE * 2
        self.counter = 0

        self.intro_images = []
        self.intro_index = None
        self.intro = None
        self.intros = []

        self.intro_names = []
        self.name = None
        self.rname = None

        self.animation = 0
        self.last_frame = 0
        self.next_frame = None
        self.right = True
        self.right_r = True
        self.right_1 = False
        self.right_2 = False
        self.right_3 = False
        self.right_4 = False
        self.left = False
        self.left_l = False
        self.left_1 = False
        self.left_2 = False
        self.left_3 = False
        self.left_4 = False

        self.introduction = False

        # self.initialize_introduction()
        self.initialize_introductions()
        self.initialize_right_pac()
        self.initialize_left_pac()
        self.initialize_inky()
        self.initialize_blinky()
        self.initialize_clyde()
        self.initialize_pinky()
        self.initialize_vulnerable()

        self.x_r = float(self.rright.x)
        self.x_l = float(self.rleft.x)
        self.x_v1 = float(self.rvuln_1.x)
        self.x_v2 = float(self.rvuln_2.x)
        self.x_v3 = float(self.rvuln_3.x)
        self.x_v4 = float(self.rvuln_4.x)
        self.x_1 = float(self.rinky.x)
        self.x_2 = float(self.rblinky.x)
        self.x_3 = float(self.rclyde.x)
        self.x_4 = float(self.rpinky.x)

        self.intermission = pygame.mixer.Sound('sounds/pacman_intermission.wav')
        self.intermission.set_volume(0.05)
        self.channel = self.settings.begin

    def initialize_introductions(self):
        self.intro_images = ['Inky_0',
                             'Blinky_0',
                             'Clyde_0',
                             'Pinky_0']
        self.counter = 0
        self.intro_index = 0
        self.image = self.intro_images[self.intro_index]
        self.intro = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
        r = self.intro.rect
        w, h = r.width, r.height
        x_pos = self.screen_rect.width/2 + self.SIZE * 6
        y_pos = self.screen_rect.height/2 - self.SIZE
        self.intros.append(pygame.Rect(x_pos, y_pos, w, h))

    def initialize_right_pac(self):
        self.right_images = [pygame.image.load('images/pacman2.png'),
                             pygame.image.load('images/pacman3.png')]
        self.rightpac = self.right_images[self.image_index]
        self.rright = self.rightpac.get_rect()
        self.rright.center = self.screen_rect.center
        self.rright.x = self.rright.x + self.settings.SIZE * 12

    def initialize_left_pac(self):
        self.left_images = [pygame.image.load('images/pacman0.png'),
                            pygame.image.load('images/pacman1.png')]
        self.leftpac = self.left_images[self.image_index]
        self.rleft = self.leftpac.get_rect()
        self.rleft.center = self.screen_rect.center
        self.rleft.x = self.rleft.x + self.settings.SIZE * 12

    def initialize_inky(self):
        self.inky_images = [pygame.image.load('images/Inky_2.png'),
                            pygame.image.load('images/Inky_3.png')]
        self.inky = self.inky_images[self.image_index]
        self.rinky = self.inky.get_rect()
        self.rinky.center = self.screen_rect.center
        self.rinky.x = self.rinky.x - self.settings.SIZE * 4

    def initialize_blinky(self):
        self.blinky_images = [pygame.image.load('images/Blinky_2.png'),
                              pygame.image.load('images/Blinky_3.png')]
        self.blinky = self.blinky_images[self.image_index]
        self.rblinky = self.blinky.get_rect()
        self.rblinky.center = self.screen_rect.center
        self.rblinky.x = self.rblinky.x

    def initialize_clyde(self):
        self.clyde_images = [pygame.image.load('images/Clyde_2.png'),
                             pygame.image.load('images/Clyde_3.png')]
        self.clyde = self.clyde_images[self.image_index]
        self.rclyde = self.clyde.get_rect()
        self.rclyde.center = self.screen_rect.center
        self.rclyde.x = self.rclyde.x + self.settings.SIZE * 4

    def initialize_pinky(self):
        self.pinky_images = [pygame.image.load('images/Pinky_2.png'),
                             pygame.image.load('images/Pinky_3.png')]
        self.pinky = self.pinky_images[self.image_index]
        self.rpinky = self.pinky.get_rect()
        self.rpinky.center = self.screen_rect.center
        self.rpinky.x = self.rpinky.x + self.settings.SIZE * 8

    def initialize_vulnerable(self):
        self.vuln_images = [pygame.image.load('images/Vulnerable_Ghost.png')]
        self.vuln_1 = self.vuln_images[self.image_index]
        self.vuln_2 = self.vuln_images[self.image_index]
        self.vuln_3 = self.vuln_images[self.image_index]
        self.vuln_4 = self.vuln_images[self.image_index]
        self.rvuln_1 = self.vuln_1.get_rect()
        self.rvuln_2 = self.vuln_2.get_rect()
        self.rvuln_3 = self.vuln_3.get_rect()
        self.rvuln_4 = self.vuln_4.get_rect()
        self.rvuln_1.center = self.screen_rect.center
        self.rvuln_2.center = self.screen_rect.center
        self.rvuln_3.center = self.screen_rect.center
        self.rvuln_4.center = self.screen_rect.center
        self.rvuln_1.x = self.rvuln_1.x - self.settings.SIZE * 4
        self.rvuln_2.x = self.rvuln_2.x
        self.rvuln_3.x = self.rvuln_3.x + self.settings.SIZE * 4
        self.rvuln_4.x = self.rvuln_4.x + self.settings.SIZE * 8

    def go_right(self, speed):
        self.x_1 += speed
        self.rinky.x = self.x_1
        self.x_2 += speed
        self.rblinky.x = self.x_2
        self.x_3 += speed
        self.rclyde.x = self.x_3
        self.x_4 += speed
        self.rpinky.x = self.x_4
        self.x_r += speed
        self.rright.x = self.x_r
        self.x_l += speed
        self.rleft.x = self.x_l
        self.x_v1 += speed
        self.rvuln_1.x = self.x_v1
        self.x_v2 += speed
        self.rvuln_2.x = self.x_v2
        self.x_v3 += speed
        self.rvuln_3.x = self.x_v3
        self.x_v4 += speed
        self.rvuln_4.x = self.x_v4
        if self.rright.x > self.settings.screen_width:
            self.right_r = True
            self.left_l = False
        if self.rinky.x > self.settings.screen_width:
            self.right_1 = True
            self.left_4 = False
        if self.rblinky.x > self.settings.screen_width:
            self.right_2 = True
            self.left_3 = False
        if self.rclyde.x > self.settings.screen_width:
            self.right_3 = True
            self.left_2 = False
        if self.rinky.x > self.settings.screen_width:
            self.right_4 = True
            self.left_1 = False
        if self.right_r and self.right_1 and self.right_2 and self.right_3 and self.right_4:
            self.right = False
            self.left = True

    def go_left(self, speed):
        self.x_1 -= speed
        self.rinky.x = self.x_1
        self.x_2 -= speed
        self.rblinky.x = self.x_2
        self.x_3 -= speed
        self.rclyde.x = self.x_3
        self.x_4 -= speed
        self.rpinky.x = self.x_4
        self.x_r -= speed
        self.rright.x = self.x_r
        self.x_l -= speed
        self.rleft.x = self.x_l
        self.x_v1 -= speed
        self.rvuln_1.x = self.x_v1
        self.x_v2 -= speed
        self.rvuln_2.x = self.x_v2
        self.x_v3 -= speed
        self.rvuln_3.x = self.x_v3
        self.x_v4 -= speed
        self.rvuln_4.x = self.x_v4
        if self.rright.right < 0:
            self.right_r = False
            self.left_l = True
        if self.rinky.x < 0:
            self.left_4 = True
            self.right_1 = False
        if self.rblinky.x < 0:
            self.left_3 = True
            self.right_2 = False
        if self.rclyde.x < 0:
            self.left_2 = True
            self.right_3 = False
        if self.rpinky.x < 0:
            self.left_1 = True
            self.right_4 = False
        if self.left_l and self.left_1 and self.left_2 and self.left_3 and self.left_4:
            self.left = False
            self.right = True
            self.introduction = True

    def draw_images(self):
        self.screen.blit(self.pacman_image, self.rpacman)
        if not self.introduction:
            if not self.channel.get_busy():
                self.channel.play(self.intermission)
            if self.right:
                self.go_right(0.3)
            if self.left:
                self.go_left(0.3)
            time_test = pygame.time.get_ticks()
            if self.animation == 1:
                if self.right:
                    self.screen.blit(self.inky, self.rinky)
                    self.screen.blit(self.blinky, self.rblinky)
                    self.screen.blit(self.clyde, self.rclyde)
                    self.screen.blit(self.pinky, self.rpinky)
                    self.screen.blit(self.rightpac, self.rright)
                if self.left:
                    self.screen.blit(self.vuln_1, self.rvuln_1)
                    self.screen.blit(self.vuln_2, self.rvuln_2)
                    self.screen.blit(self.vuln_3, self.rvuln_3)
                    self.screen.blit(self.vuln_4, self.rvuln_4)
                    self.screen.blit(self.leftpac, self.rleft)
                self.last_frame = pygame.time.get_ticks()
                if abs(time_test - self.next_frame) > 750:
                    self.image_index += 1
                    self.inky = self.inky_images[self.image_index]
                    self.blinky = self.blinky_images[self.image_index]
                    self.clyde = self.clyde_images[self.image_index]
                    self.pinky = self.pinky_images[self.image_index]
                    self.rightpac = self.right_images[self.image_index]
                    self.leftpac = self.left_images[self.image_index]
                    self.animation = 0
            elif self.animation == 0:
                if self.right:
                    self.screen.blit(self.inky, self.rinky)
                    self.screen.blit(self.blinky, self.rblinky)
                    self.screen.blit(self.clyde, self.rclyde)
                    self.screen.blit(self.pinky, self.rpinky)
                    self.screen.blit(self.rightpac, self.rright)
                if self.left:
                    self.screen.blit(self.vuln_1, self.rvuln_1)
                    self.screen.blit(self.vuln_2, self.rvuln_2)
                    self.screen.blit(self.vuln_3, self.rvuln_3)
                    self.screen.blit(self.vuln_4, self.rvuln_4)
                    self.screen.blit(self.leftpac, self.rleft)
                if abs(time_test - self.last_frame) > 500:
                    self.next_frame = pygame.time.get_ticks()
                    self.image_index -= 1
                    self.inky = self.inky_images[self.image_index]
                    self.blinky = self.blinky_images[self.image_index]
                    self.clyde = self.clyde_images[self.image_index]
                    self.pinky = self.pinky_images[self.image_index]
                    self.rightpac = self.right_images[self.image_index]
                    self.leftpac = self.left_images[self.image_index]
                    self.animation = 1
        if self.introduction:
            if self.channel.get_busy():
                pygame.mixer.fadeout(10000)
            time_test = pygame.time.get_ticks()
            if self.counter == 4:
                self.counter = 0
                self.intro_index = 0
                self.introduction = False
            elif self.counter == 3:
                for rect in self.intros:
                    self.screen.blit(self.intro.image, rect)
                self.screen.blit(self.int_pink_img, self.rint_pink)
            elif self.counter == 2:
                for rect in self.intros:
                    self.screen.blit(self.intro.image, rect)
                self.screen.blit(self.int_clyde_img, self.rint_clyde)
            elif self.counter == 1:
                for rect in self.intros:
                    self.screen.blit(self.intro.image, rect)
                self.screen.blit(self.int_blink_img, self.rint_blink)
            elif self.counter == 0:
                for rect in self.intros:
                    self.screen.blit(self.intro.image, rect)
                self.screen.blit(self.int_ink_img, self.rint_ink)
            if abs(self.last_frame - time_test) > 3000:
                self.last_frame = time_test
                self.intro_index = (self.intro_index + 1) % len(self.intro_images)
                self.image = self.intro_images[self.intro_index]
                self.counter += 1
                self.intro = ImageRect(self.screen, self.image, self.SIZE * 2, self.SIZE * 2)
