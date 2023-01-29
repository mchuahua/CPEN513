import numpy as np
from copy import deepcopy
from dataloader import *
from plot import *

def leemoore(benchmark, plot_frame, update_interval, plot_final_only):
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
    if plot_final_only:
        update_interval = 0
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
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
                        update_plot(working_grid, False, plot_frame, update_interval)
                        i+=1
                    elif grid[y][x+1] == colour:
                        # print(f'Right. x: {x} y: {y}')                                
                        break
            
            if err == 1:
                init_workspace(benchmark)
                working = {'current': 1, 'x': pin[0], 'y': pin[1], 'prev_x': pin[0], 'prev_y': pin[1]}   
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

           
        # print(grid)
        # break
    print(f'Total cells visited: {totali}')
    update_plot(grid, plot_final_only, plot_frame, update_interval)