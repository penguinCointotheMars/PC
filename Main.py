

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from Coin import *  # bring in the Coin class code
from Penguin import *  # bring in the Penguin class code
from Music import *  # bring in the Music class code
import pygwidgets

# 2 - Define constants
BLACK = (0, 0, 0)
LIME = (0, 255, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAMES_PER_SECOND = 30
N_PIXELS_TO_MOVE = 3
PENGUIN_IMAGES_PATH = 'walk_edit_images/'  # penguin sprite images path
PENGUIN_SPEED = 12  # Penguin's speed
COIN_POINT = 15  # point per coin, can be changed with coin price
OBJECT_NUMBERS = 10  # the number of dropping objects
MUSIC_PATH = 'Music/'  # the path of music tracks
COLLISION_TIME_DELAY = 100

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()  # set the speed (frames per second)
pygame.display.set_caption('Penguin Coin to the moon!!')  # window name

# 4 - Load assets: image(s), sounds, etc.
oDisplay = pygwidgets.DisplayText(
    window, (WINDOW_WIDTH - 120, 10), '', fontSize=30)

# 5 - Initialize variables
oPenguin = Penguin(window, WINDOW_WIDTH, WINDOW_HEIGHT,
                   PENGUIN_IMAGES_PATH, PENGUIN_SPEED)

# Music objects to play BGM
oMusic = Music(MUSIC_PATH, 'stage1_BGM.mp3')


# coinFeatures : list of coin's features to decide images and points
coinFeatures = [["coin", COIN_POINT], ]
# objectList : list of coins and clouds and items, etc... with cloud, item classes
objectList = []
oRestartButton = pygwidgets.TextButton(window, (5, 5), 'Restart')

score = 0
stage = 1

# stage1 BGM play
oMusic.play()

# 6 - Loop forever
while True:
    if len(objectList) <= OBJECT_NUMBERS:
        coinNumber = random.randint(0, len(coinFeatures) - 1)
        oCoin = Coin(window, WINDOW_WIDTH, WINDOW_HEIGHT,
                     coinFeatures[coinNumber][0], coinFeatures[coinNumber][1])
        objectList.append(oCoin)
        # To do : should add clouds, items objects to objectList

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if oRestartButton.handleEvent(event):  # ckicked on the Restart button
            print('User pressed the Restart button')
            score = 0
            objectList.clear()

    # BGM settings
    # change BGM with stages
    # 임시로 정해놓은 조건임.
    if score >= 200 and stage == 1:
        stage = 2
        oMusic.replace('stage2_BGM.mp3')

    elif score >= 400 and stage == 2:
        stage = 3
        oMusic.replace('stage3_BGM.mp3')

    # Add "continuous mode" code here to check for left or right arrow keys
    # If you get one, tell the basket to move itself appropriately
    # Check for user pressing keys
    keyPressedList = pygame.key.get_pressed()

    if keyPressedList[pygame.K_LEFT]:  # moving left
        oPenguin.move('left')

    if keyPressedList[pygame.K_RIGHT]:  # moving right
        oPenguin.move('right')

    # 8 - Do any "per frame" actions

    for oObject in objectList:
        oObject.update()  # tell each object to update itself
        objectRect = oObject.getRect()
        basketRect = oPenguin.getRect()
        if basketRect.colliderect(objectRect) and oObject.collision_time == 0:

            print(f'{oObject.Type} has collided with the Penguin')

            score += oObject.points
            oObject.collide(pygame.time.get_ticks())

        elif oObject.collision_time != 0 and oObject.disappear(pygame.time.get_ticks(), COLLISION_TIME_DELAY) == True:
            objectList.remove(oObject)
            oObject.reset()

    oDisplay.setValue('Score:' + str(score))

    # 9 - Clear the screen before drawing it again
    window.fill(LIME)

    # 10 - Draw the screen elements
    for oObject in objectList:
        oObject.draw()   # tell each ball to draw itself

    oRestartButton.draw()
    oPenguin.draw()
    oDisplay.draw()

    # 11 - Update the screen
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
