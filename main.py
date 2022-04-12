import time
import random
from copy import deepcopy

grid = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0],
  [6, 7, 2, 0, 9, 5, 3, 4, 8],
  [1, 9, 0, 3, 4, 2, 0, 6, 7],
  [8, 0, 0, 7, 6, 1, 4, 2, 0],
  [0, 2, 6, 0, 0, 3, 0, 0, 1],
  [7, 1, 3, 9, 2, 4, 0, 0, 6],
  [9, 0, 0, 0, 3, 7, 0, 8, 0],
  [2, 0, 7, 0, 0, 9, 6, 0, 5],
  [0, 4, 5, 2, 8, 0, 0, 7, 9]
]

class Solver:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def blockcheck(self):
        self.block = (int((self.y)/3)*3 + int((self.x)/3)) + 1 #checks in which 3x3 block the Solver is in
    
    def block_ables(self,board):
        ables = list(range(1,10))
        startx = ((self.block-1)%3)*3
        starty = int((self.block-1)/3)*3
        for x in range(0,3):
            for y in range(0,3):
                if board[starty+y][startx+x] in ables:
                    ables.remove(board[starty+y][startx+x])
        return ables
    
    def line_ables(self,board):
        ables = list(range(1,10))
        for x in board[self.y]:
            if x in ables:
                ables.remove(x)
        return ables

    def column_ables(self,board):
        ables = list(range(1,10))
        for y in board:
            if y[self.x] in ables:
                ables.remove(y[self.x])
        return ables

    def fill(self,board):
        ables = []
        for x in range(1,10):
            if x in self.block_ables(board) and x in self.line_ables(board) and x in self.column_ables(board):
                ables.append(x)
        if len(ables) > 0:
            board[self.y][self.x] = random.choice(ables)
            return True
        else:
            return False

def imput_validator(board):
    startx = 0
    starty = 0
    while starty < 9:
        in_block = []
        for x in range(0,3):
            for y in range(0,3):
                if board[starty+y][startx+x] not in in_block:
                    if board[starty+y][startx+x] != 0:
                        in_block.append(board[starty+y][startx+x])
                else:
                    return (False, f'Invalid input. There is at least one repeated element at block {(int((starty)/3)*3 + int((startx)/3)) + 1}')
        if startx + 3 == 9:
            startx = 0
            starty += 3
        else:
            startx += 3
    for y in range(0,9):
        in_line = []
        for x in board[y]:
            if x not in in_line:
                if x != 0:
                    in_line.append(x)
            else:
                return (False, f'Invalid input. There is at least one repeated element at Line {y+1}')
    for y in range(0,9):
        in_column = []
        for x in board:
            if x[y] not in in_column:
                if  x[y] != 0:
                    in_column.append(x[y])
            else:
                return (False, f'Invalid input. There is at least one repeated element at column {y+1}')
    return (True, 'Valid input, solving...')

def event(txt):
    print('')
    print('-='*int((len(txt)/2)+2))
    print(f'  {txt}')
    print('-='*int((len(txt)/2)+2))

def show_board(board):
    for x in range(0,3):
        print('-'*25)
        for z in range(0,3):
            for y in range(0,3):
                print('|',end='')
                print(f' {board[x*3+z][y*3]} {board[x*3+z][y*3+1]} {board[x*3+z][y*3+2]} '.replace('0',' '),end='')
            print('|')
    print('-'*25)

backup = deepcopy(grid)
event('Your imput:')
show_board(grid)
event('Checking for errors...')
if not imput_validator(grid)[0]:
    event(imput_validator(grid)[1])
else:
    event(imput_validator(grid)[1])
    time.sleep(2)
    solver = Solver()
    while True:
        solver.blockcheck()
        if grid[solver.y][solver.x] == 0:
            if not solver.fill(grid):
                solver.x = -1
                solver.y = 0
                grid = deepcopy(backup)
            #print('-='*15)
            #show_board(grid)
            #print(solver.x,solver.y)
            #time.sleep(0.5)  #uncomment these lines for viewing the bot process
        if solver.x+1 == 9:
            solver.x = 0
            solver.y += 1
        else:
            solver.x += 1
        if solver.y == 9:
            break
    event('Solved board:')
    show_board(grid)