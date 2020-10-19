import random
from random import choice
from functools import reduce, partial


class ProblemBase:

    def __init__(self, population, cross_rate=0.5, mutation_rate=0.05):
        self.population = population
        self.population_size = len(population)
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate

    def compete(self, candidate_one, candidate_two):
        raise NotImplementedError

    def cross(self, parent_one, parent_two):
        raise NotImplementedError

    def mutate(self, parent_one, parent_two):
        raise NotImplementedError

    def tournament(self, size=4):
        # TODO: add strategy
        if size % 2 != 0:
            raise ValueError(
                'A tournament requires even number of participants')
        if size > len(self.population):
            raise ValueError('size must be less than population')
        # ensures unique participants
        candidates = random.sample(self.population, size)
        # print('candidates:', candidates)
        # get 2 at a time and get winners for each match
        # matches = zip(*iter(candidates)*2)

        # might aswell use reduce
        winner = reduce(self.compete, candidates)
        return winner

    def lifecycle(self):
        parent_one, parent_two = self.tournament(), self.tournament()
        child_one, child_two = parent_one, parent_two
        if random.random() < self.cross_rate:
            child_one, child_two = self.cross(parent_one, parent_two)
        if random.random() < self.mutation_rate:
            child_one, child_two = self.mutate(child_one, child_two)
        return child_one, child_two

    def repopulate(self):
        new_generation = []
        for i in range(self.population_size//2):
            new_generation.extend(self.lifecycle())
        print('repopulated, new_generation:', new_generation)
        self.population = new_generation

    def run(self, generations):
        for gen in range(1, generations+1):
            print('generation:', gen)
            self.repopulate()
        print('final generation:', self.population)


class MySol(ProblemBase):
    def compete(self, candidate_one, candidate_two):
        if abs(candidate_one-100) < abs(candidate_two-100):
            return candidate_one
        return candidate_two

    def cross(self, parent_one, parent_two):
        return parent_one, parent_two

    def mutate(self, parent_one, parent_two):
        return parent_one, parent_two


if __name__ == "__main__":
    MySol([choice(list(range(20))) for _ in range(10)]).run(generations=2000)
    # print('winner:', winner)
