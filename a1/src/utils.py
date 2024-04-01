import copy
import math
import random
import pygame
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Create a random assortment of the packages from an existing list.
def generate_random_solution(package_stream):
    solution = copy.deepcopy(package_stream)
    random.shuffle(solution)
    return solution

# Calculate the total cost of delivering the packages in the given order and return its negative value for minimization
def evaluate_solution(solution):
    last_x = 0
    last_y = 0
    total_dist = 0
    total_breaking_cost = 0
    total_urgent_cost = 0

    for package in solution:
        if package == None:
            return 0
        
        # Calculate distance from the last package's location
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
            )  # Expected value of breaking cost instead of random chance in order to make the evaluation function deterministic and consistent

        if package.package_type == "urgent":
            if (
                total_dist > package.delivery_time
            ):  # 60km/h = 1km/min so total_dist is equal to the minutes elapsed
                total_urgent_cost += (total_dist - package.delivery_time) * 0.3

    total_cost = total_dist * 0.3 + total_breaking_cost + total_urgent_cost

    return -total_cost

# Print the IDs of packages in the solution in order
def print_solution_ids(solution):
    sol = "["
    for package in solution:
        sol += f"{package}, "
    sol = sol[:-2]
    sol += "]"
    print(sol)

# Visualize the delivery path of packages using pygame.
def display_path(solution):
    WIDTH = 600
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    
    map_size = 100

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Delivery Path Visualization")
    clock = pygame.time.Clock()

    delivery_path = [(0, 0)]

    # Convert package coordinates to screen positions and add to the path
    for package in solution:
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

        # Draw packages and delivery path on the screen
        for package in solution:
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
    
# Convert a solution (list of package objects) into a Pandas DataFrame for analysis.
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

