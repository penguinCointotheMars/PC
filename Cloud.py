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
        self.image1 = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'cloud.png'}, 'image1')
        self.image2 = pygwidgets.ImageCollection(window, (0, 0), {'image1': self.path+'cloud.png'}, 'image1')

        # sprite sheet index
        self.index = 1

        startingRect = self.image1.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height
        self.halfHeight = self.height / 2
        self.halfWidth = self.width / 2

#        self.x = (self.windowWidth -self.width)/2  #picture in middle
        self.x1 = 0  #picture in middle        
        self.x2 = (self.windowWidth -self.width)  #picture in middle                
#        self.y = windowHeight - self.height 
        self.y = self.height 
        self.maxX = self.windowWidth - self.width
        self.image1.setLoc((self.x1, self.y))
        self.image2.setLoc((self.x2, self.y))

    def cloudfill(self, time):
#    def cloudfill(self, carbonCloud):
        # now cloud is coming down with constant rate vs time (carbon emmision is almost constant)
        # NEED TO ADJUST THE OFFSET VALUE or reset the time 
        move_dy = ( time - 50000 ) * 0.01
        if move_dy < self.height:
            print("time: " + str(time)) 
            self.y = 0 -self.height + move_dy
        else:
        # add sine wave movement?
            self.y = 0

      # update index for background image according to the score (OLD)
#        if score > 400:
#            self.index = 4
#            self.y = 0
#        else:
#            if 400 >= score > 300:
#                self.index = 4
#                self.y = -50
#            else:
#                if 300 >= score > 200:
#                    self.index = 3
#                    self.y = -100
#                else:
#                    if 200 >= score > 100: 
#                        self.index = 2
#                        self.y = -200
#                    else:
#                        self.index = 1
#                        self.y = -250


        self.image1.setLoc((self.x1, self.y))
        self.image2.setLoc((self.x2, self.y))        
        # change image with self.index
        self.image1.replace('image1')
        self.image2.replace('image1')        

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image1.draw()
        self.image2.draw()
