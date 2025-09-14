from ast import List
import curses
import os
import time
from xxlimited import new

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

OPPOSITE_DIRECTIONS = {
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT,
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
}

SNAKE_HEAD_DICT = {
    curses.KEY_RIGHT: '>',
    curses.KEY_LEFT: '<',
    curses.KEY_UP: '^',
    curses.KEY_DOWN: 'v',
}


class Snake:
    x = 5
    y = 5
    direction = curses.KEY_RIGHT

    def get_current_head_object(self):
        return SNAKE_HEAD_DICT[self.direction]
    
    def update_direction(self, key):
        new_direction = DIRECTIONS.get(key)
        if new_direction and not is_opposite_direction(new_direction, self.direction):
            self.direction = new_direction

    def move(self):

        if self.direction == curses.KEY_RIGHT:
            self.x += 1
        elif self.direction == curses.KEY_LEFT:
            self.x -= 1
        elif self.direction == curses.KEY_UP:
            self.y -= 1
        elif self.direction == curses.KEY_DOWN:
            self.y += 1


    def __repr__(self):
        return f"X:{self.x} Y:{self.y} dir:{self.direction}"


class Board:

    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self.board = [[" " for i in range(PLAYABLE_AREA_SIZE_X)] for i in range(PLAYABLE_AREA_SIZE_Y)]

    def put_object(self, obj_x, obj_y, obj):
        self.reset_board()
        self.board[obj_y][obj_x] = obj


class Terminal:

    def __init__(self, curses_terminal):
        curses.curs_set(0)

        self.cli = curses_terminal
        self.cli.nodelay(1)
        self.cli.clear()
        self.cli.addstr("Start")
        # self.cli.timeout(500)

    def log(self, snake, iteration):
        self.cli.addstr(str(snake))
        self.cli.addstr(" ")
        self.cli.addstr(str(iteration))
        self.cli.addstr("\n")

    def clear(self):
        self.cli.clear()

    def get_key_pressed(self):
        return self.cli.getch()


    def draw_board(self, board):

        self.cli.addstr(BOARD_SIZE_X*"-")
        self.cli.addstr("\n")
        for row in board.board:
            self.cli.addstr("|")
            for cell in row:
                self.cli.addstr(cell)
            self.cli.addstr("|")
            self.cli.addstr("\n")

        self.cli.addstr(BOARD_SIZE_X*"-")




def main(curses_terminal):
    snake = Snake()
    board = Board()
    terminal = Terminal(curses_terminal)

    terminal.draw_board(board)
    
    key = ""
    iter = 0
    while True:
        try:
            key = terminal.get_key_pressed()
            snake.update_direction(key)

            terminal.clear()

            terminal.log(snake, iter)
            iter +=1

            snake.move()
            board.put_object(snake.x, snake.y, snake.get_current_head_object())
            terminal.draw_board(board)
            time.sleep(0.5)
            if key == os.linesep:
                break
        except Exception:
            pass



def is_opposite_direction(new_direction, current_direction):
    opposite = OPPOSITE_DIRECTIONS[current_direction]
    return opposite == new_direction


curses.wrapper(main)