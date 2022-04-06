from util import Operation
from screen import Screen 
import time
import random
import pygame

testBoard = [
    [5, 5, 5, 7, 7, 0],
    [0, 3, 5, 7, 6, 0],
    [0, 3, 0, 7, 6, 8],
    [0, 3, 3, 6, 6, 8],
    [0, 4, 4, 4, 8, 8],
    [1, 0, 0, 4, 0, 0],
]

def main():
        
    screen = Screen()
    
    running = True
    while running:
        print("Restarting...")
        testBoard = [
            [5, 5, 5, 7, 7, 0],
            [0, 3, 5, 7, 6, 0],
            [0, 3, 0, 7, 6, 8],
            [0, 3, 3, 6, 6, 8],
            [0, 4, 4, 4, 8, 8],
            [1, 0, 0, 4, 0, 0],
        ]
        screen.set_up(testBoard)
        running = autoPlay(testBoard, screen)
        
    pygame.quit()
    print("quitting...")

# Input Handler
def getKeyPress():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return Operation.MOVE_LEFT
            elif event.key == pygame.K_UP:
                return Operation.MOVE_UP
            elif event.key == pygame.K_RIGHT:
                return Operation.MOVE_RIGHT
            elif event.key == pygame.K_DOWN:
                return Operation.MOVE_DOWN
            elif event.key == pygame.K_r:
                return Operation.RESTART 
        elif event.type == pygame.QUIT:
            return Operation.QUIT
    
def printBoard(board):
    for line in board:
        print(line)

# Data Structure Position
class Position:
    def __init__(self, x_pos = 0, y_pos = 0):
        self.x = x_pos
        self.y = y_pos

class LShapedFigure:

    def __init__(self, num):
        self.value = num
        self.visited = False
    
    def visit(self):
        self.visited = True

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            getattr(other, 'value', None) == self.value)

    def __hash__(self):
        return hash(str(self.value))

def LnotVisited(element, l_figures):
    return element == 0 or element in l_figures

def possibleOperations(board, position, l_figures):
    operations = []

    #Check if it's possible to move up
    if position.y + 1 < len(board) and (board[position.x][position.y + 1] != 2) and LnotVisited(board[position.x][ position.y + 1], l_figures):
        operations.append(Operation.MOVE_RIGHT)

    #Check if it's possible to move right
    if position.x + 1 < len(board) and (board[position.x + 1][position.y] != 2) and LnotVisited(board[position.x + 1][ position.y], l_figures):
        operations.append(Operation.MOVE_DOWN)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1] != 2) and LnotVisited(board[position.x][ position.y - 1], l_figures):
        operations.append(Operation.MOVE_LEFT)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y] != 2) and LnotVisited(board[position.x - 1][ position.y], l_figures):
        operations.append(Operation.MOVE_UP)

    return operations

def makeMove(board, position, op, l_figures):
    board[position.x][position.y] = 2
    if op == Operation.MOVE_RIGHT:
        position.y += 1
    if op == Operation.MOVE_DOWN:
        position.x += 1
    if op == Operation.MOVE_LEFT:
        position.y -= 1
    if op == Operation.MOVE_UP:
        position.x -= 1

    element = board[position.x][position.y]
    if (element in l_figures):
        l_figures.remove(element)
    board[position.x][position.y] = 1

def gameOver(board):
    n = len(board)
    return board[0][len(board) - 1] == 1

def humanPlay(board, screen):

    #Scan the board and stores all its L shaped figures
    l_figures = set()
    for row in board:
        for element in row:
            if element >= 3:
                l_figures.add(element)

    position = Position(len(board) - 1 ,0)

    while True:
        
        possibleOps = possibleOperations(board, position, l_figures)
        screen.draw_board(board, possibleOps)
        move = getKeyPress()

        if move in possibleOps:
            makeMove(board, position, move, l_figures)
            printBoard(board)
            print("\n")
            print(possibleOps) 

        if move == Operation.RESTART:
            return True

        if gameOver(board) or move == Operation.QUIT:
            return False

def autoPlay(board, screen):
    #Scan the board and stores all its L shaped figures
    l_figures = set()
    for row in board:
        for element in row:
            if element >= 3:
                l_figures.add(element)
    listOfOperators = list(Operation)
    position = Position(len(board) - 1 ,0)
    while True:
         
        possibleOps = possibleOperations(board, position, l_figures)
        screen.draw_board(board, possibleOps)
        move = random.choice(listOfOperators)
        time.sleep(1)

        if move in possibleOps:
            makeMove(board, position, move, l_figures)
            printBoard(board)
            print("\n")
            print(possibleOps) 

        if move == Operation.RESTART:
            return True

        if gameOver(board) or move == Operation.QUIT:
            return False
    

if __name__ == "__main__":
   main()