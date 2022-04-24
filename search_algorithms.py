from utils import *
from queue import Queue, PriorityQueue
from time import sleep

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

        if board.gameOver():
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
    while not board.gameOver():

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
    if board.gameOver():
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

def iterativeDeepening(board, screen):

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
    while not board.gameOver():

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
    while not board.gameOver():

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