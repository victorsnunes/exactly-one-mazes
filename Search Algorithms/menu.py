import pygame_menu
from pygame_menu.examples import create_example_window
from search_algorithms import humanPlay, breadthSearch, depthSearch, iterativeDeepening, greedySearch, aStarAlgorithm
from time import process_time

surface = create_example_window('Exactly One Mazes', (600, 600))

def mainMenu(board, screen):
    menu = pygame_menu.Menu('Select the mode', 600, 600,
                            theme=pygame_menu.themes.THEME_BLUE)

    menu.add.button('Normal Human mode', humanPlay, board, screen)
    menu.add.button('Solve with Breadth First Search', breadthSearch, board, screen)
    menu.add.button('Solve with Depth First search', depthSearch, board, screen, process_time())
    menu.add.button('Solve with Iterative Deepening', iterativeDeepening, board, screen)
    menu.add.button('Solve with Greedy Search', greedySearch, board, screen)
    menu.add.button('Solve with A* Algorithm', aStarAlgorithm, board, screen)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(surface)

    return menu
