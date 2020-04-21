import collections
import random

from torch import nn, relu, softmax, optim, device, cuda, max, from_numpy, argmax
from torch.nn import MSELoss

NUMBER_OF_ACTIONS = 3
NUMBER_OF_PARAMS = 11
HIDDEN_LAYER_DIM = 200


class Agent:
    def __init__(self, params):
        self.reward = 0
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.model = FcNetwork().to(self.device)
        self.gamma = 0.9
        self.optimiser = optim.Adam(self.model.parameters(), lr=0.01)
        self.loss_function = MSELoss()
        self.memory = collections.deque(maxlen=params['memory_size'])

    def predict_move(self, state):
        predicts = self.model(from_numpy(state).to(self.device))

        return argmax(predicts)

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
        expected_reward = reward
        if not game_over:
            expected_reward = reward + self.gamma * max(self.model(new_state))

        predicted_output = self.model(state)
        expected_output = predicted_output.data.to(self.device)
        expected_output[action] = expected_reward
        loss = self.loss_function(predicted_output, expected_output)
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
        return softmax(self.layer3(x), dim=1)
