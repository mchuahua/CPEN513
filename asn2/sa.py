import random
from placement import *
from math import exp
from plot import *

def simulated_annealing(circuit, threshold = 10, start_temp=100, num_iters=100, update_interval=0.0001, dynamic_iters=True, k=.5, early_exit=True, early_exit_iters=50, early_exit_var=0.05,beta=0.9):
    '''
    Simulated annealing algorithm
    '''
    # Starting temperature for annealing
    T = start_temp
    # Arrays to keep track of temperatures and costs for plotting. x is an array for the x axis iterations.
    temp_arr = []
    cost_arr = []
    x = []

    while (T > threshold):
        std_arr = []
        temp_arr.append(T)
        cost_arr.append(circuit['cost'])
        ##########################################
        # Initiative 1: dynamic iterations
        ##########################################
        if (dynamic_iters):
            num_iters = int(k * (circuit['cells'] ** (4/3)))
        ##########################################
        # Initiative 2: early exit
        ##########################################
        if (early_exit & (len(x) > early_exit_iters) ):
            if (cost_arr[-1] == cost_arr[-2]):
                varu = np.var(cost_arr[-early_exit_iters:])
                if (varu < early_exit_var):
                    return

        # Swapping mechanism
        for i in range(num_iters):
            if single_pass(circuit, T):
                std_arr.append(1)
            else:
                std_arr.append(0)
        
        # Reduce T.
        T = lower_temperature(T, beta, std_arr)

        # Rolling plotting graphics
        update_plot(x, cost_arr, temp_arr, circuit, update_interval)

def single_pass(circuit=None, T=100):
    '''
    Computes single pass of anneal
    Inputs: circuit, current temperature T
    '''
    # This is only useful if we have a more complex simulated anneal temperature lowering algorithm
    swapped = False

    #Randomly choose two cells to swap. Get cost difference of the random swap, and the cell locations
    c, cell1, cell2, hpwl_list = swap_propose(circuit)
    
    # get random number from 0 to 1 
    r = random.random()

    # Swap if (r < e^(-c/T))
    if (r < np.exp(-c/T)):
        swap(circuit, cell1, cell2, hpwl_list)
        # Update cost outside of the swap
        circuit['cost'] += c
        swapped = True
    # Revert the swap because it was swapped during proposal to calculate the new hpwl
    else:
        swap_cells(circuit, cell2, cell1)

    return swapped

def lower_temperature(temp, beta, std_arr, format='simple'):
    '''
    Lowers the temperature according to what we want to do
    Simplest form: T = beta*T. More complex: T = T * e^0.7T/std of moves accepted
    '''
    # Complex doesn't really work, might need to debug this a little more.
    if format == 'complex':
        std = np.std(std_arr)
        return temp * exp(0.7 * temp / std)
    # Otherwise simple form
    else:
        return beta * temp
    