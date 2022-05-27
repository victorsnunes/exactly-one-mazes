import time

from gym import Env
from gym.spaces import Discrete, Box
from structures import Board
from utils import makeMove, operationConverter, possibleOperations
from screen import Screen

class ExactlyOneMazesEnv(Env):
    def __init__(self):

        #Actions: up, right, down, left
        self.action_space = Discrete(4)

        #Initial board
        self.state = Board([
            [5, 5, 5, 7, 7, 0],
            [0, 3, 5, 7, 6, 0],
            [0, 3, 0, 7, 6, 8],
            [0, 3, 3, 6, 6, 8],
            [0, 4, 4, 4, 8, 8],
            [1, 0, 0, 4, 0, 0],
        ])

        self.screen = Screen()
        self.screen.set_up(self.state.matrix)

        self.initial_l_figures = len(self.state.l_figures)

        self.num_steps = 100

    def step(self, action):

        op = operationConverter(action)
        possible_ops = possibleOperations(self.state)

        if (op in possible_ops):
            self.state = makeMove(self.state, operationConverter(action))

            #Next state is a lost game
            if len(possibleOperations(self.state)) == 0:
                reward = -1
            else:
                #Next state is a won game
                if (self.state.gameOver()):
                    reward = self.initial_l_figures * 5
                #Next state is a regular valid move
                else:
                    reward = self.initial_l_figures - len(self.state.l_figures)
        #Illegal move
        else:
            reward = -1

        self.num_steps -= 1
        if (self.num_steps <= 0):
            done = True
        else:
            done = False

        info = {}

        #Return step information
        return self.state, reward, done, info

    def render(self):
        self.screen.draw_board(self.state.matrix, possibleOperations(self.state))

    def reset(self):
        #Reset board
        self.state.restart()
        self.num_steps = 100

        return self.state


env = ExactlyOneMazesEnv()

episodes = 10

for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0

    while not done:
        env.reset()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward

        time.sleep(0.5)

    print('Episode:{} Score:{}'.format(episode, score))
