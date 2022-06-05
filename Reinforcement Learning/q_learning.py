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

alpha = 0.7 #learning rate
discount_factor = 0.618
epsilon = 1
max_epsilon = 1
min_epsilon = 0.01
decay = 0.01

train_episodes = 2000
test_episodes = 100
max_steps = 100

#Training the agent

#Creating lists to keep track of reward and epsilon values
training_rewards = []
epsilons = []

for episode in range(train_episodes):
    # Reseting the environment each time as per requirement
    state = env.reset()
    # Starting the tracker for the rewards
    total_training_rewards = 0

    for step in range(100):
        # Choosing an action given the states based on a random number
        exp_exp_tradeoff = random.uniform(0, 1)

        ### STEP 2: SECOND option for choosing the initial action - exploit
        # If the random number is larger than epsilon: employing exploitation
        # and selecting best action
        if exp_exp_tradeoff > epsilon:
            action = np.argmax(Q[state, :])

        ### STEP 2: FIRST option for choosing the initial action - explore
        # Otherwise, employing exploration: choosing a random action
        else:
            action = env.action_space.sample()

        ### STEPs 3 & 4: performing the action and getting the reward
        # Taking the action and getting the reward and outcome state
        new_state, reward, done, info = env.step(action)

        ### STEP 5: update the Q-table
        # Updating the Q-table using the Bellman equation
        Q[state, action] = Q[state, action] + alpha * (
                    reward + discount_factor * np.max(Q[new_state, :]) - Q[state, action])
        # Increasing our total reward and updating the state
        total_training_rewards += reward
        state = new_state

        # Ending the episode
        if done == True:
            # print ("Total reward for episode {}: {}".format(episode, total_training_rewards))
            break

    # Cutting down on exploration by reducing the epsilon
    epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

    # Adding the total reward and reduced epsilon values
    training_rewards.append(total_training_rewards)
    epsilons.append(epsilon)

print("Training score over time: " + str(sum(training_rewards) / train_episodes))