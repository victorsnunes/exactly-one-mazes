from utils import *
from queue import Queue, PriorityQueue
from time import process_time
import psutil

iteration = 1

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

        if board.gameOver():
            print("Congratulations! You won!")
            return True

        if move == Operation.QUIT:
            return False


def breadthSearch(board, screen):
    screen.set_up(board.matrix)
    global iteration
    q = Queue()
    possibleOps = possibleOperations(board)

    for op in possibleOps:
        state = makeMove(board, op)
        q.put(state)

    board = q.get()
    startTime = process_time()
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

        # sleep(0.5)

        board = q.get()
        iteration += 1
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("iterations: ", iteration)
    print("Elapsed time: %6.4f" % endTime, "seconds")
    print('RAM memory % used:', psutil.virtual_memory()[2])

    measurements = open('measurements.txt', 'a')
    measurements.write("BFS\niteration " + repr(iteration)+"\n")
    measurements.write("Elapsed process time: %6.4f" % endTime + " seconds\n")
    measurements.write("RAM memory" + repr(psutil.virtual_memory()[2])+"%\n")
    measurements.close()

    iteration = 1

    #Wait a little to show the final answer
    while getKeyPress() == False:
        continue


def depthSearch(board, screen, time):
    global iteration
    screen.set_up(board.matrix)
    possibleOps = possibleOperations(board)
    screen.draw_board(board.matrix, possibleOps)

    # sleep(0.25)

    board.print()
    print("L figures remaining to visit: ", board.l_figures)
    if (possibleOps == []):
        print("No more possible moves")
    else:
        print("Possible moves: ", possibleOps)
    print("\n\n")

    if board.gameOver():
        endTime = process_time() - time
        print("Congratulations! You found a solution")
        print("Your solution:")
        board.print()
        print("iterations: ", iteration)
        print("Elapsed time: %6.4f" % endTime, "seconds")
        print('RAM memory % used:', psutil.virtual_memory()[2])
        measurements = open('measurements.txt', 'a')
        measurements.write("DFS\niteration " + repr(iteration)+"\n")
        measurements.write("Elapsed process time: %6.4f" % endTime + " seconds\n")
        measurements.write("RAM memory" + repr(psutil.virtual_memory()[2])+"%\n")
        measurements.close()


        #Wait a little to show the final answer
        while getKeyPress() == False:
            continue

        return True

    for op in possibleOps:
        newBoard = makeMove(board, op)
        iteration += 1
        ret = depthSearch(newBoard, screen, time)
        if ret:
            iteration = 1
            return True

    return False


def iterativeDeepening(board, screen):
    screen.set_up(board.matrix)
    depth = 0
    global iteration
    startTime = process_time()
    while True:
        found, remaining = depthLimitedSearch(board, depth, screen)
        if found is not None:
            endTime = process_time() - startTime
            print("Congratulations! You found a solution")
            print("Your solution:")
            found.print()
            print("iterations: ", iteration)
            print("Elapsed time: %6.4f" % endTime, "seconds")
            print('RAM memory % used:', psutil.virtual_memory()[2])
            measurements = open('measurements.txt', 'a')
            measurements.write("Iterative deepening\niteration " + repr(iteration)+"\n")
            measurements.write("Elapsed process time: %6.4f" % endTime + " seconds\n")
            measurements.write("RAM memory" + repr(psutil.virtual_memory()[2])+"%\n")
            measurements.close()

            iteration = 1

            #Wait a little to show the final answer
            while getKeyPress() == False:
                continue

            return True

        elif not remaining:
            iteration = 1
            return False
        depth += 1


def depthLimitedSearch(board, depth, screen):
    global iteration
    iteration += 1
    possibleOps = possibleOperations(board)
    screen.draw_board(board.matrix, possibleOps)

    if depth == 0:
        if board.gameOver():
            return (board, True)
        else:
            # Not found, but maybe have children
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
            found, remaining = depthLimitedSearch(newBoard, depth - 1, screen)
            if found is not None:
                return (found, True)
            if remaining:
                # At least one node found at depth, let the algorithm deepen
                any_remaining = True
        return (None, any_remaining)


def heuristic1(board):
    return len(board.l_figures)


def greedySearch(board, screen):
    global iteration
    screen.set_up(board.matrix)
    q = PriorityQueue()
    possibleOps = possibleOperations(board)

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
            heuristic = heuristic1(board)
            q.put((heuristic, state))

        board.print()
        print("L figures remaining to visit: ", board.l_figures)
        if (possibleOps == []):
            print("No more possible moves")
        else:
            print("Possible moves: ", possibleOps)
        print("\n\n")

        # sleep(0.25)

        heuristic, board = q.get()
        iteration += 1
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("iterations: ", iteration)
    print("Elapsed time: %6.4f" % endTime, "seconds")
    print('RAM memory % used:', psutil.virtual_memory()[2])
    measurements = open('measurements.txt', 'a')
    measurements.write("Greedy Search\niteration " + repr(iteration)+"\n")
    measurements.write("Elapsed process time: %6.4f" % endTime + " seconds\n")
    measurements.write("RAM memory" + repr(psutil.virtual_memory()[2])+"%\n")
    measurements.close()

    iteration = 1

    #Wait a little to show the final answer
    while getKeyPress() == False:
        continue

    return True


def aStarAlgorithm(board, screen):
    screen.set_up(board.matrix)
    global iteration
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
        iteration += 1
    endTime = process_time() - startTime

    print("Congratulations! You found a solution")
    print("Your solution:")
    board.print()
    screen.draw_board(board.matrix, possibleOps)
    print("Heuristic: ", current_heuristic)
    print("Cost: ", current_cost)
    print("iterations: ", iteration)
    print("Elapsed time: %6.4f" % endTime, "seconds")
    print('RAM memory % used:', psutil.virtual_memory()[2])
    measurements = open('measurements.txt', 'a')
    measurements.write("A* Search\niteration " + repr(iteration)+"\n")
    measurements.write("Elapsed process time: %6.4f" % endTime + " seconds\n")
    measurements.write("RAM memory" + repr(psutil.virtual_memory()[2])+"%\n")
    measurements.close()

    iteration = 1

    #Show the final answer until a keypress
    while getKeyPress() == False:
        continue

    return True
