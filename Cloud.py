import pygame
from pygame.locals import *
import pygwidgets


# Cloud class
class Cloud():
    def __init__(self, window, windowWidth, windowHeight, path):

        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.path = path
        # to store cloud background images  ..     
        self.image = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'cloudlevel0.png', 'image2': self.path+'cloudlevel1.png',
                                                                 'image3': self.path+'cloudlevel2.png', 'image4': self.path+'cloudlevel3.png'}, 'image1')

        # sprite sheet index
        self.index = 1

        startingRect = self.image.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height
        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        self.x = (self.windowWidth -self.width)/2  #picture in middle
#        self.y = windowHeight - self.height 
        self.y = self.height 
        self.maxX = self.windowWidth - self.width
        self.image.setLoc((self.x, self.y))

    def cloudfill(self, score):
        # update index for background image according to the score
        if score > 400:
            self.index = 4
            self.y = 0
        else:
            if 400 >= score > 300:
                self.index = 4
                self.y = -50
            else:
                if 300 >= score > 200:
                    self.index = 3
                    self.y = -100
                else:
                    if 200 >= score > 100: 
                        self.index = 2
                        self.y = -200
                    else:
                        self.index = 1
                        self.y = -250


        self.image.setLoc((self.x, self.y))
        # change image with self.index
        self.image.replace(f'image{self.index}')

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image.draw()
