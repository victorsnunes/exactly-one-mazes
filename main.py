from queue import Queue, PriorityQueue
from time import sleep
from copy import deepcopy
from util import Operation, Square, Color
from screen import Screen 
import pygame

def main():
        
    screen = Screen()

    testBoard = [
        [5, 5, 5, 7, 7, 0],
        [0, 3, 5, 7, 6, 0],
        [0, 3, 0, 7, 6, 8],
        [0, 3, 3, 6, 6, 8],
        [0, 4, 4, 4, 8, 8],
        [1, 0, 0, 4, 0, 0],
    ]
    
    print("Select the mode")
    print("1: Normal Human mode")
    print("2: Solve with Breadth First Search")
    print("3: Solve with depth search")
    print("5: Solve with Greedy Search")
    print("6: Solve with A* Algorithm")

    selected = input()

    if selected == "1":
        running = True
        while running:
            print("Restarting...")
            testBoard = [
                [5, 5, 5, 7, 7, 0],
                [0, 3, 5, 7, 6, 0],
                [0, 3, 0, 7, 6, 8],
                [0, 3, 3, 6, 6, 8],
                [0, 4, 4, 4, 8, 8],
                [1, 0, 0, 4, 0, 0],
            ]
            running = humanPlay(testBoard, screen)

    if selected == "2":
        breadthSearch(testBoard, screen)
    if selected == "3":
        testBoard = [
                [5, 5, 5, 7, 7, 0],
                [0, 3, 5, 7, 6, 0],
                [0, 3, 0, 7, 6, 8],
                [0, 3, 3, 6, 6, 8],
                [0, 4, 4, 4, 8, 8],
                [1, 0, 0, 4, 0, 0], 
            ]
        depthSearchSetUp(testBoard, screen)

    if selected == "5":
        greedySearch(testBoard, screen)

    if selected == "6":
        aStarAlgorithm(testBoard, screen)

        
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
    
def printBoard(board):
    for line in board:
        for element in line:
            print(element.value, end=" ")
        print(" ")

# Data Structure Position
class Position:
    def __init__(self, x_pos = 0, y_pos = 0):
        self.x = x_pos
        self.y = y_pos

def LnotVisited(element, l_figures):
    return element == 0 or element in l_figures

def possibleOperations(board, position, l_figures):
    operations = []

    #Check if it's possible to move up
    if position.y + 1 < len(board) and (board[position.x][position.y + 1].value != 2) and LnotVisited(board[position.x][ position.y + 1].value, l_figures):
        operations.append(Operation.MOVE_RIGHT)

    #Check if it's possible to move right
    if position.x + 1 < len(board) and (board[position.x + 1][position.y].value != 2) and LnotVisited(board[position.x + 1][ position.y].value, l_figures):
        operations.append(Operation.MOVE_DOWN)
    
    #Check if it's possible to move down
    if position.y - 1 >= 0 and (board[position.x][position.y - 1].value != 2) and LnotVisited(board[position.x][ position.y - 1].value, l_figures):
        operations.append(Operation.MOVE_LEFT)

    #Check if it's possible to move left
    if position.x - 1 >= 0 and (board[position.x - 1][position.y].value != 2) and LnotVisited(board[position.x - 1][ position.y].value, l_figures):
        operations.append(Operation.MOVE_UP)

    return operations

def makeMove(board, position, op, l_figures):
    newBoard = deepcopy(board)
    newLfigures = deepcopy(l_figures)
    newPosition = deepcopy(position)

    newBoard[position.x][position.y].value = 2
    if op == Operation.MOVE_RIGHT:
        newPosition.y += 1
    elif op == Operation.MOVE_DOWN:
        newPosition.x += 1
    elif op == Operation.MOVE_LEFT:
        newPosition.y -= 1
    elif op == Operation.MOVE_UP:
        newPosition.x -= 1

    element = newBoard[newPosition.x][newPosition.y].value
    if (element in l_figures):
        newLfigures.remove(element)
    newBoard[newPosition.x][newPosition.y].value = 1

    return (newBoard, newPosition, newLfigures)

def gameOver(board, l_figures):
    if l_figures == set():
        return False
    n = len(board)
    return board[0][len(board) - 1].value == 1

def boardSetUp(board, l_figures):

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


def humanPlay(board, screen):

    #Scan the board and stores all its L shaped figures
    l_figures = set()
    boardSetUp(board, l_figures)
    screen.set_up(board)

    position = Position(len(board) - 1, 0)

    while True:
        
        possibleOps = possibleOperations(board, position, l_figures)
        if (possibleOps == []):
            print("No more possible moves. You lost!")
            return False
        screen.draw_board(board, possibleOps)
        move = getKeyPress()

        if move in possibleOps:
            board, position, l_figures = makeMove(board, position, move, l_figures)
            printBoard(board)
            print("\n")
            print(possibleOps) 

        if move == Operation.RESTART:
            return True

        if gameOver(board, l_figures) or move == Operation.QUIT:
            return True

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
    position = Position(len(board) -1, 0)

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

if __name__ == "__main__":
   main()