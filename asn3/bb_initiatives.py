# Branch and bound algorithm
'''

Goal: minimize # of edges between L and R. Keep L and R balanced

Decision tree: node n is either L or R, n+1 either L or R, etc
- n nodes = n level in tree

Idea: prune tree during building (bound). Label each node in tree with cut size of subgraph at that node
- This can be done efficiently since youre just adding single node

Label of node x <= labels of all nodes in subtree below x.
If we reach a node with label >= c, no need to construt tree below node.

Depth first to a leaf for single solution, record best solution at current moment. Keep pruning. Whenever you go down to another leaf, that's the best solution

Runtime highly depends on initial solution (initial partition)
If you have a good initial solution, you can prune earlier
(eg heuristic first)

'''
from copy import copy as deepcopy
from multiprocessing import Process, Value
from random import shuffle
best_cost = 9999
cells = 0
connections = 0
left = 0
right = 0
current_nets = []

def init_bb(best_cost1, cells1, connections1, current_nets1):
    global best_cost 
    global cells
    global connections
    global current_nets
    best_cost = best_cost1
    cells = cells1
    connections = connections1
    current_nets = current_nets1

    best_cost = init_best_cost_finder()

    left = 1
    right = 1
    globalbest = Value('i', best_cost)
    p1 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 1]), deepcopy(current_nets), 1, 1, 0, cells],))    
    p2 = Process(target=branch_bound, args=([globalbest, deepcopy([[0, 0]]), deepcopy([1, 0]), deepcopy(current_nets), 2, 0, 0, cells],))    

    p1.start()
    p2.start()
    p1.join()
    p2.join()
    return globalbest.value

def branch_bound(input_list):
    '''
    current_assignment: list of all nodes that have been assigned, in tuple
    next_node_to_assign: current node to assign, tuple (node #, left/right)
    current_nets: list of all nets that are not considered in cost
    best_cost: best cost found
    '''
    
    global connections

    best_cost = input_list[0]
    current_assignment = input_list[1]
    next_node_to_assign = input_list[2]
    nets = input_list[3]
    left = input_list[4]
    right = input_list[5]
    cost = input_list[6]
    cells = input_list[7]
    # print(f'best cost: {best_cost.value}')
    # print(f'cost: {cost}')
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
            # If odd cell size, record best cost if left and right are off by at most 1
            elif (cells%2) and (abs(left-right) < 2):
                best_cost.value = cost
                print(f'Odd cost: {cost}, best cost: {best_cost.value}')
                print(f'Current assignment: {current_assignment}')
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
    # print(f'[CALCULATE LABEL] Current cost: {cost}')
    return cost, current_nets

# Heuristic to find better initial best cost
def init_best_cost_finder(const=7):
    global best_cost 
    global cells
    global connections
    global current_nets
    
    iterations = int((connections/10) ** (const))
    print(f"Initial random iterations: {iterations}")

    for p in range(iterations):
        random_cell_list = [x for x in range(cells)]
        # half on one side, half on the other.
        shuffle(random_cell_list)
        left = [[x, 0] for x in random_cell_list[0:int(cells/2)]]
        right = [[x, 1] for x in random_cell_list[int(cells/2):]]
        random_cell_list = left + right
        random_cell_list.sort(key=lambda x: x[0])
        cost = 0
        nets = deepcopy(current_nets)
        for x in random_cell_list:
            cost, nets = calculate_label(random_cell_list, x, nets, cost)
        if cost < best_cost:
            best_cost = cost
    print(f'Initial best cost: {best_cost}')
    return best_cost
