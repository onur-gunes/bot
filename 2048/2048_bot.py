from PIL import ImageGrab, ImageOps
import pyautogui
import time

# print(pyautogui.displayMousePosition())
currentGrid = [0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0,
               0, 0, 0, 0]

UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103

scoreGrid = [99,  40, 25, 10,
             30,  -10,  5, 0,
             15,  5,   0, 0,
             5,   0,   0, 0]


class Cords:
    cord11 = (320, 400)
    cord12 = (440, 400)
    cord13 = (560, 400)
    cord14 = (680, 400)

    cord21 = (320, 520)
    cord22 = (440, 520)
    cord23 = (560, 520)
    cord24 = (680, 520)

    cord31 = (320, 640)
    cord32 = (440, 640)
    cord33 = (560, 640)
    cord34 = (680, 640)

    cord41 = (320, 760)
    cord42 = (440, 760)
    cord43 = (560, 760)
    cord44 = (680, 760)

    corArray = [cord11, cord12, cord13, cord14,
                cord21, cord22, cord23, cord24,
                cord31, cord32, cord33, cord34,
                cord41, cord42, cord43, cord44]


class Values:
    empty = 195
    two = 229
    four = 225
    eight = 190
    sixteen = 172
    thirtyTwo = 157
    sixtyFour = 135
    oneTwentyEight = 205
    twoFiftySix = 201
    fiveOneTwo = 197
    oneZeroTwoFour = 193
    twoZeroFourEight = 189

    valueArray = [empty,
                  two,
                  four,
                  eight,
                  sixteen,
                  thirtyTwo,
                  sixtyFour,
                  oneTwentyEight,
                  twoFiftySix,
                  fiveOneTwo,
                  oneZeroTwoFour,
                  twoZeroFourEight]


def getGrid():
    image = ImageGrab.grab()
    grayImage = ImageOps.grayscale(image)
    for index, cord in enumerate(Cords.corArray):
        pixel = grayImage.getpixel(cord)
        pos = Values.valueArray.index(pixel)
        if pos == 0:
            currentGrid[index] = 0
        else:
            currentGrid[index] = pow(2, pos)


def printGrid(grid):
    for i in range(16):
        if i % 4 == 0:
            print("[ " + str(grid[i]) + " " + str(grid[i + 1]) +
                  " " + str(grid[i + 2]) + " " + str(grid[i + 3]) + " ]")


def swipeRow(row):
    prev = -1
    i = 0
    temp = [0, 0, 0, 0]

    for element in row:
        if element != 0:
            if prev == -1:
                prev = element
                temp[i] = element
                i += 1
            elif prev == element:
                temp[i - 1] = 2 * prev
                prev = -1
            else:
                prev = element
                temp[i] = element
                i += 1

    return temp


def getNextGrid(grid, move):
    temp = [0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0]

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * j] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i + 4 * (3 - j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i + 4 * (3 - j)] = val

    elif move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[4 * i + (3 - j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[4 * i + (3 - j)] = val

    return temp


def getScore(grid):
    score = 0
    if grid[1] == grid[4] & grid[1] > 8:
        scoreGrid[5] = 70
        scoreGrid[4] = 16
    else:
        scoreGrid[5] = -10
        scoreGrid[4] = 30
    for i in range(4):
        for j in range(4):
            score += grid[4 * i + j]**1.1 * scoreGrid[4 * i + j]
    return score


def getBestMove(grid):
    scoreUp = getScore(getNextGrid(grid, UP))
    scoreDown = 0.1
    # getScore(getNextGrid(grid, DOWN))
    scoreLeft = getScore(getNextGrid(grid, LEFT))
    scoreRight = getScore(getNextGrid(grid, RIGHT))

    if not isMoveValid(grid, UP):
        scoreUp = 0
    if not isMoveValid(grid, DOWN):
        scoreDown = 0
    if not isMoveValid(grid, LEFT):
        scoreLeft = 0
    if not isMoveValid(grid, RIGHT):
        scoreRight = 0

    maxScore = max(scoreDown, scoreUp, scoreLeft, scoreRight)

    if scoreUp == maxScore:
        return UP
    elif scoreDown == maxScore:
        return DOWN
    elif scoreLeft == maxScore:
        return LEFT
    else:

        return RIGHT


def isMoveValid(grid, move):
    if getNextGrid(grid, move) == grid:
        return False
    else:
        return True


def performMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        time.sleep(0.05)
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        time.sleep(0.05)
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        time.sleep(0.05)
        pyautogui.keyUp('left')
    else:
        pyautogui.keyDown('right')
        time.sleep(0.05)
        pyautogui.keyUp('right')


def main():
    time.sleep(3)
    while True:
        getGrid()
        performMove(getBestMove(currentGrid))
        time.sleep(0.1)


if __name__ == '__main__':
    main()
