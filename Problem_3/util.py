import numpy as np 
import random


'''
Creat the location table as a numpy array
In the table, the 15 cities are set to follow the below order:
Incheon, Seoul, Busan, Daegu, Daejeon, Gwangju, suwon-si, Ulsan, Jeonju, Cheongju-si, Changwon, Jeju-si, Chuncheon, Hongsung, Muan

reference : https://www.distancecalculator.net/country/south-korea

'''
# (a)
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


# (b) Calculate how many evaluation of objective function required if one attempts the exhaustive enumeration

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == '__main__':
    all_possible_solution = factorial(15) # 1307674368000
    print(f"number of evaluation of objective function required if using exhaustive enumeration : {all_possible_solution}") 


# (c) Random Walk
'''
The design solution vector X, which is a one dimensional *list* with lenght 16, 
Each middle element in the vector is a positive integer from 1 to 14. No repeat value (Do not visit the same city twice)
The first element and the last element are 0 (start and end at Incheon)

We use city_mutation() to perform a local search.
Also, we use Obj_function() to calculate the overall distance.
In this problem, we do not set any constraints(compare to problem 2), since we now just do not allow a mutation from 
feasible solution to non-feasible solution in city_mutation()
'''

def Obj_function(X):
    '''
    Simply compute the overall distance of the given path X
    '''
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
    
    distance = 0
    for i in range(len(X)):
        if i != 0:
            distance += Distance_table[X[i], X[i-1]]

    return distance

def city_mutation(X, limit_1, limit_2):
    '''
    The mutation of the previous solution is defined as:
        33% possibility --> performing 3* (2-opt operation), i.e doing 3 node reversing in 3 random locations
        33% possibility --> performing 2* (reinsertion), i.e. random sample two nodes, and reisert them in other locations
        33% possibility --> performing 1* (fliping path whose length is >= 3), i.e. random sample start node & lenght(>=3)
    ** The start node & the end node will not be considered !
    '''

    num_node =len(X)
    random_number = np.random.rand()
    
    if random_number <= 1/3:
        mutated_X = two_opt_mutation(X, num_node)
        mutated_type = 1
        print("==== 2-opt operation ====")
    elif random_number >= 2/3:
        mutated_X = reinsertion_mutation(X, num_node)
        mutated_type = 2
        print("====   Reinsertion   ====")
    else:
        mutated_X = flip_path_mutation(X, num_node)
        mutated_type = 3
        print("====    Flip Path    ====")

    return mutated_X, mutated_type

def two_opt_mutation(X, num_node):
    '''
    Sampling random positive integer to represent the location of left node to perform reversing
    '''

    possible_left_idx = list(range(1, num_node-2)) # from 1 to (num_node - 3)

    left_idx_1 = random.choice(possible_left_idx)
    possible_left_idx.remove(left_idx_1)
    left_idx_2 = random.choice(possible_left_idx)
    possible_left_idx.remove(left_idx_2)
    left_idx_3 = random.choice(possible_left_idx)

    temp_left = X[left_idx_1]
    X[left_idx_1] = X[left_idx_1 + 1]
    X[left_idx_1 + 1] = temp_left

    temp_left = X[left_idx_2]
    X[left_idx_2] = X[left_idx_2 + 1]
    X[left_idx_2 + 1] = temp_left    
    
    temp_left = X[left_idx_3]
    X[left_idx_3] = X[left_idx_3 + 1]
    X[left_idx_3 + 1] = temp_left

    return X


def reinsertion_mutation(X, num_node):
    def perform_reinsertion(X):
        draw_idx = random.choice(range(1, num_node - 1))
        insert_idx = random.choice([i for i in range(1, num_node - 1) if i != draw_idx])
        draw_node = X.pop(draw_idx)
        X.insert(insert_idx, draw_node)

    perform_reinsertion(X)
    perform_reinsertion(X)

    return X

def flip_path_mutation(X, num_node):
    random_length = random.randint(3, num_node - 2)
    start_node_idx = random.randint(1, num_node - random_length - 1)

    if start_node_idx + random_length >= num_node - 1:
        random_length = num_node - start_node_idx - 2

    reversed_segment = list(reversed(X[start_node_idx : start_node_idx + random_length]))

    X[start_node_idx : start_node_idx + random_length] = reversed_segment

    return X
