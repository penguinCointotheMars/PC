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

#        self.image1 = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'wave1.png', 'image2': self.path+'wave2.png',
#                                                                 'image3': self.path+'wave3.png', 'image4': self.path+'wave4.png'}, 'image1')
        self.image1 = pygwidgets.ImageCollection(
            window, (0, 0), {'image1': self.path+'wave1.png'}, 'image1')
        self.image2 = pygwidgets.ImageCollection(
            window, (0, 0), {'image2': self.path+'wave2.png'}, 'image2')
        self.image3 = pygwidgets.ImageCollection(
            window, (0, 0), {'image3': self.path+'wave3.png'}, 'image3')
        self.image4 = pygwidgets.ImageCollection(
            window, (0, 0), {'image4': self.path+'wave4.png'}, 'image4')

#        # sprite sheet index
#        self.index = 1

        startingRect = self.image1.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height

        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

        self.x = (self.windowWidth - self.width)/2  # picture in middle
        self.y = self.windowHeight - self.height
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

        # set sine wave movements
        #        t = pygame.time.get_ticks() / 2 % 360  # scale and loop time
        t = pygame.time.get_ticks() % 3600  # scale and loop time
#        print('t'+str(t))
        ysin1 = -math.sin(t/450.0 * math.pi) * 10 + self.windowHeight - \
            self.height + 20    # scale sine wave
#        ysin1 = int(ysin1)                             # needs to be int
        (self.windowWidth - self.width)/2

        xsin1 = math.sin((t/600.0 - 0.5) * math.pi) * 15 + (self.windowWidth -
                                                            self.width)/2     # scale sine wave
#        xsin1 = int(xsin1)

        ysin2 = math.sin(t/600.0 * math.pi) * 10 + self.windowHeight - \
            self.height - 80    # scale sine wave2
#        ysin2 = int(ysin2)                             # needs to be int
        xsin2 = (1-math.cos(t/900.0 * math.pi)) * 13 + (self.windowWidth -
                                                        self.width)/2     # scale sine wave
#        xsin2 = int(xsin2)

        ysin3 = (1-math.cos(t/900.0 * math.pi)) * 10 + self.windowHeight - \
            self.height - 180    # scale sine wave3
#        ysin3 = int(ysin3)                             # needs to be int
        xsin3 = math.sin(t/1200.0 * math.pi) * 11 + (self.windowWidth -
                                                     self.width)/2     # scale sine wave
#        xsin3 = int(xsin3)

        ysin4 = math.sin(t/1200.0 * math.pi) * 10 + self.windowHeight - \
            self.height - 270    # scale sine wave3
#        ysin4 = int(ysin4)                             # needs to be int
        xsin4 = (1-math.cos(t/1800.0 * math.pi)) * 9 + (self.windowWidth -
                                                        self.width)/2     # scale sine wave
#        xsin4 = int(xsin4)

        yout = self.windowHeight + 200
#        print("sin " + str(math.sin(t/360)))

        if score < self.ml3:
            self.y1 = ysin4
            self.y2 = ysin3
            self.y3 = ysin2
            self.y4 = ysin1
            self.x1 = xsin4
            self.x2 = xsin3
            self.x3 = xsin2
            self.x4 = xsin1
        else:
            if score <= self.ml2 and score > self.ml3:
                self.y1 = ysin3
                self.y2 = ysin2
                self.y3 = ysin1
                self.y4 = yout
                self.x1 = xsin3
                self.x2 = xsin2
                self.x3 = xsin1
                self.x4 = xsin1
            else:
                if score < 0:
                    self.y1 = ysin2
                    self.y2 = ysin1
                    self.y3 = yout
                    self.y4 = yout
                    self.x1 = xsin2
                    self.x2 = xsin1
                    self.x3 = xsin1
                    self.x4 = xsin1
                else:
                    self.y1 = ysin1
                    self.y2 = yout
                    self.y3 = yout
                    self.y4 = yout
                    self.x1 = xsin1
                    self.x2 = xsin1
                    self.x3 = xsin1
                    self.x4 = xsin1

        self.image1.setLoc((self.x1, self.y1))
        self.image2.setLoc((self.x2, self.y2))
        self.image3.setLoc((self.x3, self.y3))
        self.image4.setLoc((self.x4, self.y4))

        # change image with self.index
        self.image1.replace('image1')
        self.image2.replace('image2')
        self.image3.replace('image3')
        self.image4.replace('image4')

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image1.draw()
        self.image2.draw()
        self.image3.draw()
        self.image4.draw()
