"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame.font
from startscreen import StartScreen


class Button:
    def __init__(self, ai_settings, screen, msg):
        """Create the play button."""
        self.startup = StartScreen(screen, ai_settings)
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (0, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y = self.rect.y + self.screen_rect.height/4 - self.ai_settings.SIZE

        # The button message needs to be prepped only once
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Prepare the message."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.black)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the play button on the screen."""
        self.screen.fill(self.black)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.startup.draw_images()
