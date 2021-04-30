import pygame
from pygame.locals import *
import random
import pygwidgets


# Coin class
class Coin():

    def __init__(self, window, windowWidth, windowHeight, coinType, points=15):
        self.points = points
        self.Type = coinType
        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight

        # store same coin image, should replace to display sprite sheets
        self.image = pygwidgets.Image(
            window, (0, 0), f"coin_images/{coinType}.png")
        # 이미지가 너무 커서 임시로 작게 만듬 (추후 해상도 낮춰서 적용)
        self.image.scale(10, scaleFromCenter=True)

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
