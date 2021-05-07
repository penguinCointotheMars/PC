import pygame
from pygame.locals import *
import random
import pygwidgets


# Coin class
class Coin:

    def __init__(self, window, path, windowWidth, windowHeight, coinType, points=15, price=6):
        self.points = points
        self.Type = coinType
        self.window = window  # remember the window, so we can draw later
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.collision_time = 0  # store collision time
        self.path = path

        # store same coin image, should replace to display sprite sheets
        self.image = pygwidgets.Image(
            window, (0, 0), "{}{}.png".format(str(self.path), coinType))

        # 이미지가 너무 커서 임시로 작게 만듬 (추후 해상도 낮춰서 적용)
        self.image.scale(10, scaleFromCenter=True)
        self.points = points
        # A rect is made up of [x, y, width, height]
        startingRect = self.image.getRect()
        self.width = startingRect[2]  # width
        self.height = startingRect[3]  # height

        # Choose a random speed in the y direction
        #self.ySpeed = random.randrange(5, 9)
        self.ySpeed = price
        self.maxX = self.windowWidth - self.width
        self.reset()

        # Choose a random speed of rotation
        self.rSpeed = random.randrange(-15, 15)

    def reset(self):
        # Pick a random starting position
        self.x = random.randrange(0, self.maxX)
        self.y = random.randrange(-450, -self.height)
        self.image.setLoc((self.x, self.y))

    def update(self):
        # check for going off screen, move to above the windows
        if self.y > self.windowHeight:
            self.reset()

        # Rotate Coin # Code Credit: Sohye Park
        before_rot = self.image.getRect()
        self.image.rotate(self.rSpeed)
        after_rot = self.image.getRect()
        self.x = before_rot[0] - ((after_rot[2] - before_rot[2])/2)
        self.y = before_rot[1] - ((after_rot[3] - before_rot[3])/2)

        # move location
        self.y = self.y + self.ySpeed
        self.image.setLoc((self.x, self.y))

    def getRect(self):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        return myRect

    def draw(self):
        self.image.draw()

    def collide(self, collision_time):
        self.collision_time = collision_time

    def disappear(self, keep_time, time_delay):
        self.keep_time = keep_time  # get keep_time
        # when time is delayed after collision, return True
        if (self.keep_time - self.collision_time) >= time_delay:
            return True
        else:
            return False
