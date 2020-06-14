import pyautogui
import cv2
import numpy
import PIL
import time


def main():
    dimensions_of_board = (18, 170, 498, 650)
    original_board = capture_board(dimensions_of_board)
    size_of_board = vertical_line_detector(original_board)
    size_of_square = (
        dimensions_of_board[2] - dimensions_of_board[0]) / size_of_board
    # centre_of_circles = locate_colors()
    board_of_pixels = create_pixel_board(
        dimensions_of_board, size_of_board, size_of_square)
    board_of_colors = create_color_board(board_of_pixels, size_of_board)
    # print(board_of_colors)
    solved_board = solveboard(board_of_colors, size_of_board)
    print(solved_board)


def solveboard(unsolved_board, size_of_board):
    characters_that_are_ends = ['b', 'r', 'g', 'y', 'o',
                                'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w']
    original_unsolved_board = unsolved_board
    unsolved_board_with_x = boardX(
        unsolved_board, size_of_board, characters_that_are_ends)
    unsolved_board = forced_move_check(
        unsolved_board, size_of_board, characters_that_are_ends)

    solved_color_board = board_output(unsolved_board, size_of_board)
    # print(solved_color_board)
    solved_color_board_l = numpy.core.defchararray.lower(solved_color_board)
    board_with_x_l = numpy.core.defchararray.lower(unsolved_board)
    solved_number_board = unsolved_board

    for i in (characters_that_are_ends):
        a = 1
        if i in solved_color_board_l:
            for k in range(size_of_board + 2):
                for l in range(size_of_board + 2):
                    if board_with_x_l[k][l] == unsolved_board_with_x[k][l]:
                        solved_number_board[k][l] = 1
                        a += 1

    print(solved_number_board)
    return(solved_color_board_l)
    '''
    if original_unsolved_board != unsolved_board:
        solveboard(unsolved_board)
    else:
        pass
    return(unsolved_board)
    '''


def boardX(unsolved_board, size_of_board, characters_that_are_ends):
    board_with_x = numpy.zeros(
        (size_of_board + 2, size_of_board + 2), dtype=str)
    for i in range(size_of_board + 2):
        for j in range(size_of_board + 2):
            board_with_x[i, j] = 'X'
    for i in range(size_of_board):
        for j in range(size_of_board):
            board_with_x[i + 1, j + 1] = unsolved_board[i, j]

    unsolved_board_with_x = board_with_x
    return(unsolved_board_with_x)


def forced_move_check(unsolved_board, size_of_board, characters_that_are_ends):
    board_with_x = numpy.zeros(
        (size_of_board + 2, size_of_board + 2), dtype=str)
    for i in range(size_of_board + 2):
        for j in range(size_of_board + 2):
            board_with_x[i, j] = 'X'
    for i in range(size_of_board):
        for j in range(size_of_board):
            board_with_x[i + 1, j + 1] = unsolved_board[i, j]

    print(board_with_x)
    print(size_of_board)

    er1 = True
    er2 = True
    er3 = True
    er4 = True
    num = 0
    while (er1 or er2 or er3 or er4):
        num += 1

        if num == 10000:
            print(board_with_x)
            er1 = False
            er2 = False
            er3 = False
            er4 = False
        if numpy.all(numpy.core.defchararray.isupper(board_with_x)):
            er1 = False
            er2 = False
            er3 = False
            er4 = False
        else:
            for i in range(1, size_of_board + 1):
                for j in range(1, size_of_board + 1):
                    # check connection
                    if board_with_x[i, j] in characters_that_are_ends:
                        if board_with_x[i, j + 1] == board_with_x[i, j] and (str.islower(board_with_x[i, j]) or str.islower(board_with_x[i, j + 1])):
                            #board_with_x[i, j + 1] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            board_with_x[i, j + 1] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j + 1])

                        elif board_with_x[i, j - 1] == board_with_x[i, j]and (str.islower(board_with_x[i, j]) or str.islower(board_with_x[i, j - 1])):
                            #board_with_x[i, j - 1] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            board_with_x[i, j - 1] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j - 1])

                        elif board_with_x[i - 1, j] == board_with_x[i, j]and (str.islower(board_with_x[i, j]) or str.islower(board_with_x[i - 1, j])):
                            #board_with_x[i - 1, j] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            board_with_x[i - 1, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i - 1, j])

                        elif board_with_x[i + 1, j] == board_with_x[i, j]and (str.islower(board_with_x[i, j]) or str.islower(board_with_x[i + 1, j])):
                            #board_with_x[i + 1, j] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            board_with_x[i + 1, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i + 1, j])

                        # check right
                        elif board_with_x[i - 1, j] != '0' and board_with_x[i, j - 1] != '0' and board_with_x[i + 1, j] != '0'and board_with_x[i, j + 1] == '0':
                            board_with_x[i, j + 1] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            er1 = True
                            er2 = True
                            er3 = True
                            er4 = True
                        else:
                            er1 = False

                    # check left
                    if board_with_x[i, j] in characters_that_are_ends:
                        if board_with_x[i - 1, j] != '0' and board_with_x[i, j - 1] == '0' and board_with_x[i + 1, j] != '0'and board_with_x[i, j + 1] != '0':
                            board_with_x[i, j - 1] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            er1 = True
                            er2 = True
                            er3 = True
                            er4 = True
                        else:
                            er2 = False
                    # check up
                    if board_with_x[i, j] in characters_that_are_ends:
                        if board_with_x[i - 1, j] == '0' and board_with_x[i, j - 1] != '0' and board_with_x[i + 1, j] != '0'and board_with_x[i, j + 1] != '0':
                            board_with_x[i - 1, j] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            er1 = True
                            er2 = True
                            er3 = True
                            er4 = True
                        else:
                            er3 = False
                    # check down
                    if board_with_x[i, j] in characters_that_are_ends:
                        if board_with_x[i - 1, j] != '0' and board_with_x[i, j - 1] != '0' and board_with_x[i + 1, j] == '0'and board_with_x[i, j + 1] != '0':
                            board_with_x[i + 1, j] = board_with_x[i, j]
                            board_with_x[i, j] = numpy.core.defchararray.capitalize(
                                board_with_x[i, j])
                            er1 = True
                            er2 = True
                            er3 = True
                            er4 = True
                        else:
                            pass
                            #er4 = False

    # print(board_with_x)
    print(num)
    return(board_with_x)


