'''
Let's assume in the Tabu Search, we can only use the exact same three mutation operator as in Hill Climbing and Random Walk.

The three operator and simple demos are as follows:
original --> [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
==== 2-opt operation ====
(switch neighbor nodes sequentially at random 3 location)
[0, 2, 1, 3, 4, 6, 7, 5, 8, 9, 0] 
[0, 2, 1, 4, 3, 5, 6, 8, 7, 9, 0]
...
====   Reinsertion   ====
(pick a random node out and insert it at another random location, do twice sequentially)
[0, 1, 6, 3, 2, 4, 5, 7, 8, 9, 0] 
[0, 1, 9, 2, 3, 7, 4, 5, 6, 8, 0]
...
====    Flip Path    ====
(pick random two nodes as start and end, reverse the path in beween. The chosen path should be >= 3)
[0, 1, 8, 7, 6, 5, 4, 3, 2, 9, 0] 
[0, 1, 2, 8, 7, 6, 5, 4, 3, 9, 0]
...

=========================================================================================================

Now, remember that the spirit of the Tabu Search is to generalize the Random Walk process so that 
it can avoid walking to the next solution as a way too similar to the previous walking.
i.e.
"solution 1 --(walk a)--> solution 2 --(walk b)--> solution 3..."
*Do not want (walk b) to be to similar as (walk a), so that the algorithm can aprroach new solution space

So, it's intuitively that in our case, we choose "Mutation Operators" as our "Tabu Object".
Also, if we want the algorithm can try as many different possible solutions as possible in the same iteration number,
then according to my understanding(& guessing), the algorithm should work something like follows:

"solution 1 --(reinsertion)--> solution 2 --(Flip Path)--> solution 3 --(2-opt operation)-->...."
"solution 1 --(reinsertion)--> solution 2 --(2-opt operation)--> solution 3 --(Flip Path)-->...."
...

Thus, the Tabu Tenure will be set to "2" to encourage this kind of behavior
Tabu List is with lenght "2" also

=========================================================================================================

However, to prevent the algorithm to be totally manipulated(guided) by our above designs, 
we give an "Aspiration Criteria" : 
if mod(iteratoin_num, 7) == 0:
    clear the Tabu List
'''

import numpy as np 
import random
from util import Obj_function, city_mutation

# Note that in this problem, we want to find a minima, not a maxima like in Problem 2.

def main(iteration = 100, num_node = 16):
    '''
    The main loop of Tabu Search

    Step 1.
        Generate a random initial solution (A list, starts from 0, end at 0, no repeating node in between)
        Generate a Tabu List
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
    
    tabu_list = []

    # Create a list for recording the experiment process
    best_S_of_iteration = []

    for iter in range(iteration):

        print(f"TS : Start the {iter} iteration")

        if np.mod(iter, 7) == 0:
            tabu_list = []
        '''
        Step 3.
        Do the "Mutation" on "X_now"
        '''
        X_mutated = city_mutation(X_now, tabu_list[0], tabu_list[1])
        print(X_mutated)

        '''
        Step 4. 
            "X_now = X_mutated"
            Evaluate the objective function 
            If it's smaller than the current best 
                ---> "X_best" = "X_now"
            If stop criteria met:
                Return "X_best"
            else:
                Back to Step 2.
        '''
        X_now = X_mutated
        
        s_X_now  = Obj_function(X_now)
        if s_X_now < s_X_best:
            X_best = X_now
            s_X_best = s_X_now
        
        best_S_of_iteration.append(s_X_best)

    return X_best, s_X_best, best_S_of_iteration

if __name__ == '__main__':
    X_best, s_X_best, best_S_of_iteration = main(iteration = 100, num_node = 16)
    print("===== Tabu Search =====")
    print(f"Best shortest path is : {X_best}")
    print(f"The length of the shortest path is : {s_X_best}")
    print(f"The length of the shortest path found in each iteration is : \n{best_S_of_iteration}")
