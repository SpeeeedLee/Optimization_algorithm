from Problem2_util import *
import random

'''
X : A individual in the population
all_X : All chromosome now in the population (each row is for a individual)
'''

def roulette_wheel_selection(all_X, population_size = 10):
    '''
    Given all_x, first calulate survuval points each solution gets, and stored in S_all_X.
    Secondly, calculate the probability of selection based on S_all_X, and stored in Prob_all_X, 
    Finally, get the selection results by roulette wheel selection.
    '''
    S_all_X = np.zeros((all_X.shape[0], 1))
    all_S = 0
    Prob_all_x = np.zeros((all_X.shape[0], 1))
    cummulated_Prob_all_x = np.zeros((all_X.shape[0], 1))

    for i in range(all_X.shape[0]):
        S_X = Obj_function(all_X[i, :], True) # use penalty
        S_all_X[i] = S_X
        all_S += S_X

    for i in range (Prob_all_x.shape[0]):
        prob = S_all_X[i] / all_S
        Prob_all_x[i] = prob
        if i == 0:
            cummulated_Prob_all_x[i] = prob
        else:
            cummulated_Prob_all_x[i] = cummulated_Prob_all_x[i-1] + prob

    selected_X = np.zeros((population_size, all_X.shape[1]))
    for i in range(population_size):
        random_number = np.random.rand()
        for j in range(cummulated_Prob_all_x.shape[0]):
            if cummulated_Prob_all_x[j] > random_number:
                selected_X[i,:] = all_X[j,:]
                break

    return S_all_X, Prob_all_x, cummulated_Prob_all_x, selected_X


def choose_two_parents(population_size, chosen_parents):
    '''
    Do not want the same combination of parents that is already appeared in "chosen parents"
    '''
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

def crossover_loop(selected_X, population_size = 10, crossover_prob = 0.1):
    
    '''
    The mechanism of this function is as follows:
    1. Random sample two different parents from the selected population
    2. Use the crossover porbability = 0.1 to perform unifrom crossover 
        In more details:
        with 10% probability --> create two children using unifrom crossover
        with 90% probability --> copy the two parents as children
    3. Back to 1. until there are 10 children created
    ** Will want to avoid sample the same parent sets **
    '''
    chosen_parents = [] # record the chosen parents so we can avoid same parents combination
    children_all_X = np.zeros((population_size, selected_X.shape[1]))
    created_children = 0
    while created_children < population_size:
        (parent_1_idx, parent_2_idx) = choose_two_parents(population_size, chosen_parents)
        chosen_parents.append((parent_1_idx, parent_2_idx))
       
        # perform uniform crossover
        children_X1, children_X2 = uniform_crossover(selected_X[parent_1_idx, :], selected_X[parent_2_idx, :], crossover_prob)         
        children_all_X[created_children, :] = children_X1
        children_all_X[created_children + 1 , :] = children_X2

        created_children += 2

        '''
        # This is not the question want us to do !
        else:
            # do not perform crossover, just simple copy the same Gene
            children_all_X[created_children, :] = selected_X[parent_1_idx, :] 
            children_all_X[created_children + 1 , :] = selected_X[parent_2_idx, :]
        '''
    return children_all_X



def uniform_crossover(parent_X1, parent_X2, crossover_prob):
    '''
    Generate a 1*15 random list for reference, with its element being either 0 or 1
    Each element of this random list is 1 with corssover_prob, 0 with (1-crossover_prob) 
    if 0 --> (90%)
    the first children will look at the first parent at that location
    the second children will look at the second parent at that location
    
    if 1 --> (10%)
    the first children will look at the second parent at that location
    the second children will look at the first parent at that location
    '''
    reference_list = []
    for i in range(parent_X1.shape[0]):
        random_num = np.random.rand()
        if random_num >  crossover_prob:
            reference_list.append(0)
        else:
            reference_list.append(1)

    children_X1 = np.zeros_like(parent_X1)
    children_X2 = np.zeros_like(parent_X2)

    for i in range(parent_X1.shape[0]):
        if reference_list[i] == 0 :
            children_X1[i] = parent_X1[i]
            children_X2[i] = parent_X2[i]
        else:
            children_X1[i] = parent_X2[i]
            children_X2[i] = parent_X1[i]
    
    return children_X1, children_X2
            
 


