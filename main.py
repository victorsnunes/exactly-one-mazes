from structures import Board
from screen import Screen
import pygame
import pygame_menu
import menu
from search_algorithms import humanPlay, breadthSearch, depthSearch, iterativeDeepening, greedySearch, aStarAlgorithm, process_time
from utils import getKeyPress, Operation



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

    menu.mainMenu(board, screen)
    
    # print("Select the mode")
    # print("1: Normal Human mode")
    # print("2: Solve with Breadth First Search")
    # print("3: Solve with Depth First search")
    # print("4: Solve with Iterative Deepening")
    # print("5: Solve with Greedy Search")
    # print("6: Solve with A* Algorithm")

    # selected = input()

    # if selected == "1":
    #     humanPlay(board, screen)
    # elif selected == "2":
    #     breadthSearch(board, screen)
    # elif selected == "3":
    #     startTime = process_time()
    #     depthSearch(board, screen, 0.0, startTime)
    # elif selected == "4":
    #     iterativeDeepening(board, screen)
    # elif selected == "5":
    #     greedySearch(board, screen)
    # elif selected == "6":
    #     aStarAlgorithm(board, screen)

    pygame.quit()
    print("quitting...")

if __name__ == "__main__":
   main()