import collections
import numpy as np
import random

NUMBER_OF_ACTIONS = 4


class Agent:
    def __init__(self, params, model):
        self.reward = 0
        self.model = model
        self.gamma = 0.9
        # self.learning_rate = params['learning_rate']
        # self.first_layer = params['first_layer_size']
        # self.second_layer = params['second_layer_size']
        # self.third_layer = params['third_layer_size']
        self.memory = collections.deque(maxlen=params['memory_size'])
        # self.weights = params['weights_path']
        # self.load_weights = params['load_weights']

    def predict_move(self, state):
        # Utiliser le model pour faire des predictions
        predicts = self.model.predict(state)
        action = np.zeros(NUMBER_OF_ACTIONS)
        action[np.argmax(predicts)] = 1

        return action

    def set_reward(self, player_ate, game_over):
        self.reward = 0
        if player_ate:
            self.reward = 10
        elif game_over:
            self.reward = -10

        return self.reward

    def save_state(self, state, action, new_step, reward, game_over):
        self.memory.append((state, action, new_step, reward, game_over))

    def train_step(self, state, action, new_state, reward, game_over):
        target = reward
        if not game_over:
            target = reward + self.gamma * np.amax(self.predict_move(new_state))
        expected_targets = self.predict_move(state)
        expected_targets[np.argmax(action)] = target
        self.model.fit(state, expected_targets, epochs=1, verbose=0)

    def replay_memory(self, batch_size):
        if len(self.memory) > batch_size:
            batch = random.sample(self.memory, batch_size)
        else:
            batch = self.memory

        for state, action, new_state, reward, game_over in batch:
            self.train_step(state, action, new_state, reward, game_over)
