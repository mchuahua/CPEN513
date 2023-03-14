'''
Main assignment3 script.

To use the baseline bi-partitioning algorithm, uncomment line 10 (bb).
To use the initiatives 1+2 bi-partitioning algorithm, uncomment line 11 (bb_initiatives).
To use the initiatives 1-4 bi-partitioning algorithm, uncomment line 12 (bb_initiatives2).
'''

from dataloader import *
# from bb import *
# from bb_initiatives import *
from bb_initiatives2 import *
from time import perf_counter
from plot import *

def main():
    global best_cost
    global cells
    global connections
    global current_nets

    # Load data into circuits dict and names list
    circuits, names = dataloader()
    
    # Initialize each circuit
    for circuit in circuits:
        # Start timer
        t1 = perf_counter()

        # Uncomment the next two lines for running individual circuits
        # if circuit != 'cm138a':            
        #     continue
        
        x = circuits[circuit]
        
        # Initialize values for branch and bound
        cells = x['cells']
        connections = x['connections']
        best_cost = connections + 1
        current_nets = deepcopy(x['nets'])
        
        print(circuit)
        print(f'Cells: {cells}, nets: {connections}')
        print(f'Nets: {current_nets}')

        # Run the branch and bound bi-partitioning algorithm for the circuit
        mincut = init_bb(circuit,best_cost, cells, connections, current_nets)
        
        print(f'best cost: {mincut}')
        print(f'Time elapsed: {perf_counter()-t1}')

if __name__ == '__main__':
    main()


    