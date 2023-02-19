'''
Start with random placement
T = start temp
do {
    for some number of iterations {
        randomly choose two cells to swap
        c = cost(new) - cost(old)
        r = random(0,1)
        if (r < e^(-c/T)):
            take move
    }
    reduce T. 
} until some exit criteria, maybe some T threshold or no more moves being accepted


'''
import random
from placement import *
from math import exp

def simulated_annealing(circuit, threshold = 10, start_temp=100, num_iters=100, beta=0.9):
    T = start_temp
    
    while (T > threshold):
        std_arr = []

        # Figure out if we want to or d'not want to swap
        for i in range(num_iters):
            if single_pass(circuit, T):
                std_arr.append(1)
            else:
                std_arr.append(0)
        
        # Reduce T.
        T = lower_temperature(T, beta, std_arr)


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
    if (r < exp(-c/T)):
        swap(circuit, cell1, cell2, hpwl_list)
        # Update cost outside of the swap
        circuit['cost'] += c
        swapped = True
    
    return swapped

def lower_temperature(temp, beta, std_arr, format='simple'):
    '''
    Lowers the temperature according to what we want to do
    Simplest form: T = beta*T. More complex: T = T * e^0.7T/std of moves accepted
    '''
    if format == 'complex':
        std = np.std(std_arr)
        return temp * exp(0.7 * temp / std)
    # Otherwise simple form
    else:
        return beta * temp
    