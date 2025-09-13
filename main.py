import curses
import os
from sqlite3 import Cursor
from time import sleep


PLAYABLE_AREA_SIZE_X = 50
PLAYABLE_AREA_SIZE_Y = 10

BOARD_SIZE_X = PLAYABLE_AREA_SIZE_X + 2
BOARD_SIZE_Y = PLAYABLE_AREA_SIZE_Y

DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_RIGHT,
    curses.KEY_LEFT: curses.KEY_LEFT,
    curses.KEY_UP: curses.KEY_UP,
    curses.KEY_DOWN: curses.KEY_DOWN,
    97: curses.KEY_LEFT, # a
    65: curses.KEY_LEFT, # A
    115: curses.KEY_DOWN, # s
    83: curses.KEY_DOWN, # S
    100: curses.KEY_RIGHT, # d
    68: curses.KEY_RIGHT, # D
    119: curses.KEY_UP, # w
    87: curses.KEY_UP, # W
}

SNAKE_HEAD_DICT = {
    curses.KEY_RIGHT: '>',
    curses.KEY_LEFT: '<',
    curses.KEY_UP: '^',
    curses.KEY_DOWN: 'v',
}



def reset_board():
    return [[" " for i in range(PLAYABLE_AREA_SIZE_X)] for i in range(PLAYABLE_AREA_SIZE_Y)]


def draw_board(win, board):

    win.addstr(BOARD_SIZE_X*"-")
    win.addstr("\n")
    for row in board:
        win.addstr("|")
        for cell in row:
            win.addstr(cell)
        win.addstr("|")
        win.addstr("\n")

    win.addstr(BOARD_SIZE_X*"-")

def put_snake(board, x, y, direction):
    board[y][x] = SNAKE_HEAD_DICT[direction]

def put_fruit(board):
    pass

#TODO make a way to update the snake's position maybe class??

def update_snake_position(direction):
    if direction == curses.KEY_RIGHT:
        snake_x += 1
    elif direction == curses.KEY_LEFT:
        snake_x -= 1
    elif direction == curses.KEY_UP:
        snake_y -= 1
    elif direction == curses.KEY_DOWN:
        snake_y += 1


def main(win):




    curses.curs_set(0)
    win.nodelay(True)
    key = ""
    win.clear()
    win.addstr("Start")
    win.timeout(500)

    board = reset_board()
    put_snake(board)
    put_fruit(board)

    while True:
        try:
            key = win.getch()
            snake_direction = directions.get(key)

            win.clear()

            draw_board(win, board)
            put_snake(board)
            put_fruit(board)
            update_snake_position()
            board[1][1] = snake_direction
            if key == os.linesep:
                break
        except Exception:
            pass



curses.wrapper(main)