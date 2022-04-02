import pygame

class Screen:
    def __init__(self) -> None:
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)

        self.colors = [self.BLUE, self.GREEN, self.YELLOW, self.CYAN, self.MAGENTA]
        self.l_color = {}
        self.window_height = 300
        self.window_width = 300
        self.screen = 0

    def set_up(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_height, self.window_width))
        self.screen.fill(self.WHITE)
        self.build_color_dict()
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
                rect = pygame.Rect(wx, wy, step, step)
                if board[x][y] == 1:
                    pygame.draw.circle(self.screen, self.RED, ((wx + step/2), (wy + step/2)), 10)
                if board[x][y] >= 3:
                    pygame.draw.rect(self.screen, self.l_color[board[x][y]], rect, 0)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                wy += step
            wx += step
    
    def build_color_dict(self):
        color_index = 0
        for i in range(10):
            self.l_color[i] = self.colors[color_index]
            color_index = (color_index + 1)%(len(self.colors))