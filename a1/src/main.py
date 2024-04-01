import time

from problem import *
from utils import *
from hill_climbing import *
from simulated_annealing import *
from tabu_search import *
from genetic import *


def print_package_num():
    print("Welcome to the package delivery system!")
    print("")
    print("How many packages would you like to deliver?")
    print("1. 10 packages")
    print("2. 30 packages")
    print("3. 50 packages")
    print("4. Generate multiple list of packages")
    print("5. Custom number of packages")
    print("6. Exit")
    return int(input("Enter your choice: "))

def print_map_size():
    print("What is the size of the map?")
    print("1. 10x10")
    print("2. 20x20")
    print("3. 30x30")
    print("4. Custom size")
    print("5. Back")
    choice = int(input("Enter your choice: "))
    return choice
    
def print_options():
    print("Which algorithm would you like to use?")
    print("1. Hill Climbing")
    print("2. Steepest Ascent Hill Climbing")
    print("3. Simulated Annealing")
    print("4. Tabu Search")
    print("5. Genetic Algorithm")
    print("6. Compare all")
    print("7. Compare two algorithms")
    print("8. Back")
    choice = int(input("Enter your choice: "))
    return choice

def print_end():
    print("Thank you for using the package delivery system!")
    print("Goodbye!")

def get_cooling_schedule():
    print("What cooling level would you like to use?")
    print("Note: The cooling level should be less than 1.")
    while True:
        print("Enter the cooling level: ")
        print("1. Default cooling level (0.99)")
        print("2. Custom cooling level")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            cooling = 0.99
            break
        elif choice == 2:
            while True:
                cooling = float(input("Enter the cooling level (T < 1): "))
                if cooling >= 1:
                    print("Invalid cooling level. Please enter a valid cooling level.")
                else:
                    break
            break
        else:
            print("Invalid choice. Please enter a valid choice.")
    return cooling

def print_both_options():
    print("Which two algorithms would you like to compare?")
    print("1. Hill Climbing vs Steepest Ascent Hill Climbing")
    print("2. Hill Climbing vs Simulated Annealing")
    print("3. Hill Climbing vs Tabu Search")
    print("4. Hill Climbing vs Genetic Algorithm")
    print("5. Steepest Ascent Hill Climbing vs Simulated Annealing")
    print("6. Steepest Ascent Hill Climbing vs Tabu Search")
    print("7. Steepest Ascent Hill Climbing vs Genetic Algorithm")
    print("8. Simulated Annealing vs Tabu Search")
    print("9. Simulated Annealing vs Genetic Algorithm")
    print("10. Tabu Search vs Genetic Algorithm")
    print("11. Back")
    return int(input("Enter your choice: "))