# Plot the progress of scores in a Hill Climbing optimization algorithm.
def show_hc_graph(scores):
    best_scores, neighbour_scores = zip(*scores)

    iterations = np.arange(1, len(scores) + 1)

    plt.plot(iterations, best_scores, label='Best Score')
    plt.plot(iterations, neighbour_scores, label='Neighbour Score')
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Hill Climbing Progress')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare Hill Climbing and Steepest Ascent Hill Climbing algorithms over iterations.   
def show_hc_iteration_comparison_graph(hc_scores, sahc_scores):
    best_hc_scores, _ = zip(*hc_scores)
    best_sahc_scores, _ = zip(*sahc_scores)
    
    hc_iterations = np.arange(1, len(best_hc_scores) + 1)
    sahc_iterations = np.arange(1, len(best_sahc_scores) + 1)
    
    plt.plot(hc_iterations, best_hc_scores, label='Basic')
    plt.plot(sahc_iterations, best_sahc_scores, label='Steepest Ascent')
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Hill Climbing Progress Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare scores of basic and Steepest Ascent Hill Climbing for different package counts.
def show_hc_score_comparison_graph(num_packages_list, hc_scores, sahc_scores):
    plt.plot(num_packages_list, hc_scores, label='Basic')
    plt.plot(num_packages_list, sahc_scores, label='Steepest Ascent')

    plt.xlabel('Number of Packages')
    plt.ylabel('Best Score')
    plt.title('Hill Climbing Best Solution Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare execution times of basic and Steepest Ascent Hill Climbing for different package counts.
def show_hc_time_comparison_graph(num_packages_list, hc_times, sahc_times):
    plt.plot(num_packages_list, hc_times, label='Basic')
    plt.plot(num_packages_list, sahc_times, label='Steepest Ascent')

    plt.xlabel('Number of Packages')
    plt.ylabel('Execution Time (s)')
    plt.title('Hill Climbing Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the progress of scores in a Simulated Annealing optimization algorithm.
def show_sa_graph(scores):
    best_scores, current_scores = zip(*scores)

    iterations = np.arange(1, len(scores) + 1)

    plt.plot(iterations, best_scores, label='Best Score')
    plt.plot(iterations, current_scores, label='Current Score')
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Simulated Annealing Progress')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare scores of basic and Steepest Ascent Hill Climbing for different package counts.
def show_sa_score_comparison_graph(num_packages_list, hc_scores, sa_score1, sa_score2, sa_score3, sa_score4):
    plt.plot(num_packages_list, hc_scores, label='Hill Climbing')
    plt.plot(num_packages_list, sa_score1, label='SA: Cooling = 0.9')
    plt.plot(num_packages_list, sa_score2, label='SA: Cooling = 0.95')
    plt.plot(num_packages_list, sa_score3, label='SA: Cooling = 0.99')
    plt.plot(num_packages_list, sa_score4, label='SA: Cooling = 0.999')
    plt.xlabel('Number of Packages')
    plt.ylabel('Best Score')
    plt.title('Simulated Annealing Best Solution Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
    
def show_sa_time_comparison_graph(num_packages_list, hc_times, sa_time1, sa_time2, sa_time3, sa_time4):
    plt.plot(num_packages_list, hc_times, label='Hill Climbing')
    plt.plot(num_packages_list, sa_time1, label='SA: Cooling = 0.9')
    plt.plot(num_packages_list, sa_time2, label='SA: Cooling = 0.95')
    plt.plot(num_packages_list, sa_time3, label='SA: Cooling = 0.99')
    plt.plot(num_packages_list, sa_time4, label='SA: Cooling = 0.999')
    plt.xlabel('Number of Packages')
    plt.ylabel('Execution Time (s)')
    plt.title('Simulated Annealing Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the progress of scores in a Tabu Search optimization algorithm.
def show_ts_graph(scores):
    best_scores, current_scores = zip(*scores)

    iterations = np.arange(1, len(scores) + 1)

    plt.plot(iterations, best_scores, label='Best Score')
    plt.plot(iterations, current_scores, label='Current Score')
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Tabu Search Progress')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot the progress of scores in a Genetic Algorithm optimization algorithm.
def show_ga_graph(scores):
    best_scores = scores

    generations = np.arange(1, len(scores) + 1)

    z = np.polyfit(generations, scores, 5)  
    p = np.poly1d(z)
    plt.plot(generations, p(generations), "r--", label="Trend Line")

    plt.plot(generations, best_scores, label='Best Score')
    plt.xlabel('Generations')
    plt.ylabel('Score')
    plt.title('Genetic Algorithm Progress')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compare best scores achieved by different algorithms for varying numbers of packages.   
def show_best_scores_graph(num_packages_list, hc_scores, sahc_scores, sa_scores, ts_scores, ga_scores):
    plt.plot(num_packages_list, hc_scores, label='Hill Climbing')
    plt.plot(num_packages_list, sahc_scores, label='Steepest Ascent Hill Climbing')
    plt.plot(num_packages_list, sa_scores, label='Simulated Annealing')
    plt.plot(num_packages_list, ts_scores, label='Tabu Search')
    plt.plot(num_packages_list, ga_scores, label='Genetic Algorithm')
    plt.xlabel('Number of Packages')
    plt.ylabel('Best Score')
    plt.title('Algorithm Best Solution Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
    
# Compare execution times of different algorithms for varying numbers of packages.
def show_times_graph(num_packages_list, hc_times, sahc_times, sa_times, ts_times, ga_times):
    plt.plot(num_packages_list, hc_times, label='Hill Climbing')
    plt.plot(num_packages_list, sahc_times, label='Steepest Ascent Hill Climbing')
    plt.plot(num_packages_list, sa_times, label='Simulated Annealing')
    plt.plot(num_packages_list, ts_times, label='Tabu Search')
    plt.plot(num_packages_list, ga_times, label='Genetic Algorithm')
    plt.xlabel('Number of Packages')
    plt.ylabel('Execution Time (s)')
    plt.title('Algorithm Execution Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()