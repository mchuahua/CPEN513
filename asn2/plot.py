import matplotlib.pyplot as plt
import numpy as np

def plot(circuit):
    '''
    Plots and initializes circuit
    Inputs: circuit dict 
    Outputs: none.
    '''
    # setup plot
    circuit['lines'] = []
    circuit['figure'] = plt.figure()
    circuit['ax1'] = circuit['figure'].add_subplot(111, label='cost')
    circuit['ax2'] = circuit['figure'].add_subplot(111, label='temp', frame_on=False)
    
    # Set up cost
    temp1, = circuit['ax1'].plot([],[],'b-')
    circuit['ax1'].set_xlabel('Iteration')
    circuit['ax1'].set_ylabel('Cost', color='Blue')
    circuit['ax1'].tick_params(axis='y', colors='Blue')
    circuit['ax1'].set_ylim(bottom=0)

    # Set up temperature
    temp2, = circuit['ax2'].plot([],[],'r-')
    circuit['ax2'].set_ylabel('Temp', color='Red')
    circuit['ax2'].yaxis.set_label_position('right')
    circuit['ax2'].yaxis.tick_right()
    circuit['ax2'].tick_params(axis='y', colors='Red')

    circuit['lines'].append(temp1)
    circuit['lines'].append(temp2)

    # Name of plot
    name = circuit['name']
    plt.title(f'Simulated annealling of {name}')
    # autoscale
    circuit['ax1'].set_autoscaley_on(True)
    circuit['ax2'].set_autoscaley_on(True)
    # add a grid
    circuit['ax1'].grid()

def update_plot(x, cost, temp, circuit, update_interval):
    '''
    Function used to update plot for animation
    Inputs: circuit dict, x, y, update interval
    '''
    # Update latest value in x axis
    x.append(len(cost))
    # Update cost and temperature
    circuit['lines'][0].set(xdata=x,ydata=cost)
    circuit['lines'][1].set(xdata=x,ydata=temp)
    # Scaling the graph
    circuit['ax1'].relim()
    circuit['ax1'].autoscale_view()
    circuit['ax2'].relim()
    circuit['ax2'].autoscale_view()
    # Redraw
    circuit['figure'].canvas.draw()
    circuit['figure'].canvas.flush_events()
    # update interval must be non-zero
    plt.pause(update_interval)
