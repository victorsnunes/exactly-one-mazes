from structures import Operation
from copy import deepcopy
import pygame

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

def possibleOperations(board):
    operations = []

    if board.canMoveUp():
        operations.append(Operation.MOVE_UP)

    if board.canMoveRight():
        operations.append(Operation.MOVE_RIGHT)

    if board.canMoveDown():
        operations.append(Operation.MOVE_DOWN)

    if board.canMoveLeft():
        operations.append(Operation.MOVE_LEFT)

    return operations


def makeMove(board, op):
    new_board = deepcopy(board)

    new_board.setCurrentSquareVisited()

    if op == Operation.MOVE_UP:
        new_board.position.moveUp()
    elif op == Operation.MOVE_RIGHT:
        new_board.position.moveRight()
    elif op == Operation.MOVE_DOWN:
        new_board.position.moveDown()
    elif op == Operation.MOVE_LEFT:
        new_board.position.moveLeft()

    new_board.setCurrentPositionAsCurrentSquare()

    return new_board
