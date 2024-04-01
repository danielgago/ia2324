from neighbours import get_random_neighbour_solution, get_all_neighbours, get_best_neighbour
from utils import evaluate_solution


def get_hc_solution(package_stream, num_iterations, log=False, scores_info=False):
    iteration = 0
    best_solution = package_stream
    best_score = evaluate_solution(best_solution)
    
    scores = []

    if log:
        print(f"Initial score: {best_score}")

    while iteration < num_iterations:
        iteration += 1
        neighbor_solution = get_random_neighbour_solution(best_solution)
        neighbor_score = evaluate_solution(neighbor_solution)

        if neighbor_score > best_score:
            best_solution = neighbor_solution
            best_score = neighbor_score
            iteration = 0
            if log:
                print(f"New best score: {neighbor_score}")
        scores.append((best_score, neighbor_score))


    if(scores_info):
        return best_solution, scores
    else:
        return best_solution

def get_sahc_solution(package_stream, log=False, scores_info=False):
    best_solution = package_stream
    best_score = evaluate_solution(best_solution)

    if log:
        print(f"Initial score: {best_score}")
    
    scores = []

    improved = True
    while improved:
        improved = False
        neighbours = get_all_neighbours(best_solution)
        neighbour_solution = get_best_neighbour(neighbours)
        neighbor_score = evaluate_solution(neighbour_solution)

        if neighbor_score > best_score:
            best_solution = neighbour_solution
            best_score = neighbor_score
            improved = True
            if log:
                print(f"New best score: {neighbor_score}")
        scores.append((best_score, neighbor_score))

    if(scores_info):
        return best_solution, scores
    else:
        return best_solution
