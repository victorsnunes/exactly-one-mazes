from utils import *
from queue import Queue, PriorityQueue
from time import sleep, process_time

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
    interaction = 0
    q = Queue()
    possibleOps = possibleOperations(board)

    for op in possibleOps:
        state = makeMove(board, op)
        interaction += 1
        q.put(state)

    board = q.get()
    startTime = process_time()
    while not board.gameOver():

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            q.put(state)
            interaction += 1

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("\n\n")

        #sleep(0.5)

        board = q.get()
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("Interactions: ", interaction)
    print("Elapsed time: %6.4f" % endTime, "seconds")


def depthSearch(board, screen,interaction, time):
    possibleOps = possibleOperations(board)
    screen.draw_board(board.matrix, possibleOps)
  
    #sleep(0.25)

    board.print()
    print("L figures remaining to visit: ", board.l_figures)
    if (possibleOps == []):
        print("No more possible moves")
    else:
        print("Possible moves: ", possibleOps)
    print("\n\n")
    
    for op in possibleOps:
        newBoard = makeMove(board, op)
        interaction += 1
        ret = depthSearch(newBoard, screen, interaction,time)
        if ret:
            return True
    

    if board.gameOver():
        endTime = process_time() - time
        print("Congratulations! You found a solution")
        print("Your solution:")
        print("Interactions: ", interaction)
        print("Elapsed time: %6.4f" % endTime, "seconds")
        board.print()

        return True

    return False

def iterativeDeepening(board, screen):
    depth = 0
    interaction = 0
    startTime = process_time()
    while True:
        found, remaining = depthLimitedSearch(board, depth, screen, interaction)
        if found is not None:
            endTime = process_time() - startTime
            print("Congratulations! You found a solution")
            print("Your solution:")
            print("Interactions: ", interaction)
            print("Elapsed time: %6.4f" % endTime, "seconds")
            found.print()
            return True
        elif not remaining:
            return False
        depth += 1

def depthLimitedSearch(board, depth, screen, interaction):
    possibleOps = possibleOperations(board)
    screen.draw_board(board.matrix, possibleOps)

    if depth == 0:
        if board.gameOver():
            return (board, True)
        else:
            #Not found, but maybe have children
            return (None, True)
    elif depth > 0:
        any_remaining = False

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("\n\n")

        for op in possibleOps:
            newBoard = makeMove(board, op)
            interaction += 1
            found, remaining = depthLimitedSearch(newBoard, depth - 1, screen, interaction+1)
            if found is not None:
                return (found, True)
            if remaining:
                interaction+=1
                #At least one node found at depth, let the algorithm deepen
                any_remaining = True
        return (None, any_remaining)


def heuristic1(board):
    return len(board.l_figures)


def greedySearch(board, screen):
    q = PriorityQueue()
    possibleOps = possibleOperations(board)
    interaction = 0

    for op in possibleOps:
        state = makeMove(board, op)
        heuristic = heuristic1(board)
        q.put((heuristic, state))

    heuristic, board = q.get()
    startTime = process_time()
    while not board.gameOver():

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            interaction += 1
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
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("Interactions: ", interaction)
    print("Elapsed time: %6.4f" % endTime, "seconds")

    return True


def aStarAlgorithm(board, screen):
    interaction = 0
    q = PriorityQueue()
    possibleOps = possibleOperations(board)

    current_cost = 0
    current_heuristic = 0

    for op in possibleOps:
        state = makeMove(board, op)
        heuristic = heuristic1(board)
        q.put((heuristic, state))

    heuristicAndCost, board = q.get()
    startTime = process_time()
    while not board.gameOver():

        possibleOps = possibleOperations(board)
        screen.draw_board(board.matrix, possibleOps)

        for op in possibleOps:
            state = makeMove(board, op)
            interaction += 1
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
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("Heuristic: ", current_heuristic)
    print("Cost: ", current_cost)
    print("Interactions: ", interaction)
    print("Elapsed time: %6.4f" % endTime, "seconds")

    return True