from problem import *
from utils import *
from hill_climbing import *
from simulated_annealing import *
from tabu_search import *
from genetic import *

num_packages = 10
map_size = 60


def main():
    package_stream = generate_package_stream(num_packages, map_size)
    display_path(package_stream)

    """
    solution1 = get_hc_solution(package_stream, 10000, True)
    display_path(solution1)
    """

    """
    solution2 = get_sahc_solution(package_stream, True)
    display_path(solution2)
    """

    solution3 = get_sa_solution(package_stream, 10000, True)
    display_path(solution3)

    solution4 = get_tabu_solution(package_stream, 100, 5, 20 ,True)
    display_path(solution4)


    solution5 = genetic_algorithm(10000, package_stream, 50, order_based_crossover, mutate_solution_2)
    display_path(solution5)


if __name__ == "__main__":
    main()
