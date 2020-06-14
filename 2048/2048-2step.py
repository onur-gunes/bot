import numpy as np
import random
import math
import sys


sys.setrecursionlimit(10000)
UP = 100
LEFT = 101
DOWN = 102
RIGHT = 103

currentGrid = np.zeros((4, 4))

scoreGrid = [[99,  60, 40, 10],
             [0,  0,  0, 0],
             [0,  0,  0, 0],
             [0,  0,  0, 0]]


def createGame():
    global currentGrid
    currentGrid = np.zeros((4, 4))

    while (np.count_nonzero(currentGrid) < 2):
        currentGrid[random.randint(0, 3)][random.randint(
            0, 3)] = 2 * math.ceil(random.randint(1, 10) / 9.0)


'''
    print('the game is:')
    print(currentGrid, '\n')
'''


def isMoveValid(grid, move):
    if np.array_equal(getNextGrid(grid, move), grid):
        return False
    else:
        return True


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
    temp = np.zeros((4, 4))

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[j][i])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[j][i] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i][j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i][j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[3 - j][i])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[3 - j][i] = val

    if move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i][3 - j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i][3 - j] = val

    return temp


def getNextGrid2(grid, move):
    temp = np.zeros((4, 4))

    if move == UP:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[j][i])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[j][i] = val

    elif move == LEFT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i][j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i][j] = val

    elif move == DOWN:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[3 - j][i])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[3 - j][i] = val

    if move == RIGHT:
        for i in range(4):
            row = []
            for j in range(4):
                row.append(grid[i][3 - j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                temp[i][3 - j] = val

    return temp


def getScore(grid):
    score = 0
    for i in range(4):
        for j in range(4):
            score += grid[i][j] * scoreGrid[i][j]
    return score


def getBestMove(grid):
    scoreUp = max(getScore(getNextGrid2(getNextGrid(grid, UP), UP)), getScore(getNextGrid2(getNextGrid(grid, UP), DOWN)), getScore(
        getNextGrid2(getNextGrid(grid, UP), LEFT)), getScore(getNextGrid2(getNextGrid(grid, UP), RIGHT)))
    scoreDown = 0.1
    # getScore(getNextGrid(grid, DOWN))
    scoreLeft = max(getScore(getNextGrid2(getNextGrid(grid, UP), LEFT)), getScore(getNextGrid2(getNextGrid(grid, UP), DOWN)), getScore(
        getNextGrid2(getNextGrid(grid, UP), LEFT)), getScore(getNextGrid2(getNextGrid(grid, UP), RIGHT)))
    scoreRight = max(getScore(getNextGrid2(getNextGrid(grid, UP), RIGHT)), getScore(getNextGrid2(getNextGrid(grid, UP), DOWN)), getScore(
        getNextGrid2(getNextGrid(grid, UP), LEFT)), getScore(getNextGrid2(getNextGrid(grid, UP), RIGHT)))

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


def performMove(grid, move):
    global currentGrid
    currentGrid = getNextGrid(grid, move)

    a = random.randint(0, 3)
    b = random.randint(0, 3)
    while (currentGrid[a][b] != 0):
        a = random.randint(0, 3)
        b = random.randint(0, 3)
    currentGrid[a][b] = 2 * math.ceil(random.randint(1, 10) / 9.0)
    '''
    print(move, '\n')
    print('updated grid is:')
    print(currentGrid, '\n')
'''


def main():
    createGame()
    # performMove(currentGrid, getBestMove(currentGrid))
    a = 0
    score = 0
    while ((np.count_nonzero(currentGrid) != 16) or (isMoveValid(currentGrid, UP) or isMoveValid(currentGrid, DOWN) or isMoveValid(currentGrid, LEFT) or isMoveValid(currentGrid, RIGHT))):
        performMove(currentGrid, getBestMove(currentGrid))
        a += 1
    score = np.amax(currentGrid)
    #print(a, '\n')
    return score


avg = 0
for i in range(100):
    avg += main() / 100
print(avg)
