from enum import Enum

class Operation(Enum):
    MOVE_UP = 0
    MOVE_RIGHT = 1
    MOVE_DOWN = 2
    MOVE_LEFT = 3
    RESTART = 4
    QUIT = 9