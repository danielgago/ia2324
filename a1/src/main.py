import random, math, copy
import pandas as pd
import numpy as np
import pygame
import matplotlib.pyplot as plt


num_packages = 15
map_size = 60
WIDTH = 600


class Package:
    def __init__(self, package_type, coordinates):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]
        if package_type == "fragile":
            self.breaking_chance = random.uniform(
                0.0001, 0.01
            )  # 0.01-1% chance of breaking per km
            self.breaking_cost = random.uniform(3, 10)  # Extra cost in case of breaking
        elif package_type == "urgent":
            self.delivery_time = random.uniform(
                100, 240
            )  # Delivery time in minutes (100 minutes to 4 hours)


class DeliveredPackage(Package):
    def __init__(self, package, broken, delivery_time):
        super().__init__(
            package.package_type, (package.coordinates_x, package.coordinates_y)
        )
        if package.package_type == "fragile":
            self.broken = broken
        self.delivery_time = delivery_time


class DeliveryStats:
    def __init__(
        self, delivered_packages, total_distance, total_breaking_cost, total_late_time
    ):
        self.delivered_packages = delivered_packages
        self.total_distance = total_distance
        self.total_breaking_cost = total_breaking_cost
        self.total_late_time = total_late_time

    def show(self):
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, WIDTH))
        pygame.display.set_caption("Delivery Path Visualization")
        clock = pygame.time.Clock()

        delivery_path = [(0, 0)]  # Starting point

        # Calculate delivery path
        for package in self.delivered_packages:
            destination = (
                package.coordinates_x * (WIDTH / map_size),
                package.coordinates_y * (WIDTH / map_size),
            )
            delivery_path.append(destination)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill(WHITE)

            # Update the screen
            for package in self.delivered_packages:
                draw_x = package.coordinates_x * (WIDTH / map_size)
                draw_y = package.coordinates_y * (WIDTH / map_size)
                if package.package_type == "fragile":
                    pygame.draw.circle(screen, GREEN, (draw_x, draw_y), 5)
                elif package.package_type == "urgent":
                    pygame.draw.circle(screen, RED, (draw_x, draw_y), 5)
                else:
                    pygame.draw.circle(screen, BLUE, (draw_x, draw_y), 5)
            pygame.draw.lines(screen, BLUE, False, delivery_path, 2)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def generate_package_stream(num_packages, map_size):
    package_types = ["fragile", "normal", "urgent"]
    package_stream = [
        Package(
            random.choice(package_types),
            (random.uniform(0, map_size), random.uniform(0, map_size)),
        )
        for _ in range(num_packages)
    ]
    return package_stream


def generate_random_solution(package_stream):
    solution = copy.deepcopy(package_stream)
    random.shuffle(solution)
    return solution


def evaluate_solution(solution):
    last_x = 0
    last_y = 0
    total_dist = 0
    total_breaking_cost = 0
    total_broken = 0
    total_urgent_cost = 0

    for package in solution:
        if package == None:
             return 0
        dist = math.sqrt(
            (package.coordinates_x - last_x) ** 2
            + (package.coordinates_y - last_y) ** 2
        )
        total_dist += dist

        last_x = package.coordinates_x
        last_y = package.coordinates_y

        if package.package_type == "fragile":
            p_damage = 1 - ((1 - package.breaking_chance) ** total_dist)
            total_breaking_cost += (
                p_damage * package.breaking_cost
            )  # Expected value of breaking cost

        if package.package_type == "urgent":
            if (
                total_dist > package.delivery_time
            ):  # 60km/h = 1km/min so total_dist is equal to the minutes elapsed
                total_urgent_cost += (total_dist - package.delivery_time) * 0.3

    total_cost = total_dist * 0.3 + total_breaking_cost + total_urgent_cost

    return -total_cost


# Pick a package and place it somewhere else on the solution
def get_neighbour_solution1(solution):
    neighbour = copy.deepcopy(solution)

    package_number = random.randint(0, len(neighbour) - 1)
    package = neighbour.pop(package_number)

    new_pos = random.randint(0, len(neighbour) - 1)
    neighbour.insert(new_pos, package)

    return neighbour


# Swap 2 packages from the order
def get_neighbour_solution2(solution):
    neighbour = copy.deepcopy(solution)

    package1 = random.randint(0, len(neighbour) - 1)
    package2 = random.randint(0, len(neighbour) - 1)
    neighbour[package1], neighbour[package2] = neighbour[package2], neighbour[package1]

    return neighbour


