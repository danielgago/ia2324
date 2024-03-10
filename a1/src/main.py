import random, math, copy
import pandas as pd


class Package:
    def __init__(self, package_type, coordinates):
        self.package_type = package_type
        self.coordinates_x = coordinates[0]
        self.coordinates_y = coordinates[1]
        if package_type == "fragile":
            self.breaking_chance = random.uniform(
                0.0001, 0.01
            )  # 0.01-1% chance of breaking per km
            self.breaking_cost = random.uniform(3, 10)  # Extra cost in case of breaking
        elif package_type == "urgent":
            self.delivery_time = random.uniform(
                100, 240
            )  # Delivery time in minutes (100 minutes to 4 hours)


def generate_package_stream(num_packages, map_size):
    package_types = ["fragile", "normal", "urgent"]
    package_stream = [
        Package(
            random.choice(package_types),
            (random.uniform(0, map_size), random.uniform(0, map_size)),
        )
        for _ in range(num_packages)
    ]
    return package_stream

def evaluate_solution(solution):
    last_x = 0
    last_y = 0
    total_dist = 0
    total_breaking_cost = 0
    total_urgent_cost = 0
    
    for package in package_stream:
        dist = math.sqrt((package.coordinates_x - last_x)**2 + (package.coordinates_y - last_y)**2)
        total_dist += dist
        
        last_x = package.coordinates_x
        last_y = package.coordinates_y
        
        if package.package_type == "fragile":
            p_damage = 1 - ((1 - package.breaking_chance) ** total_dist)
            if random.uniform(0, 1) < p_damage:
                total_breaking_cost += package.breaking_cost
           
        if(package.package_type == "urgent"):
            if(total_dist > package.delivery_time): # 60km/h = 1km/min so total_dist is equal to the minutes elapsed
                total_urgent_cost += (total_dist - package.delivery_time) * 0.3   
                
    total_cost = total_dist*0.3 + total_breaking_cost + total_urgent_cost
        
    return -total_cost

# Pick a package and place it somewhere else on the solution
def get_neighbour_solution1(solution):
    neighbour = copy.deepcopy(solution)
    
    package_number = random.randint(0, len(neighbour))
    package = neighbour.pop(package_number)
    
    new_pos = random.randint(0, len(neighbour))
    
    neighbour.insert(new_pos, package)
    

# Swap 2 packages from the order
def get_neighbour_solution2(solution):
    neighbour = copy.deepcopy(solution)
    package1 = random.randint(0, len(neighbour))
    package2 = random.randint(0, len(neighbour))
    neighbour[package1], neighbour[package2] = neighbour[package2], neighbour[package1]
    
    return neighbour
    
# Neighbour 1 or 2 with 50% each
def get_neighbour_solution3(solution): 
    if random.randint(0, 2) == 0:
        return get_neighbour_solution1(solution)
    else:
        return get_neighbour_solution2(solution)
    
def midpoint_crossover(solution_1, solution_2):
    length = len(solution_1)
    midpoint = length // 2

    #Your Code Here
    child_1 = solution_1[:midpoint] + solution_2[midpoint:]
    child_2 = solution_2[:midpoint] + solution_1[midpoint:]

    return child_1, child_2

def randompoint_crossover(solution_1, solution_2):
    length = len(solution_1)
    midpoint = random.randint(0, length)

    #Your Code Here
    child_1 = solution_1[:midpoint] + solution_2[midpoint:]
    child_2 = solution_2[:midpoint] + solution_1[midpoint:]

    return child_1, child_2

# Example: Generate a stream of 15 packages in a map of size 60x60
num_packages = 15
map_size = 60
package_stream = generate_package_stream(num_packages, map_size)
df = pd.DataFrame(
    [
        (
            i,
            package.package_type,
            package.coordinates_x,
            package.coordinates_y,
            package.breaking_chance if package.package_type == "fragile" else None,
            package.breaking_cost if package.package_type == "fragile" else None,
            package.delivery_time if package.package_type == "urgent" else None,
        )
        for i, package in enumerate(package_stream, start=1)
    ],
    columns=[
        "Package",
        "Type",
        "CoordinatesX",
        "CoordinatesY",
        "Breaking Chance",
        "Breaking Cost",
        "Delivery Time",
    ],
)

pd.set_option('display.max_columns', None)
print(df.iloc[0:,:])
print(evaluate_solution(package_stream))

"""
#Example: Randomly assign a package as broken based on distance_covered
distance_covered = sum(distances)
chance_of_damage = package.breaking_chance
p_damage = 1 - ((1 - chance_of_damage) ** distance_covered)
if random.uniform(0, 1) < p_damage:
    print('Package broken')
"""
