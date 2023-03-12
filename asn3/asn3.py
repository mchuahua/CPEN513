# Goal is to minimize halfperimeter of smallest bounding box containing all pins for each net

from dataloader import *
# from placement import *
from bb import *
from time import perf_counter
# from plot import *

def main():
    global best_cost
    global cells
    global connections
    global current_nets

    # Load data into circuits dict and names list
    circuits, names = dataloader()
    c = 0

    # Start timer
    t1 = perf_counter()
    
    # Initialize each circuit
    # Do ugly 8 first because it's the smallest number of cells and connections
    for circuit in circuits:
        if circuit != 'z4ml':
        # if circuit != 'ugly8':
        # if circuit != 'z4ml':            
            continue
        x = circuits[circuit]
        
        # Initialize values for branch and bound
        cells = x['cells']
        connections = x['connections']
        best_cost = cells
        current_nets = x['nets']
        
        print(circuit)
        print(f'Cells: {cells}, nets: {connections}')
        print(f'Nets: {current_nets}')

        b = init_bb(best_cost, cells, connections, current_nets)

        print(f'best cost: {b}')
    
    print(f'Time elapsed: {perf_counter()-t1}')

if __name__ == '__main__':
    main()
    