# Neighbour 1 or 2 with 50% each
def get_neighbour_solution3(solution):
    if random.randint(0, 1) == 0:
        return get_neighbour_solution1(solution)
    else:
        return get_neighbour_solution2(solution)


def get_hc_solution(package_stream, num_iterations, log=False):
    iteration = 0
    best_solution = package_stream  # Best solution after 'num_iterations' iterations without improvement
    best_score = evaluate_solution(best_solution)

    print(f"Initial score: {best_score}")

    while iteration < num_iterations:
        iteration += 1
        neighbor_solution = get_neighbour_solution3(best_solution)
        neighbor_score = evaluate_solution(neighbor_solution)

        if neighbor_score > best_score:
            best_solution = neighbor_solution
            best_score = neighbor_score
            iteration = 0
            print(f"New best score: {neighbor_score}")

    return best_solution


def solution_to_data_frame(solution):
    df = pd.DataFrame(
        [
            (
                i,
                package.package_type,
                package.coordinates_x,
                package.coordinates_y,
                package.breaking_chance if package.package_type == "fragile" else None,
                package.breaking_cost if package.package_type == "fragile" else None,
                package.delivery_time if package.package_type == "urgent" else None,
            )
            for i, package in enumerate(solution, start=1)
        ],
        columns=[
            "Package",
            "Type",
            "CoordinatesX",
            "CoordinatesY",
            "Breaking Chance",
            "Breaking Cost",
            "Delivery Time",
        ],
    )
    return df


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
        if (prob == 0):
            cum_prob += 0.0001
        else:
            cum_prob += 1/prob
        cumulative_probs.append(cum_prob)

    spin = random.random()
    for i, solution in enumerate(population):
        if spin <= cumulative_probs[i]:
            return solution
        
def mutate_solution_1(solution):
    index_1 = np.random.randint(0, len(solution))
    index_2 = (index_1 + np.random.randint(0, len(solution))) % (len(solution) - 1) # Efficient way to generate a non-repeated index
    solution[index_1], solution[index_2] = solution[index_2], solution[index_1]
    return solution

def mutate_solution_2(solution):
    if len(solution) > 1:  # Ensure there are at least two elements to swap
        index_1, index_2 = np.random.choice(range(len(solution)), size=2, replace=False)
        solution[index_1], solution[index_2] = solution[index_2], solution[index_1]
    return solution


def mutate_solution_3(solution):
    return (get_neighbour_solution3(solution))

def get_greatest_fit(population):
    best_solution = population[0]
    best_score = evaluate_solution(population[0])
    for i in range(1, len(population)-1):
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

def genetic_algorithm(num_generations, package_stream, population_size, crossover_func, mutation_func):
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

    while (num_generations > 0):
        generation_no += 1

        tournament_winner = tournament_selection(population, fitness_scores, 4)
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
        else:
            num_generations -= 1

        print(f" Current score: {best_score}")
        scores_history.append(abs(best_score))


    plt.figure(figsize=(10, 6))
    plt.scatter(range(1, generation_no + 1), scores_history, color='blue', s=5)
    z = np.polyfit(range(1, generation_no + 1), scores_history, 5)
    p = np.poly1d(z)

    plt.plot(range(1, generation_no + 1), p(range(1, generation_no + 1)), "r--", label='Trend Line')

    plt.title("Genetic Algorithm Performance Over Generations")
    plt.xlabel("Generation")
    plt.ylabel("Best Score")
    plt.grid(True)
    plt.legend()
    plt.show()


    print(f"  Final score: {best_score}")
    print(f"  Found on generation {best_solution_generation}")

    return best_solution

    



def main():
    package_stream = generate_package_stream(num_packages, map_size)
    df1 = solution_to_data_frame(package_stream)
    pd.set_option("display.max_columns", None)
    print(df1.iloc[0:, :])
    stats1 = DeliveryStats(package_stream, 0, 0, 0)
    stats1.show()

    solution = get_hc_solution(package_stream, 1000)
    print(f"Final solution: {solution}")
    df2 = solution_to_data_frame(solution)
    print(df2.iloc[0:, :])
    stats2 = DeliveryStats(solution, 0, 0, 0)
    stats2.show()

    best_solution = genetic_algorithm(1000, package_stream, 50, order_based_crossover, mutate_solution_2)
    df3 = solution_to_data_frame(best_solution)
    print(df3.iloc[0:, :])
    stats3 = DeliveryStats(best_solution, 0, 0, 0)
    stats3.show()







if __name__ == "__main__":
    main()
