import pygame
from pygame.locals import *
import pygwidgets


# Water class
class Water:
    def __init__(self, window, windowWidth, windowHeight, path):

        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.path = path
        # to store Glacier background images  ..

        self.image = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'waterlevel1.png', 'image2': self.path+'waterlevel2.png',
                                                                 'image3': self.path+'waterlevel3.png', 'image4': self.path+'waterlevel4.png'}, 'image1')

        # sprite sheet index
        self.index = 1

        startingRect = self.image.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height

        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        self.x = self.windowWidth - 900
        self.y = windowHeight - self.height
        self.maxX = self.windowWidth - self.width
        self.image.setLoc((self.x, self.y))

    def waterfill(self, score):
        # update index for background image according to the score
        if score < -200:
            self.index = 4
        else:
            if score < -100:
                self.index = 3
            else:
                if score < 0:
                    self.index = 2
                else:
                    self.index = 1

        self.image.setLoc((self.x, self.y))
        # change image with self.index
        self.image.replace(f'image{self.index}')

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image.draw()
