import numpy as np
import matplotlib.pyplot as plt
import Problem3_RW, Problem3_HC, Problem3_TS, Problem3_SA, Problem3_ACO

'''
Ploting the diagram:
y axis : objective function of the best solution found so far 
x axis : number of function evaluation 
-->
    for RW、HC、TS、SA, is equivalent to iteration round；
    for ACO, is equivalent to (iteration round) * (population size)

Do 10 experiments for each of the algorithms and plot the mean and standard deviation
'''


def run(num_node = 16, iteration = 100, exp_num = 10, population_size = 10):
    
    S_ACO = []
    S_RW = []
    S_HC = []
    S_TS = []
    S_SA = []

    for exp in range(exp_num):
        _, _, _, ACO_best_S_of_iteration = Problem3_ACO.main(
                            iteration = int(iteration / population_size), num_node = num_node - 1, population_size = population_size)
        S_ACO.append(ACO_best_S_of_iteration)
        
        _, _, HC_best_S_of_iteration = Problem3_HC.main(iteration = iteration, num_node = num_node)
        S_HC.append(HC_best_S_of_iteration)

        _, _, RW_best_S_of_iteration = Problem3_RW.main(iteration = iteration, num_node = num_node)
        S_RW.append(RW_best_S_of_iteration)

        _, _, TS_best_S_of_iteration = Problem3_TS.main(iteration = iteration, num_node = num_node)
        S_TS.append(TS_best_S_of_iteration)

        _, _, SA_best_S_of_iteration = Problem3_SA.main(iteration = iteration, num_node = num_node)
        S_SA.append(TS_best_S_of_iteration)


    S_ACO_arr = np.array(S_ACO)
    S_HC_arr = np.array(S_HC)
    S_RW_arr = np.array(S_RW)
    S_TS_arr = np.array(S_TS)
    S_SA_arr = np.array(S_SA)

    ACO_means = np.mean(S_ACO_arr, axis=0).tolist()
    HC_means = np.mean(S_HC_arr, axis=0).tolist()
    RW_means = np.mean(S_RW_arr, axis=0).tolist()
    TS_means = np.mean(S_TS_arr, axis=0).tolist()
    SA_means = np.mean(S_SA_arr, axis=0).tolist()
    
    ACO_stds = np.std(S_ACO_arr, axis=0).tolist()
    HC_stds = np.std(S_HC_arr, axis=0).tolist()
    RW_stds = np.std(S_RW_arr, axis=0).tolist()
    TS_stds = np.std(S_TS_arr, axis=0).tolist()
    SA_stds = np.std(S_SA_arr, axis=0).tolist()

    # Need to "strech" the results of ACO"
    expanded_ACO_means = [item for item in ACO_means for _ in range(population_size)]
    expanded_ACO_stds = [item for item in ACO_stds for _ in range(population_size)]


    return expanded_ACO_means, expanded_ACO_stds, HC_means, HC_stds, RW_means, RW_stds, TS_means, TS_stds, SA_means, SA_stds


def plot_and_save(means1, stds1, means2, stds2, means3, stds3, means4, stds4, means5, stds5):
    '''
    Given the experiment data as input, plot and save the desired diagram
    '''

    plt.figure(figsize=(18, 12))  

    x_values = range(len(means1))

    plt.plot(x_values, means1, label='ACO', marker='', linestyle='-')
    plt.plot(x_values, means2, label='HC', marker='', linestyle='-')
    plt.plot(x_values, means3, label='RW', marker='', linestyle='-')
    plt.plot(x_values, means4, label='TS', marker='', linestyle='-')
    plt.plot(x_values, means5, label='SA', marker='', linestyle='-')

    plt.fill_between(x_values, np.array(means1) - np.array(stds1), np.array(means1) + np.array(stds1), alpha=0.1)
    plt.fill_between(x_values, np.array(means2) - np.array(stds2), np.array(means2) + np.array(stds2), alpha=0.1)
    plt.fill_between(x_values, np.array(means3) - np.array(stds3), np.array(means3) + np.array(stds3), alpha=0.1)
    plt.fill_between(x_values, np.array(means4) - np.array(stds4), np.array(means4) + np.array(stds4), alpha=0.1)
    plt.fill_between(x_values, np.array(means5) - np.array(stds5), np.array(means5) + np.array(stds5), alpha=0.1)

    plt.xlabel('Function Evaluation Used')
    plt.ylabel('Max Survival Points Found')
    plt.title('Comparison of 5 different algorithms')

    x_tick_positions = x_values[::100]
    x_tick_labels = x_tick_positions  # 使用x值作为标签
    plt.xticks(x_tick_positions, x_tick_labels)
    
    plt.ylim(800, 3500) 
    
    plt.legend()
    plt.grid(True)
    plt.savefig('./Problem_3/progress_diagram.png', dpi=300)
    plt.show()



if __name__ == '__main__':
    expanded_ACO_means, expanded_ACO_stds, HC_means, HC_stds, RW_means, RW_stds, TS_means, TS_stds, SA_means, SA_stds = run(
                                        num_node = 16, iteration = 800, exp_num = 10, population_size = 10)
    plot_and_save(expanded_ACO_means, expanded_ACO_stds, HC_means, HC_stds, RW_means, RW_stds, TS_means, TS_stds, SA_means, SA_stds)