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
        [0, 7, 7, 8, 8, 7, 0, 0],
        [0, 7, 3, 3, 8, 7, 7, 7],
        [0, 7, 0, 3, 8, 5, 5, 0],
        [0, 6, 0, 3, 9, 0, 5, 0],
        [4, 6, 6, 6, 9, 6, 5, 0],
        [4, 0, 0, 9, 9, 6, 0, 9],
        [4, 4, 7, 7, 7, 6, 6, 9],
        [1, 0, 0, 0, 7, 0, 9, 9]
       
    ]

    board = Board(board_with_numbers)
    board2 = Board(board_with_numbers2)

    #menu.mainMenu(board2,screen)
    menu.mainMenu(board2, screen)

    pygame.quit()
    print("quitting...")

if __name__ == "__main__":
   main()