from enum import Enum
from copy import deepcopy

class Operation(Enum):
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    RESTART = 4
    QUIT = 9

class Color(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    INDIGO = (75,0,130)
    MAGENTA = (255, 0, 255)
    TEAL = (0, 128, 128)
    LIGHT_CORAL = (240, 128, 128)
    BLACK = (0, 0, 0)

    #TODO: Add more colors to avoid conflicts in the table
    L_colors = [BLUE, GREEN, CYAN, INDIGO, MAGENTA, TEAL, LIGHT_CORAL]


class Position:
    def __init__(self, x_pos=0, y_pos=0):
        self.x = x_pos
        self.y = y_pos

    def getMoveUp(self):
        return Position(self.x - 1, self.y)
    def getMoveRight(self):
        return Position(self.x, self.y + 1)
    def getMoveDown(self):
        return Position(self.x + 1, self.y)
    def getMoveLeft(self):
        return Position(self.x, self.y - 1)

    def moveUp(self):
        self.x -= 1
    def moveRight(self):
        self.y += 1
    def moveDown(self):
        self.x += 1
    def moveLeft(self):
        self.y -= 1


class Square:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def visit(self):
        self.value = 2

    def setAsCurrentSquare(self):
        self.value = 1

    def isVisited(self):
        return self.value == 2


class Board:
    def __init__(self, board):

        #Set up Board with Square Structure and Scan the board and stores all its L shaped figures
        l_figures = set()
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

        self.matrix = board
        self.initialMatrix = deepcopy(board)
        self.l_figures = l_figures
        self.initialL_figures = deepcopy(l_figures)
        self.position = Position(len(board) - 1, 0)

    def setCurrentSquareVisited(self):
        self.matrix[self.position.x][self.position.y].visit()

    def setCurrentPositionAsCurrentSquare(self):
        element = self.matrix[self.position.x][self.position.y].value
        if (element in self.l_figures):
            self.l_figures.remove(element)
        self.matrix[self.position.x][self.position.y].setAsCurrentSquare()

    def isAtFinalSquare(self):
        return self.matrix[0][len(self.matrix) - 1].value == 1

    def canMoveUp(self):
        isBoardEdge = self.position.x == 0
        if isBoardEdge:
            return False
        else:
            isNotVisited = not self.matrix[self.position.x - 1][self.position.y].isVisited()
            isLnotVisited = self.isLnotVisited(self.position.getMoveUp())
            return isNotVisited and isLnotVisited

    def canMoveRight(self):
        isBoardEdge = self.position.y == len(self.matrix) - 1
        if isBoardEdge:
            return False
        else:
            isNotVisited = not self.matrix[self.position.x][self.position.y + 1].isVisited()
            isLnotVisited = self.isLnotVisited(self.position.getMoveRight())
            return isNotVisited and isLnotVisited

    def canMoveDown(self):
        isBoardEdge = self.position.x == len(self.matrix) - 1
        if isBoardEdge:
            return False
        else:
            isNotVisited = not self.matrix[self.position.x + 1][self.position.y].isVisited()
            isLnotVisited = self.isLnotVisited(self.position.getMoveDown())
            return isNotVisited and isLnotVisited

    def canMoveLeft(self):
        isBoardEdge = self.position.y == 0
        if isBoardEdge:
            return False
        else:
            isNotVisited = not self.matrix[self.position.x][self.position.y - 1].isVisited()
            isLnotVisited = self.isLnotVisited(self.position.getMoveLeft())
            return isNotVisited and isLnotVisited

    def isLnotVisited(self, pos):
        square = self.matrix[pos.x][pos.y]
        #Checks if square is a normal unvisited square or if it is a unvisited square of an unvisited L figure
        return (square.value == 0) or (square.value in self.l_figures)

    #Restarts the board
    def restart(self):
        print ("Restarting...")
        self.matrix = deepcopy(self.initialMatrix)
        self.l_figures = deepcopy(self.initialL_figures)
        self.position = Position(len(self.matrix) - 1, 0)

    #Finds out it the player won
    def gameOver(self):
        return (self.l_figures == set()) and self.isAtFinalSquare()

    def get_obs(self):
        res_matrix = []
        height = len(self.matrix)
        width = len(self.matrix[0])
        for x in range(height):
            line = []
            for y in range(width):
                element = self.matrix[x][y].value
                if element > 2:
                    line.append(0)
                else:
                    line.append(element)
            res_matrix.append(line)
        return res_matrix

    def print(self):
        for line in self.matrix:
            for element in line:
                print(element.value, end=" ")
            print(" ")

    def __lt__(self, other):
        return False
