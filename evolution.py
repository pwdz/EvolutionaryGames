from numpy.core.fromnumeric import sort
from player import Player
import numpy as np
from config import CONFIG


class Evolution():

    def __init__(self, mode):
        self.mode = mode

    # calculate fitness of players
    def calculate_fitness(self, players, delta_xs):
        for i, p in enumerate(players):
            p.fitness = delta_xs[i]

    def mutate(self, child):

        # TODO
        # child: an object of class `Player`
        pass


    def generate_new_population(self, num_players, prev_players=None):

        # in first generation, we create random players
        if prev_players is None:
            return [Player(self.mode) for _ in range(num_players)]

        else:

            # TODO
            # num_players example: 150
            # prev_players: an array of `Player` objects

            # TODO (additional): a selection method other than `fitness proportionate`
            # TODO (additional): implementing crossover

            new_players = prev_players
            return new_players

    def next_population_selection(self, players, num_players):

        # TODO
        # num_players example: 100
        # players: an array of `Player` objects

        # TODO (additional): a selection method other than `top-k`
        # TODO (additional): plotting
        wheel = self.make_wheel(players)
        selected_players = self.select_sus(wheel, num_players)

        return selected_players


    def make_wheel(self, players):
        sum_fitness = sum(p.fitness for p in players)

        # [1, 10, 100, ...]
        players.sort(reverse=False, key=lambda p: p.fitness)

        wheel = []
        top = 0
        for p in players:
            f = p.fitness / sum_fitness
            wheel.append((top, top+f, p))
            top += f

        return wheel

    def binSearch(self, wheel, num):
        mid = len(wheel)//2

        low, high, player = wheel[mid]

        if low <= num <= high:
            return player
        elif num < low:
            return self.binSearch(wheel[:mid], num)
        else:
            return self.binSearch(wheel[mid+1:], num)

    def select_sus(self, wheel, N):
        stepSize = 1.0/N
        selected_players = []
        r = np.random.random_sample()
        for _ in range(N):
            selected_players.append(self.binSearch(wheel, r))
            r += stepSize
            if r>1:
                r %= 1
        return selected_players