def multi_bit_mutation(X, mutation_prob = 0.20):
    '''
    Do the multi bit flip mutation (consecutive based on item types), 
    In more details, 
        ranodom choose one item type from the total 4 item types
        flip the bit on items belong to that type only
    '''
    random_number = np.random.rand()
    if random_number > mutation_prob:
        return X
    else:
        chosen_item_type = random.randint(1, 4)
        if chosen_item_type == 1:
            flip_location = [0,1,2]
            X[flip_location] = 1 - X[flip_location]
        elif chosen_item_type == 2:
            flip_location = [3,4,5]
            X[flip_location] = 1 - X[flip_location]
        elif chosen_item_type == 3:    
            flip_location = [6,7,8,9,10,11]
            X[flip_location] = 1 - X[flip_location]
        elif chosen_item_type == 4:
            flip_location = [12,13,14]
            X[flip_location] = 1 - X[flip_location]
        return X

    
def main(iteration = 20, crossover_prob = 0.1, mutation_prob = 0.20, bit_length = 15, population_size = 10):
    '''
    The main loop of GA
    input arguments:
    iteration, crossober_prob, mutation_prob, bit_length, population_size

    Need to add the visualizatio in the future
    '''

    # Generate the first population, denoted as all_X
    # each row is a solution, overall 10 rows
    all_X = np.random.randint(2, size=(population_size, bit_length))
    
    # Create a list for recording the experiment process
    # Create a list for recording the experiment process    
    best_Xwc_of_iteration = []
    best_S_of_iteration = []

    best_S_for_now = []
    best_Xwc_for_now = []

    # Start the GA simulation
    for i in range(iteration):

        print(f"GA : start the {i} iteration")

        # select the better solutions using roulette wheel mechanism (with replacement)
        _, _, _, selected_X = roulette_wheel_selection(all_X)
        
        # do the crossover
        children_all_X = crossover_loop(selected_X, population_size = population_size, crossover_prob = crossover_prob)

        # do the mutation
        next_X = np.zeros_like(all_X)
        idx = 0
        for children in children_all_X:
            mutated_children = multi_bit_mutation(children, mutation_prob)
            next_X[idx, :] = mutated_children
            idx += 1

        # Store the next_X as all_X, to perform another round
        all_X = next_X

        # calculate the solution points, all_S
        all_S = []
        check_constraints = []
        for X in all_X:
            all_S.append(Obj_function(X, False)) # In the evaluation step, so do not use penalty
            
            # Check whether the final soulution satisfy all constraints (strickly)
            if constraint_max_weight(X) and constraint_carry_items(X):
                check_constraints.append(True)
            else:
                check_constraints.append(False)
        # find the max in all_S that satisfy the constraints
        all_S_constraints =  [0 if not condition else element for element, condition in zip(all_S, check_constraints)]
        max_S_w_constraints = max(all_S_constraints)
        best_Xwc = all_X[all_S_constraints.index(max_S_w_constraints)]
        best_S_of_iteration.append(max_S_w_constraints)
        best_Xwc_of_iteration.append(best_Xwc)

        # find the best combination found SO FAR 
        best_overall_S = max(best_S_of_iteration)
        best_overall_Xwc = best_Xwc_of_iteration[best_S_of_iteration.index(best_overall_S)]
        best_S_for_now.append(best_overall_S)
        best_Xwc_for_now.append(best_overall_Xwc)

    '''
    # for final generation, calculate in more details
    # find the max in all_S
    max_S = max(all_S)
    # find the carrying weights of the best solution
    best_index = all_S.index(max_S_w_constraints)
    best_solution = all_X[best_index, :]
    W = [3.3, 3.4, 6.0, 26.1, 37.6, 62.5, 100.2, 141.1, 119.2, 122.4, 247.6, 352.0, 24.2, 32.1, 42.5] 
    carrying_weights = np.dot(W,best_solution)
    '''

    return best_Xwc_of_iteration, best_S_of_iteration, best_Xwc_for_now, best_S_for_now


if __name__ == '__main__':
    best_Xwc_of_iteration, best_S_of_iteration, best_Xwc_for_now, best_S_for_now = main(iteration = 20, crossover_prob = 0.1, mutation_prob = 0.10, bit_length = 15, population_size = 10)

    print("===== Genetic Alforithm =====")
    print(f"Best combination found is : {best_Xwc_for_now[-1]}")
    print(f"The largest survival point is : {best_S_for_now[-1]}")
    print(f"The largest survival point found in each iteration is : \n{best_S_of_iteration}")
    print(f"The largest survival point found in progress is : \n{best_S_for_now}")

    # print(f"All Solutions in the final Generation : \n{all_X}")
    # print(f"All Survival points in the final Generation : \n{all_S}")
    # print(f"Maximun Survival points in the final Generation : \n{max_S}")
    # print(f"Do every final solutions satisfy the constraints ? : \n{check_constraints}")
    # print(f"Maximun Survival points in the final Generation that satisfy every constraints : \n{max_S_w_constraints}")
    # print(f"Best suitable solution : \n{best_solution}")
    # print(f"Carrying weights of the best solution : \n{carrying_weights}")
