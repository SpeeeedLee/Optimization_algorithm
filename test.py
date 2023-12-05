import numpy as np
import random

def choose_two_parents(population_size, chosen_parents):
    available_parents = list(range(population_size))

    while True:
        parent_1_idx = random.choice(available_parents)
        available_parents.remove(parent_1_idx)
    
        parent_2_idx = random.choice(available_parents)

        if (parent_1_idx, parent_2_idx) not in chosen_parents and (parent_2_idx, parent_1_idx) not in chosen_parents:
            chosen_parents.append((parent_1_idx, parent_2_idx))
            break
    
    if parent_1_idx < parent_2_idx:        
        return (parent_1_idx, parent_2_idx)
    else:
        return (parent_2_idx, parent_1_idx)

print(choose_two_parents(4, [(0,1), (0,2), (0,3), (1,2)]))