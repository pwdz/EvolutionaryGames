import numpy as np
import math

class NeuralNetwork():

    def __init__(self, layer_sizes):

        # layer_sizes example: [4, 10, 2]
        center = 0
        margin = 1

        self.w = []
        self.b = []
        for i in range(len(layer_sizes)-1):
            w = np.random.normal(center, margin, size = (layer_sizes[i + 1], layer_sizes[i]))
            self.w.append(w)
            b = np.zeros((layer_sizes[i + 1],1))
            self.b.append(b)

        self.activation = np.vectorize(self.activation)

    def activation(self, x):
        if x<0:
            return 1 - 1/(1 + math.exp(x))
        else:
            return 1/(1 + math.exp(-x))

    def forward(self, x):
        
        # TODO
        # x example: np.array([[0.1], [0.2], [0.3]])

        a = x
        for i in range(len(self.w)):
            z = (self.w[i] @ a) + self.b[i]
            a = self.activation(z)
        
        return a