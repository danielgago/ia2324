import random, math, copy
import pandas as pd
import pygame

num_packages = 100
map_size = 1
WIDTH = 600


class Time:
    def __init__(self, minutes):
        self.days = minutes // 3600
        self.hours = (minutes % 3600) // 60
        self.minutes = minutes % 60


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
                    pygame.draw.circle(screen, RED, (draw_x, draw_y), 5)
                elif package.package_type == "urgent":
                    pygame.draw.circle(screen, GREEN, (draw_x, draw_y), 5)
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
    child1 = [None] * len(solution1)
    
    child2 = [None] * len(solution1)

    indices = sorted(random.sample(range(len(solution1)), len(solution1) // 2))

    for index in indices:
        child1[index] = solution1[index]
        child2[index] = solution2[index]
    
    solution2_rest = [pkg for pkg in solution2 if pkg not in child1]
    iterator = iter(solution2_rest)

    for i in range(len(child1)):
        if child1[i] is None:
            child1[i] = next(iterator)

    solution1_rest = [pkg for pkg in solution1 if pkg not in child2]
    iterator = iter(solution1_rest)

    for i in range(len(child2)):
        if child2[i] is None:
            child2[i] = next(iterator)
    
    return child1, child2
    




def main():
    package_stream = generate_package_stream(num_packages, map_size)

    df1 = solution_to_data_frame(package_stream)
    pd.set_option("display.max_columns", None)
    print(df1.iloc[0:, :])

    stats1 = DeliveryStats(package_stream, 0, 0, 0)
    stats1.show()

    solution = get_hc_solution(package_stream, 10000)
    df2 = solution_to_data_frame(solution)
    print(df2.iloc[0:, :])

    stats2 = DeliveryStats(solution, 0, 0, 0)
    stats2.show()


if __name__ == "__main__":
    main()
