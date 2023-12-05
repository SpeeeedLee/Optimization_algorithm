import numpy as np
import matplotlib.pyplot as plt
import problem2_GA, problem2_HC, problem2_RW

'''
Ploting the diagram:
y axis : objective function of the best solution  
x axis : number of function evaluation 
(for RW & FC, is equivalent to iteration round；for GA, equivalent to (iteration round) * (population size) )

Do 10 experiments for each of the 3 algorithms and plot the mean and standard deviation
'''


def run(bit_length, iteration, exp_num, population_size, crossover_prob, mutation_prob):
    
    S_GA = []
    S_HC = []
    S_RW = []

    for exp in range(exp_num):
        _, _, _, _, _, _, _, GA_best_S_of_iteration = problem2_GA.main(
            int(iteration / population_size), crossover_prob, mutation_prob, bit_length, population_size)
        S_GA.append(GA_best_S_of_iteration)
        
        _, _, HC_best_S_of_iteration = problem2_HC.main(iteration, crossover_prob, mutation_prob, bit_length)
        S_HC.append(HC_best_S_of_iteration)

        _, _, RW_best_S_of_iteration = problem2_RW.main(iteration, crossover_prob, mutation_prob, bit_length)
        S_RW.append(RW_best_S_of_iteration)

    S_GA_arr = np.array(S_GA)
    S_HC_arr = np.array(S_HC)
    S_RW_arr = np.array(S_RW)

    GA_means = np.mean(S_GA_arr, axis=0).tolist()
    HC_means = np.mean(S_HC_arr, axis=0).tolist()
    RW_means = np.mean(S_RW_arr, axis=0).tolist()
    
    GA_stds = np.std(S_GA_arr, axis=0).tolist()
    HC_stds = np.std(S_HC_arr, axis=0).tolist()
    RW_stds = np.std(S_RW_arr, axis=0).tolist()

    # Need to "strech" the results of GA"
    expanded_GA_means = [item for item in GA_means for _ in range(population_size)]
    expanded_GA_stds = [item for item in GA_stds for _ in range(population_size)]


    return expanded_GA_means, expanded_GA_stds, HC_means, HC_stds, RW_means, RW_stds


def plot_and_save(means1, stds1, means2, stds2, means3, stds3):
    '''
    Given the experiment data as input, plot and save the desired diagram
    '''

    plt.figure(figsize=(18, 12))  

    x_values = range(len(means1))

    plt.plot(x_values, means1, label='GA', marker='', linestyle='-')
    plt.plot(x_values, means2, label='HC', marker='', linestyle='-')
    plt.plot(x_values, means3, label='RW', marker='', linestyle='-')

    plt.fill_between(x_values, np.array(means1) - np.array(stds1), np.array(means1) + np.array(stds1), alpha=0.3)
    plt.fill_between(x_values, np.array(means2) - np.array(stds2), np.array(means2) + np.array(stds2), alpha=0.3)
    plt.fill_between(x_values, np.array(means3) - np.array(stds2), np.array(means3) + np.array(stds3), alpha=0.3)

    plt.xlabel('Function Evaluation Used')
    plt.ylabel('Max Survival Points Found')
    plt.title('Comparison of 3 different algorithms')

    x_tick_positions = x_values[::100]
    x_tick_labels = x_tick_positions  # 使用x值作为标签
    plt.xticks(x_tick_positions, x_tick_labels)
    
    plt.ylim(0, 1000) 
    
    plt.legend()
    plt.grid(True)
    plt.savefig('./Problem_2/progress_diagram.png', dpi=300)
    plt.show()



if __name__ == '__main__':
    expanded_GA_means, expanded_GA_stds, HC_means, HC_stds, RW_means, RW_stds = run(
        bit_length = 15, iteration = 800, exp_num = 10, population_size = 10, crossover_prob = 0.1, mutation_prob = 0.3)
    
    plot_and_save(expanded_GA_means, expanded_GA_stds, HC_means, HC_stds, RW_means, RW_stds)