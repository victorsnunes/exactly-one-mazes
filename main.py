from copy import deepcopy
from util import Operation, Board
from screen import Screen
import pygame
from queue import Queue, PriorityQueue
from time import sleep

def main():
    screen = Screen()

    board_with_numbers = [
        [5, 5, 5, 7, 7, 0],
        [0, 3, 5, 7, 6, 0],
        [0, 3, 0, 7, 6, 8],
        [0, 3, 3, 6, 6, 8],
        [0, 4, 4, 4, 8, 8],
        [1, 0, 0, 4, 0, 0],
    ]

    board = Board(board_with_numbers)
    
    print("Select the mode")
    print("1: Normal Human mode")
    print("2: Solve with Breadth First Search")
    print("3: Solve with Depth First search")
    print("4: Solve with Iterative Deepening")
    print("5: Solve with Greedy Search")
    print("6: Solve with A* Algorithm")

    selected = input()

    if selected == "1":
        humanPlay(board, screen)
    elif selected == "2":
        breadthSearch(board, screen)
    elif selected == "3":
        depthSearchSetUp(board, screen)
    elif selected == "5":
        greedySearch(board, screen)
    elif selected == "6":
        aStarAlgorithm(board, screen)
        
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


def possibleOperations(board):
    operations = []

    # Check if it's possible to move up
    if board.canMoveUp():
        operations.append(Operation.MOVE_UP)

    #Check if it's possible to move right
    if board.canMoveRight():
        operations.append(Operation.MOVE_RIGHT)

    #Check if it's possible to move down
    if board.canMoveDown():
        operations.append(Operation.MOVE_DOWN)
    
    #Check if it's possible to move left
    if board.canMoveLeft():
        operations.append(Operation.MOVE_LEFT)

    return operations

def makeMove(board, op):
    newBoard = deepcopy(board)

    newBoard.setCurrentSquareVisited()

    if op == Operation.MOVE_UP:
        newBoard.position.moveUp()
    elif op == Operation.MOVE_RIGHT:
        newBoard.position.moveRight()
    elif op == Operation.MOVE_DOWN:
        newBoard.position.moveDown()
    elif op == Operation.MOVE_LEFT:
        newBoard.position.moveLeft()

    newBoard.setCurrentPositionAsCurrentSquare()

    return newBoard

def gameOver(board):
    return (board.l_figures == set()) and board.isAtFinalSquare()

def humanPlay(board, screen):

    screen.set_up(board.matrix)

    while True:
        possibleOps = possibleOperations(board)
        if (possibleOps == []):
            print("No more possible moves. You lost! Try again...")
            board.restart()
        screen.draw_board(board.matrix, possibleOps)
        move = getKeyPress()

        if move in possibleOps:
            board = makeMove(board, move)
            board.print()
            print("\n")
            print(board.l_figures)
            print(possibleOps) 

        if move == Operation.RESTART:
            board.restart()

        if gameOver(board):
            print("Congratulations! You won!")
            return True

        if move == Operation.QUIT:
            return False
'''
def breadthSearch(board, screen):
    q = Queue()
    l_figures = set()
    boardSetUp(board, l_figures)
    position = Position(len(board) - 1, 0)
    possibleOps = possibleOperations(board, position, l_figures)

    screen.set_up(board)

    newBoard = board
    newLfigures = l_figures

    for op in possibleOps:
        state = makeMove(board, position, op, l_figures)
        q.put(state)

    while not gameOver(newBoard, newLfigures):
        newBoard, newPosition, newLfigures = q.get()
        possibleOps = possibleOperations(newBoard, newPosition, newLfigures)
        screen.draw_board(newBoard, possibleOps)

        for op in possibleOps:
            state = makeMove(newBoard, newPosition, op, newLfigures)
            q.put(state)

        sleep(0.25)


def depthSearchSetUp(board, screen):
    l_figures = set()
    boardSetUp(board, l_figures)
    position = Position(len(board) - 1, 0)

    possibleOps = possibleOperations(board, position, l_figures)

    screen.set_up(board)

    for op in possibleOps:
        newBoard, newPosition, newLfigures = makeMove(board, position, op, l_figures)
        ret = depthSearch(newBoard, newPosition, newLfigures, op, screen)
        if ret:
            break

    return True


def depthSearch(board, position, l_figures, operation, screen):
    if gameOver(board, l_figures):
        return True

    sleep(0.25)

    possibleOps = possibleOperations(board, position, l_figures)
    screen.draw_board(board, possibleOps)
    for op in possibleOps:
        newBoard, newPosition, newLfigures = makeMove(board, position, op, l_figures)
        ret = depthSearch(newBoard, newPosition, newLfigures, op, screen)
        if ret:
            return True

    return False


def heuristic1(board, l_figures):
    return len(l_figures)


def greedySearch(board, screen):
    q = PriorityQueue()
    l_figures = set()
    boardSetUp(board, l_figures)
    position = Position(len(board) - 1, 0)
    possibleOps = possibleOperations(board, position, l_figures)

    screen.set_up(board)

    newBoard = board
    newLfigures = l_figures

    for op in possibleOps:
        state = makeMove(board, position, op, l_figures)
        heuristic = heuristic1(board, l_figures)
        q.put((heuristic, state))

    while not gameOver(newBoard, newLfigures):
        heuristic, (newBoard, newPosition, newLfigures) = q.get()
        possibleOps = possibleOperations(newBoard, newPosition, newLfigures)
        screen.draw_board(newBoard, possibleOps)

        for op in possibleOps:
            state = makeMove(newBoard, newPosition, op, newLfigures)
            heuristic = heuristic1(newBoard, newLfigures)
            q.put((heuristic, state))

        sleep(0.25)

    return True


def aStarAlgorithm(board, screen):
    q = PriorityQueue()
    l_figures = set()
    boardSetUp(board, l_figures)
    position = Position(len(board) - 1, 0)
    possibleOps = possibleOperations(board, position, l_figures)

    screen.set_up(board)

    newBoard = board
    newLfigures = l_figures
    cost = 0

    for op in possibleOps:
        state = makeMove(board, position, op, l_figures)
        heuristic = heuristic1(board, l_figures)

        q.put((heuristic + cost, state))

    while not gameOver(newBoard, newLfigures):
        heuristic, (newBoard, newPosition, newLfigures) = q.get()
        possibleOps = possibleOperations(newBoard, newPosition, newLfigures)
        screen.draw_board(newBoard, possibleOps)

        # Each move increments one cost
        cost += 1

        for op in possibleOps:
            state = makeMove(newBoard, newPosition, op, newLfigures)
            heuristic = heuristic1(newBoard, newLfigures)
            q.put((heuristic + cost, state))

        sleep(0.25)

    return True
'''

if __name__ == "__main__":
   main()