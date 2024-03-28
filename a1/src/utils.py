import copy
import math
import random
import pygame
import pandas as pd


def generate_random_solution(package_stream):
    solution = copy.deepcopy(package_stream)
    random.shuffle(solution)
    return solution

def evaluate_solution(solution):
    #declare the variables in one line
    
    last_x = 0
    last_y = 0
    total_dist = 0
    total_breaking_cost = 0
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

def print_solution_ids(solution):
    sol = "["
    for package in solution:
        sol += f"{package}, "
    sol = sol[:-2]
    sol += "]"
    print(sol)

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

    delivery_path = [(0, 0)]  # Starting point

    # Calculate delivery path
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

        # Update the screen
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