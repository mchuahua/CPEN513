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
from copy import deepcopy
best_cost = 9999
cells = 0
connections = 0
left = 0
right = 0

def init_bb(best_cost1, cells1, connections1, current_nets1):
    global best_cost 
    global cells
    global connections
    global current_nets
    best_cost = best_cost1
    cells = cells1
    connections = connections1
    current_nets = current_nets1
    left = 1
    right = 1
    branch_bound(deepcopy([[0, 0]]), deepcopy([1, 1]), deepcopy(current_nets), deepcopy(left), deepcopy(right))
    right = 0
    left = 2
    branch_bound(deepcopy([[0, 0]]), deepcopy([1, 0]), deepcopy(current_nets), deepcopy(left), deepcopy(right))
    # branch_bound(deepcopy([[0, 1]]), [1, 0], deepcopy(current_nets), left, right)

    return best_cost

def branch_bound(current_assignment, next_node_to_assign, nets, left, right, cost=0):
    '''
    current_assignment: list of all nodes that have been assigned, in tuple
    next_node_to_assign: current node to assign, tuple (node #, left/right)
    current_nets: list of all nets that are not considered in cost
    best_cost: best cost found
    '''
    global best_cost
    global cells
    global connections
    
    # Calculate label of current node. 
    cost, temp_nets = calculate_label(deepcopy(current_assignment), deepcopy(next_node_to_assign), deepcopy(nets), deepcopy(cost))
    # print(cost)
    if (cost < best_cost):
        current_assignment.append(next_node_to_assign)
        if len(current_assignment) < cells:
            temp_next_node_L = [len(current_assignment), 0]
            branch_bound(deepcopy(current_assignment), deepcopy(temp_next_node_L), deepcopy(temp_nets), deepcopy(left+1), deepcopy(right), deepcopy(cost))
            temp_next_node_R = [len(current_assignment), 1]
            branch_bound(deepcopy(current_assignment), deepcopy(temp_next_node_R), deepcopy(temp_nets), deepcopy(left), deepcopy(right+1), deepcopy(cost))
        else:
            # If even cell size, record best cost only if left and right are equal
            if not (cells%2) and (left == right):
                best_cost = cost
                print(f'Even cost: {cost}, best cost: {best_cost}, left: {left}, right: {right}')
                print(f'Current assignment: {current_assignment}')                
            # If odd cell size, record best cost if left and right are off by at most 1
            elif (cells%2) and (abs(left-right) < 2):
                best_cost = cost
                print(f'Odd cost: {cost}, best cost: {best_cost}')
                print(f'Current assignment: {current_assignment}')

def calculate_label(current_assignments, current_node, current_nets, cost):
    '''
    Find cost of current node (cuts) by calculating ONLY current node's cuts
    '''
    # print(cost)
    nets_to_remove = []
    # Cost of current assignemnts is 0 if there's only one node

    # print(f'[CALCULATE LABEL] Current Assignments: {current_assignments}')
    # print(f'[CALCULATE LABEL] Current node: {current_node}')
    # print(f'[CALCULATE LABEL] Current nets: {current_nets}')
    # print(f'[CALCULATE LABEL] Current cost: {cost}')
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
