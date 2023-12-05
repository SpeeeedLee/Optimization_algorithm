import numpy as np 

# Deifine the constraints function
def constraint_max_weight(X):
    '''
    Output whether the carrying items satisfy the weight constraints
    '''
    W = [3.3, 3.4, 6.0, 26.1, 37.6, 62.5, 100.2, 141.1, 119.2, 122.4, 247.6, 352.0, 24.2, 32.1, 42.5] 
    total_weights = np.dot(W,X)

    if total_weights > 529:
        return False
    else:
        return True


def constraint_carry_items(X):
    '''
    Output whether the carrying items satisfy the constraint : "at least one knife, one pistal and one equipment"
    '''
    knife_location = [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]
    pistal_location = [0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]
    equipment_location = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1] 
    
    if np.dot(knife_location, X) >= 1 and np.dot(pistal_location, X) >= 1 and np.dot(equipment_location, X) >= 1 :
        return True
    else:
        return False
    
def check_bonus(X):
    '''
    A function for checking how much bonus points X will get
    '''
    bonus_points = 0

    # If you carry shadow daggers and desert eagle magnum at the same time, add an additional 5 survival points
    if X[0] == 1 and X[5] == 1:
        bonus_points += 5
    # If you carry 228 compact handgun and either AK-47 rifle or M4A1 carbine at the same time, add an additional 15 survival points
    if (X[3] == 1 and X[9] == 1) or (X[3] == 1 and X[8] ==1):
        bonus_points += 15
    # If you carry all three equipments in your inventory, add an additional 70 survival points
    if(X[12] == 1) and (X[13] == 1) and (X[14] == 1):
        bonus_points += 70
    #If you carry either Leone YG1265 Auto Shotgun or Krieg 500 Sniper Rifles as primary
    #weapon, plus Desert Eagle Magnum and tactical shield, add an additional 25 survival points
    if ((X[7] == 1) and (X[5] == 1) and (X[14] == 1)) or ((X[10] == 1) and (X[5] == 1) and (X[14] == 1)):
        bonus_points += 25

    return bonus_points

def Obj_function(X, penalty):
    '''
    Calculte how much is the survival points, given the items in the inventory bag.
    Consider all the bounus points.
    Additionally, consider penalty if violated the two constraints : "constraint_max_weight", "constraint_carry_items"
    Whether consider penalty is constrolled by a boolean parameter : "penalty"
    '''
    S = [7,8,13,29,48,99,177,213,202,210,380,485,9,12,15]
    original_points = np.dot(S,X)
    bonus_points = check_bonus(X)
    total_points = original_points + bonus_points

    # consider penalty, which is a soft constraint when consider "constraint_max_weight", 
    # and a strick constraint when consider "constraint_carry_items"
    # the points will only be positive, so it is easier for calculation in selection process.
    if penalty:
        penalty_points = 0
        if not constraint_max_weight(X):
            W = [3.3, 3.4, 6.0, 26.1, 37.6, 62.5, 100.2, 141.1, 119.2, 122.4, 247.6, 352.0, 24.2, 32.1, 42.5] 
            total_weights = np.dot(W,X)
            penalty_points += 5*(total_weights - 529)**2
            #penalty_points += 2000
        if not constraint_carry_items(X):
            penalty_points += 2000
        total_points -= penalty_points
        if total_points < 0:
            total_points = 0
    return total_points

def decimal_to_binary_array(decimal_number):
        '''
        This is a function to convert decimal number to binary number, 
        so that we can easily iterate over the whole solution space using decimal number
        '''
        # decimal to binary using python function, remove the prefix
        binary_string = bin(decimal_number)[2:]
        # Pad the binary string with zeros to make its length 15
        binary_string_padded = binary_string.zfill(15)
        # Convert the string to an array
        binary_list = [int(bit) for bit in binary_string_padded]
        binary_array = np.array(binary_list)
        return binary_array


# (b) Calculate the maximum number of possible combinations of inventory bags
'''
Since the solution space is just 2^15 -1 = 32767  (omitting the constraints)
Is it feasible to iterate over the whole solution space, and exclude the solutions that do not satisfy any constraints
'''
if __name__ == "__main__":
    max_decimal = 32767
    n_possible_soulutions = 0
    for i in range (32767 + 1):
        X = decimal_to_binary_array(i)
        if constraint_max_weight(X) and constraint_carry_items(X):
            n_possible_soulutions += 1

    print(n_possible_soulutions) # 6455
