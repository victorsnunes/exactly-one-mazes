from enum import Enum
from turtle import pos

testBoard = [
    [5, 5, 5, 7, 7, 0],
    [0, 4, 5, 7, 6, 0],
    [0, 4, 0, 7, 6, 8],
    [0, 4, 4, 6, 6, 8],
    [0, 3, 3, 3, 8, 8],
    [0, 0, 0, 3, 0, 0],
]

def main():

    print("Welcome to the Only One Mazes puzzle!\n\n")

    
    print("Choose the game mode:\n")
    print("1. Human Mode\n")
    print("2. Computer Solve\n\n")
    
    print("Input: ")
    game_mode = input()
    
    if (game_mode == 1):
        humanPlay(testBoard)
    elif (game_mode == 2):
        pass



    return True

class Position:
    def __init__(self, x_pos = 0, y_pos = 0):
        self.x = x_pos
        self.y = y_pos

class Operation(Enum):
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3


def Lvisited(board, x, y):
    return False

def possibleOperations(board, position):
    operations = []


    #Check if it's possible to move up
    if position.y + 1 < board.length and (board[position.x][position.y + 1] != 2) and not Lvisited(board, position.x, position.y + 1):
        operations.append(Operation.MOVE_UP)

    #Check if it's possible to move right
    if position.x + 1 < board.length and (board[position.x + 1][position.y] != 2) and not Lvisited(board, position.x + 1, position.y):
        operations.append(Operation.MOVE_RIGHT)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1] != 2) and not Lvisited(board, position.x, position.y - 1):
        operations.append(Operation.MOVE_DOWN)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y] != 2) and not Lvisited(board, position.x - 1, position.y):
        operations.append(Operation.MOVE_LEFT)

def gameOver(board):
    n = len(board)
    if board[n - 1][n - 1] == 19:
        return True
    return False

def humanPlay(board):

    position = Position()

    operationsList = possibleOperations(board, position)

if __name__ == "__main__":
   main()