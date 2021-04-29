import pygame
from pygame.locals import *
import random
import pygwidgets


# Coin class
# should change Fruit -> Coin, fruitType -> coinType
# should add items (cloud, double etc...)
class Fruit():

    def __init__(self, window, windowWidth, windowHeight, fruitType, points=15):
        self.points = points
        self.fruitType = fruitType
        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.image = pygwidgets.Image(
            window, (0, 0), f"images/{fruitType}.png")

        self.points = points
        # A rect is made up of [x, y, width, height]
        startingRect = self.image.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height

        # Choose a random speed in the y direction
        self.ySpeed = random.randrange(5, 9)
        self.maxX = self.windowWidth - self.width
        self.reset()

    def reset(self):
        # Pick a random starting position
        self.x = random.randrange(0, self.maxX)
        self.y = random.randrange(-450, -self.height)
        self.image.setLoc((self.x, self.y))

    def update(self):
        # check for going off screen, move to above the windows
        if self.y > self.windowHeight:
            self.reset()

        # move location
        self.y = self.y + self.ySpeed
        self.image.setLoc((self.x, self.y))

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image.draw()
