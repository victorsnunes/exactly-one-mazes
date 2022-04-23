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
    screen.set_up(board.matrix)
    
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
        depthSearch(board, screen)
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

def gameOver(board):
    return (board.l_figures == set()) and board.isAtFinalSquare()

def humanPlay(board, screen):

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

def breadthSearch(board, screen):

    q = Queue()
    possibleOps = possibleOperations(board)

    for op in possibleOps:
        state = makeMove(board, op)
        q.put(state)

    board = q.get()
    while not gameOver(board):

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            q.put(state)

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("\n\n")

        #sleep(0.5)

        board = q.get()

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()

def depthSearch(board, screen):
    if gameOver(board):
        print("Congratulations! You found a solution")
        print("Your solution:")
        board.print()
        return True

    #sleep(0.25)

    possibleOps = possibleOperations(board)
    screen.draw_board(board.matrix, possibleOps)

    board.print()
    print("L figures remaining to visit: ", board.l_figures)
    if (possibleOps == []):
        print("No more possible moves")
    else:
        print("Possible moves: ", possibleOps)
    print("\n\n")

    for op in possibleOps:
        newBoard = makeMove(board, op)
        ret = depthSearch(newBoard, screen)
        if ret:
            return True

    return False


def heuristic1(board):
    return len(board.l_figures)


def greedySearch(board, screen):
    q = PriorityQueue()
    possibleOps = possibleOperations(board)

    for op in possibleOps:
        state = makeMove(board, op)
        heuristic = heuristic1(board)
        q.put((heuristic, state))

    heuristic, board = q.get()
    while not gameOver(board):

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            heuristic = heuristic1(board)
            q.put((heuristic, state))

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("\n\n")

        #sleep(0.25)

        heuristic, board = q.get()

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()

    return True


def aStarAlgorithm(board, screen):
    q = PriorityQueue()
    possibleOps = possibleOperations(board)

    current_cost = 0
    current_heuristic = 0

    for op in possibleOps:
        state = makeMove(board, op)
        heuristic = heuristic1(board)
        q.put((heuristic, state))

    heuristicAndCost, board = q.get()
    while not gameOver(board):

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            heuristic = heuristic1(state)
            # Each move increments one cost
            q.put((heuristic + current_cost + 1, state))

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("Heuristic: ", current_heuristic)
        print("Cost: ", current_cost)
        print("\n\n")

        # sleep(0.25)

        heuristicAndCost, board = q.get()
        current_heuristic = heuristic1(board)
        current_cost = heuristicAndCost - current_heuristic

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    print("Heuristic: ", current_heuristic)
    print("Cost: ", current_cost)

    return True


if __name__ == "__main__":
   main()