# Branch and bound algorithm with initiatives 1 and 2

# Imports
from copy import copy as deepcopy
from multiprocessing import Process, Value
from random import shuffle
from plot import save
# Global variables
best_cost = 9999
cells = 0
connections = 0
left = 0
right = 0
current_nets = []

# Initialize branch and bound
def init_bb(best_cost1, cells1, connections1, current_nets1):
    global best_cost 
    global cells
    global connections
    global current_nets
    best_cost = best_cost1
    cells = cells1
    connections = connections1
    current_nets = current_nets1

    # INITIATIVE 2: initial random heuristic
    best_cost = init_best_cost_finder()
    # Global best is a synchronized variable between the two processes
    globalbest = Value('i', best_cost)

    # Create two parallel processes for left and right partition
    p1 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 1]), deepcopy(current_nets), 1, 1, 0, cells],))    
    p2 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 0]), deepcopy(current_nets), 2, 0, 0, cells],))    
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

    # Calculate label of current node. 
    cost, temp_nets = calculate_label(current_assignment, next_node_to_assign, deepcopy(nets), cost)
    # PRUNING: stop calculations for additional leaf nodes if cost is greater than global cost.
    if (cost < best_cost.value):
        current_assignment.append(next_node_to_assign)
        if len(current_assignment) < cells:
            # PRUNING: Stop going left if left > half of the total cell size
            if left < cells/2:
                temp_next_node_L = [len(current_assignment), 0]
                branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_L, temp_nets, left+1, right, cost, cells])
            # PRUNING: Stop going right if right > half of the total cell size
            if right < cells/2:
                temp_next_node_R = [len(current_assignment), 1]
                branch_bound([best_cost, deepcopy(current_assignment), temp_next_node_R, temp_nets, left, right+1, cost, cells])
        else:
            # If even cell size, record best cost only if left and right are equal
            if not (cells%2) and (left == right):
                best_cost.value = cost
                print(f'Even cost: {cost}, best cost: {best_cost.value}, left: {left}, right: {right}')
                print(f'Current assignment: {current_assignment}')               
                with open('asn3.log', 'w') as writer:
                    writer.write(str(current_assignment))                 
            # If odd cell size, record best cost if left and right are off by at most 1
            elif (cells%2) and (abs(left-right) < 2):
                best_cost.value = cost
                print(f'Odd cost: {cost}, best cost: {best_cost.value}')
                print(f'Current assignment: {current_assignment}')
                with open('asn3.log', 'w') as writer:
                    writer.write(str(current_assignment))                
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

# Heuristic to find a better initial best cost by randomly shuffling and computing cost
def init_best_cost_finder(const=7):
    global best_cost 
    global cells
    global connections
    global current_nets
    
    # Arbitrary cost function calculation from number of connections of the circuit
    iterations = int((connections/10) ** (const))
    print(f"Initial random iterations: {iterations}")

    # Repeat for N iterations
    for p in range(iterations):
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
        
        # Record best cost
        if cost < best_cost:
            best_cost = cost
            save(random_cell_list)

    print(f'Initial best cost: {best_cost}')
    
    return best_cost
