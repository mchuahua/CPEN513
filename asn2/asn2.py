# Goal is to minimize halfperimeter of smallest bounding box containing all pins for each net

from dataloader import *
from placement import *
from sa import *
from time import perf_counter
from plot import *

def main(th, iters):
    # Load data into circuits dict and names list
    circuits, names = dataloader()
    c = 0

    t1 = perf_counter()
    # Initialize each circuit
    for circuit in circuits:
        x = circuits[circuit]

        initialize(x)
        init_normal(x)
        hpwl(x, init=True)
        calc_cost(x, update=True)
        print(circuit)
        cost = x['cost']
        # print(f'Initial cost: {cost}')
        # print(x)
        
        plot(x)

        simulated_annealing(x, threshold = th, start_temp=10, num_iters=iters, dynamic_iters=True, beta=0.95, k=1)
        cost = x['cost']
        print(f'Final cost: {cost}')
        # print(x)
        c += cost
    print(f'Avg cost: {c/len(names)}')
    print(f'time elapsed: {perf_counter()-t1}')

if __name__ == '__main__':
    main(0.001, 100)
    # main(0.001, 1000)
    # main(0.00001, 1000)