import random, math, copy
import pandas as pd


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
            total_breaking_cost += p_damage*package.breaking_cost # Expected value of breaking cost

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


# Example: Generate a stream of 15 packages in a map of size 60x60
num_packages = 15
map_size = 60
package_stream = generate_package_stream(num_packages, map_size)

df1 = solution_to_data_frame(package_stream)
pd.set_option("display.max_columns", None)
print(df1.iloc[0:, :])

solution = get_hc_solution(package_stream, 10000)
df2 = solution_to_data_frame(solution)
print(df2.iloc[0:, :])
