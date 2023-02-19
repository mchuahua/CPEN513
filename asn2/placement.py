# This file contains several different placement heuristics.

import random
import numpy as np
from copy import deepcopy

def initialize(circuit):
    '''
    initialize a working grid, which contains pointers to all HPWL net the location affects.
    initialize a working cell list location.
    initialize a working hpwl computation list.
    '''
    
    grid = [[[] for x in range(circuit['size'][0])] for y in range(circuit['size'][1])]
    cells = [[] for x in range(circuit['cells'])]
    hpwl = np.zeros(circuit['connections'])
    grid_list = [[(x, y) for x in range(circuit['size'][0])] for y in range(circuit['size'][1])]

    circuit['grid'] = grid
    circuit['cell_list'] = cells
    circuit['hpwl_list'] = hpwl
    circuit['grid_list'] = grid_list

def init_random(circuit):
    '''
    Initialize cells by placing cells at random throughout the entire valid circuit size.
    '''
    pass

def init_normal(circuit):
    '''
    Initialize cells by placing cells just from the beginning at (0,0) -> size
    '''
    x,y = 0,0
    size = circuit['cells']
    xmax = circuit['size'][0]
    
    for i in range(size):
        if (x == xmax):
            x = 0
            y += 1
        circuit['cell_list'][i] = (x, y)
        x+=1
    


def swap_propose(circuit, type='both'):
    '''
    Propose a swap a random placed cell with one of the following logics:
    - empty: swap with an empty cell
    - placed: swap with another random existing placed cell
    - both: randomly choose empty or placed
    '''
    # First cell must be a cell that is placed (so that we don't choose two empty cells which is useless computation)
    cell1 = random.choice(circuit['cell_list'])
    # Do-while to choose any other cell that isn't cell1
    cell2 = cell1
    while(cell2 == cell1):
        cell2 = random.choice(random.choice(circuit['grid_list']))

    recalculate_nets = []
    # Find all nets affected
    for i in circuit['grid'][cell1[1]][cell1[0]]:
        if i not in recalculate_nets:
            recalculate_nets.append(i)
    for i in circuit['grid'][cell2[1]][cell2[0]]:
        if i not in recalculate_nets:
            recalculate_nets.append(i)
    
    # Proposed cost is the difference between new nets (that are now changed) and the old nets
    hpwl_list, proposed_cost = hpwl(circuit, changed=recalculate_nets)

    return proposed_cost, cell1, cell2, hpwl_list

def swap(circuit, cell1, cell2, hpwl_list):
    '''
    Swap cell1 and cell2. Switches the cell grid pointers around. Also switches the hpwl dependencies around.
    '''
    circuit['hpwl_list'] = deepcopy(hpwl_list)
    
    # Swap hpwl dependencies 
    temp = deepcopy(circuit['grid'][cell2[1]][cell2[0]])
    circuit['grid'][cell2[1]][cell2[0]] = deepcopy(circuit['grid'][cell1[1]][cell1[0]] )
    circuit['grid'][cell1[1]][cell1[0]] = deepcopy(temp)

    # Update cell list pointers. Index is needed to temporarily prevent updating cell1 before checking if cell2 exists. This prevents multiple cells in the same location.
    index = circuit['cell_list'].index(cell1)
    if cell2 in circuit['cell_list']:
        circuit['cell_list'][circuit['cell_list'].index(cell2)] = cell1
    circuit['cell_list'][index] = cell2
  

def hpwl(circuit, init=False, changed=None):
    '''
    hwpl calculations for entire placed circuit
    '''
    old_values_sum = 0
    new_values_sum = 0
    if init:
        hpwl_list = circuit['hpwl_list']
        for i in range(len(hpwl_list)):
            hpwl_list[i] = calc_hpwl(circuit, i, init=True)
    else:
        hpwl_list = deepcopy(circuit['hpwl_list'])
        for i in range(len(changed)):
            old_values_sum += hpwl_list[i]
            hpwl_list[i] = calc_hpwl(circuit, i, init=True)
            new_values_sum += hpwl_list[i]
    
    return hpwl_list, new_values_sum-old_values_sum 

def calc_hpwl(circuit, net=0, init=False):
    '''
    Calcluate hwpl for a net. 
    '''
    circuit_net = circuit['nets'][net]
    cell_list = circuit['cell_list']
    
    # Get bounding box values for xmin, xmax, ymin, ymax
    for i,cell in enumerate(circuit_net):
        y = cell_list[cell][1]
        x = cell_list[cell][0]
        if init:
            circuit['grid'][y][x].append(net)
        # Initialize the bounding box values
        if (i == 0):
            ymin = y
            ymax = y
            xmin = x
            xmax = x
        else:
            if(ymin > y):
                ymin = y
            if(ymax < y):
                ymax = y
            if(xmax < x):
                xmax = x
            if(xmin > x):
                xmin = x

    return (xmax-xmin) + ((ymax-ymin) * 2)

def calc_cost(circuit, update=False):
    sum = 0
    for i in circuit['hpwl_list']:
        sum +=i
    if update:
        circuit['cost'] = sum
    return sum