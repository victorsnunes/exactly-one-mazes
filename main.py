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

    board_with_numbers2 = [
        [5, 5, 0, 8, 8, 8, 7, 0, 0],
        [5, 3, 3, 8, 7, 7, 7, 0, 9],
        [5, 0, 3, 6, 0, 5, 8, 8, 9],
        [0, 0, 3, 6, 0, 5, 8, 9, 9],
        [4, 0, 6, 6, 5, 5, 8, 0, 0],
        [4, 4, 4, 8, 8, 6, 6, 6, 0],
        [0, 5, 5, 8, 0, 6, 0, 0, 9],
        [0, 5, 0, 8, 7, 7, 7, 0, 9],
        [1, 5, 0, 0, 7, 0, 0, 9, 9]
       
    ]

    board = Board(board_with_numbers)
    board2 = Board(board_with_numbers2)

    menu.mainMenu(board2,screen)

    pygame.quit()
    print("quitting...")

if __name__ == "__main__":
   main()