import os
import numpy as np


# Colour definitions 
COLOURS = {'white': 0, 'working': 9, 'obstacle': 10}

def putname(folder, match):
    '''
    Helper function for dataloader
    '''
    temp = []
    for dir, _, filenames in os.walk(folder):
        for filename in filenames:
            if match in filename:
                temp.append(folder + '/' + filename)
    return temp

def dataloader():
    '''
    Data loader into benchmark dict from benchmark file, assuming run location contains 'benchmarks' folder
    '''
    filesuffix = '.infile'
    benchmark_files = putname('./benchmarks', filesuffix)
    names = []
    print(f'Number of benchmarks:   {len(benchmark_files)}')
    # Open each file and put data into a dict
    benchmarks = {}
    for benchmark_file in benchmark_files:
        filename = benchmark_file.split('/')[-1].split('.')[0]
        names.append(filename)
        # Append benchmark file name as a dict into benchmarks
        benchmarks[filename] = {}
        benchmarks[filename]
        bmfile = open(benchmark_file)
        # First line is grid size, put x,y into benchmarks dict
        coord = bmfile.readline().split(' ')
        benchmarks[filename]['size'] = (int(coord[0]), int(coord[1]))
        # Second line is number of obstructions, followed by obstructions
        arr = []
        obstruction_size = int(bmfile.readline())
        for i in range(obstruction_size):
            tempstr = bmfile.readline().split(' ')
            arr.append((int(tempstr[0]), int(tempstr[1].split("\\")[0])))
        benchmarks[filename]['obstructions'] = arr.copy()
        # After obstructions is getting the wires to route
        wirearr = []
        wires = int(bmfile.readline())
        for i in range(wires):
            tempstr = bmfile.readline().split(' ')
            sourcesinks = []
            x = 1
            y = 2
            # Iterate through all sources/sinks within the line
            for j in range(int(tempstr[0])):
                sourcesinks.append((int(tempstr[x]), int(tempstr[y])))
                x+=2
                y+=2
            wirearr.append(sourcesinks)
        benchmarks[filename]['wires'] = wirearr.copy()
        bmfile.close()
    return benchmarks, names



def initialize_benchmark(benchmark):
    '''
    Initializes benchmarks with obstructions and pins to wire up.
    Inputs: benchmark dict
    Outputs: none.
    '''
    size = benchmark['size']
    grid = np.zeros(size, dtype=int).transpose()

    for obstruction in benchmark['obstructions']:
        grid[obstruction[1]][obstruction[0]] = COLOURS['obstacle']

    for i,wire in enumerate(benchmark['wires']):
        for j,sourcesink in enumerate(wire):
            grid[sourcesink[1]][sourcesink[0]] = i+1

    benchmark['grid'] = grid


def init_workspace(benchmark):
    '''
    Initializes the workspace (basically a sctrachpad for the searching algos).
    '''
    dictlist = [dict() for x in range(benchmark['size'][0])]
    benchmark['workspace'] = [dictlist.copy() for x in range(benchmark['size'][1])]