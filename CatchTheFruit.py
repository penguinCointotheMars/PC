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
from datetime import datetime
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

# 5 - Initialize variables
oBasket = Basket(window, WINDOW_WIDTH, WINDOW_HEIGHT)

fruitFeatures = [["apple", 15], ["banana", 15], ["cherry", 15], [
    "grapes", 15], ["strawberry", 15], ["pear", -100]]
fruitList = []

oRestartButton = pygwidgets.TextButton(window, (5, 5), 'Restart')

score = 0

stage = 1
coin = []
carbon = 0

def carbon_emission_update():
    url = "https://daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com/api/co2-api"

    headers = {
        'x-rapidapi-key': "7aaa41456emshcba46ed7902daa5p1bbe7djsn5b1827a7a2e7",
        'x-rapidapi-host': "daily-atmosphere-carbon-dioxide-concentration.p.rapidapi.com"
    }
    while True:
        response = requests.request("GET", url, headers=headers)
        u = response.json()
        h = response.text
        #print(u["co2"][0]["trend"])
        print(len(u["co2"])) #3773 items

        print("carbon_emission" + h)
        time.sleep(2)


y = threading.Thread(target=carbon_emission_update, args=())
y.start()


def coin_price_update():
    global coin
    url = "https://api.coinpaprika.com/v1/tickers/doge-dogecoin"

    while True:
        response = requests.request("GET", url)
        u = response.json()
        coin.append(u['quotes']['USD']['price'])

        if len(coin) > 10:
            coin = coin[1:]
        time.sleep(1)


x = threading.Thread(target=coin_price_update, args=())
x.start()

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

    print(coin)

    if score > 100:
        graphStartY = WINDOW_HEIGHT / 2

        if len(coin) >= 2:
            coinPrev = coin[0]
            prevX = 0
            step = WINDOW_WIDTH / len(coin)

            for i in range(0, len(coin)):
                x = i * step
                coinNow = coin[i]
                #TODO: scale coinprice to visualize the price
                pygame.draw.line(window, BLACK, (prevX, graphStartY + coinPrev), (x, graphStartY + coinNow), 1)
                coinPrev = coinNow
                prevX = x

    # 10 - Draw the screen elements
    for oFruit in fruitList:
        oFruit.draw()   # tell each ball to draw itself

    oRestartButton.draw()
    oBasket.draw()
    oDisplay.draw()

    # 11 - Update the screen
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
