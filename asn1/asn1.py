# Imports
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib import animation
from copy import deepcopy
import operator
import numpy as np
import os

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

# Colour definitions 
COLOURS = {'white': 0, 'working': 7, 'obstacle': 10}

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

benchmarks, names = dataloader()
# Initialize each benchmark
for benchmark in benchmarks:
    initialize_benchmark(benchmarks[benchmark])

# Colours: white, red, yellow, grey, orange, cyan, green, magenta, pink, blue, HOTPINK
cmap = colors.ListedColormap(['white','red','yellow','grey',"#D95319",'cyan','green','magenta', '#FFC0CB', '#FF33FF', 'blue'])

def plot(benchmark):
    '''
    Plots and initializes benchmark grid. 
    Inputs: benchmark dict 
    Outputs: none.
    '''
    # Normalize grid
    grid = benchmark['grid']/11
    fg = plt.figure()
    ax = fg.gca()
    h = ax.pcolormesh(grid[::-1], cmap=cmap, edgecolors='k',linewidths=1)  # set initial display dimensions

    return h

def update_plot(data):
    '''
    Function used to update plot for animation
    '''
    grid = data/9
    frame.set_array(grid[::-1])
    plt.draw()
    plt.pause(update)

def init_workspace(benchmark):
    '''
    Initializes the workspace (basically a sctrachpad for the searching algos).
    '''
    dictlist = [dict() for x in range(benchmark['size'][0])]
    benchmark['workspace'] = [dictlist.copy() for x in range(benchmark['size'][1])]

def leemoore(benchmark):
    '''
    The basic lee-moore (djikstra) routing algorithm
    1: Start at source
    2: Expand, keeping in mind boundaries (ie. edge, obstacles, existing)
    3: Check if expansion is at sink. If sink is reached, stop and backtrack. Otherwise keep doing (2). 
    4. Move to next sink and keep doing (2) again until any part of the net in (3) is reached.
    5. Repeat 4 until no more sinks and move onto the next wire (if available).
    '''
    grid = benchmark['grid']
    size_x = benchmark['size'][0]
    size_y = benchmark['size'][1]
    totali=0
    for wire in benchmark['wires']:
        # Set colour
        colour = benchmark['grid'][wire[0][1]][wire[0][0]]
        # Pre-emptively clear grid first, so all subsequent pins will be connected to the main net (otherwise they might make their own separate net)
        for pin in wire[2:]:
            grid[pin[1]][pin[0]] = -1
        # Connect every pin
        for pin in wire:
            # Reset workspace after every expansion
            init_workspace(benchmark)
            err = 0
            workspace = benchmark['workspace']
            curr = {'current': 1, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}
            current = [curr]
            workspace[pin[1]][pin[0]] = curr
            grid[pin[1]][pin[0]] = -1
            # Working grid for animation
            working_grid = deepcopy(grid)
            # Expansion until any pin or wire is reached. Check all 4 sides
            i = 0
            while(1):
                i+=1
                try:
                    working = current.pop(0)            
                except:
                    print('Unable to route!')
                    err = 1
                    break

                x = working['x']
                y = working['y']
                # if q == 2:
                # print(f'x: {x} y: {y}')
                    # print(f'current {current}')
                # Check each direction for expansion        
                # Left check
                if ((x > 0) & (workspace[y][x-1] == dict())):
                    if (grid[y][x-1] == 0):
                        temp = {'current': working['current']+1, 'x': x-1, 'y': y, 'prev_x': x, 'prev_y': y}
                        workspace[y][x-1] = temp
                        current.append(temp)
                        working_grid[y][x-1] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y][x-1] == colour: 
                        # print(f'Left. x: {x} y: {y}')            
                        break
                # Up
                if ((y > 0) & (workspace[y-1][x] == dict())):
                    if (grid[y-1][x] == 0):
                        temp = {'current': working['current']+1, 'x': x, 'y': y-1, 'prev_x': x, 'prev_y': y}
                        workspace[y-1][x] = temp
                        current.append(temp)
                        working_grid[y-1][x] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y-1][x] == colour:
                        # print(f'Up. x: {x} y: {y}')                                
                        break
                # Down
                if ((y < size_y-1)):
                    if ((workspace[y+1][x] == dict()) & (grid[y+1][x] == 0)):
                        temp = {'current': working['current']+1, 'x': x, 'y': y+1, 'prev_x': x, 'prev_y': y}
                        workspace[y+1][x] = temp
                        current.append(temp)
                        working_grid[y+1][x] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y+1][x] == colour:
                        # print(f'Down. x: {x} y: {y}')                                
                        break
                # Right
                if ((x < size_x-1)):
                    if ((workspace[y][x+1] == dict()) & (grid[y][x+1] == 0)):
                        temp = {'current': working['current']+1, 'x': x+1, 'y': y, 'prev_x': x, 'prev_y': y}
                        workspace[y][x+1] = temp
                        current.append(temp)
                        working_grid[y][x+1] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y][x+1] == colour:
                        # print(f'Right. x: {x} y: {y}')                                
                        break
            
            if err == 1:
                init_workspace(benchmark)
                working = {'current': 1, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}   
            totali+=i                
            # Backtrack for routing
            # print(f'working: {working}')
            grid[working['y']][working['x']] = colour
            while((working['prev_x'] != working['x']) | (working['prev_y'] != working['y'])):
                x = working['x']
                y = working['y']
                # print(f'x: {x} y: {y}')
                working = workspace[working['prev_y']][working['prev_x']]
                # print(f'working: {working}')
                grid[working['y']][working['x']] = colour

           
        # print(grid)
        # break
    print(f'Total iterations: {totali}')
    update_plot(grid)

