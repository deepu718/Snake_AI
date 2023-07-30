
from game import SnakeGameAI
import random
import numpy as np
from keras import Sequential
from collections import deque
from keras.layers import Dense
import matplotlib.pyplot as plt
from keras.optimizers import Adam
from helper import plot
import imageio
import time


class DQN:

    """ Deep Q Network """

    def __init__(self, env, params):

        self.action_space = env.action_space
        self.state_space = env.state_space
        self.epsilon = params['epsilon'] 
        self.gamma = params['gamma'] 
        self.batch_size = params['batch_size'] 
        self.epsilon_min = params['epsilon_min'] 
        self.epsilon_decay = params['epsilon_decay'] 
        self.learning_rate = params['learning_rate']
        self.layer_sizes = params['layer_sizes']
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()


    def build_model(self):
        model = Sequential([
            Dense(self.layer_sizes[0],input_shape=(self.state_space,),activation="relu"),
            Dense(self.layer_sizes[1],activation="relu"),
            Dense(self.layer_sizes[2],activation="relu"),
            Dense(self.action_space,activation="softmax")
        ])
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))


    def act(self, state):

        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])


    def replay(self):

        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_dqn(episode, env):
    total_score = 0
    mean_score = 0
    sum_of_rewards = []
    plot_scores = []
    plot_mean_scores = []
    high_score = 0
    high_reward = 0
    agent = DQN(env, params)
    for e in range(1,episode+1):
        state = env.reset()
        state = np.reshape(state, (1, env.state_space))
        total_reward = 0
        frames = []
        max_steps = 10000
        for i in range(max_steps):
            move=[0,0,0]
            action = agent.act(state)
            move[action] = 1
            prev_state = state
            next_state, reward, done = env.play_step(move)
            total_reward += reward
            
            next_state = np.reshape(next_state, (1, env.state_space))
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if params['batch_size'] > 1:
                agent.replay()
            if done:
                print(f'episode: {e}/{episode}, score: {total_reward}')
                plot_scores.append(env.score)
                total_score += env.score
                mean_score = total_score / e
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
                if env.score > high_score:
                    high_score = env.score
                    imageio.mimsave(f"snake_gif/episode_{e}_score_{env.score}.gif",frames)
                if total_reward > high_reward:
                    high_reward = total_reward
                    agent.model.save(f"models/episode_{e}_reward_{total_reward}.h5")
                break
            if not done:
                frame = env.display()
                frames.append(frame)



if __name__ == '__main__':

    params = dict()
    params['epsilon'] = 1
    params['gamma'] = .95
    params['batch_size'] = 250
    params['epsilon_min'] = .01
    params['epsilon_decay'] = .995
    params['learning_rate'] = 0.00025
    params['layer_sizes'] = [128, 128, 128]

    results = dict()
    ep = 200
    env = SnakeGameAI()
    train_dqn(ep, env)

    