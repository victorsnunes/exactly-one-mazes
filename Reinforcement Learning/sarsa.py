from gym import ActionWrapper, RewardWrapper
from ExactlyOneMazesEnv import ExactlyOneMazesEnv
import numpy as np
import random

np.random.seed(0)

env = ExactlyOneMazesEnv()
state = env.reset()
env.render()

#Getting the state space
print("Action Space {}".format(env.action_space))
print("State Space {}".format(env.observation_space))


Q = np.zeros((env.observation_space.n, env.action_space.n))

alpha = 0.7         #Learning rate
gamma = 0.618       #Discount rate
epsilon = 1         #Exploration rate
max_epsilon = 1     #Exploration probability at start
min_epsilon = 0.01  #Minimum exploration probability
decay = 0.01        #Exponential decay rate for exploration prob

train_episodes = 2000
test_episodes = 100
max_steps = 100

def chose_action(state):
    action=0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state, :])
    return action

#Function to learn the Q-value
def update(state, state2, reward, action, action2):
    predict = Q[state, action]
    target = reward + gamma * Q[state2, action2]
    Q[state, action] = Q[state, action] + alpha * (target - predict)


#Training the agent

#Creating lists to keep track of reward and epsilon values
training_rewards = []
epsilons = []

reward = 0
for episode in range(train_episodes):
    t = 0
    state1 = env.reset()
    action1 = chose_action(state1)

    for step in range(max_steps):
        env.render()

        state2, reward, done, info = env.step(action1)

        action2 = chose_action(state2)

        update(state1, state2, reward, action1, action2)

        state1 = state2
        action1 = action2

        reward += 1

        # Ending the episode
        if done == True:
            # print ("Total reward for episode {}: {}".format(episode, total_training_rewards))
            break

print("reward/episodes = " + reward/train_episodes)

print(Q)