def calc_closest(net, grid, x, y):
    '''
    Calculates the closest point to an existing net given a grid and your current x,y coordinate
    '''
    min = 999
    temp = [0, 0]
    # Basically minimize manhattan distance
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == net:
                tempv = manhattan(x, i, y, j)
                if tempv < min:
                    min = tempv
                    temp[0] = i
                    temp[1] = j
    return min, temp[0], temp[1]

def cost(x1, x2, x3, y1, y2, y3):
    '''
    The cost is defined as the current location's distance from source + current location's distance to destination
    '''
    return manhattan(x1, x2, y1, y2) + manhattan(x2,x3,y2,y3)

def manhattan(x1, x2, y1, y2):
    '''
    Calculates manhattan distance
    '''
    return abs(x1-x2) + abs(y1-y2)

# connect wires (source to sinks)
def astar(benchmark):
    grid = benchmark['grid']
    size_x = benchmark['size'][0]
    size_y = benchmark['size'][1]
    totali=0
    for wire in benchmark['wires']:
        # Set colour
        colour = grid[wire[0][1]][wire[0][0]]
        # Pre-emptively clear grid first, so all subsequent pins will be connected to the main net (otherwise they might make their own separate net)
        for pin in wire[2:]:
            grid[pin[1]][pin[0]] = -1
        # Connect every pin
        for first, pin in enumerate(wire):
            # Reset workspace after every expansion
            init_workspace(benchmark)
            err = 0
            workspace = benchmark['workspace']
            # Initial manhattan calculations
            if first == 0:
                continue
            elif first == 1:
                dist = manhattan(wire[0][0], pin[0], wire[0][1], pin[1])
                destx = wire[0][0]
                desty = wire[0][1]
            # Else take closest point of already connected net and use that as the manhattan
            else:
                dist, destx, desty = calc_closest(colour, grid, pin[0], pin[1])
        
            curr = {'cost': dist, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}
            current = [curr]
            workspace[pin[1]][pin[0]] = curr
            grid[pin[1]][pin[0]] = -1
            # Working grid for animation
            working_grid = deepcopy(grid)
            working_grid[pin[1]][pin[0]] = COLOURS['working']
            # Expansion until any pin or wire is reached. Check all 4 sides
            i = 0
            while(1):
                i+=1
                try:
                    # Get lowest cost first
                    current.sort(key=operator.itemgetter('cost'))
                    working = current.pop(0)            
                except:
                    print('Unable to route!')
                    err = 1
                    break
                x = working['x']
                y = working['y']
                dist = working['cost']       
                # Check each direction for expansion        
                # Left check
                if ((x > 0) & (workspace[y][x-1] == dict())):
                    if (grid[y][x-1] == 0):
                        tempcost = cost(pin[0], x-1, destx, pin[1], y, desty)
                        temp = {'cost': tempcost, 'x': x-1, 'y': y, 'prev_x': x, 'prev_y': y}
                        workspace[y][x-1] = temp
                        current.append(temp)
                        working_grid[y][x-1] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y][x-1] == colour: 
                        # print(f'Left. x: {x} y: {y}')            
                        break
                # Up
                if ((y > 0) & (workspace[y-1][x] == dict())):
                    if (grid[y-1][x] == 0):
                        tempcost = cost(pin[0], x, destx, pin[1], y-1, desty)
                        temp = {'cost': tempcost, 'x': x, 'y': y-1, 'prev_x': x, 'prev_y': y}
                        workspace[y-1][x] = temp
                        current.append(temp)
                        working_grid[y-1][x] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y-1][x] == colour:
                        # print(f'Up. x: {x} y: {y}')                                
                        break
                # Down
                if ((y < size_y-1)):
                    if ((workspace[y+1][x] == dict()) & (grid[y+1][x] == 0)):
                        tempcost = cost(pin[0], x, destx, pin[1], y+1, desty)
                        temp = {'cost': tempcost, 'x': x, 'y': y+1, 'prev_x': x, 'prev_y': y}
                        workspace[y+1][x] = temp
                        current.append(temp)
                        working_grid[y+1][x] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y+1][x] == colour:
                        # print(f'Down. x: {x} y: {y}')                                
                        break
                # Right
                if ((x < size_x-1)):
                    if ((workspace[y][x+1] == dict()) & (grid[y][x+1] == 0)):
                        tempcost = cost(pin[0], x+1, destx, pin[1], y, desty)
                        temp = {'cost': tempcost, 'x': x+1, 'y': y, 'prev_x': x, 'prev_y': y}
                        workspace[y][x+1] = temp
                        current.append(temp)
                        working_grid[y][x+1] = COLOURS['working']
                        update_plot(working_grid)
                    elif grid[y][x+1] == colour:
                        # print(f'Right. x: {x} y: {y}')                                
                        break
            
            if err == 1:
                init_workspace(benchmark)
                working = {'cost': dist, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}   
            totali+=i
            # Backtrack for routing
            # print(f'working: {working}')
            grid[working['y']][working['x']] = colour
            while((working['prev_x'] != working['x']) | (working['prev_y'] != working['y'])):
                x = working['x']
                y = working['y']
                # print(f'x: {x} y: {y}')
                working = workspace[working['prev_y']][working['prev_x']]
                # print(f'working: {working}')
                grid[working['y']][working['x']] = colour

    print(f'Total iterations: {totali}')
    update_plot(grid)

test = benchmarks['sydney']
initialize_benchmark(test)
frame = plot(test)
update = 0.001
leemoore(test)
plt.pause(5)
update = 0.01
initialize_benchmark(test)
frame = plot(test)
astar(test)
plt.pause(5)

# for i in range(10):
#     test['grid'][i][i] += 1
#     update_plot(frame, benchmarks['sydney']['grid'])
    