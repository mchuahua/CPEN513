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

    # Start timer
    t1 = perf_counter()
    
    # Initialize each circuit
    for circuit in circuits:
        x = circuits[circuit]
        initialize(x)
        init_normal(x, cluster=True)
        hpwl(x, init=True)
        calc_cost(x, update=True)
        print(circuit)
        cost = x['cost']
        # print(f'Initial cost: {cost}')
        # print(x)
        
        # Initialize plot graphics for simulated anneal
        plot(x)

        # Run simulated annealing with the following parameters
        simulated_annealing(circuit=x,                  # Individual circuit 
                            threshold = th,             # End temperature threshold 
                            start_temp=10,              # Start temperature
                            num_iters=iters,            # Number of iterations. If dynamic iters is true, this is ignored
                            dynamic_iters=True,         # Enable/disable dynamic iterations according to # cells
                            beta=0.95,                  # How fast we want to lower the temperature
                            k=1,                        # Controls how big the dynamic iterations is
                            update_interval=0.0001,     # Controls how fast the graphics update
                            early_exit=True,            # Enable/disable early exit
                            early_exit_iters=50,        # Specify how large the window for determining early exit should be
                            early_exit_var=0.05,        # Specify the variance threshold for the early exit window
                            cluster=True                # Enable/disable initial clustering
                            )
        
        # Calculate running total
        cost = x['cost']
        c += cost

        # print(f'Final cost: {cost}')
        # print(x)

    print(f'Avg cost: {c/len(names)}')
    print(f'Time elapsed: {perf_counter()-t1}')

if __name__ == '__main__':
    main(0.001, 100)
    # main(0.001, 1000)
    # main(0.00001, 1000)