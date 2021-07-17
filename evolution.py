from numpy.core.defchararray import index
from numpy.core.fromnumeric import sort
from player import Player
import numpy as np
import copy
from config import CONFIG
import os

class Evolution():

    def __init__(self, mode):
        self.mode = mode

    # calculate fitness of players
    def calculate_fitness(self, players, delta_xs):
        for i, p in enumerate(players):
            p.fitness = delta_xs[i]

    def mutate(self, child):
        # child: an object of class `Player`

        mutation_threshold = 0.3
        center = 0
        margin = 0.5

        for i in range(len(child.nn.w)):
            if np.random.random_sample() >= mutation_threshold:
                child.nn.w[i] += np.random.normal(center, margin, size = (child.nn.w[i].shape))

        for i in range(len(child.nn.b)):
            if np.random.random_sample() >= mutation_threshold:
                child.nn.b[i] += np.random.normal(center, margin, size = (child.nn.b[i].shape))



    def generate_new_population(self, num_players, prev_players=None):

        # in first generation, we create random players
        if prev_players is None:
            return [Player(self.mode) for _ in range(num_players)]

        else:
            crossover_percent = 0.75
            
            tournament_children_count = int(num_players * (1 - crossover_percent))
            crossover_children_count = num_players - tournament_children_count
            
            new_players = self.tournament_select(tournament_children_count, prev_players, 5)
            new_players = self.apply_crossover(crossover_children_count, new_players, prev_players)

            for child in new_players:
                self.mutate(child)

            return new_players

    def tournament_select(self, num_players, prev_players, Q):
        new_players = []
        while len(new_players) != num_players:
            indexes = []
            possible_indexes = [i for i in range(len(prev_players))]
            while len(indexes) < Q:
                i = np.random.randint(low=0, high=len(possible_indexes))
                indexes.append(possible_indexes[i])
                del possible_indexes[i]

            best_player = prev_players[indexes[0]]
            for index in indexes:
                if best_player.fitness < prev_players[index].fitness:
                    best_player = prev_players[index]
            new_players.append(copy.deepcopy(best_player))
            # prev_players.remove(best_player)
        print("tournament select:",len(new_players))
        return new_players

    def apply_crossover(self, num_players, new_players, prev_players):
        for c in range(num_players):
            i1, i2 = np.random.randint(low=0 , high=len(prev_players)), np.random.randint(low=0 , high=len(prev_players))
            
            while i1 == i2:
                i2 = np.random.randint(low=0 , high=len(prev_players))
            
            #i1 and i2 are differnet.
            new_child = copy.deepcopy(prev_players[i1])

            if np.random.random_sample() >= 0.5:            
                w_cross_index = np.random.randint(low=1, high=len(new_child.nn.w))
                b_cross_index = np.random.randint(low=1, high=len(new_child.nn.b))

                for i in range(w_cross_index, len(new_child.nn.w)):
                    new_child.nn.w[i] = prev_players[i2].nn.w[i]
                
                for i in range(b_cross_index, len(new_child.nn.b)):
                    new_child.nn.b[i] = prev_players[i2].nn.b[i] 
            else:
                for i in range(len(new_child.nn.w)):
                    new_child.nn.w[i] = (new_child.nn.w[i] + prev_players[i2].nn.w[i]) / 2
        
                for i in range(len(new_child.nn.b)):
                    new_child.nn.b[i] = (new_child.nn.b[i] + prev_players[i2].nn.b[i]) / 2

            new_players.append(new_child)    
        
        return new_players



    def next_population_selection(self, players, num_players):

        # TODO (additional): plotting
        self.save_fitness(players)

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

    def save_fitness(self, players):
        if not os.path.exists('fitness'):
            os.makedirs('fitness')

        f = open("fitness/fitness.txt", "a")
        for p in players:
            f.write(str(p.fitness))
            f.write(" ")
        f.write("\n")
        f.close()