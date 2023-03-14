# Branch and bound algorithm
# Initiatives 1-4

# Imports and global variables
from copy import copy as deepcopy
from multiprocessing import Process, Value
from random import shuffle, choice
from plot import *
best_cost = 9999
cells = 0
connections = 0
left = 0
right = 0
current_nets = []

# Initialize branch and bound
def init_bb(name, best_cost1, cells1, connections1, current_nets1):
    global best_cost 
    global cells
    global connections
    global current_nets

    best_cost = best_cost1
    cells = cells1
    connections = connections1
    current_nets = deepcopy(current_nets1)

    # INITIATIVE 2+4: initial random heuristic followed by low temperature simulated annealing
    best_cost = init_best_cost_finder()
    # Global best is a synchronized variable between the two processes
    globalbest = Value('i', best_cost)
    # Create two parallel processes for left and right partition
    final_assignment = []
    p1 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 1]), deepcopy(current_nets), 1, 1, 0, cells, True, final_assignment],))    
    p2 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 0]), deepcopy(current_nets), 2, 0, 0, cells, True, final_assignment],))    
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Plot
    plot(name, current_nets1, globalbest.value)

    return globalbest.value

# Recursive branch and bound
def branch_bound(input_list):
    '''
    current_assignment: list of all nodes that have been assigned, in tuple
    next_node_to_assign: current node to assign, tuple (node #, left/right)
    current_nets: list of all nets that are not considered in cost
    best_cost: best cost found
    '''
    
    # Input list is used for multi-processing workaround, since there are a lot of args
    best_cost = input_list[0]
    current_assignment = input_list[1]
    next_node_to_assign = input_list[2]
    nets = input_list[3]
    left = input_list[4]
    right = input_list[5]
    cost = input_list[6]
    cells = input_list[7]
    final_assignment = input_list[8]
    
    # Calculate label of current node. Wrapped in a try block because of INITIATIVE 3 when we already calculate label from peeking into the node
    try: 
        init = input_list[8]
        cost, temp_nets = calculate_label(current_assignment, next_node_to_assign, nets, cost, False)
    except: 
        temp_nets = nets

    # PRUNING: stop calculations for additional leaf nodes if cost is greater than global cost.
    if (cost < best_cost.value):
        current_assignment.append(next_node_to_assign)
        if len(current_assignment) < cells:
            # INITIATIVE 3: determine which one to go based on least cost
            # PRUNING: Stop going left if left > half of the total cell size
            if left < cells/2:
                temp_next_node_L = [len(current_assignment), 0]
                peek_cost_left,temp_left_nets = calculate_label(current_assignment, temp_next_node_L, deepcopy(temp_nets), cost)
            else:
                peek_cost_left = -1
            # PRUNING: Stop going right if right > half of the total cell size
            if right < cells/2:
                temp_next_node_R = [len(current_assignment), 1]
                peek_cost_right,temp_right_nets = calculate_label(current_assignment, temp_next_node_R, deepcopy(temp_nets), cost)
            else: 
                peek_cost_right = -1
            # INTIATIVE: least cost traversal
            if (peek_cost_left > -1 and peek_cost_right > -1):
                # Do left then right if left cost is less than right cost, or the same
                if (peek_cost_left <= peek_cost_right):
                    branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_L, temp_left_nets, left+1, right, peek_cost_left, cells, final_assignment])
                    branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_R, temp_right_nets, left, right+1, peek_cost_right, cells, final_assignment])
                else: 
                    branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_R, temp_right_nets, left, right+1, peek_cost_right, cells, final_assignment])
                    branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_L, temp_left_nets, left+1, right, peek_cost_left, cells, final_assignment])
            # If it's just the left
            elif (peek_cost_left > -1):
                branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_L, temp_left_nets, left+1, right, peek_cost_left, cells, final_assignment])                
            # If it's just the right
            elif (peek_cost_right > -1):
                branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_R, temp_right_nets, left, right+1, peek_cost_right, cells, final_assignment])            
        else:
            # If even cell size, record best cost only if left and right are equal
            if not (cells%2) and (left == right):
                best_cost.value = cost
                print(f'Even cost: {cost}, best cost: {best_cost.value}, left: {left}, right: {right}')
                print(f'Current assignment: {current_assignment}')
                save(current_assignment)
            # If odd cell size, record best cost if left and right are off by at most 1
            elif (cells%2) and (abs(left-right) < 2):
                best_cost.value = cost
                print(f'Odd cost: {cost}, best cost: {best_cost.value}')
                print(f'Current assignment: {current_assignment}')
                save(current_assignment)
            else:
                # Shouldn't happen
                assert False

