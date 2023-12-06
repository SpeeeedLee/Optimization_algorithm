'''
This file is for Ant Colony Optimization

Step 1. 
    For each ant k, place it at a randomly chosen node i
    Do 14 times:
        travel from previous node to another unvisited node, based on pheromone & distance of the edge 
                                                                        --> This will need "roulette wheel selection"
    Add a trip back to the start node i

Step 2.
    Calculate delta(pheromone_ij) on every edge
        --> Assuming each ant has total Pheromon Q to spread on the path.
        --> Pheromone spred on unit length, unit_pheromone = Q / (total lenght of the path)
        --> delta(pheromone_ij) = unit_pheromone * lenght(ij)
Step 3. 
    Update the pheromone map, based on 
        (pheromone)_ij = (1-rho)*pheromone_ij + delta(pheromone_ij)
        where, rho is evaporation constant

Return : the best solution being visited

'''

import numpy as np 
import random
from util import Obj_function

def update_pheromone_map(pheromone_map, path_for_all_ants, rho=0.7):
    path_for_all_ants_copy = [list(path) for path in path_for_all_ants]

    # Evaporation
    new_pheromone_map = pheromone_map * rho

    # Phemoron left by ant on path i --> j
    for ant_idx in range(len(path_for_all_ants_copy)):
        total_path = Obj_function(path_for_all_ants_copy[ant_idx])
        for i in range(len(path_for_all_ants_copy[ant_idx]) - 1):
            start = path_for_all_ants_copy[ant_idx][i]
            end = path_for_all_ants_copy[ant_idx][i + 1]
            delta_pheromon = pheromon_left_on_path(start, end, total_path)

            # Let the Pheromon Map Matrix be symmetric
            new_pheromone_map[start, end] += delta_pheromon
            new_pheromone_map[end, start] += delta_pheromon

    return new_pheromone_map


def pheromon_left_on_path(start, end, total_path):
    Distance_table = np.array([
                    [0, 27, 335, 244, 141, 257, 33, 316, 186, 115, 304, 439, 102, 95, 275],
                    [27, 0, 330, 237, 144, 268, 31, 307, 195, 113, 301, 453, 75, 111, 290],
                    [335, 330, 0, 95, 199, 193, 304, 54, 189, 221, 35, 291, 330, 271, 233],
                    [244, 237, 95, 0, 117, 171, 212, 75, 130, 130, 72, 324, 236, 191, 215],
                    [141, 144, 199, 117, 0, 137, 114, 192, 61, 36, 167, 323, 175, 74, 171],
                    [257, 268, 193, 171, 137, 0, 238, 222, 77, 173, 161, 186, 311, 162, 44],
                    [33, 31, 304, 212, 114, 238, 0, 284, 164, 84, 274, 423, 91, 83, 260],
                    [316, 307, 54, 75, 192, 222, 284, 0, 198, 205, 67, 341, 296, 266, 265],
                    [186, 195, 189, 130, 61, 77, 164, 198, 0, 96, 154, 263, 234, 97, 111],
                    [115, 113, 221, 130, 36, 173, 84, 205, 96, 0, 190, 359, 139, 74, 205],
                    [304, 301, 35, 72, 167, 161, 274, 67, 154, 190, 0, 275, 306, 237, 202],
                    [439, 453, 291, 324, 323, 186, 423, 341, 263, 359, 275, 0, 498, 344, 165],
                    [102, 75, 330, 236, 175, 311, 91, 296, 234, 139, 306, 408, 0, 170, 340],
                    [95, 111, 271, 191, 74, 162, 83, 266, 97, 74, 237, 344, 170, 0, 180],
                    [275, 290, 233, 215, 171, 44, 260, 265, 111, 205, 202, 165, 340, 180, 0]])
    
    local_factor = (500 - Distance_table[start, end])**2 # since maximum distance beween two city is 498
    global_factor = (5 - total_path / 1000)**2        # since never saw total path can exceed 4500

    delta_pheromon =  0.85 * global_factor + 0.15 * local_factor

    return delta_pheromon    


def roulette_wheel_selection(pheromone_map, visited_path):

    start = visited_path[-1]
    all_city = list(range(15))
    feasible_neighbors = list(set(all_city) - set(visited_path[:-1])) # do not consider start node itself
    
    neighbor_pheromone = []
    for neighbor_order in range(len(feasible_neighbors)):
        neighbor_pheromone.append(pheromone_map[start, feasible_neighbors[neighbor_order]])
    
    # normalize to one
    cumulative_sum = 0
    cumulative_values = []
    for element in neighbor_pheromone:
        cumulative_sum += element
        cumulative_values.append(cumulative_sum)
    last_cumulative_value = cumulative_values[-1]
    cumulative_prob_list = [element / last_cumulative_value for element in cumulative_values]

    # Start the roulette_wheel_selection
    random_number = np.random.rand()
    for neighbor_order in range(len(feasible_neighbors)):
        if random_number < cumulative_prob_list[neighbor_order]:
            next_city = feasible_neighbors[neighbor_order]
            break

    return next_city

def main(iteration = 10, num_node = 15, population_size = 10):
    
    # different from previous algorithm
    # In ACO, every ant in every round start at random node


    # set the initial pheromone map to be all 10 (except on the diogonal):
    pheromone_map = (np.ones(num_node) -np.eye(num_node)) * 10

    # Create a list for recording the experiment process    
    best_X_of_iteration = []
    best_S_of_iteration = []

    best_S_for_now = []
    best_X_for_now = []

    # iterate over every round
    for iter in range(iteration):
        
        print(f"AGO : Start the {iter} iteration")

        path_for_all_ants = []
        S_for_all_ants = []
        # iterate over every ant
        for k in range (population_size):
            path_for_current_ant = []
            start_node = random.randint(0, num_node - 1)
            end_node = start_node
            path_for_current_ant.append(start_node)
            
            while len(path_for_current_ant) < 15:
                next_node = roulette_wheel_selection(pheromone_map, path_for_current_ant)
                path_for_current_ant.append(next_node)    
            path_for_current_ant.append(end_node)

            #print(path_for_current_ant)
            path_for_all_ants.append(path_for_current_ant)
            
            # when performing the function evaluation, we don't need to find the 仁川 in our path
            # since the overall path is equivalent !!
            S_for_all_ants.append(Obj_function(path_for_current_ant))  
        
        # find the best path in an iteration
        best_S = min(S_for_all_ants)
        best_X = path_for_all_ants[S_for_all_ants.index(best_S)]
        best_S_of_iteration.append(best_S)
        best_X_of_iteration.append(best_X)
        print(best_S)
        # find the best path found SO FAR 
        best_overall_S = min(best_S_of_iteration)
        best_overall_X = best_X_of_iteration[best_S_of_iteration.index(best_overall_S)]
        best_S_for_now.append(best_overall_S)
        best_X_for_now.append(best_overall_X)

        # update the pheromone map
        pheromone_map = update_pheromone_map(pheromone_map, path_for_all_ants)
    
    return best_X_of_iteration, best_S_of_iteration, best_X_for_now, best_S_for_now

if __name__ == '__main__':
    best_X_of_iteration, best_S_of_iteration, best_X_for_now, best_S_for_now = main(iteration = 100, num_node = 15, population_size = 10)
    print("===== Ant Colony Optimization =====")
    print(f"Best shortest path is : {best_X_for_now[-1]}")
    print(f"The length of the shortest path is : {best_S_for_now[-1]}")
    print(f"The length of the shortest path found in each iteration is : \n{best_S_of_iteration}")
    print(f"The length of the shortest path found in progress is : \n{best_S_for_now}")



