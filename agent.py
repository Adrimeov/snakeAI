import collections


class Agent:
    def __init__(self, params, model):
        self.reward = 0
        self.model = model
        # self.learning_rate = params['learning_rate']
        # self.first_layer = params['first_layer_size']
        # self.second_layer = params['second_layer_size']
        # self.third_layer = params['third_layer_size']
        # self.memory = collections.deque(maxlen=params['memory_size'])
        # self.weights = params['weights_path']
        # self.load_weights = params['load_weights']

    def set_reward(self):
        pass

    def save_state(self):
        pass

    def train_step(self):
        pass

    def replay_memory(self):
        pass
