from dataloader import *
from plot import *
from copy import deepcopy
from astar import *
import operator

# connect wires (source to sinks)
def initiative(benchmark, plot_frame, update_interval, plot_final_only):
    grid = benchmark['grid']
    size_x = benchmark['size'][0]
    size_y = benchmark['size'][1]
    if plot_final_only:
        update_interval = 0

    ################ 
    # Initiative 1: Approximately pre-sort wires from shortest path to longest path
    # This is done by adding up all the manhattan costs for each pin to another then taking the average, and then adding the number of pins
    ################
    cost_arr = []
    factor = 1
    # print(benchmark['wires'])
    for i, wire in enumerate(benchmark['wires']):
        cost_value = 0
        for j, pin in enumerate(wire):
            if j == 0:
                continue
            cost_value += manhattan(pin[0], wire[j-1][0], pin[1], wire[j-1][1])
        cost_arr.append([i, cost_value/np.size(wire) + np.size(wire)*factor])
    # Sort the costs and put the sorted back into the benchmark['wires']
    # print(cost_arr)
    cost_arr = sorted(cost_arr, key=lambda x: x[1])
    new_wires = []
    for sorted_wire in cost_arr:
        new_wires.append(benchmark['wires'][sorted_wire[0]])
    benchmark['wires'] = deepcopy(new_wires)
    # print(benchmark['wires'])

    ################ 
    # initiative 2: ripup and reroute
    # This is done by keeping a priority queue and upping the failed priorities by one (ie moving up one) 
    # We define number of retries so that it doesnt keep trying
    ################
    retries = 50
    priority_queue = []
    for num,i in enumerate(benchmark['wires']):
        priority_queue.append([num+retries, i])
    reset_grid = deepcopy(grid)
    for asdf in range(retries):
        print(f'Iteration: {asdf}')
        # print(priority_queue)
        totali=0
        # Reset ok flag
        ok = True
        # Sort priority queue
        priority_queue = sorted(priority_queue, key=lambda x:x[0])
        # Reset grid
        grid = deepcopy(reset_grid)
        # Base A* algorithm except for ok flag that notes that the current net failed to route and we use priority queue 
        for z, iter in enumerate(priority_queue):
            wire = iter[1]
            print(wire)
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
                        ok = False
                        priority_queue[z][0] = iter[0] - 1
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
                   
                
                if err == 1:
                    init_workspace(benchmark)
                    working = {'cost': dist, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}   
                
                totali+=i
                # print(f'Cells visited: {i}')
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
        
        if ok:
            break

    print(f'Total cells visited: {totali}')
    update_plot(grid, plot_final_only, plot_frame, update_interval)