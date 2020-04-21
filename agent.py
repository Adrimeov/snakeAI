import collections
import numpy as np
import random

from torch import nn, relu, softmax, optim
from torch.nn import MSELoss

NUMBER_OF_ACTIONS = 4
NUMBER_OF_PARAMS = 11
HIDDEN_LAYER_DIM = 200


class Agent:
    def __init__(self, params):
        self.reward = 0
        self.model = FcNetwork()
        self.gamma = 0.9
        self.optimiser = optim.Adam(self.model.parameters(), lr=0.01)
        self.loss_function = MSELoss()
        self.memory = collections.deque(maxlen=params['memory_size'])

    def predict_move(self, state):
        predicts = self.model(state)
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
        actual_targets = self.predict_move(state)
        expected_targets = np.array(actual_targets, copy=True)
        expected_targets[np.argmax(action)] = target
        loss = self.loss_function(expected_targets, actual_targets)
        loss.backward()
        self.optimiser.step()

    def replay_memory(self, batch_size):
        if len(self.memory) > batch_size:
            batch = random.sample(self.memory, batch_size)
        else:
            batch = self.memory

        for state, action, new_state, reward, game_over in batch:
            self.train_step(state, action, new_state, reward, game_over)


class FcNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(NUMBER_OF_PARAMS, HIDDEN_LAYER_DIM)
        self.layer2 = nn.Linear(HIDDEN_LAYER_DIM, HIDDEN_LAYER_DIM)
        self.layer3 = nn.Linear(HIDDEN_LAYER_DIM, NUMBER_OF_ACTIONS)

    def forward(self, state):
        x = relu(self.layer1(state))
        x = relu(self.layer2(x))
        return  softmax(self.layer3(x), dim=1)
