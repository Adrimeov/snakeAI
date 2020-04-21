import collections
import datetime
import random

from torch import nn, relu, softmax, optim, device, cuda, max, from_numpy, argmax, save
from torch.nn import MSELoss

MODEL_PATH = "Snake_model"

NUMBER_OF_ACTIONS = 3
NUMBER_OF_PARAMS = 11
HIDDEN_LAYER_DIM = 120


class Agent:
    def __init__(self):
        self.reward = 0
        self.device = device("cuda" if cuda.is_available() else "cpu")
        self.model = FcNetwork().to(self.device)
        self.gamma = 0.9
        self.optimiser = optim.Adam(self.model.parameters(), lr=0.0005)
        self.loss_function = MSELoss()
        self.memory = collections.deque(maxlen=1000)
        self.death_memory = collections.deque(maxlen=1000)
        self.food_memory = collections.deque(maxlen=1000)
        self.date = datetime.datetime.today().strftime('%M')

    def predict_move(self, state):
        predicts = self.model(from_numpy(state).float().to(self.device))

        return argmax(predicts)

    def set_reward(self, player_ate, game_over):
        self.reward = 0
        if player_ate:
            self.reward = 10
        elif game_over:
            self.reward = -10

        return self.reward

    def save_state(self, state, action, new_state, reward, game_over):
        if reward > 0:
            self._save_food_state(state, action, new_state, reward, game_over)
        elif reward < 0:
            self._save_death_state(state, action, new_state, reward, game_over)
        else:
            self.memory.append((state, action, new_state, reward, game_over))

    def _save_death_state(self, state, action, new_state, reward, game_over):
        self.death_memory.append((state, action, new_state, reward, game_over))

    def _save_food_state(self, state, action, new_state, reward, game_over):
        self.food_memory.append((state, action, new_state, reward, game_over))

    def train_step(self, state, action, new_state, reward, game_over):
        expected_reward = reward
        if not game_over:
            expected_reward = reward + self.gamma * max(self.model(from_numpy(new_state).float().to(self.device)))
        self.optimiser.zero_grad()
        predicted_output = self.model(from_numpy(state).float().to(self.device))
        expected_output = predicted_output.clone().to(self.device)
        expected_output[action] = expected_reward
        loss = self.loss_function(predicted_output, expected_output)
        loss.backward()
        self.optimiser.step()
        return loss

    def replay_memory(self, batch_size):
        batch_size = min(len(self.food_memory), len(self.death_memory), len(self.memory), batch_size)
        food_batch = random.sample(self.food_memory, batch_size)
        death_batch = random.sample(self.death_memory, batch_size)
        walk_batch = random.sample(self.memory, batch_size)
        batch = food_batch + death_batch + walk_batch
        random.shuffle(batch)

        for state, action, new_state, reward, game_over in batch:
            self.train_step(state, action, new_state, reward, game_over)

    def save_model(self):
        save(self.model, MODEL_PATH + self.date)


class FcNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(NUMBER_OF_PARAMS, HIDDEN_LAYER_DIM)
        self.layer2 = nn.Linear(HIDDEN_LAYER_DIM, HIDDEN_LAYER_DIM)
        self.layer3 = nn.Linear(HIDDEN_LAYER_DIM, HIDDEN_LAYER_DIM)
        self.layer4 = nn.Linear(HIDDEN_LAYER_DIM, NUMBER_OF_ACTIONS)

    def forward(self, state):
        x = relu(self.layer1(state))
        x = relu(self.layer2(x))
        x = relu(self.layer3(x))
        return softmax(self.layer4(x), dim=0)
