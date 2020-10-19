from itertools import combinations
import random
from pprint import pprint

POPULATION = 10
CROSS_RATE = 0.5
MUTATION_RATE = 0.05


def take_inputs():
    count = int(input("Enter the number of items : "))
    weight_input = input(f'Enter the weights, seperated by spaces : ')
    value_input = input(f'Enter the values, seperated by spaces : ')
    weights = list(map(int,weight_input.split()))
    values = list(map(int,value_input.split()))
    limit = int(input("Enter the weight limit : "))
    return count, weights, values, limit


def get_random_solution(size):
    return [random.choice([0, 1]) for _ in range(size)]


def get_value(candidate, weights, values, limit):
    weight = 0
    value = 0
    for is_chosen, w, v in zip(candidate, weights, values):
        if is_chosen:
            weight += w
            value += v
    return (candidate, value, weight <= limit)


def compete(candidate1, candidate2):
    if candidate1[1] > candidate2[1]:
        return candidate1
    return candidate2


def tournament(candidates):
    chosen_candidates = [random.sample(candidates, 2) for _ in range(2)]
    winners = [compete(*c) for c in chosen_candidates]
    # print(f'{chosen_candidates=}, {winners=}')
    return winners


def mutate(candidate):
    mutated_candidate = []
    for bit in candidate:
        if random.random() < MUTATION_RATE:
            if bit:
                mutated_candidate.append(0)
            else:
                mutated_candidate.append(1)

    return mutated_candidate


def cross_and_mutate(parent1, parent2):
    children = []
    for (b1, b2) in zip(parent1[0], parent2[0]):
        if random.random() < CROSS_RATE:
            children.append((b2, b1,))
        else:
            children.append((b1, b2,))
    c1, c2 = zip(*children)
    # print(f'parents:{[parent1,parent2]} children: {[c1,c2]}')
    mc1, mc2 = mutate(c1), mutate(c2)
    # print(f'mutated children: {[c1,c2]}')
    return c1,c2


def regenerate_population(): pass


def run_simulation(knapsack_input, epochs=1):
    items_count, item_weights, item_values, limit = knapsack_input
    # lets calculate some combinations of solutions
    for epoch in range(1,epochs+1):
        print(f'Epoch: {epoch}')
        candidate_solutions = []
        while len(candidate_solutions) < POPULATION:
            candidate_solution = get_random_solution(items_count)
            candidate = get_value(candidate_solution,
                                item_weights, item_values, limit)
            if candidate[2]:
                candidate_solutions.append(candidate)
        best_solution = sorted(candidate_solutions,key = lambda x:x[1],reverse=True)[0]
        print(f'best solution:{best_solution}')
        # print('candiates:', candidate_solutions)
        next_gen = []
        # each tournament produces 2 candidates
        while len(next_gen) < (POPULATION //2):
            parents = tournament(candidate_solutions)
            children = cross_and_mutate(*parents)
            next_gen.extend(children)
        print(f'{next_gen=}')


def main():
    knapsack_input = take_inputs()
    print(f'{knapsack_input=}')

    run_simulation(knapsack_input, 10)


if __name__ == "__main__":
    main()
