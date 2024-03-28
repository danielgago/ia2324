import random
from matplotlib import pyplot as plt
import numpy as np

from neighbours import get_neighbour_solution3
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


def tournament_selection(population, fitness_scores, tournament_size):
    selected_indices = random.sample(range(len(population)), tournament_size)
    selected_fitness = [fitness_scores[i] for i in selected_indices]
    winner_index = selected_indices[selected_fitness.index(max(selected_fitness))]
    return population[winner_index]


def roulette_selection(population, fitness_scores):
    total_fitness = sum(fitness_scores)
    selection_probs = [score / total_fitness for score in fitness_scores]

    cumulative_probs = []
    cum_prob = 0
    for prob in selection_probs:
        if prob == 0:
            cum_prob += 0.0001
        else:
            cum_prob += 1 / prob
        cumulative_probs.append(cum_prob)

    spin = random.random()
    for i, solution in enumerate(population):
        if spin <= cumulative_probs[i]:
            return solution


def mutate_solution_1(solution):
    index_1 = np.random.randint(0, len(solution))
    index_2 = (index_1 + np.random.randint(0, len(solution))) % (
        len(solution) - 1
    )  # Efficient way to generate a non-repeated index
    solution[index_1], solution[index_2] = solution[index_2], solution[index_1]
    return solution


def mutate_solution_2(solution):
    if len(solution) > 1:  # Ensure there are at least two elements to swap
        index_1, index_2 = np.random.choice(range(len(solution)), size=2, replace=False)
        solution[index_1], solution[index_2] = solution[index_2], solution[index_1]
    return solution


def mutate_solution_3(solution):
    return get_neighbour_solution3(solution)


def get_greatest_fit(population):
    best_solution = population[0]
    best_score = evaluate_solution(population[0])
    for i in range(1, len(population) - 1):
        score = evaluate_solution(population[i])
        if score > best_score:
            best_score = score
            best_solution = population[i]
    return best_solution, best_score


def replace_least_fittest(population, offspring):
    least_fittest_index = 0
    least_fittest_value = evaluate_solution(population[0])
    for i in range(1, len(population)):
        score = evaluate_solution(population[i])
        if score < least_fittest_value:
            least_fittest_value = score
            least_fittest_index = i
    population[least_fittest_index] = offspring


def genetic_algorithm(
    num_generations, package_stream, population_size, crossover_func, mutation_func
):
    population = []
    population.append(package_stream)
    scores_history = []
    for i in range(1, population_size):
        population.append(generate_random_solution(package_stream))

    fitness_scores = [evaluate_solution(solution) for solution in population]
    best_solution = population[0]
    best_score = evaluate_solution(best_solution)
    best_solution_generation = 0
    print(f"Initial score: {best_score}")

    generation_no = 0

    while num_generations > 0:
        generation_no += 1

        tournament_winner = tournament_selection(population, fitness_scores, 20)
        roulette_winner = roulette_selection(population, fitness_scores)

        offspring1, offspring2 = crossover_func(tournament_winner, roulette_winner)

        offspring1 = mutation_func(offspring1)
        offspring2 = mutation_func(offspring2)

        replace_least_fittest(population, offspring1)
        replace_least_fittest(population, offspring2)

        greatest_fit, greatest_fit_score = get_greatest_fit(population)
        if greatest_fit_score > best_score:
            best_solution = greatest_fit
            best_score = greatest_fit_score
            best_solution_generation = generation_no

        num_generations -= 1

        print(f" Current score: {best_score}")
        print(f" Generation: {generation_no}")
        scores_history.append(abs(best_score))

    plt.figure(figsize=(10, 6))
    plt.scatter(range(1, generation_no + 1), scores_history, color="blue", s=5)
    z = np.polyfit(range(1, generation_no + 1), scores_history, 5)
    p = np.poly1d(z)

    plt.plot(
        range(1, generation_no + 1),
        p(range(1, generation_no + 1)),
        "r--",
        label="Trend Line",
    )

    plt.title("Genetic Algorithm Performance Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Score")
    plt.grid(True)
    plt.legend()
    plt.show()

    print(f"  Final score: {best_score}")
    print(f"  Found on generation {best_solution_generation}")

    return best_solution
