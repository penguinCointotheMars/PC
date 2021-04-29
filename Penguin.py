import pygame
from pygame.locals import *
import pygwidgets


# Penguin class
class Penguin():

    def __init__(self, window, windowWidth, windowHeight, path, xSpeed=12):

        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.path = path
        # ImageCollection to store Penguin sprite sheets
        self.image = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'walk1.png', 'image2': self.path+'walk2.png',
                                                                 'image3': self.path+'walk3.png', 'image4': self.path+'walk4.png', 'image5': self.path+'walk5.png', 'image6': self.path+'walk6.png'}, 'image1')
        # sprite sheet index
        self.index = 1

        startingRect = self.image.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height

        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        self.x = self.windowWidth / 2
        self.y = windowHeight - self.height - 20
        self.maxX = self.windowWidth - self.width
        self.image.setLoc((self.x, self.y))

        # Choose speed in the x direction
        self.xSpeed = xSpeed

    def move(self, leftOrRight):
        # add code here to move the basket and restrict it to stay in the window
        if leftOrRight == "left":
            self.x = self.x - \
                self.xSpeed if (self.x - self.xSpeed >= 0) else(self.x)
            # move direction change from right to left
            if self.index <= 3:
                self.index = 4
            # same direction
            else:
                if self.index >= 6:
                    self.index = 4
                else:
                    self.index += 1
        else:
            self.x = self.x + \
                self.xSpeed if (self.x + self.xSpeed <= self.maxX) else(self.x)
            # move direction change from left to right
            if self.index > 3:
                self.index = 1
            # same direction
            else:
                if self.index >= 3:
                    self.index = 1
                else:
                    self.index += 1

        self.image.setLoc((self.x, self.y))
        # change image with self.index
        self.image.replace(f'image{self.index}')

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image.draw()
