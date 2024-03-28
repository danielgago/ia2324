import copy
import math
import random

from neighbours import get_neighbour_solution3
from utils import evaluate_solution


def prob(current_score, new_score, temperature):
    if new_score >= current_score:
        return 2
    return math.exp(-(current_score - new_score) / temperature)


def get_sa_solution(package_stream, num_iterations, log=False):
    it = 0
    it_no_imp = 0
    temperature = 1000
    solution = copy.deepcopy(package_stream)
    score = evaluate_solution(solution)

    best_solution = copy.deepcopy(solution)
    best_score = score

    if log:
        print(f"Initial score: {best_score}")

    while it_no_imp < num_iterations:
        temperature = temperature * 0.999
        it += 1
        it_no_imp += 1

        temp_solution = get_neighbour_solution3(solution)
        temp_score = evaluate_solution(temp_solution)

        if temp_score > best_score:
            best_solution = copy.deepcopy(temp_solution)
            best_score = temp_score
            it_no_imp = 0
            if log:
                print(f"New best score: {temp_score}")
        if prob(score, temp_score, temperature) >= random.random():
            solution = copy.deepcopy(temp_solution)
            score = temp_score

    return best_solution