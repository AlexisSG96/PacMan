"""
Name: Alexis Steven Garcia
Project: PacMan
Date: October 25, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
from pygame import mixer


class Settings:
    def __init__(self):
        self.SIZE = 13
        self.screen_width = self.SIZE*47
        self.screen_height = self.SIZE*55
        self.bg_color = (255, 255, 255)

        self.ghost_x = 1
        self.ghost_y = 1
        self.get_out = self.SIZE * 4

        self.lives_limit = 3

        self.audio_channels = 5
        self.player_channel = mixer.Channel(0)
        self.ghost_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.eat_channel = mixer.Channel(3)
        self.begin = mixer.Channel(4)
        self.initialize_audio_settings()

    def initialize_audio_settings(self):
        """Initialize mixer settings."""
        # Allows for other sounds to be played with background music
        mixer.init()
        mixer.set_num_channels(self.audio_channels)
        mixer.music.load('sounds/pacman_beginning.wav')
        mixer.music.set_volume(11)
