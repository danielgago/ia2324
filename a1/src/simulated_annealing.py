import copy
import math
import random

from neighbours import get_random_neighbour_solution
from utils import evaluate_solution


def prob(current_score, new_score, temperature):
    if new_score >= current_score:
        return 2
    # This formula is used to calculate the probability of accepting the new score if it's worse than the current score.
    return math.exp(-(current_score - new_score) / temperature)

# Executes the Simulated Annealing algorithm with an optional cooling schedule.
def get_sa_solution(package_stream, log=False, scores_info=False, cooling=0.99):
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
        # Default temperature is 0.99 to ensure the algorithm doesn't converge too fast or too slow.
        temperature = temperature * cooling
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
        # If the new solution is better or the probability of accepting it is greater than a random number, the solution is updated.
        if prob(score, temp_score, temperature) >= random.random():
            solution = copy.deepcopy(temp_solution)
            score = temp_score
        scores.append((best_score, score))
        
    if(scores_info):
        return best_solution, scores
    return best_solution