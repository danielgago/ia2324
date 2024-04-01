import random

from neighbours import get_random_neighbour_solution
from utils import evaluate_solution

# Obtains a random number of neighbours for the current solution, ensuring that they are not in the tabu list.
def get_tabu_neighbour(solution, tabu_list):
    neighbours_size = random.randint(3, 10)
    neighbourhood = []
    for i in range(neighbours_size):
        neighbour = get_random_neighbour_solution(solution)
        while neighbour in tabu_list:
            neighbour = get_random_neighbour_solution(solution)
        if (
            not any(neighbour == pair[0] for pair in tabu_list)
            and neighbour not in neighbourhood
        ):
            neighbourhood.append(neighbour)

    return neighbourhood

# Executes the tabu search algorithm over a specified number of iterations. It has a base tabu tenure and a maximum stagnation count.
# The base tabu tenure is used to determine the number of iterations a solution is kept in the tabu list. It also increases when the algorithm stagnates.
# The maximum stagnation count is used to determine when the algorithm has stagnated.
def get_tabu_solution(package_stream,num_iterations, base_tabu_tenure, max_stagnation, log=False, scores_info=False):
    iteration = 0
    stagnation_count = 0
    best_solution = package_stream
    best_candidate = None
    best_score = evaluate_solution(best_solution)
    tabu_list = []
    scores = []
    if log:
        print(f"Initial score: {best_score}")

    while iteration < num_iterations:
        iteration += 1
        neighbours = get_tabu_neighbour(best_solution, tabu_list)
        best_candidate_eval = -float('inf')
        for neighbour in neighbours:
            neighbour_score = evaluate_solution(neighbour)
            if neighbour_score > best_candidate_eval:
                best_candidate = neighbour
                best_candidate_eval = neighbour_score

        if best_candidate_eval == -float("inf"):
            break

        if best_candidate_eval > best_score:
            best_solution = best_candidate
            best_score = best_candidate_eval
            iteration = 0
            stagnation_count = 0
            if log:
                print(f"New best score: {best_score}")
        else:
            stagnation_count += 1
            if stagnation_count >= max_stagnation:
                base_tabu_tenure = int(base_tabu_tenure + pow(base_tabu_tenure, 0.5))
                stagnation_count = 0   

        scores.append((best_score, best_candidate_eval))
        tabu_list = [tabu for tabu in tabu_list if tabu[1] > 0]
        tabu_list = [[tabu[0], tabu[1] - 1] for tabu in tabu_list]
        tabu_list.append([best_candidate, base_tabu_tenure])

    if (scores_info):
        return best_solution, scores
    return best_solution