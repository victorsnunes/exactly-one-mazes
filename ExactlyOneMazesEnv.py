import time

from gym import Env, spaces
from gym.spaces import Discrete
from structures import Board
from utils import makeMove, operationConverter, possibleOperations
from screen import Screen

class ExactlyOneMazesEnv(Env):
    def __init__(self):

        #Actions: up, right, down, left
        self.action_space = Discrete(4)

        #Observation space of the problem
        self.observation_space = spaces.Discrete(200)

        #Initial board
        self.state = Board([
            [3, 3, 0, 0],
            [0, 3, 4, 0],
            [0, 3, 4, 0],
            [1, 0, 4, 4],
        ])

        self.screen = Screen()
        self.screen.set_up(self.state.matrix)

        self.initial_l_figures = len(self.state.l_figures)

    def step(self, action):

        op = operationConverter(action)
        possible_ops = possibleOperations(self.state)
        done = False

        if (op in possible_ops):

            l_figures_not_consumed_before = len(self.state.l_figures)
            self.state = makeMove(self.state, operationConverter(action))

            # Next state is a won game
            if (self.state.gameOver()):
                reward = self.initial_l_figures * 100
                done = True
            else:
                # Next state is a lost game
                if len(possibleOperations(self.state)) == 0:
                    print("You lost the game")
                    reward = -1
                    done = True
                # Next state is a regular valid move
                else:
                    l_figures_not_consumed_after = len(self.state.l_figures)
                    if l_figures_not_consumed_before - l_figures_not_consumed_after > 0:
                        reward = 1
                    else:
                        reward = 0
        # Illegal move
        else:
            print("Illegal move")
            reward = -1

        info = {}

        # Return step information
        return self.state, reward, done, info

    def render(self):
        self.screen.draw_board(self.state.matrix, possibleOperations(self.state))

    def reset(self):
        #Reset board
        self.state.restart()

        return self.state

    def print(self):
        self.state.print()

a = ExactlyOneMazesEnv()
