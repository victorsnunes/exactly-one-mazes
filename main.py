from enum import Enum
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
    screen.set_up(testBoard)

    """   
    print("Input: ")
    game_mode = int(input())

    print("Welcome to the Only One Mazes puzzle!\n\n")

    
    print("Choose the game mode:\n")
    print("1. Human Mode\n")
    print("2. Computer Solve\n\n")
    
    print("Input: ")
    game_mode = int(input())
    
    if (game_mode == 1):
    elif (game_mode == 2):
        pass 
    """
    humanPlay(testBoard, screen)

    pygame.quit()
    print("quitting...")

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
        elif event.type == pygame.QUIT:
            return Operation.QUIT
    
def printBoard(board):
    for line in board:
        print(line)

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
    

class Operation(Enum):
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    QUIT = 9


def Lvisited(board, x, y):
    return False

def possibleOperations(board, position):
    operations = []

    #Check if it's possible to move up
    if position.y + 1 < len(board) and (board[position.x][position.y + 1] != 2) and not Lvisited(board, position.x, position.y + 1):
        operations.append(Operation.MOVE_UP)

    #Check if it's possible to move right
    if position.x + 1 < len(board) and (board[position.x + 1][position.y] != 2) and not Lvisited(board, position.x + 1, position.y):
        operations.append(Operation.MOVE_RIGHT)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1] != 2) and not Lvisited(board, position.x, position.y - 1):
        operations.append(Operation.MOVE_DOWN)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y] != 2) and not Lvisited(board, position.x - 1, position.y):
        operations.append(Operation.MOVE_LEFT)

    return operations

def operation(board, position, op):
    board[position.x][position.y] = 2
    #TODO: Add the l in the visited list
    if op == Operation.MOVE_UP:
        position.y += 1
    if op == Operation.MOVE_LEFT:
        position.x += 1
    if op == Operation.MOVE_DOWN:
        position.y -= 1
    if op == Operation.MOVE_DOWN:
        position.x -= 1
    board[position.x][position.y] = 1

def gameOver(board):
    n = len(board)
    return board[n - 1][n - 1] == 1

def humanPlay(board, screen):

    #Scan the board and stores all its L shaped figures
    l_figures = set()
    for row in board:
        for element in row:
            if element >= 3:
                l_figures.add(LShapedFigure(element))

    position = Position()

    while True:
        screen.draw_board(board)
        possibleOps = possibleOperations(board, position)

        # print("Choose your move:\n")
        # print("1. Move up\n")
        # print("2. Move right\n")
        # print("3. Move down\n")
        # print("4. Move left\n\n")

        # print("Possible moves: ")
        # for op in possibleOps:
        #     print(op + " ")
        # print("\n\n")

        # input = int(input)
        
        move = getKeyPress()
        
        if move in possibleOps:
            #TODO: Not working, not sure why
            operation(board, position, move)
        
        if gameOver(board) or move == Operation.QUIT:
            break

if __name__ == "__main__":
   main()