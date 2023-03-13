# Goal is to minimize halfperimeter of smallest bounding box containing all pins for each net

from dataloader import *
# from placement import *
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
    c = 0

    # Start timer
    
    # Initialize each circuit
    for circuit in circuits:
        t1 = perf_counter()

        # print(circuit)
        # if circuit != 'cc':
        # if circuit != 'cm150a' and circuit != 'cm162a' and circuit != 'cm138a':
        # if circuit != 'cc':
        if circuit != 'cm138a':            
            continue
        x = circuits[circuit]
        
        # Initialize values for branch and bound
        cells = x['cells']
        
        connections = x['connections']
        best_cost = connections + 1
        current_nets = deepcopy(x['nets'])
        
        print(circuit)
        print(f'Cells: {cells}, nets: {connections}')
        print(f'Nets: {current_nets}')

        mincut = init_bb(circuit,best_cost, cells, connections, current_nets)
        
        print(f'best cost: {mincut}')
            
        print(f'Time elapsed: {perf_counter()-t1}')


if __name__ == '__main__':
    main()


    