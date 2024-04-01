import random
from matplotlib import pyplot as plt
import numpy as np

from neighbours import get_random_neighbour_solution
from utils import evaluate_solution, generate_random_solution


def order_based_crossover(solution1, solution2):
    length = len(solution1)
    child1 = [None] * length
    child2 = [None] * length

    indices = sorted(random.sample(range(length), length // 2))

    for index in indices:
        child1[index] = solution1[index]
        child2[index] = solution2[index]

    solution2_rest = [pkg for pkg in solution2 if pkg not in child1]
    iterator1 = iter(solution2_rest)

    for i in range(len(child1)):
        if child1[i] is None:
            child1[i] = next(iterator1)

    solution1_rest = [pkg for pkg in solution1 if pkg not in child2]
    iterator2 = iter(solution1_rest)

    for i in range(len(child2)):
        if child2[i] is None:
            child2[i] = next(iterator2)

    return child1, child2


def order_crossover(solution1, solution2):
    length = len(solution1)
    mid_point1, mid_point2 = sorted(random.sample(range(length), 2))

    child1 = [None] * length
    child2 = [None] * length

    child1[mid_point1:mid_point2] = solution1[mid_point1:mid_point2]
    child2[mid_point1:mid_point2] = solution2[mid_point1:mid_point2]

    current_pos = mid_point2

    for p in solution2:
        if p not in child1:
            if current_pos >= length:
                current_pos = 0

            child1[current_pos] = p
            current_pos += 1

    current_pos = mid_point2

    for p in solution1:
        if p not in child2:
            if current_pos >= length:
                current_pos = 0

            child2[current_pos] = p
            current_pos += 1

    return child1, child2


def crossover(solution1, solution2):
    if random.randint(0, 1) == 0:
        return order_based_crossover(solution1, solution2)
    else:
        return order_crossover(solution1, solution2)


def tournament_selection(population, fitness_scores, tournament_size):
    selected_indices = random.sample(range(len(population)), tournament_size)
    selected_fitness = [fitness_scores[i] for i in selected_indices]
    winner_index = selected_indices[selected_fitness.index(max(selected_fitness))]
    return population[winner_index]


def roulette_selection(population, fitness_scores):
    total_fitness = abs(sum(fitness_scores))
    selection_probs = [abs(score) / total_fitness for score in fitness_scores]

    cumulative_probs = []
    cum_prob = 0
    for prob in selection_probs:
        cum_prob += prob  # Accumulate the selection probability
        cumulative_probs.append(cum_prob)

    spin = random.random()
    for i, solution in enumerate(population):
        if spin <= cumulative_probs[i]:
            return solution


def mutate_solution(solution):
    return get_random_neighbour_solution(solution)


def get_greatest_fit(population, fitness_scores):
    greatest_fit_index = fitness_scores.index(max(fitness_scores))
    return population[greatest_fit_index], fitness_scores[greatest_fit_index]


def get_greatest_fits(population, fitness_scores, no_greatest_fits):
    greatest_fits = []
    scores_copy = fitness_scores[:]
    for _ in range(no_greatest_fits):
        greatest_fit_index = scores_copy.index(max(scores_copy))
        greatest_fits.append(population[greatest_fit_index])
        scores_copy[greatest_fit_index] = -float("inf")
    return greatest_fits


def genetic_algorithm(num_generations, package_stream, population_size):
    population = []
    population.append(package_stream)
    scores_history = []
    for _ in range(1, population_size):
        population.append(generate_random_solution(package_stream))

    fitness_scores = [evaluate_solution(solution) for solution in population]
    best_solution = population[0]
    best_score = evaluate_solution(best_solution)
    best_solution_generation = 0
    print(f"Initial score: {best_score}")

    generation_no = 0

    tournament_size = int(population_size * 0.2)

    while generation_no < num_generations:
        greatest_fits = get_greatest_fits(population, fitness_scores, 4)
        new_population = greatest_fits

        for _ in range((population_size - 4) // 2):
            tournament_winner = tournament_selection(
                population, fitness_scores, tournament_size
            )
            roulette_winner = roulette_selection(population, fitness_scores)

            if random.random() < 0.9:
                offspring1, offspring2 = crossover(tournament_winner, roulette_winner)
            else:
                offspring1, offspring2 = tournament_winner, roulette_winner

            if random.random() < 0.5:
                offspring1 = mutate_solution(offspring1)
            if random.random() < 0.5:
                offspring2 = mutate_solution(offspring2)

            new_population.append(offspring1)
            new_population.append(offspring2)

        population = new_population
        generation_no += 1

        fitness_scores = [evaluate_solution(solution) for solution in population]

        greatest_fit, greatest_fit_score = get_greatest_fit(population, fitness_scores)
        if greatest_fit_score > best_score:
            best_solution = greatest_fit
            best_score = greatest_fit_score
            best_solution_generation = generation_no

        print(f" Best score so far: {best_score}")
        print(f" Generation: {generation_no}")
        scores_history.append(abs(best_score))
    

    print(f"  Final score: {best_score}")
    print(f"  Found on generation {best_solution_generation}")

    return best_solution
