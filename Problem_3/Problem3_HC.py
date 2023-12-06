import numpy as np 
import random
from util import Obj_function, city_mutation



# Note that in this problem, we want to find a minima, not a maxima like in Problem 2.

def main(iteration = 100, num_node = 16):
    '''
    The main loop of Hill Climbing

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

        print(f"HC : Start the {iter} iteration")

        '''
        Step 3.
        Do the "Mutation" on "X_now"
        '''
        X_mutated, _ = city_mutation(X_now, None, None)
        s_X_mutated  = Obj_function(X_mutated)

        '''
        Step 4. 
            Evaluate the objective function of X_mutated
            If it's smaller than the current best 
                ---> "X_best" = "X_mutated"
            ---> "X_now = "X_best"
            If stop criteria met:
                Return "X_best"
            else:
                Back to Step 2.
        '''
        if s_X_mutated < s_X_best:
            X_best = X_mutated
            s_X_best = s_X_mutated
        
        print(f"{X_mutated}, path length : {s_X_mutated}, best : {s_X_best} ")

        X_now = X_best

        best_S_of_iteration.append(s_X_best)

    return X_best, s_X_best, best_S_of_iteration

if __name__ == '__main__':
    X_best, s_X_best, best_S_of_iteration = main(iteration = 100, num_node = 16)
    print("===== Hill Climbing =====")
    print(f"Best shortest path is : {X_best}")
    print(f"The length of the shortest path is : {s_X_best}")
    print(f"The length of the shortest path found in each iteration is : \n{best_S_of_iteration}")