# Heuristic Search Methods for Problem-Solving ([A1](a1))

**Theme chosen:** Metaheuristics for Optimization/Decision Problems - Delivery Scheduling

**Description:** The objective is to develop an algorithm to optimize the delivery order of packages in a scenario where there exists packages of three types - fragile, normal, and urgent - must be transported to various delivery locations. The algorithm aims to minimize damage to the fragile packages as well as travel costs incurred for each kilometer traveled, and adhere to time constraints for urgent packages. This problem is based on the classic Traveling Salesperson problem. The system will solve multiple instances of this problem using different algorithms and the results will be compared.

## File Structure

All implemented algorithms are located in separate files, all in [a1/src](a1/src)

Neighbourhood, evaluation and graph functions are located in [a1/src/utils.py](a1/src/utils.py) file.

## Libraries

These are the necessary libraries to run our project:

| Name               | Command               |
|--------------------|-----------------------|
|   pandas           | pip install pandas    |    
|   pygame           | pip install pygame    |
|   numpy            | pip install numpy     |
|   matplotlib       | pip install matplotlib|


## Execution

To run our project all you need to do is:

``` python3 main.py ``` on the terminal. 

Note: You need to be in ```a1/src``` directory. 

## Usage

Firstly, the user will be asked to choose the number of packages, which can be defined by the user or already defined. There is also an option to run multiple instances of the problem with different numbers of packages, already predefined. After that, the user will be asked to choose the map size, which can also be defined by the user or already defined.
Then, the user will be asked to choose the algorithm(s) to run. The options are:

 - Hill Climbing
 - Steepest Ascent Hill Climbing
 - Simulated Annealing
 - Tabu Search
 - Genetic Algorithm
 - All algorithms
 - Compare 2 algorithms at a time


Every time the user chooses the Simulated Annealing algorithm, the user will be asked to choose the cooling schedule. Being able to choose a custom value or a default one(0.99).

After the algoritm(s) finish, the user will receive a message with the best solution found and the time it took to find it, as well as a visual representation of the solution and graph. In case of comparisons, the user will receive a message with the best solution found by each algorithm and the time it took to find it, as well as a visual representation of the solution and graph comparing the two algorithms.

## Authors

- Daniel Gago ([lovedzhd](https://github.com/lovedzhd))
- João Teixeira ([JTomas12](https://github.com/JTomas12))
- José Santos ([Sereno1710](https://github.com/Sereno1710))
