import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from search_algorithms import humanPlay, breadthSearch, depthSearch, iterativeDeepening, greedySearch, aStarAlgorithm, process_time
from utils import getKeyPress, Operation

surface = create_example_window('Example - Simple', (600, 400))

def menuhandler():
    pygame_menu.Menu.get_current

def mainMenu(board,screen):
    menu = pygame_menu.Menu('Select the mode', 600, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

    menu.add.text_input('Name: ', default='John Doe', maxchar=10)

    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.add.button('Solve with A* Algorithm', menuhandler())
    print(menu.get_current)
    menu.mainloop(surface)


    return menu