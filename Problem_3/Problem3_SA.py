'''
Simulated Annealing is a variation of Hill Climbing,
with a additional parameter "Temperature" for controlling the accepting probability for going to a non-better solution.

Temerature is scheduled as "Linear Decay" :
    T(iteration) = T_start * (1 - iteration / total iteration)
    where, T_start is a hyperparameter

The accepting probability of a better point is 1
The accepting probability of a non-better point is decided by current Temperature(T) :
    Accept_prob = np.exp(-(dealta_E) / T)
    where, dealta_E is a positive number, meaning the "climbing value" of the evaluation function

In case of the next solution is non-better, 
    If accept, then start form that non-better solution in next iteration, 
    else, start from the current best solution in next iteration.
'''

# Note that in this problem, we want to find a minima, not a maxima like in Problem 2.

import numpy as np 
import random
from util import Obj_function, city_mutation

def get_Temp_Linear(curr_iter , iteration, start_Temp = 200):
    '''
    To decide the hyperparameter start_Temp, one can reference on the following :
        exp(-1) = 0.368
    
    One can ask "how much (dealta E) in the first iteration do I want so that it will be accepted by prob = 0.368 ?"
    --> My ans for this is 200
    '''

    cuur_Temp = start_Temp * (1 - (curr_iter /iteration))

    return cuur_Temp




def main(iteration = 100, num_node = 16):
    '''
    The main loop of Simulated Annealing

    Step 1.
        Generate a random initial solution (A list, starts from 0, end at 0, no repeating node in between)
    Step 2.     
        ---> Store it in "X_now"
        ---> "X_best" = "X_now"
    '''
    X = random.sample(range(1, num_node-1), num_node-2)
    X = [0] + X + [0]
    print(X)

    X_now = X
    X_best = X
    s_X_best = Obj_function(X_best)

    # Create a list for recording the experiment process
    best_S_of_iteration = []

    for iter in range(iteration):

        print(f"SA : Start the {iter} iteration")

        s_X_now = Obj_function(X_now)
        print(f"{X_now}, path length : {s_X_now}, best : {s_X_best}")

        X_mutated, _ = city_mutation(X_now, None, None)
        s_X_mutated  = Obj_function(X_mutated)

        if s_X_mutated < s_X_now:
            X_now = X_mutated
            # Maybe not just find the better in local, but find the best in global
            if s_X_mutated < s_X_best:
                X_best = X_mutated
                s_X_best = s_X_mutated
        else:
            random_number = np.random.rand()
            dealta_E = s_X_now - s_X_mutated
            curr_Temp = get_Temp_Linear(iter , iteration, start_Temp = 200)
            if (np.exp(-(dealta_E) / curr_Temp) > random_number):
                X_now = X_mutated

        best_S_of_iteration.append(s_X_best)

    return X_best, s_X_best, best_S_of_iteration

if __name__ == '__main__':
    X_best, s_X_best, best_S_of_iteration = main(iteration = 100, num_node = 16)
    print("===== Hill Climbing =====")
    print(f"Best shortest path is : {X_best}")
    print(f"The length of the shortest path is : {s_X_best}")
    print(f"The length of the shortest path found in each iteration is : \n{best_S_of_iteration}")