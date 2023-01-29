from matplotlib import colors
from matplotlib import pyplot as plt

# Colours: white, red, yellow, grey, orange, cyan, green, magenta, pink, blue, HOTPINK
cmap = colors.ListedColormap(['white','red','yellow','grey',"#D95319",'cyan','green','magenta', '#FFC0CB', '#FF33FF', 'blue'])

def plot(benchmark):
    '''
    Plots and initializes benchmark grid. 
    Inputs: benchmark dict 
    Outputs: none.
    '''
    # Normalize grid
    grid = benchmark['grid']/10
    fg = plt.figure()
    ax = fg.gca()
    h = ax.pcolormesh(grid[::-1], cmap=cmap, edgecolors='k',linewidths=1)  # set initial display dimensions

    return h

def update_plot(data, final, frame, update):
    '''
    Function used to update plot for animation
    '''
    
    if update > 0:
        grid = data/10
        frame.set_array(grid[::-1])
        plt.draw()
        plt.pause(update)
    elif final == True:
        grid = data/10
        frame.set_array(grid[::-1])
        plt.draw()
        plt.pause(5)