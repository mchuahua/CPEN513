# This file contains several different placement heuristics.

import random
import numpy as np

def initialize(circuit):
    '''
    initialize a working grid, which contains pointers to all HPWL net the location affects.
    initialize a working cell list location.
    initialize a working hpwl computation list.
    '''
    
    grid = [[[] for x in range(circuit['size'][0])] for y in range(circuit['size'][1])]
    cells = np.zeros(circuit['cells'], dtype=tuple)
    hpwl = np.zeros(circuit['connections'])

    circuit['grid'] = grid
    circuit['cell_list'] = cells
    circuit['hpwl_list'] = hpwl

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
    


def swap(circuit, type='both'):
    '''
    Swap a random placed cell with one of the following logics:
    - empty: swap with an empty cell
    - placed: swap with another random existing placed cell
    - both: randomly choose empty or placed
    '''
    pass

def init_hpwl(circuit):
    '''
    Initialize hwpl calculations for entire placed circuit
    '''
    connections = circuit['connections']
    hpwl_list = circuit['hpwl_list']
    for i in range(connections):
        hpwl_list[i] = calc_hpwl(circuit, i, init=True)
    

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

def calc_cost(circuit):
    sum = 0
    for i in circuit['hpwl_list']:
        sum +=i
    circuit['cost'] = sum
    return sum