import numpy as np
import math
import random

class Network:
    def __init__(self, nbrInput, nbrMilieu, nbrOutput):

        self.premiereLayer = np.zeros(int(nbrInput))
        self.matrice1 = np.random.randn(nbrInput, nbrMilieu) / np.sqrt(nbrInput)
        self.matrice2 = np.random.randn(nbrMilieu, nbrOutput) /np.sqrt(nbrOutput)
        self.decision = 0


    def feed_forward(self, npInput):
        sigmoid_v = np.vectorize(self.sigmoid)
        vecteur1 = sigmoid_v(np.dot(npInput, self.matrice1))
        self.decision = sigmoid_v(np.dot(vecteur1, self.matrice2))

    def sigmoid(self,x):
        return 1 / (1 + math.exp(-x))

    def mutationNetwork(self):
        #choisir des index au hasard
        self._mutationMatrix(self.matrice1)
        self._mutationMatrix(self.matrice2)

    def _mutationMatrix(self, matrix):
        shape = matrix.shape

        for i in range(10):
            X = random.randint(0, shape[0] - 1)
            Y = random.randint(0, shape[1] - 1)
            matrix[X][Y] = np.random.rand(1)[0]


    def decider(self):
        return np.argmax(self.decision)


a = Network(6, 6, 3)
npInpute = np.array([0, 0, 1, 1, 1, 1])
a.feed_forward(npInpute)



