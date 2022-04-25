import pygame
from structures import Operation, Color

class Screen:
    def __init__(self) -> None:
        self.window_height = 600
        self.window_width = 400
        self.screen = 0

    def set_up(self, board):
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_height, self.window_width))
        self.screen.fill(Color.WHITE.value)
        self.draw_board(board)
        
    def draw_board(self, board, possible_ops = []):
        board_size = len(board)

        step = self.window_height/board_size
        wx = 0
        wy = 0
        
        for y in range(0, board_size):
            wy = 0
            for x in range(0, board_size):
                rect = pygame.Rect(wx, wy, step, step)
                pygame.draw.rect(self.screen, board[x][y].color, rect, 0)

                pygame.draw.rect(self.screen, Color.BLACK.value, rect, 1)
                
                wy += step
            wx += step
       
        wx = 0
        wy = 0
        for x in range(0, board_size):
            wx = 0
            for y in range(0, board_size):
                rect = pygame.Rect(wx, wy, step, step)

                if board[x][y].value == 1:
                    pygame.draw.circle(self.screen, Color.RED.value, ((wx + step/2), (wy + step/2)), 10)
                    for op in possible_ops:
                        if op == Operation.MOVE_UP:
                            rect = pygame.Rect(wx, wy - step, step, step)
                        elif op == Operation.MOVE_RIGHT:
                            rect = pygame.Rect(wx + step, wy, step, step)
                        elif op == Operation.MOVE_LEFT:
                            rect = pygame.Rect(wx - step, wy, step, step)
                        elif op == Operation.MOVE_DOWN:
                            rect = pygame.Rect(wx, wy + step, step, step)
                        pygame.draw.rect(self.screen, Color.YELLOW.value, rect, 6)
                if board[x][y].value == 2:
                    pygame.draw.circle(self.screen, Color.RED.value, ((wx + step/2), (wy + step/2)), 10)
                
                wx += step
            wy += step
        pygame.display.update()