def calculate_label(current_assignments, current_node, current_nets, cost):
    '''
    Find cost of current node (cuts) by calculating ONLY current node's cuts
    '''
    nets_to_remove = []
    # Iterate through nets
    for idx, net in enumerate(current_nets):
        try:
            # Try to access net if it's got current node in it
            net.index(current_node[0])
            # If it does with no error, then for every value inside the net that's not current_node, we see if it's the same as the current node's position
            for value in net:
                if (value == current_node[0]):
                    continue
                if current_assignments[value][1] != current_node[1]:
                    # Remove current net
                    nets_to_remove.append(idx)
                    # Increment cost
                    cost += 1
                    # Break out of try block, but not out of the top level for loop
                    break
        except:
            # not in index. so we can skip
            pass

    # Remove nets to remove from the current nets
    for i in sorted(nets_to_remove, reverse=True):
        current_nets.pop(i)
    return cost, current_nets

# Heuristic to find better initial best cost
def init_best_cost_finder(const=7):
    global best_cost 
    global cells
    global connections
    global current_nets
    
    # Determine dynamic random iterations, arbitrary cost function calculation from number of connections of the circuit

    random_iterations = int((connections/10) ** (const))
    if random_iterations > 15000:
        random_iterations = 15000
    # Determine annealing iterations
    swapping_iterations = int(random_iterations/2)

    # Repeat for N iterations
    for p in range(random_iterations):
        # Create random cell list, shuffle, then split into a balanced left and right partition.        
        random_cell_list = [x for x in range(cells)]
        shuffle(random_cell_list)
        left = [[x, 0] for x in random_cell_list[0:int(cells/2)]]
        right = [[x, 1] for x in random_cell_list[int(cells/2):]]
        random_cell_list = left + right
        random_cell_list.sort(key=lambda x: x[0])
        cost = 0
        nets = deepcopy(current_nets)

        # Compute cost for the random bi-partition
        for x in random_cell_list:
            cost, nets = calculate_label(random_cell_list, x, nets, cost)
        # Record best cost and save left and good partitions
        if cost < best_cost:
            best_cost = cost
            good_left = left
            good_right = right
            save(random_cell_list)
            
    print(f'Initial best cost from random heuristic: {best_cost}')

    # Do initiative 4: low temperature anneal for N/2 iterations 
    for p in range(swapping_iterations):
        best_cost, good_left, good_right = zero_degree_anneal(good_left, good_right, best_cost)
    
    print(f'Initial best cost from annealing heuristic: {best_cost}')

    return best_cost

def zero_degree_anneal(left, right, cost):
    '''
    Swaps a random cell within the list and computes cost. Returns the better of: original or swapped
    '''
    global current_nets
    
    # Create copies
    og_left = deepcopy(left)
    og_right = deepcopy(right)
    og_cost = deepcopy(cost)

    # Choose random value from left and right partition to swap
    rand_left = choice(left)
    rand_right = choice(right)
    temp_right = deepcopy([rand_right[0], 0])
    temp_left = deepcopy([rand_left[0], 1])
    
    # Swap
    left[left.index(rand_left)] = temp_right
    right[right.index(rand_right)] = temp_left

    # Merge into one list to compute cost
    random_cell_list = left + right
    random_cell_list.sort(key=lambda x: x[0])
    new_cost = 0
    nets = deepcopy(current_nets)
    # Compute cost
    for x in random_cell_list:
        new_cost, nets = calculate_label(random_cell_list, x, nets, new_cost)

    # Save if new cost is better
    if new_cost < og_cost:
        save(random_cell_list)
        return new_cost, left, right
    return og_cost, og_left, og_right