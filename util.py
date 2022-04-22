from enum import Enum

class Operation(Enum):
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    RESTART = 4
    QUIT = 9

class Color(Enum):
    #TODO: Add more colors to avoid conflicts in the table
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)

    L_colors = [BLUE, GREEN, CYAN, MAGENTA]

class Square:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.isPossibleMove = False
        self.isVisited = False

    def __lt__(self, other):
        return False