def main():
    num_packages = 0
    map_size = 0
    num_package_list = []
    both_choice = 0
    choice = 0
    while True:
        num_packages_choice = print_package_num()
        if num_packages_choice in [1,2,3,4]:
            break
        elif num_packages_choice == 5:
            print("Enter the number of packages:")
            num_packages = int(input())
            break
        elif num_packages_choice == 6:
            print_end()
            return
        else:
            print("Invalid choice. Please enter a valid choice.")
    while True:        
        map_size_choice = print_map_size()
        if map_size_choice in [1,2,3]:
            break
        elif map_size_choice == 4:
            print("Enter the size of the map:")
            map_size = int(input())
            break
        elif map_size_choice == 5:
            main()
            return
        else:
            print("Invalid choice. Please enter a valid choice.")
    
    if num_packages_choice == 1:
        num_packages = 10
    elif num_packages_choice == 2:
        num_packages = 30
    elif num_packages_choice == 3:
        num_packages = 50
    elif num_packages_choice == 4:
        num_package_list = [15,20,25,30,35,40,45,50]


    while True:
        choice = print_options()
        if choice in [1,2,3,4,5,6]:
            break
        elif choice == 7:
            while True:
                both_choice = print_both_options()
                if both_choice in [1,2,3,4,5,6,7,8,9,10]:
                    break
                elif both_choice == 11:
                    main()
                    return
                else:
                    print("Invalid choice. Please enter a valid choice.")
            choice = 0
            break
        elif choice == 8:
            main()
            return
        else:
            print("Invalid choice. Please enter a valid choice.")

    if map_size_choice != 4:
        map_size = map_size_choice*10

    package_stream = generate_package_stream(num_packages, map_size)

    if choice == 1 and num_packages_choice != 4: 

        start_time = time.time()
        solution, scores = get_hc_solution(package_stream, 1000, False,True)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print(f"Best score: {evaluate_solution(solution)}")
        print("Hill Climbing:",print_solution_ids(solution))
        display_path(solution,map_size)
        show_hc_graph(scores)

    elif choice == 1 and num_packages_choice == 4:
        hc_scores = []
        hc_times = []

        for num_package in num_package_list:
            package_stream = generate_package_stream(num_package, map_size)
            start_time = time.time()
            solution = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_scores.append(evaluate_solution(solution))
            hc_times.append(execution_time)

        show_best_scores_graph_single(num_package_list, hc_scores, "Hill Climbing")
        show_times_graph_single(num_package_list, hc_times, "Hill Climbing") 

    elif choice == 2 and num_packages_choice != 4:
        start_time = time.time()
        solution,scores = get_sahc_solution(package_stream, False,True)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print(f"Best score: {evaluate_solution(solution)}")
        print("Steepest Ascent Hill Climbing:",print_solution_ids(solution))
        display_path(solution,map_size)
        show_hc_graph(scores)

    elif choice == 2 and num_packages_choice == 4:
        sahc_scores = []
        sahc_times = []

        for num_package in num_package_list:
            package_stream = generate_package_stream(num_package, map_size)
            start_time = time.time()
            solution = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_scores.append(evaluate_solution(solution))
            sahc_times.append(execution_time)

        show_best_scores_graph_single(num_package_list, sahc_scores, "Steepest Ascent Hill Climbing")
        show_times_graph_single(num_package_list, sahc_times, "Steepest Ascent Hill Climbing")

    elif choice == 3 and num_packages_choice != 4:

        cooling = get_cooling_schedule()
        
        start_time = time.time()
        solution,scores = get_sa_solution(package_stream, False, True, cooling)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print(f"Best score: {evaluate_solution(solution)}")
        print("Simulated Annealing:", print_solution_ids(solution))
        display_path(solution,map_size)
        show_sa_graph(scores)
    
    elif choice == 3 and num_packages_choice == 4:
        sa_scores = []
        sa_times = []
        cooling = get_cooling_schedule()
        for num_package in num_package_list:
            package_stream = generate_package_stream(num_package, map_size)
            start_time = time.time()
            solution = get_sa_solution(package_stream, False, True,cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_scores.append(evaluate_solution(solution))
            sa_times.append(execution_time)

        show_best_scores_graph_single(num_package_list, sa_scores, "Simulated Annealing")
        show_times_graph_single(num_package_list, sa_times, "Simulated Annealing")
    
    elif choice == 4 and num_packages_choice != 4:

        start_time = time.time()
        solution,scores = get_tabu_solution(package_stream, 200, 5, num_packages ,False, True)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print(f"Best score: {evaluate_solution(solution)}")
        print("Tabu Search:",print_solution_ids(solution))
        display_path(solution,map_size)
        show_ts_graph(scores)
    
    elif choice == 4 and num_packages_choice == 4:

        ts_scores = []
        ts_times = []

        for num_package in num_package_list:
            package_stream = generate_package_stream(num_package, map_size)
            start_time = time.time()
            solution = get_tabu_solution(package_stream, 200, 5, num_package ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_scores.append(evaluate_solution(solution))
            ts_times.append(execution_time)

        show_best_scores_graph_single(num_package_list, ts_scores, "Tabu Search")
        show_times_graph_single(num_package_list, ts_times, "Tabu Search")
    
    elif choice == 5 and num_packages_choice != 4:
        generations = num_packages*20
        population_size = int(generations/10)
        start_time = time.time()
        solution,scores= genetic_algorithm(generations, package_stream, population_size, False ,True)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time}")
        print(f"Best score: {evaluate_solution(solution)}")
        print("Genetic Algorithm:",print_solution_ids(solution))
        display_path(solution,map_size)
        show_ga_graph(scores)
    
    elif choice == 5 and num_packages_choice == 4:
        ga_scores = []
        ga_times = []

        for num_package in num_package_list:
            package_stream = generate_package_stream(num_package, map_size)
            generations = num_package*20
            population_size = int(generations/10)
            start_time = time.time()
            solution = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_scores.append(evaluate_solution(solution))
            ga_times.append(execution_time)

        show_best_scores_graph_single(num_package_list, ga_scores, "Genetic Algorithm")
        show_times_graph_single(num_package_list, ga_times, "Genetic Algorithm")
        
    elif choice == 6 and num_packages_choice != 4:
        cooling= get_cooling_schedule()
        start_time = time.time()
        solution1 = get_hc_solution(package_stream, 1000, False)
        end_time = time.time()
        execution_time = end_time - start_time
        hc_score= evaluate_solution(solution1)
        hc_time= execution_time
        print("Hill Climbing:",print_solution_ids(solution1))
        display_path(solution1,map_size)


        start_time = time.time()
        solution2 = get_sahc_solution(package_stream, False)
        end_time = time.time()
        execution_time = end_time - start_time
        sahc_score= evaluate_solution(solution2)
        sahc_time= execution_time
        print("Steepest Ascent Hill Climbing:",print_solution_ids(solution2))
        display_path(solution2,map_size)

        start_time = time.time()
        solution3 = get_sa_solution(package_stream, False, False, cooling)
        end_time = time.time()
        execution_time = end_time - start_time
        sa_score= evaluate_solution(solution3)
        sa_time= execution_time
        print("Simulated Annealing:",print_solution_ids(solution3))
        display_path(solution3,map_size)

        start_time = time.time()
        solution4 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
        end_time = time.time()
        execution_time = end_time - start_time
        ts_score= evaluate_solution(solution4)
        ts_time= execution_time
        print("Tabu Search:",print_solution_ids(solution4))
        display_path(solution4,map_size)
        
        start_time = time.time()
        generations = num_packages*20
        population_size = int(generations/10)
        solution5 = genetic_algorithm(generations, package_stream, population_size, False)
        end_time = time.time()
        execution_time = end_time - start_time
        ga_score= evaluate_solution(solution5)
        ga_time= execution_time
        print("Genetic Algorithm:",print_solution_ids(solution5))
        display_path(solution5,map_size)

        show_best_scores_graph_same(num_packages,hc_score, sahc_score, sa_score, ts_score, ga_score)
        show_times_graph_same(num_packages,hc_time, sahc_time, sa_time, ts_time, ga_time)

    elif choice == 0 and num_packages_choice != 4:
        if both_choice == 1: 
            start_time = time.time()
            solution1 = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_score = evaluate_solution(solution1)
            print("Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_score = evaluate_solution(solution2)
            print("Steepest Ascent Hill Climbing:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,hc_score, sahc_score, 0, 0, 0)
            show_times_graph_same(num_packages,execution_time, execution_time, 0, 0, 0)

        elif both_choice == 2:
            cooling= get_cooling_schedule()
            start_time = time.time()
            solution1 = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_score = evaluate_solution(solution1)
            print("Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_sa_solution(package_stream, False, False, cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_score = evaluate_solution(solution2)
            print("Simulated Annealing:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,hc_score, 0, sa_score, 0, 0)
            show_times_graph_same(num_package_list, hc_times, 0, sa_times, 0, 0)

        elif both_choice == 3:
            start_time = time.time()
            solution1 = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_score = evaluate_solution(solution1)
            print("Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_score = evaluate_solution(solution2)
            print("Tabu Search:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,hc_score, 0, 0, ts_score, 0)
            show_times_graph_same(num_package_list, hc_times, 0, 0, ts_times, 0)

        elif both_choice == 4:
            start_time = time.time()
            solution1 = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_score = evaluate_solution(solution1)
            print("Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            generations = num_packages*20
            population_size = int(generations/10)
            solution2 = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_score = evaluate_solution(solution2)
            print("Genetic Algorithm:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,hc_score, 0, 0, 0, ga_score)
            show_times_graph_same(num_package_list, hc_times, 0, 0, 0, ga_times)

        elif both_choice == 5:
            cooling= get_cooling_schedule()
            start_time = time.time()
            solution1 = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_score = evaluate_solution(solution1)
            print("Steepest Ascent Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_sa_solution(package_stream, False, False, cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_score = evaluate_solution(solution2)
            print("Simulated Annealing:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, sahc_score, sa_score, 0, 0)
            show_times_graph_same(num_package_list, 0, sahc_times, sa_times, 0, 0)

        elif both_choice == 6:
            start_time = time.time()
            solution1 = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_score = evaluate_solution(solution1)
            print("Steepest Ascent Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_score = evaluate_solution(solution2)
            print("Tabu Search:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, sahc_score, 0, ts_score, 0)
            show_times_graph_same(num_package_list, 0, sahc_times, 0, ts_times, 0)

        elif both_choice == 7:
            start_time = time.time()
            solution1 = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_score = evaluate_solution(solution1)
            print("Steepest Ascent Hill Climbing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            generations = num_packages*20
            population_size = int(generations/10)
            solution2 = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_score = evaluate_solution(solution2)
            print("Genetic Algorithm:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, sahc_score, 0, 0, ga_score)
            show_times_graph_same(num_package_list, 0, sahc_times, 0, 0, ga_times)

        elif both_choice == 8:
            cooling= get_cooling_schedule()
            start_time = time.time()
            solution1 = get_sa_solution(package_stream, False, False, cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_score = evaluate_solution(solution1)
            print("Simulated Annealing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_score = evaluate_solution(solution2)
            print("Tabu Search:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, 0, sa_score, ts_score, 0)
            show_times_graph_same(num_package_list, 0, 0, sa_times, ts_times, 0)

        elif both_choice == 9:
            cooling= get_cooling_schedule()
            start_time = time.time()
            solution1 = get_sa_solution(package_stream, False, False, cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_score = evaluate_solution(solution1)
            print("Simulated Annealing:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            generations = num_packages*20
            population_size = int(generations/10)
            solution2 = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_score = evaluate_solution(solution2)
            print("Genetic Algorithm:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, 0, sa_score, 0, ga_score)
            show_times_graph_same(num_package_list, 0, 0, sa_times, 0, ga_times)

        elif both_choice == 10:
            start_time = time.time()
            solution1 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_score = evaluate_solution(solution1)
            print("Tabu Search:",print_solution_ids(solution1))
            display_path(solution1,map_size)

            start_time = time.time()
            generations = num_packages*20
            population_size = int(generations/10)
            solution2 = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_score = evaluate_solution(solution2)
            print("Genetic Algorithm:",print_solution_ids(solution2))
            display_path(solution2,map_size)

            show_best_scores_graph_same(num_packages,0, 0, 0, ts_score, ga_score)
            show_times_graph_same(num_package_list, 0, 0, 0, ts_times, ga_times)

    elif choice == 0 and num_packages_choice == 4:
        if both_choice == 1:
            hc_scores = []
            hc_times = []
            sahc_scores = []
            sahc_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_hc_solution(package_stream, 1000, False)
                end_time = time.time()
                execution_time = end_time - start_time
                hc_scores.append(evaluate_solution(solution1))
                hc_times.append(execution_time)

                start_time = time.time()
                solution2 = get_sahc_solution(package_stream, False)
                end_time = time.time()
                execution_time = end_time - start_time
                sahc_scores.append(evaluate_solution(solution2))
                sahc_times.append(execution_time)

            show_hc_score_comparison_graph(num_package_list, hc_scores, sahc_scores)
            show_hc_time_comparison_graph(num_package_list, hc_times, sahc_times)

        elif both_choice == 2:

            cooling= get_cooling_schedule()
            hc_scores = []
            hc_times = []
            sa_scores = []
            sa_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_hc_solution(package_stream, 1000, False)
                end_time = time.time()
                execution_time = end_time - start_time
                hc_scores.append(evaluate_solution(solution1))
                hc_times.append(execution_time)

                start_time = time.time()
                solution2 = get_sa_solution(package_stream, False, False, cooling)
                end_time = time.time()
                execution_time = end_time - start_time
                sa_scores.append(evaluate_solution(solution2))
                sa_times.append(execution_time)

            show_best_scores_graph(num_package_list, hc_scores, [], sa_scores, [], [])
            show_times_graph(num_package_list, hc_times, [], sa_times, [], [])

        elif both_choice == 3:
            hc_scores = []
            hc_times = []
            ts_scores = []
            ts_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_hc_solution(package_stream, 1000, False)
                end_time = time.time()
                execution_time = end_time - start_time
                hc_scores.append(evaluate_solution(solution1))
                hc_times.append(execution_time)

                start_time = time.time()
                solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ts_scores.append(evaluate_solution(solution2))
                ts_times.append(execution_time)

            show_best_scores_graph(num_package_list, hc_scores, [], [], ts_scores, [])
            show_times_graph(num_package_list, hc_times, [], [], ts_times, [])
        elif both_choice == 4:
            hc_scores = []
            hc_times = []
            ga_scores = []
            ga_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_hc_solution(package_stream, 1000, False)
                end_time = time.time()
                execution_time = end_time - start_time
                hc_scores.append(evaluate_solution(solution1))
                hc_times.append(execution_time)

                start_time = time.time()
                generations = num_packages*20
                population_size = int(generations/10)
                solution2 = genetic_algorithm(generations, package_stream, population_size, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ga_scores.append(evaluate_solution(solution2))
                ga_times.append(execution_time)

            show_best_scores_graph(num_package_list, hc_scores, [], [], [], ga_scores)
            show_times_graph(num_package_list, hc_times, [], [], [], ga_times)
        elif both_choice == 5:
            cooling= get_cooling_schedule()
            sahc_scores = []
            sahc_times = []
            sa_scores = []
            sa_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_sahc_solution(package_stream, False)
                end_time = time.time()
                execution_time = end_time - start_time
                sahc_scores.append(evaluate_solution(solution1))
                sahc_times.append(execution_time)

                start_time = time.time()
                solution2 = get_sa_solution(package_stream, False, False, cooling)
                end_time = time.time()
                execution_time = end_time - start_time
                sa_scores.append(evaluate_solution(solution2))
                sa_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], sahc_scores, sa_scores, [], [])
            show_times_graph(num_package_list, [], sahc_times, sa_times, [], [])
        elif both_choice == 6:
            sahc_scores = []
            sahc_times = []
            ts_scores = []
            ts_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_sahc_solution(package_stream, False)
                end_time = time.time()
                execution_time = end_time - start_time
                sahc_scores.append(evaluate_solution(solution1))
                sahc_times.append(execution_time)

                start_time = time.time()
                solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ts_scores.append(evaluate_solution(solution2))
                ts_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], sahc_scores, [], ts_scores, [])
            show_times_graph(num_package_list, [], sahc_times, [], ts_times, [])
        elif both_choice == 7:
            sahc_scores = []
            sahc_times = []
            ga_scores = []
            ga_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_sahc_solution(package_stream, False)
                end_time = time.time()
                execution_time = end_time - start_time
                sahc_scores.append(evaluate_solution(solution1))
                sahc_times.append(execution_time)

                start_time = time.time()
                generations = num_packages*20
                population_size = int(generations/10)
                solution2 = genetic_algorithm(generations, package_stream, population_size, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ga_scores.append(evaluate_solution(solution2))
                ga_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], sahc_scores, [], [], ga_scores)
            show_times_graph(num_package_list, [], sahc_times, [], [], ga_times)

        elif both_choice == 8:
            cooling= get_cooling_schedule()
            sa_scores = []
            sa_times = []
            ts_scores = []
            ts_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_sa_solution(package_stream, False, False, cooling)
                end_time = time.time()
                execution_time = end_time - start_time
                sa_scores.append(evaluate_solution(solution1))
                sa_times.append(execution_time)

                start_time = time.time()
                solution2 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ts_scores.append(evaluate_solution(solution2))
                ts_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], [], sa_scores, ts_scores, [])
            show_times_graph(num_package_list, [], [], sa_times, ts_times, [])

        elif both_choice == 9:
            cooling= get_cooling_schedule()
            sa_scores = []
            sa_times = []
            ga_scores = []
            ga_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_sa_solution(package_stream, False, False, cooling)
                end_time = time.time()
                execution_time = end_time - start_time
                sa_scores.append(evaluate_solution(solution1))
                sa_times.append(execution_time)

                start_time = time.time()
                generations = num_packages*20
                population_size = int(generations/10)
                solution2 = genetic_algorithm(generations, package_stream, population_size, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ga_scores.append(evaluate_solution(solution2))
                ga_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], [], sa_scores, [], ga_scores)
            show_times_graph(num_package_list, [], [], sa_times, [], ga_times)
        elif both_choice == 10:
            ts_scores = []
            ts_times = []
            ga_scores = []
            ga_times = []
            for num_packages in num_package_list:
                package_stream = generate_package_stream(num_packages, map_size)
                start_time = time.time()
                solution1 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ts_scores.append(evaluate_solution(solution1))
                ts_times.append(execution_time)

                start_time = time.time()
                generations = num_packages*20
                population_size = int(generations/10)
                solution2 = genetic_algorithm(generations, package_stream, population_size, False)
                end_time = time.time()
                execution_time = end_time - start_time
                ga_scores.append(evaluate_solution(solution2))
                ga_times.append(execution_time)

            show_best_scores_graph(num_package_list, [], [], [], ts_scores, ga_scores)
            show_times_graph(num_package_list, [], [], [], ts_times, ga_times)
    else: 
        hc_scores = []
        hc_times = []
        sahc_scores = []
        sahc_times = []
        sa_scores = []
        sa_times = []
        ts_scores = []
        ts_times = []
        ga_scores = []
        ga_times = []
        cooling= get_cooling_schedule()

        for num_packages in num_package_list:        
            package_stream = generate_package_stream(num_packages, map_size)

            start_time = time.time()
            solution1 = get_hc_solution(package_stream, 1000, False)
            end_time = time.time()
            execution_time = end_time - start_time
            hc_scores.append(evaluate_solution(solution1))
            hc_times.append(execution_time)

            start_time = time.time()
            solution2 = get_sahc_solution(package_stream, False)
            end_time = time.time()
            execution_time = end_time - start_time
            sahc_scores.append(evaluate_solution(solution2))
            sahc_times.append(execution_time)

            start_time = time.time()
            solution3 = get_sa_solution(package_stream, False, False, cooling)
            end_time = time.time()
            execution_time = end_time - start_time
            sa_scores.append(evaluate_solution(solution3))
            sa_times.append(execution_time)

            start_time = time.time()
            solution4 = get_tabu_solution(package_stream, 200, 5, num_packages ,False, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ts_scores.append(evaluate_solution(solution4))
            ts_times.append(execution_time)
            
            start_time = time.time()
            generations = num_packages*20
            population_size = int(generations/10)
            solution5 = genetic_algorithm(generations, package_stream, population_size, False)
            end_time = time.time()
            execution_time = end_time - start_time
            ga_scores.append(evaluate_solution(solution5))
            ga_times.append(execution_time)
            
        show_best_scores_graph(num_package_list, hc_scores, sahc_scores, sa_scores, ts_scores, ga_scores)
        show_times_graph(num_package_list, hc_times, sahc_times, sa_times, ts_times, ga_times)
    
    print("")
    print("Would you like to try another option?")
    print("")
    print("1. Yes")
    print("2. No")
    print("")
    choice = int(input("Enter your choice: "))
    if choice == 2:
        print_end()
        return
    else:
        main()
        
if __name__ == "__main__":
    main()
