from enum import Enum
import pygame

testBoard = [
    [5, 5, 5, 7, 7, 0],
    [0, 4, 5, 7, 6, 0],
    [0, 4, 0, 7, 6, 8],
    [0, 4, 4, 6, 6, 8],
    [0, 3, 3, 3, 8, 8],
    [1, 0, 0, 3, 0, 0],
]

def main():

    pygame.init()
    #window = pygame.display.set_mode(300, 300)

    print("Welcome to the Only One Mazes puzzle!\n\n")

    
    print("Choose the game mode:\n")
    print("1. Human Mode\n")
    print("2. Computer Solve\n\n")
    
    print("Input: ")
    game_mode = int(input())
    
    if (game_mode == 1):
        humanPlay(testBoard)
    elif (game_mode == 2):
        pass

    pygame.quit()
    print("quitting...")

def getKeyPress():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return Operation.MOVE_LEFT
            if event.key == pygame.K_UP:
                return Operation.MOVE_UP
            if event.key == pygame.K_RIGHT:
                return Operation.MOVE_RIGHT
            if event.key == pygame.K_DOWN:
                return Operation.MOVE_DOWN

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
    MOVE_UP = "up"
    MOVE_RIGHT = "right"
    MOVE_DOWN = "down"
    MOVE_LEFT = "left"


def Lvisited(board, x, y):
    return False

def possibleOperations(board, position):
    operations = []


    #Check if it's possible to move up
    if position.y + 1 < len(board) and (board[position.x][position.y + 1] != 2) and not Lvisited(board, position.x, position.y + 1):
        operations.append(Operation.MOVE_RIGHT)

    #Check if it's possible to move right
    if position.x + 1 < len(board) and (board[position.x + 1][position.y] != 2) and not Lvisited(board, position.x + 1, position.y):
        operations.append(Operation.MOVE_DOWN)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1] != 2) and not Lvisited(board, position.x, position.y - 1):
        operations.append(Operation.MOVE_LEFT)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y] != 2) and not Lvisited(board, position.x - 1, position.y):
        operations.append(Operation.MOVE_UP)

    return operations

def makeMove(board, position, op):
    board[position.x][position.y] = 2
    #TODO: Add the l in the visited list
    if op == Operation.MOVE_RIGHT:
        position.y += 1
    if op == Operation.MOVE_DOWN:
        position.x += 1
    if op == Operation.MOVE_LEFT:
        position.y -= 1
    if op == Operation.MOVE_UP:
        position.x -= 1
    board[position.x][position.y] = 1

def gameOver(board):
    n = len(board)
    return board[0][len(board) - 1] == 1

def humanPlay(board):

    #Scan the board and stores all its L shaped figures
    l_figures = set()
    for row in board:
        for element in row:
            if element >= 3:
                l_figures.add(LShapedFigure(element))

    position = Position(len(board) - 1 ,0)

    print("x = ", position.x)
    print("y = ", position.y)

    while True:
        printBoard(board)
        print("x = ", position.x)
        print("y = ", position.y)
        possibleOps = possibleOperations(board, position)

        print("\nPossible moves: ")
        for op in possibleOps:
            print(op)

        print("\n\n")

        while True:

            ans = input()

            if (ans == "up"):
                chosen_move = Operation.MOVE_UP

            if (ans == "right"):
                chosen_move = Operation.MOVE_RIGHT

            if (ans == "down"):
                chosen_move = Operation.MOVE_DOWN

            if (ans == "left"):
                chosen_move = Operation.MOVE_LEFT


            if (chosen_move in possibleOps):
                break

        makeMove(board, position, chosen_move) 

        '''
        move = getKeyPress()
        
        if move in possibleOps:
            makeMove(board, position, move)
        '''

        if gameOver(board):
            break

if __name__ == "__main__":
   main()