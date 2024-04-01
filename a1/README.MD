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




