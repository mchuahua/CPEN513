# Goal is to minimize halfperimeter of smallest bounding box containing all pins for each net

from dataloader import *
from placement import *
from sa import *
from time import perf_counter
from plot import *

def main(th, iters, plotting):
    # Load data into circuits dict and names list
    circuits, names = dataloader()
    c = 0

    # Start timer
    t1 = perf_counter()
    
    # Initialize each circuit
    for circuit in circuits:
        x = circuits[circuit]
        initialize(x)
        init_normal(x, 
            cluster=True                                # Enable/disable initial clustering
        )
        hpwl(x, init=True)
        calc_cost(x, update=True)
        print(circuit)
        cost = x['cost']
        # print(f'Initial cost: {cost}')
        # print(x)

        # Run simulated annealing with the following parameters
        simulated_annealing(circuit=x,                  # Individual circuit 
                            plotting=plotting,          # Enable/disable plotting
                            update_interval=0.0001,     # Controls how fast the graphics update
                            threshold = th,             # End temperature threshold 
                            start_temp=17,              # Start temperature
                            iters=10000,                # Max number of iterations. 
                            dynamic_iters=True,         # Enable/disable dynamic iterations according to # cells
                            beta=0.995,                 # How fast we want to lower the temperature
                            k=1,                        # Controls how big the dynamic iterations is
                            early_exit=True,            # Enable/disable early exit
                            early_exit_iters=50,        # Specify how large the window for determining early exit should be
                            early_exit_var=0.05,        # Specify the variance threshold for the early exit window
                            range_window=True,          # Enable/disable range windows
                            range_window_min=10         # Set range window min size
                            )
        
        # Calculate running total
        cost = x['cost']
        c += cost

        print(f'Final cost: {cost}')
        # print(x)

    print(f'Avg cost: {c/len(names)}')
    print(f'Time elapsed: {perf_counter()-t1}')

if __name__ == '__main__':
    main(0.001, 100, plotting=True)
    # main(0.001, 1000)
    # main(0.00001, 1000)