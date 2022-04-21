from traceback import print_tb
from util import Operation, Square, Color
from screen import Screen 
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
        running = humanPlay(testBoard, screen)
        
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

def LnotVisited(element, l_figures):
    return element == 0 or element in l_figures

def possibleOperations(board, position, l_figures):
    operations = []

    #Check if it's possible to move up
    if position.y + 1 < len(board) and (board[position.x][position.y + 1].value != 2) and LnotVisited(board[position.x][ position.y + 1].value, l_figures):
        operations.append(Operation.MOVE_RIGHT)

    #Check if it's possible to move right
    if position.x + 1 < len(board) and (board[position.x + 1][position.y].value != 2) and LnotVisited(board[position.x + 1][ position.y].value, l_figures):
        operations.append(Operation.MOVE_DOWN)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1].value != 2) and LnotVisited(board[position.x][ position.y - 1].value, l_figures):
        operations.append(Operation.MOVE_LEFT)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y].value != 2) and LnotVisited(board[position.x - 1][ position.y].value, l_figures):
        operations.append(Operation.MOVE_UP)

    return operations

def makeMove(board, position, op, l_figures):
    board[position.x][position.y].value = 2
    if op == Operation.MOVE_RIGHT:
        position.y += 1
    if op == Operation.MOVE_DOWN:
        position.x += 1
    if op == Operation.MOVE_LEFT:
        position.y -= 1
    if op == Operation.MOVE_UP:
        position.x -= 1

    element = board[position.x][position.y].value
    if (element in l_figures):
        l_figures.remove(element)
    board[position.x][position.y].value = 1

def gameOver(board):
    n = len(board)
    return board[0][len(board) - 1].value == 1

def boardSetUp(board, l_figures):

    color_dict = {0: Color.WHITE.value}

    for i in range(len(board)):
        for j in range(len(board[0])):

            element = board[i][j]

            if (element not in l_figures) and (element >= 3):
                l_figures.add(element)
                color_index = (element - 3) % len(Color.L_colors.value)
                color_dict[element] = Color.L_colors.value[color_index]

            if (element != 1):
                board[i][j] = Square(element, color_dict[element])
            else:
                board[i][j] = Square(1, Color.WHITE.value)


def humanPlay(board, screen):

    #Scan the board and stores all its L shaped figures
    l_figures = set()
    boardSetUp(board, l_figures)
    screen.set_up(board)

    position = Position(len(board) - 1 ,0)

    while True:
        
        possibleOps = possibleOperations(board, position, l_figures)
        if (possibleOps == []):
            print("No more possible moves. You lost!")
            return False
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
            if (l_figures == set()):
                print("Congratulations! You won!")
            else:
                print("You did't pass through all the L figures. You lost!")
            return False

if __name__ == "__main__":
   main()