import matplotlib.pyplot as plt
import numpy as np

def plot(circuit):
    '''
    Plots and initializes circuit
    Inputs: circuit dict 
    Outputs: none.
    '''
    # setup plot
    circuit['figure'], circuit['ax'] = plt.subplots()
    circuit['lines'], = circuit['ax'].plot([],[],'b-')
   
    # autoscale
    circuit['ax'].set_autoscaley_on(True)
    # add a grid
    circuit['ax'].grid()
    

def update_plot(x, y, circuit, update_interval):
    '''
    Function used to update plot for animation
    INputs: circuit dict, x, y, update interval
    '''
    x.append(len(y))
    # if update > 0:
    # xvals = list(range(0,len(data)))
    circuit['lines'].set(xdata=x,ydata=y)
    circuit['ax'].relim()
    circuit['ax'].autoscale_view()

    # frame.set_xdata(xvals)
    circuit['figure'].canvas.draw()
    circuit['figure'].canvas.flush_events()
    # plt.draw()
    # plt.flush_events()
    plt.pause(update_interval)

    # elif final == True:
    #     grid = data/10
    #     frame.set_array(grid[::-1])
    #     plt.draw()
    #     plt.pause(5)