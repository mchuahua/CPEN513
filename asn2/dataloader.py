import os
import numpy as np

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

def readline(bmfile):
    line = bmfile.readline().split(' ')
    if line[0] == "\n":    
        line = bmfile.readline().split(' ')
    print(line)
    return line


def dataloader(folder='./ass2_files', filesuffix='8a.txt'):
    '''
    Data loader into benchmark dict from netlist file, assuming run location contains 'ass2_files' folder
    '''
    benchmark_files = putname(folder, filesuffix)
    names = []
    print(f'Number of netlists:   {len(benchmark_files)}')
    # Open each file and put data into a dict
    benchmarks = {}
    for benchmark_file in benchmark_files:
        filename = benchmark_file.split('/')[-1].split('.')[0]
        names.append(filename)
        print(filename)
        # Append benchmark file name as a dict into benchmarks
        benchmarks[filename] = {}
        bmfile = open(benchmark_file)
        # First line is number of cells, number of connections between cells, and x,y
        coord = readline(bmfile)
        size = int(coord[0])
        connections = int(coord[1])
        benchmarks[filename]['size'] = (int(coord[2]), int(coord[3]))
        benchmarks[filename]['cells'] = size
        print(f'cells: {size}, connections: {connections}, gridx: {coord[2]}, gridy: {coord[3]}')
        benchmarks[filename]['nets'] = []
        # Go through all nets
        for i in range(connections):
            # Second+ line is each net's number of logic blocks, followed by each logic block it connects to
            arr = []
            tempstr = readline(bmfile)
            logic_size = int(tempstr[0])
            for j in range(logic_size):
                arr.append((logic_size, int(tempstr[1].split("\\")[0])))
            benchmarks[filename]['nets'].append(arr.copy())
        
        bmfile.close()
    return benchmarks, names

# circuit_dict, names = dataloader()
# print(names)
# print(circuit_dict)
