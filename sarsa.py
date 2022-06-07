from gym import ActionWrapper, RewardWrapper
from ExactlyOneMazesEnv import ExactlyOneMazesEnv
from utils import possibleOperations, operationConverter
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
decay = 0.001        #Exponential decay rate for exploration prob

train_episodes = 6000
test_episodes = 100
max_steps = 100

def chose_action(state):
    action = 0
    if np.random.uniform(0, 1) < epsilon:
        action = env.action_space.sample()
    else:
        action = np.argmax(Q[state.get_obs(), :])
    return action

#Function to learn the Q-value
def update(state, state2, reward, action, action2):
    predict = Q[state.get_obs(), action]
    target = reward + gamma * Q[state2.get_obs(), action2]
    Q[state.get_obs(), action] = Q[state.get_obs(), action] + alpha * (target - predict)


#Training the agent

#Creating lists to keep track of reward and epsilon values
training_rewards = []
epsilons = []

reward = 0
for episode in range(train_episodes):
    state1 = env.reset()
    action1 = chose_action(state1)
    total_training_rewards = 0

    for step in range(max_steps):
        env.render()

        state2, reward, done, info = env.step(action1)

        action2 = chose_action(state2)

        update(state1, state2, reward, action1, action2)

        state1 = state2
        action1 = action2

        total_training_rewards += reward

        # Ending the episode
        if done:
            # print ("Total reward for episode {}: {}".format(episode, total_training_rewards))
            break

    # Cutting down on exploration by reducing the epsilon
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    # Adding the total reward and reduced epsilon values
    training_rewards.append(total_training_rewards)
    epsilons.append(epsilon)

print("*** END TRAINING ***\n\n")

rewards_per_hundred_episodes = np.split(np.array(training_rewards), train_episodes/100)
count = 100
print("*** AVERAGE REWARD PER HUNDRED EPISODES ***\n")
for rew in rewards_per_hundred_episodes:
    print(count, ": ", str(sum(rew/100)))
    count += 100

print("*** AGENT TESTING ***")
state = env.reset()
done = False

while not done:
    env.render()
    state.print()
    action = np.argmax(Q[state.get_obs()])
    state, reward, done, info = env.step(action)
    print("Action: ", operationConverter(action))