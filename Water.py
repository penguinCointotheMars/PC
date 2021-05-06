import pygame
from pygame.locals import *
import pygwidgets
import math
import time

# Water class


class Water:
    def __init__(self, window, windowWidth, windowHeight, path, melting_level_1, melting_level_2,  melting_level_3):

        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.path = path
        self.ml1 = melting_level_1
        self.ml2 = melting_level_2
        self.ml3 = melting_level_3

        # to store Glacier background images  ..

        self.image1 = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'wave1.png', 'image2': self.path+'wave2.png',
                                                                 'image3': self.path+'wave3.png', 'image4': self.path+'wave4.png'}, 'image1')
        # sprite sheet index
        self.index = 1

        startingRect = self.image1.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height
        
        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        self.x = (self.windowWidth - self.width)/2  # picture in middle
        self.y = windowHeight - self.height
        self.maxX = self.windowWidth - self.width
        self.image1.setLoc((self.x, self.y))

    def waterfill(self, score):
        # update index for background image according to the score
        # if score >= 0:
        #     self.index = 1
        # else:
        #     if score < 0:
        #         self.index = 2
        #     elif score < self.ml1:
        #         self.index = 3
        #     else:
        #         self.index = 4

        if score < self.ml3:
            self.index = 4
        else:
            if score <= self.ml2 and score > self.ml3:
                self.index = 3
            else:
                if score < 0:
                    self.index = 2
                else:
                    self.index = 1

        # add sine wave movement
        t = pygame.time.get_ticks() / 2 % 400  # scale and loop time
        ysin = math.sin(t/120.0) * 10 + self.windowHeight - \
            self.height     # scale sine wave
        ysin = int(ysin)                             # needs to be int

        self.y = ysin

        self.image1.setLoc((self.x, self.y))
        # change image with self.index
        self.image1.replace(f'image{self.index}')

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image1.draw()