import numpy as np


class NeuralNetwork():

    def __init__(self, layer_sizes):

        # layer_sizes example: [4, 10, 2]
        center = 0
        margin = 1

        self.w1 = np.random.normal(center, margin, size = (layer_sizes[1], layer_sizes[0]))
        self.b1 = np.zeros((layer_sizes[1],1))

        self.w2 = np.random.normal(center, margin, size = (layer_sizes[2], layer_sizes[1]))
        self.b2 = np.zeros((layer_sizes[2],1))


        self.activation = np.vectorize(self.activation)

    def activation(self, x):
        if x<0:
            return 1 - 1/(1 + math.exp(x))
        else:
            return 1/(1 + math.exp(-x))

    def forward(self, x):
        
        # TODO
        # x example: np.array([[0.1], [0.2], [0.3]])
        z1 = (self.w1 @ x) + self.b1
        a1 = self.activation(z1)

        z2 = (self.w2 @ a1) + self.b2
        a2 = self.activation(z2)

        return a2