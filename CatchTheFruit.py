# Catch the fruit

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from Fruit import *  # bring in the Fruit class code
from Basket import *  # bring in the Basket class code
import pygwidgets
import threading
import time
import requests

# 2 - Define constants
BLACK = (0, 0, 0)
BLUE = (0, 0, 205)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
FRAMES_PER_SECOND = 30
N_PIXELS_TO_MOVE = 3

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()  # set the speed (frames per second)

# 4 - Load assets: image(s), sounds, etc.
oDisplay = pygwidgets.DisplayText(
    window, (WINDOW_WIDTH - 120, 10), '', fontSize=30)

oCarbon = pygwidgets.DisplayText(
    window, (WINDOW_WIDTH - 200, 100), '', fontSize=10)

# 5 - Initialize variables
oBasket = Basket(window, WINDOW_WIDTH, WINDOW_HEIGHT)

fruitFeatures = [["apple", 15], ["banana", 15], ["cherry", 15], [
    "grapes", 15], ["strawberry", 15], ["pear", -100]]
fruitList = []

oRestartButton = pygwidgets.TextButton(window, (5, 5), 'Restart')

score = 0

stage = 1
coin = []
coinMin = 0
coinMax = 0
carbon = 0


def carbon_emission_update():
    url = "https://daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com/api/co2-api"

    headers = {
        'x-rapidapi-key': "7aaa41456emshcba46ed7902daa5p1bbe7djsn5b1827a7a2e7",
        'x-rapidapi-host': "daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com"
    }
    global carbon
    response = requests.request("GET", url, headers=headers)
    u = response.json()
    for i in range(0, len(u['co2'])):
        carbon = u['co2'][i]['trend']


def coin_price_update():
    global coin, coinMin, coinMax
    url = "https://api.coinpaprika.com/v1/tickers/doge-dogecoin/historical?start=2021-05-01"
    response = requests.request("GET", url)
    u = response.json()

    coinMin = u[0]['price']
    coinMax = u[0]['price']

    for i in range(0, len(u)):
        coin.append(u[i]['price'])
        if coinMax < u[i]['price']: coinMax = u[i]['price']
        if coinMin > u[i]['price']: coinMin = u[i]['price']


coin_price_update()
carbon_emission_update()

frameCounter = 0

# 6 - Loop forever
while True:
    frameCounter = (frameCounter + 1) % 1200

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
        oBasket.move('left')

    if keyPressedList[pygame.K_RIGHT]:  # moving right
        oBasket.move('right')

    # 8 - Do any "per frame" actions

    for oFruit in fruitList:
        oFruit.update()  # tell each fruit to update itself
        fruitRect = oFruit.getRect()
        basketRect = oBasket.getRect()
        if basketRect.colliderect(fruitRect):
            print(f'{oFruit.fruitType} has collided with the basket')
            oFruit.reset()
            score += oFruit.points

    oDisplay.setValue('Score:' + str(score))

    # 9 - Clear the screen before drawing it again
    window.fill(BLUE)

    if score > 10:
        graphStartY = WINDOW_HEIGHT / 2

        coinPrev = coin[0]

        prevX = 0
        step = WINDOW_WIDTH / len(coin)

        currentRange = (frameCounter / 1200) * len(coin)

        for i in range(0, int(currentRange)):
            x = i * step
            coinNow = coin[i]

            # percentage position
            coinPrevRatio = abs(coinPrev - coinMin) / abs(coinMax - coinMin)
            coinNowRatio = abs(coinNow - coinMin) / abs(coinMax - coinMin)

            # linear mapping
            yNowPosition = graphStartY - 50 + (coinNowRatio * 200)
            yPrevPosition = graphStartY - 50 + (coinPrevRatio * 200)

            pygame.draw.line(window, BLACK, (prevX, yPrevPosition), (x, yNowPosition), 1)
            coinPrev = coinNow
            prevX = x

    if score > 50:
        #TODO :
        for i in range(0, len(carbon)):
            print(str(carbon[i]))
            oCarbon.setValue('CO2:    ' + str(carbon[i]) + '   ppm')
            oCarbon.draw()

    # 10 - Draw the screen elements
    for oFruit in fruitList:
        oFruit.draw()  # tell each ball to draw itself

    oRestartButton.draw()
    oBasket.draw()
    oDisplay.draw()

    # 11 - Update the screen
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
