import matplotlib.pyplot as plt
import matplotlib
from matplotlib.patches import ConnectionPatch
import numpy as np


def plot(name, nets, mincut, partitioned_circuit=None):
    if partitioned_circuit is None:
        partitioned_circuit = []
        with open('asn3.log', 'r') as reader:
            temp = reader.read()[2:-2].split('], [')
        for strr in temp:
            split = strr.split(', ')
            partitioned_circuit.append([int(split[0]), int(split[1])])
    
    # Split partitioned circuit into left and right
    partitioned_circuit.sort(key=lambda x: x[1])
    size = int(len(partitioned_circuit)/2)
    if partitioned_circuit[size][1] == 0:
        left = [x[0] for x in partitioned_circuit[0:size+1]]
        right = [x[0] for x in partitioned_circuit[size+1:]]
    elif partitioned_circuit[size-1][1] == 1:
        left = [x[0] for x in partitioned_circuit[0:size-1]]
        right = [x[0] for x in partitioned_circuit[size-1:]]
    else:
        left = [x[0] for x in partitioned_circuit[0:size]]
        right = [x[0] for x in partitioned_circuit[size:]]

    # Initialize plot
    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    x1,y1 = np.random.rand(len(left)),np.random.rand(len(left))
    x2,y2 = np.random.rand(len(right)),np.random.rand(len(right))

    ax1.plot(x1,y1,'ko')
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.plot(x2,y2,'ko')
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    # Labels
    for idx,i in enumerate(x1):
        ax1.annotate(str(left[idx]), xy=(x1[idx],y1[idx]), xytext=(-5,3), textcoords='offset points')
    for idx,i in enumerate(x2):
        ax2.annotate(str(right[idx]), xy=(x2[idx],y2[idx]), xytext=(-5,3), textcoords='offset points')
    

    # Colours
    cmap = plt.get_cmap('nipy_spectral')
    colours = [cmap(i) for i in np.linspace(0, 1, len(nets))]

    # Draw all nets
    for i, net in enumerate(nets):
        for j, coord in enumerate(net):
            # First coord is 0, next coord is 1
            xya, axa = find_coord(ax1,ax2,x1,y1,x2,y2,left,right,coord)
            xyb, axb = find_coord(ax1,ax2,x1,y1,x2,y2,left,right,net[j+1])
            # Make line
            con = ConnectionPatch(xyA=xya, xyB=xyb, coordsA="data", coordsB="data",axesA=axa, axesB=axb, color=colours[i])
            ax2.add_artist(con)

            if j+2 == len(net):
                break
        # plt.show()

    fig.suptitle(f"Bi-partition of {name}, mincut={mincut}")

    # ax1.plot(x1[i,y1[i],'ro',markersize=10)
    # ax2.plot(x2[i],y2[i],'ro',markersize=10)

    plt.show()

def find_coord(axa,axb,x1,y1,x2,y2,left,right,value):
    '''
    Given value to find, return xy coordinate
    '''
    if value in left:
        return (x1[left.index(value)], y1[left.index(value)]), axa
    elif value in right:
        return (x2[right.index(value)], y2[right.index(value)]), axb
    else:
        # Should never happen
        assert False

circuit = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 1], [5, 1], [6, 0], [7, 0], [8, 0], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1], [14, 0], [15, 1], [16, 0], [17, 1], [18, 1], [19, 0], [20, 1], [21, 0], [22, 0], [23, 0], [24, 0], [25, 0], [26, 1], [27, 0], [28, 1], [29, 1], [30, 1], [31, 1], [32, 0], [33, 1], [34, 0], [35, 1], [36, 0]]
nets=[[0, 27], [1, 8], [11, 28, 13], [35, 28, 13, 31, 20], [4, 17, 28, 13], [33, 31, 20], [16, 22], [7, 14], [10, 26, 13], [9, 17, 30, 29], [2, 36, 34, 3], [23, 21, 34], [24, 34], [12, 17, 30, 29], [36, 32], [21, 19], [6, 25], [17, 5], [18, 15], [8, 36], [30, 36, 21, 6], [13, 36, 34, 3], [22, 21], [3, 21], [14, 6], [34, 6], [26, 18], [27, 18], [28, 8, 22, 14, 26, 27, 30], [29, 8, 22, 14, 26, 27], [20, 8, 22, 14, 27], [31, 26, 30]]

# name = 'cm162a'
# mincut = 6
# plot(name, nets, mincut, circuit)