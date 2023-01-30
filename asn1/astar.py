from dataloader import *
from plot import *
from copy import deepcopy
import operator

def calc_closest(net, grid, x, y):
    '''
    Calculates the closest point to an existing net given a grid and your current x,y coordinate
    Inputs: working net colour value, 2d grid, xy coordinates of pin 
    '''
    min = 999
    temp = [0, 0]
    # Basically minimize manhattan distance
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == net:
                tempv = manhattan(x, j, y, i)
                
                if tempv < min:
                    min = tempv
                    temp[0] = i
                    temp[1] = j
    print(f'minium: {min}')
    print(f'location of closest net point: {temp[1]},{temp[0]}')
    return min, temp[1], temp[0]

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
def astar(benchmark, plot_frame, update_interval, plot_final_only):
    grid = benchmark['grid']
    size_x = benchmark['size'][0]
    size_y = benchmark['size'][1]
    totali=0
    if plot_final_only:
        update_interval = 0
    for wire in benchmark['wires']:
        # Set colour
        colour = grid[wire[0][1]][wire[0][0]]
        # Pre-emptively clear grid first, so all subsequent pins will be connected to the main net (otherwise they might make their own separate net)
        for pin in wire[2:]:
            grid[pin[1]][pin[0]] = 0
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
            working_grid[pin[1]][pin[0]] = colour
            # Expansion until any pin or wire is reached. Check all 4 sides
            i = 0
            while(1):
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
                    elif grid[y][x+1] == colour:
                        # print(f'Right. x: {x} y: {y}')                                
                        break
            
            if err == 1:
                init_workspace(benchmark)
                working = {'cost': dist, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}   
            totali+=i
            print(f'Cells visited: {i}')
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

    print(f'Total cells visited: {totali}')
    update_plot(grid, plot_final_only, plot_frame, update_interval)