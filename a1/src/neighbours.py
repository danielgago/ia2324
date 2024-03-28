# Pick a package and place it somewhere else on the solution
import copy
import random

from utils import evaluate_solution


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


def get_all_neighbours(solution):
    neighbours = []

    for i in range(len(solution)):
        neighbour = copy.deepcopy(solution)
        package = neighbour.pop(i)
        for j in range(len(solution)):
            neighbour2 = copy.deepcopy(neighbour)
            neighbour2.insert(j, package)
            neighbours.append(neighbour2)

    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbour = copy.deepcopy(solution)
            neighbour[i], neighbour[j] = neighbour[j], neighbour[i]
            neighbours.append(neighbour)
    return neighbours


def get_best_neighbour(neighbours):
    best_neighbour = neighbours[0]
    best_score = evaluate_solution(best_neighbour)
    for neighbour in neighbours:
        score = evaluate_solution(neighbour)
        if score > best_score:
            best_neighbour = neighbour
            best_score = score
    return best_neighbour