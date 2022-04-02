from turtle import window_height, window_width
import pygame

class Screen:
    def __init__(self) -> None:
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        
        self.window_height = 300
        self.window_width = 300
        self.screen = 0

    def set_up(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_height, self.window_width))
        self.screen.fill(self.WHITE)
        self.draw_board(board)
        pygame.display.update()
        
    def draw_board(self, board):
        board_size = len(board)

        step = self.window_height/board_size
        wx = 0
        wy = 0
        for y in range(0, board_size):
            wy = 0
            for x in range(0, board_size):
                print("x = {} y = {} wx = {} wy = {} Bxy = {}".format(x, y, wx, wy, board[x][y]))
                rect = pygame.Rect(wx, wy, step, step)
                if board[x][y] == 0:
                    pygame.draw.rect(self.screen, self.WHITE, rect, 0)
                if board[x][y] == 1:
                    pygame.draw.rect(self.screen, self.RED, rect, 0)
                if board[x][y] >= 3:
                    pygame.draw.rect(self.screen, self.YELLOW, rect, 0)
                wy += step
            wx += step

