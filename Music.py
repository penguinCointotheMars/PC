import pygame


class Music:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.file = path + name
        pygame.mixer.init()
        pygame.mixer.music.load(self.file)

    def play(self):
        pygame.mixer.music.play()

    def replace(self, next_music_name):
        self.next_file = self.path + next_music_name
        pygame.mixer.music.pause()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(self.next_file)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()
