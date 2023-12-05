import numpy as np 
import random
from Problem2_util import constraint_max_weight, constraint_carry_items, decimal_to_binary_array, Obj_function
from problem2_GA import uniform_crossover, multi_bit_mutation

### Need to add the code for plotting !! ###
# 每一輪都輸出X_best


'''
Implying Random Walk
The overall steps is as follows:

Step 1.
    Generate a random initial solution (each bit is 50% to be 0, 50% to be 1)
Step 2. 
    Check if the initial solution satisfy the constraints.
    If don't, "get_nearest_feasible"
        ---> Store it in "X_now"
        ---> "X_best" = "X_now"
Step 3.
    Do the "Mutation" on "X_now", more details of the designed mutation process are listed below:
        a. cut off at 8th bit (0~7、8~14)
        b. reverse and copy each part, form two parents
        c. perform uniform crossover with probability = 0.1
        d. pick either of the output children at random
        e. perform multi bit flip mutation (consecutive based on itme types)
Step 4. 
    Check if the mutated solution satisfy the constraints.
    If don't, "get_nearest_feasible"
        ---> Store it in "X_mutated"
Step 5. 
    "X_now = X_mutated"
    Evaluate the objective function 
    If it's larger than the current best 
        ---> "X_best" = "X_now"
    If stop criteria met:
        Return "X_best"
    else:
        Back to Step 3.

'''

def generate_nearest_feasible(X):
    '''
    Convert the binary strings X to decimal number,
    and find another closet decimal number that is a feasible solution
    We already known that the input X itself is not a feasible solution.
    '''

    binary_string = ''.join(map(str, X))
    decimal_number = int(binary_string, 2)
    
    find_feasible = False
    increment = 0
    while not find_feasible:
        increment += 1
        if decimal_number + increment <= 32767: # check whether exceed upper bound
            upper_try_X = decimal_to_binary_array(decimal_number + increment)
            if constraint_max_weight(upper_try_X) and constraint_carry_items(upper_try_X):
                nearest_feasible_X = upper_try_X
                find_feasible = True
        if decimal_number - increment >= 0: # check whether exceed lower bound
            lower_try_X = decimal_to_binary_array(decimal_number - increment)
            if constraint_max_weight(lower_try_X) and constraint_carry_items(lower_try_X):
                nearest_feasible_X = lower_try_X
                find_feasible = True

    return nearest_feasible_X


def main(iteration = 200, crossover_prob = 0.1, mutation_prob = 0.20, bit_length = 15):
    '''
    The main loop of Random Walk
    input arguments:
    iteration, crossober_prob, mutation_prob, bit_length

    Need to add the visualizatio in the future
    '''

    '''
    Step 1.
        Generate a random initial solution (each bit is 50% to be 0, 50% to be 1)
    Step 2. 
        Check if the initial solution satisfy the constraints.
        If don't, "get_nearest_feasible"
            ---> Store it in "X_now"
            ---> "X_best" = "X_now"
    '''
    X = np.random.randint(2, size=(bit_length))
    if constraint_max_weight(X) and constraint_carry_items(X):
        X_now = X
        X_best = X
        s_X_best = Obj_function(X_best, False)
    else:
        X = generate_nearest_feasible(X)
        X_now = X
        X_best = X
        s_X_best = Obj_function(X_best, False)


    for iter in range(iteration):

        print(f"Start the {iter} iteration")

        '''
        Step 3.
        Do the "Mutation" on "X_now", more details of the designed mutation process are listed below:
            a. cut off at 8th bit (0~7、7~14)
            b. reverse and copy each part, form two parents
            c. perform uniform crossover with probability = 0.1
            d. pick either of the output children at random
            e. perform multi bit flip mutation (consecutive based on itme types)
        '''
        # a & b 
        X_parent_1 = X_now[:8] # first 8 bits
        X_parent_2 = X_now[7:] # last 8 bits
        X_parent_1 = np.concatenate((X_parent_1, X_parent_1[::-1]))
        X_parent_2 = np.concatenate((X_parent_2, X_parent_2[::-1])) # length is now 16, too long
        # Cropping the first or the final bit at random 
        random_num = np.random.rand()
        if random_num > 0.5:
            X_parent_1 = X_parent_1[:15]
            X_parent_2 = X_parent_2[1:]
        else:
            X_parent_1 = X_parent_1[1:]
            X_parent_2 = X_parent_2[:15]

        # c & d
        children_X1, children_X2 = uniform_crossover(X_parent_1, X_parent_2, crossover_prob)
        random_num = random.randint(1, 2)
        if random_num == 1:
            children_X = children_X1
        else:
            children_X = children_X2
        
        # e
        X_mutated = multi_bit_mutation(children_X, mutation_prob)

        '''
        Step 4. 
        Check if the mutated solution satisfy the constraints.
        If don't, "get_nearest_feasible"
            ---> Store it in "X_mutated"
        Step 5. 
        "X_now = X_mutated"
        Evaluate the objective function 
        If it's larger than the current best 
            ---> "X_best" = "X_now"
        If stop criteria met:
            Return "X_best"
        else:
            Back to Step 2.
        '''
        if constraint_max_weight(X_mutated) and constraint_carry_items(X_mutated):
            X_now = X_mutated
        else:
            X_mutated = generate_nearest_feasible(X_mutated)
            X_now = X_mutated
        
        s_X_now  = Obj_function(X_now, False)
        if s_X_now > s_X_best:
            X_best = X_now
            s_X_best = s_X_now


    return X_best, s_X_best


X_best, s_X_best = main(iteration = 200, crossover_prob = 0.1, mutation_prob = 0.20, bit_length = 15)
print("===== Random Walk =====")
print(f"Best suitable solution founded is : {X_best}")
print(f"The survival point is : {s_X_best}")




