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

alpha = 0.7
gamma = 0.618
#alpha = 0.1
#gamma = 0.99
epsilon = 1
max_epsilon = 1
min_epsilon = 0.01
decay = 0.001

train_episodes = 10000
max_steps = 100

#Training the agent

training_rewards = []
epsilons = []

for episode in range(train_episodes):
    # Reseting the environment each time as per requirement
    state = env.reset()
    # Starting the tracker for the rewards
    total_training_rewards = 0

    for step in range(max_steps):
        # Choosing an action given the states based on a random number
        exp_exp_tradeoff = random.uniform(0, 1)

        if exp_exp_tradeoff > epsilon:
            action = np.argmax(Q[state.get_obs(), :])
            #while (operationConverter(action) not in possibleOperations(state)):
            #    action = env.action_space.sample()
        else:
            action = env.action_space.sample()
            #while (operationConverter(action) not in possibleOperations(state)):
            #    action = env.action_space.sample()

        new_state, reward, done, info = env.step(action)

       #Q[state.get_obs(), action] = Q[state.get_obs(), action] + alpha * (
        #            reward + gamma * np.max(Q[new_state.get_obs(), :]) - Q[state.get_obs(), action])
        Q[state.get_obs(), action] = Q[state.get_obs(), action] * (1 - alpha) + (
            reward + gamma * np.max(Q[new_state.get_obs(), :])
        )

        total_training_rewards += reward
        state = new_state

        env.render()
        state.print()
        print("Reward: ", reward, "\n")

        if done:
            # print ("Total reward for episode {}: {}".format(episode, total_training_rewards))
            break

    # Cutting down on exploration by reducing the epsilon
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    # Adding the total reward and reduced epsilon values
    training_rewards.append(total_training_rewards)
    epsilons.append(epsilon)

print("Training score over time: " + str(sum(training_rewards) / train_episodes))


rewards_per_hundred_episodes = np.split(np.array(training_rewards), train_episodes/100)
count = 100
print("*** AVERAGE REWARD PER HUNDRED EPISODES ***\n")
for rew in rewards_per_hundred_episodes:
    print(count, ": ", str(sum(rew/100)))
    count += 100

total_epochs, total_penalties = 0, 0
episodes = 100

state = env.reset()
epochs, penalties, reward = 0, 0, 0

done = False

while not done:
    env.render()
    action = np.argmax(Q[state.get_obs()])
    state, reward, done, info = env.step(action)
    print("Action: ", operationConverter(action))
    print(state)
    if reward == -10:
        penalties += 1
    epochs += 1
total_penalties += penalties
total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")