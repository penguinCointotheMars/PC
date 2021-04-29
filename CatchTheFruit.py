# Catch the fruit

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from Fruit import *  # bring in the Fruit class code  (Fruit -> Coin)
from Penguin import *  # bring in the Penguin class code
import pygwidgets

# 2 - Define constants
BLACK = (0, 0, 0)
LIME = (0, 255, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
FRAMES_PER_SECOND = 30
N_PIXELS_TO_MOVE = 3
PENGUIN_IMAGES_PATH = 'walk_edit_images/'  # penguin sprite images path
PENGUIN_SPEED = 12  # Penguin's speed

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()  # set the speed (frames per second)
pygame.display.set_caption('Penguin Coin to the moon!!')  # window name

# 4 - Load assets: image(s), sounds, etc.
oDisplay = pygwidgets.DisplayText(
    window, (WINDOW_WIDTH - 120, 10), '', fontSize=30)

# 5 - Initialize variables
# oBasket --> oPenguin with Penguin class
oPenguin = Penguin(window, WINDOW_WIDTH, WINDOW_HEIGHT,
                   PENGUIN_IMAGES_PATH, PENGUIN_SPEED)


# should change fruitFeatures to coin types
# should change fruitFreatures -> coinFeatures
fruitFeatures = [["apple", 15], ["banana", 15], ["cherry", 15], [
    "grapes", 15], ["strawberry", 15], ["pear", -100]]
fruitList = []

oRestartButton = pygwidgets.TextButton(window, (5, 5), 'Restart')

score = 0


# 6 - Loop forever
while True:
    if len(fruitList) <= 10:
        fruitNumber = random.randint(0, 5)
        oFruit = Fruit(window, WINDOW_WIDTH, WINDOW_HEIGHT,
                       fruitFeatures[fruitNumber][0], fruitFeatures[fruitNumber][1])
        fruitList.append(oFruit)

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if oRestartButton.handleEvent(event):  # ckicked on the Restart button
            print('User pressed the Restart button')
            score = 0
            fruitList.clear()

    # Add "continuous mode" code here to check for left or right arrow keys
    # If you get one, tell the basket to move itself appropriately
        # Check for user pressing keys
    keyPressedList = pygame.key.get_pressed()

    if keyPressedList[pygame.K_LEFT]:  # moving left
        oPenguin.move('left')

    if keyPressedList[pygame.K_RIGHT]:  # moving right
        oPenguin.move('right')

    # 8 - Do any "per frame" actions

    for oFruit in fruitList:
        oFruit.update()  # tell each fruit to update itself
        fruitRect = oFruit.getRect()
        basketRect = oPenguin.getRect()
        if basketRect.colliderect(fruitRect):
            print(f'{oFruit.fruitType} has collided with the Penguin')
            oFruit.reset()
            score += oFruit.points

    oDisplay.setValue('Score:' + str(score))

    # 9 - Clear the screen before drawing it again
    window.fill(LIME)

    # 10 - Draw the screen elements
    for oFruit in fruitList:
        oFruit.draw()   # tell each ball to draw itself

    oRestartButton.draw()
    oPenguin.draw()
    oDisplay.draw()

    # 11 - Update the screen
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
