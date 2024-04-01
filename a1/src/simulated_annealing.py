import copy
import math
import random

from neighbours import get_random_neighbour_solution
from utils import evaluate_solution


def prob(current_score, new_score, temperature):
    if new_score >= current_score:
        return 2
    return math.exp(-(current_score - new_score) / temperature)


def get_sa_solution(package_stream, num_iterations, log=False, scores_info=False):
    it = 0
    it_no_imp = 0
    temperature = 1000
    solution = copy.deepcopy(package_stream)
    score = evaluate_solution(solution)

    best_solution = copy.deepcopy(solution)
    best_score = score
    
    scores = []

    if log:
        print(f"Initial score: {best_score}")

    while temperature > 0.1:
        temperature = temperature * 0.99
        it += 1
        it_no_imp += 1

        temp_solution = get_random_neighbour_solution(solution)
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
        scores.append((best_score, score))
        
    if(scores_info):
        return best_solution, scores
    else:
        return best_solution
