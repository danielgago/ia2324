import random

from neighbours import get_neighbour_solution3
from utils import evaluate_solution


def get_tabu_neighbour(solution, tabu_list,tabu_size=10):
    neighbours_size = random.randint(3, tabu_size)
    neighbourhood = []
    for i in range(neighbours_size):
        neighbour = get_neighbour_solution3(solution)
        while neighbour in tabu_list:
            neighbour = get_neighbour_solution3(solution)
        if (
            not any(neighbour == pair[0] for pair in tabu_list)
            and neighbour not in neighbourhood
        ):
            neighbourhood.append(neighbour)

    return neighbourhood

def get_tabu_solution(package_stream, num_iterations, base_tabu_tenure, max_stagnation, log=False, scores_info=False):
    iteration = 0
    stagnation_count = 0
    best_solution = package_stream
    best_candidate = package_stream
    best_score = evaluate_solution(best_solution)
    tabu_list = []
    scores = []
    if log:
        print(f"Initial score: {best_score}")

    while iteration < num_iterations:
        iteration += 1
        neighbours = get_tabu_neighbour(best_candidate, tabu_list, base_tabu_tenure)
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
                base_tabu_tenure += 1
            else:
                base_tabu_tenure = max(base_tabu_tenure - 1, 3)
        scores.append((best_score, best_candidate_eval))
        tabu_list = [tabu for tabu in tabu_list if tabu[1] > 0]
        tabu_list = [[tabu[0], tabu[1] - 1] for tabu in tabu_list]
        tabu_list.append([best_candidate, base_tabu_tenure])

    if (scores_info):
        return best_solution, scores
    return best_solution