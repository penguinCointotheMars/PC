import pygame


class Music:

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.file = path + name
        pygame.mixer.init()
        pygame.mixer.music.load(self.file)
        pygame.mixer.music.set_volume(0.3)  # 넘 시끄렁...

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

    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)

    def volume(self, v):
        self.v = v
        pygame.mixer.music.set_volume(self.v)
