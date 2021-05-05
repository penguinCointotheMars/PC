# 1 - Import packages
import sys
import time

import requests

import pygwidgets
from Coin import *  # bring in the Coin class code
from Music import *  # bring in the Music class code
from Penguin import *  # bring in the Penguin class code
from Water import *  # bring in the Water class code
from Cloud import *  # bring in the Cloud class code

# 2 - Define constants
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAMES_PER_SECOND = 30
N_PIXELS_TO_MOVE = 3
# source file paths
PENGUIN_IMAGES_PATH = 'walk_edit_images/'  # penguin sprite images path
WATER_IMAGES_PATH = 'water_images/'  # iceberg images path
MUSIC_PATH = 'Music/'  # the path of music tracks
STAGE_IMAGE_PATH = 'stage_images'
CLOUD_IMAGES_PATH = 'cloud_images/'

# constants to play
PENGUIN_SPEED = 12  # Penguin's speed
PENGUIN_HEIGHT = 200
COIN_POINT = 15  # point per coin, can be changed with coin price
OBJECT_NUMBERS = 10  # the number of dropping objects
COLLISION_TIME_DELAY = 100

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()  # set the speed (frames per second)
pygame.display.set_caption('Penguin Coin to the moon!!')  # window name

# 4 - Load assets: image(s), sounds, etc.
oDisplay = pygwidgets.DisplayText(
    window, (WINDOW_WIDTH - 120, 10), '', fontSize=30)

oCarbon = pygwidgets.DisplayText(
    window, (5, 25), '', fontSize=30)

# 5 - Initialize variables
oPenguin = Penguin(window, WINDOW_WIDTH, WINDOW_HEIGHT,
                   PENGUIN_IMAGES_PATH, PENGUIN_SPEED, PENGUIN_HEIGHT)
oWater = Water(window, WINDOW_WIDTH, WINDOW_HEIGHT, WATER_IMAGES_PATH)

oCloud = Cloud(window, WINDOW_WIDTH, WINDOW_HEIGHT, CLOUD_IMAGES_PATH)

# Music objects to play BGM
oMusic = Music(MUSIC_PATH, 'stage1_BGM.mp3')

# coinFeatures : list of coin's features to decide images and points
coinFeatures = [["coin", COIN_POINT], ]
# objectList : list of coins and clouds and items, etc... with cloud, item classes
objectList = []
oRestartButton = pygwidgets.TextButton(window, (5, 5), 'Restart')


# constants
score = 0
stage = 1
coin = []
coinMin = 0
coinMax = 0
carbon =[]


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
        carbon.append(u['co2'][i]['trend'])


def coin_price_update():
    global coin, coinMin, coinMax
    url = "https://api.coinpaprika.com/v1/tickers/doge-dogecoin/historical?start=2021-05-01"
    response = requests.request("GET", url)
    u = response.json()

    coinMin = u[0]['price']
    coinMax = u[0]['price']

    for i in range(0, len(u)):
        coin.append(u[i]['price'])
        if coinMax < u[i]['price']:
            coinMax = u[i]['price']
        if coinMin > u[i]['price']:
            coinMin = u[i]['price']


coin_price_update()
carbon_emission_update()

frameCounter = 0
carbonCounter = 0
carbonIndex = 0
# stage1 BGM play
oMusic.play()


# 6 - Loop forever
while True:
    frameCounter = (frameCounter + 1) % 1200
    carbonCounter = carbonCounter + 1

    if carbonCounter > 60:
        carbonIndex = (carbonIndex+1) % len(carbon)
        carbonCounter = 0

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

    oDisplay.setValue('Score:' + str(score))

    # 9 - Clear the screen before drawing it again
    window.fill(BLUE)

    # BGM settings
    # change BGM with stages
    # 임시로 정해놓은 조건임.
    if score >= 50 and stage == 1:
        stage = 2
        oMusic.stop()

        stage_image = pygwidgets.Image(
            window, (0, 0), 'stage_images/stage2.jpeg')
        stage_image.draw()
        objectList.clear()
        pygame.display.update()
        time.sleep(5)
        oMusic.replace('stage2_BGM.mp3')

    if stage >= 2:
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

            pygame.draw.line(
                window, BLACK, (prevX, yPrevPosition), (x, yNowPosition), 1)

            if coinPrev > coinNow:
                oCoin.ySpeed = oCoin.ySpeed - 0.2
            else:
                oCoin.ySpeed = oCoin.ySpeed + 0.2

            coinPrev = coinNow
            prevX = x

    if score >= 100 and stage == 2:
        oMusic.stop()

        stage_image2 = pygwidgets.Image(
            window, (0, 0), 'stage_images/stage3.jpeg')
        stage_image2.draw()
        objectList.clear()
        pygame.display.update()
        time.sleep(5)
        oMusic.replace('stage3_BGM.mp3')
        stage = 3

    if stage == 3:
        score = score - float(carbon[carbonIndex]) * 0.1
        oCarbon.setValue('CO2:' + carbon[carbonIndex] + 'ppm')
        oCarbon.draw()
        oCloud.cloudfill(score)
        oCloud.draw()

    if score > 5000:
        stage = 4

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
        waterRect = oWater.getRect()
        if basketRect.colliderect(objectRect) and oObject.collision_time == 0:

            print(f'{oObject.Type} has collided with the Penguin')

            score += oObject.points
            oObject.collide(pygame.time.get_ticks())
            oWater.waterfill(score)

        elif oObject.collision_time != 0 and oObject.disappear(pygame.time.get_ticks(), COLLISION_TIME_DELAY) == True:
            objectList.remove(oObject)
            oObject.reset()

    oWater.draw()
    # 10 - Draw the screen elements
    for oObject in objectList:
        oObject.draw()  # tell each ball to draw itself

    oRestartButton.draw()
    oPenguin.draw()
    oDisplay.draw()

    # 11 - Update the screen
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make PyGame wait the correct amount
