import numpy as np 

'''
Implying Hill Climbing
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
    Evaluate the objective function 
    If it's larger than the current best 
        ---> "X_best" = "X_now"
    else:
        "X_now" = "X_best"
    If stop criteria met:
        Return "X_best"
    else:
        Back to Step 2.

'''