def board_output(board_with_x, size_of_board):
    board_out_x = numpy.empty((size_of_board, size_of_board), dtype=str)
    for i in range(1, size_of_board + 1):
        for j in range(1, size_of_board + 1):
            board_out_x[i - 1][j - 1] = board_with_x[i][j]

    # print(board_out_x)
    return(board_out_x)


'''

        # check left
        for i in range(1, size_of_board + 1):
            for j in range(1, size_of_board + 1):
                if board_with_x[i, j] in characters_that_are_ends:
                    if board_with_x[i - 1, j] != '0' and board_with_x[i, j - 1] == '0' and board_with_x[i + 1, j] != '0'and board_with_x[i, j + 1] != '0':
                        board_with_x[i, j - 1] = board_with_x[i, j]
                        board_with_x[i, j] = numpy.core.defchararray.capitalize(
                            board_with_x[i, j])
                        er1 = True
                        er2 = True
                        er3 = True
                        er4 = True
                    else:
                        er2 = False

        # check up
        for i in range(1, size_of_board + 1):
            for j in range(1, size_of_board + 1):
                if board_with_x[i, j] in characters_that_are_ends:

                    if board_with_x[i - 1, j] == '0' and board_with_x[i, j - 1] != '0' and board_with_x[i + 1, j] != '0'and board_with_x[i, j + 1] != '0':
                        board_with_x[i - 1, j] = board_with_x[i, j]
                        board_with_x[i, j] = numpy.core.defchararray.capitalize(
                            board_with_x[i, j])
                        er1 = True
                        er2 = True
                        er3 = True
                        er4 = True
                    else:
                        er3 = False
        # check down
        for i in range(1, size_of_board + 1):
            for j in range(1, size_of_board + 1):
                if board_with_x[i, j] in characters_that_are_ends:

                    if board_with_x[i - 1, j] != '0' and board_with_x[i, j - 1] != '0' and board_with_x[i + 1, j] == '0'and board_with_x[i, j + 1] != '0':
                        board_with_x[i + 1, j] = board_with_x[i, j]
                        board_with_x[i, j] = numpy.core.defchararray.capitalize(
                            board_with_x[i, j])
                        er1 = True
                        er2 = True
                        er3 = True
                        er4 = True
                    else:
                        er4 = False
'''


def create_color_board(board_of_pixels, size_of_board):
    dict_of_colors = {(0, 0, 255): 'b', (255, 0, 0): 'r', (0, 128, 0): 'g', (238, 238, 0): 'y', (255, 127, 0): 'o', (255, 0, 255): 'p', (128, 0, 120): 'z', (
        0, 255, 255): 'c', (0, 128, 128): 't', (0, 0, 139): 'd', (166, 166, 166): 'q', (189, 183, 107): 's', (0, 255, 0): 'l', (165, 42, 42): 'm', (255, 255, 255): 'w'}

    board_of_colors = numpy.zeros((size_of_board, size_of_board), dtype=str)
    for i in range(size_of_board):
        for j in range(size_of_board):
            if (pyautogui.pixel(board_of_pixels[i, j][0], board_of_pixels[i, j][1])) in dict_of_colors.keys():
                board_of_colors[i][j] = dict_of_colors[pyautogui.pixel(
                    board_of_pixels[i, j][0], board_of_pixels[i, j][1])]
            else:
                board_of_colors[i][j] = '0'
    return(board_of_colors)


def create_pixel_board(dimensions_of_board, size_of_board, size_of_square):
    x_dim, y_dim = dimensions_of_board[0:2]

    board_of_pixels = numpy.zeros((size_of_board, size_of_board), dtype=object)
    for i in range(size_of_board):
        for j in range(size_of_board):
            board_of_pixels[i, j] = (int(x_dim + j * size_of_square + 0.5 * size_of_square),
                                     int(y_dim + i * size_of_square + 0.5 * size_of_square))
    return(board_of_pixels)


def capture_board(dimensions_of_board):
    image_of_board = numpy.array(
        PIL.ImageGrab.grab(bbox=(dimensions_of_board)))
    image_of_board = cv2.cvtColor(image_of_board, cv2.COLOR_BGR2RGB)
    return(image_of_board)


def vertical_line_detector(image):
    line_tolerance = 5
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edge_image = cv2.Canny(gray_image, threshold1=100,
                           threshold2=200, apertureSize=3)
    lines = cv2.HoughLinesP(image=edge_image, rho=1, theta=numpy.pi,
                            threshold=100, lines=numpy.array([]), minLineLength=400, maxLineGap=5)

    lines_to_keep = []
    for line1 in lines:
        for line2 in lines:
            if line1[0][0] < line2[0][0] and line1[0][0] + line_tolerance > line2[0][0]:
                lines_to_keep.append(line1)
    lines_to_keep = numpy.array(lines_to_keep)

    return(len(lines_to_keep) - 1)


main()
